"""
YALL M&E Dashboard.

Run locally:
    streamlit run dashboard/app.py

Deploy free: push this repo to GitHub, then deploy on share.streamlit.io
(Streamlit Community Cloud), pointing it at dashboard/app.py. See README.md.
"""

import os
import sys
import datetime

import pandas as pd
import altair as alt
import requests
from fpdf import FPDF, FontFace
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.indicators import PROJECTS, INDICATORS, project_by_id, indicators_for, communities_for
from dashboard import auth

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LIVE_CSV = os.path.join(DATA_DIR, "submissions.csv")
SAMPLE_CSV = os.path.join(DATA_DIR, "submissions_sample.csv")
FIELDS = ["project", "indicator", "value", "assessed", "improved", "community", "group",
          "obs_date", "lat", "lon", "photo_url",
          "note", "coordinator", "_submission_time"]

STALE_DAYS = 60  # flag an indicator as "needs attention" if untouched this long

st.set_page_config(page_title="YALL M&E System", page_icon="\U0001F4CA", layout="wide")

STATUS_GOOD = "#3F7D4A"
STATUS_WARN = "#B9812A"
STATUS_BAD = "#AE3B36"


# ---------------------------------------------------------------
# DATA
# ---------------------------------------------------------------
def load_submissions() -> pd.DataFrame:
    path = LIVE_CSV if os.path.exists(LIVE_CSV) else SAMPLE_CSV
    if not os.path.exists(path):
        return pd.DataFrame(columns=FIELDS)
    df = pd.read_csv(path)
    for col in FIELDS:
        if col not in df.columns:
            df[col] = pd.NA
    return df


def append_manual_entry(project_id, indicator_id, obs_date, note, coordinator,
                         value=None, assessed=None, improved=None, community=None, group=None):
    df = load_submissions()
    new_row = {
        "project": project_id, "indicator": indicator_id,
        "value": value, "assessed": assessed, "improved": improved,
        "community": community, "group": group,
        "obs_date": obs_date, "note": note, "coordinator": coordinator,
        "_submission_time": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(LIVE_CSV, index=False)


def _entries_for(df, indicator_id):
    sub = df[df["indicator"] == indicator_id].copy()
    if sub.empty:
        return sub
    sub["obs_date"] = pd.to_datetime(sub["obs_date"], errors="coerce")
    return sub.sort_values("obs_date")


def latest_entry(df, indicator_id):
    sub = _entries_for(df, indicator_id)
    if sub.empty:
        return None
    return sub.iloc[-1]


def earliest_entry(df, indicator_id):
    sub = _entries_for(df, indicator_id)
    if sub.empty:
        return None
    return sub.iloc[0]


def _to_float(v):
    try:
        f = float(v)
        return f if not pd.isna(f) else None
    except (TypeError, ValueError):
        return None


def sum_values(df, indicator_id):
    """Total of every logged 'value' entry for a count/milestone-style indicator.
    Each log entry is treated as one data-collection event (e.g. one training
    session's headcount) — entries add up rather than overwrite each other,
    so activity logged in different communities doesn't get silently dropped."""
    sub = df[df["indicator"] == indicator_id]
    if sub.empty:
        return None
    vals = [v for v in (_to_float(x) for x in sub["value"]) if v is not None]
    return sum(vals) if vals else None


def sum_percent_components(df, indicator_id):
    """Total assessed and total improved across every logged round for a
    percent-type indicator — so a second community's assessment adds to the
    first's rather than replacing it."""
    sub = df[df["indicator"] == indicator_id]
    total_assessed, total_improved = 0.0, 0.0
    any_data = False
    for _, row in sub.iterrows():
        a = _to_float(row.get("assessed"))
        i = _to_float(row.get("improved"))
        if a is not None:
            total_assessed += a
            any_data = True
        if i is not None:
            total_improved += i
    return (total_assessed, total_improved) if any_data else (None, None)


def average_group_changes(df, indicator_id):
    """For 'average' type indicators: groups entries by (community, group) so
    each tracked cohort's own baseline is compared only to its own later
    readings — never mixing one location's starting point with another's.
    Returns (average % change across cohorts with a follow-up reading,
    number of such cohorts, number of cohorts with only a baseline so far)."""
    sub = _entries_for(df, indicator_id)
    if sub.empty:
        return 0.0, 0, 0
    sub = sub.copy()
    sub["community"] = sub["community"].fillna("")
    sub["group"] = sub["group"].fillna("")
    changes = []
    baseline_only = 0
    for _, gdf in sub.groupby(["community", "group"]):
        vals = [v for v in (_to_float(x) for x in gdf.sort_values("obs_date")["value"]) if v is not None]
        if len(vals) >= 2 and vals[0] != 0:
            changes.append((vals[-1] - vals[0]) / vals[0] * 100.0)
        elif len(vals) == 1:
            baseline_only += 1
    avg = sum(changes) / len(changes) if changes else 0.0
    return avg, len(changes), baseline_only


def current_value(df: pd.DataFrame, indicator: dict):
    """Returns the indicator's current progress value:
    - count: sum of every logged entry (each entry = one event's count)
    - milestone: highest value logged (achieved once any entry hits target)
    - percent: total improved / total assessed, summed across all entries
    - average: average % change across tracked (community, group) cohorts
    """
    ind_id = indicator["id"]

    if indicator["type"] == "average":
        avg, _, _ = average_group_changes(df, ind_id)
        return avg

    if indicator["type"] == "percent":
        total_a, total_i = sum_percent_components(df, ind_id)
        if total_a and total_a > 0:
            return total_i / total_a * 100.0
        return indicator["baseline"]

    if indicator["type"] == "milestone":
        sub = df[df["indicator"] == ind_id]
        vals = [v for v in (_to_float(x) for x in sub["value"]) if v is not None]
        return max(vals) if vals else indicator["baseline"]

    # count
    total = sum_values(df, ind_id)
    return total if total is not None else indicator["baseline"]


def last_update_date(df, indicator_id):
    row = latest_entry(df, indicator_id)
    if row is None or pd.isna(row.get("obs_date")):
        return None
    return row["obs_date"]


def pct_complete(indicator: dict, df: pd.DataFrame):
    cur = current_value(df, indicator)
    base, target = indicator["baseline"], indicator["target"]
    if target == base:
        return 100.0 if cur >= target else 0.0
    return (cur - base) / (target - base) * 100.0


def status_of(pct):
    if pct >= 90:
        return "On track", STATUS_GOOD
    if pct >= 50:
        return "At risk", STATUS_WARN
    return "Behind", STATUS_BAD


def project_summary(project_id, df):
    inds = indicators_for(project_id)
    if not inds:
        return dict(avg=0, good=0, warn=0, bad=0, total=0)
    pcts = [max(0, min(100, pct_complete(i, df))) for i in inds]
    statuses = [status_of(pct_complete(i, df))[0] for i in inds]
    return dict(
        avg=round(sum(pcts) / len(pcts)),
        good=statuses.count("On track"),
        warn=statuses.count("At risk"),
        bad=statuses.count("Behind"),
        total=len(inds),
    )


def visible_projects(user):
    """Admins and viewers see every project; coordinators see only their own."""
    if user["role"] in ("admin", "viewer"):
        return PROJECTS
    return [p for p in PROJECTS if p["id"] == user["project"]]


def needs_attention(df, project_ids=None):
    """Indicators that either have no field data yet, or haven't been
    updated in STALE_DAYS+ days."""
    today = pd.Timestamp(datetime.date.today())
    flagged = []
    for ind in INDICATORS:
        if project_ids is not None and ind["project_id"] not in project_ids:
            continue
        last = last_update_date(df, ind["id"])
        pct = pct_complete(ind, df)
        if last is None:
            flagged.append({"indicator": ind, "reason": "No update logged yet", "days": None, "pct": pct})
        else:
            days = (today - last).days
            if days >= STALE_DAYS and pct < 100:
                flagged.append({"indicator": ind, "reason": f"No update in {days} days", "days": days, "pct": pct})
    flagged.sort(key=lambda f: (f["days"] is not None, -(f["days"] or 0)))
    return flagged


# ---------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------
def render_login():
    st.markdown("## YALL M&E System")
    st.caption("Youth Action Lead Liberia — Monitoring, Evaluation, Accountability & Learning")
    users = auth.load_users()
    options = {uid: f"{u['name']} — {u['title']}" for uid, u in users.items()}

    with st.form("login_form"):
        username = st.selectbox("Your account", options=list(options.keys()), format_func=lambda u: options[u])
        pin = st.text_input("PIN", type="password")
        submitted = st.form_submit_button("Sign in")

    if submitted:
        user = auth.verify(username, pin)
        if user:
            st.session_state["user"] = user
            st.rerun()
        else:
            st.error("Incorrect PIN. Please try again.")

    st.caption("Default PIN is 1234 for every account until changed in Settings.")


# ---------------------------------------------------------------
# DASHBOARD HOME
# ---------------------------------------------------------------
def render_dashboard(user, df):
    st.title("Dashboard")
    vp = visible_projects(user)
    cols = st.columns(len(vp)) if len(vp) > 1 else [st.container()]

    for col, p in zip(cols, vp):
        with col:
            s = project_summary(p["id"], df)
            st.markdown(f"#### {p['short_name']}")
            st.caption(f"{p['funder']} · {p['locations']}")
            st.metric("Average progress", f"{s['avg']}%", help=f"Across {s['total']} indicators")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"<span style='color:{STATUS_GOOD};font-size:12px;'>&#9679; {s['good']} on track</span>", unsafe_allow_html=True)
            c2.markdown(f"<span style='color:{STATUS_WARN};font-size:12px;'>&#9679; {s['warn']} at risk</span>", unsafe_allow_html=True)
            c3.markdown(f"<span style='color:{STATUS_BAD};font-size:12px;'>&#9679; {s['bad']} behind</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Progress at a glance")
    chart_rows = []
    for p in vp:
        s = project_summary(p["id"], df)
        chart_rows.append({"Project": p["short_name"], "Status": "On track", "Indicators": s["good"]})
        chart_rows.append({"Project": p["short_name"], "Status": "At risk", "Indicators": s["warn"]})
        chart_rows.append({"Project": p["short_name"], "Status": "Behind", "Indicators": s["bad"]})
    chart_df = pd.DataFrame(chart_rows)
    status_chart = (
        alt.Chart(chart_df)
        .mark_bar()
        .encode(
            x=alt.X("Project:N", title=None, sort=[p["short_name"] for p in vp],
                     axis=alt.Axis(labelAngle=-30)),
            y=alt.Y("Indicators:Q", title="Number of indicators"),
            color=alt.Color(
                "Status:N",
                scale=alt.Scale(domain=["On track", "At risk", "Behind"], range=[STATUS_GOOD, STATUS_WARN, STATUS_BAD]),
                legend=alt.Legend(title=None, orient="top"),
            ),
            order=alt.Order("Status:N", sort="descending"),
            tooltip=["Project", "Status", "Indicators"],
        )
        .properties(height=320)
    )
    st.altair_chart(status_chart, use_container_width=True)

    st.markdown("---")
    st.subheader("Needs attention")
    st.caption(f"Indicators with no field data yet, or untouched for {STALE_DAYS}+ days.")
    project_ids = {p["id"] for p in vp}
    flags = needs_attention(df, project_ids)
    if not flags:
        st.success("Nothing stale right now — every indicator has a recent update.")
    else:
        for f in flags[:15]:
            ind = f["indicator"]
            proj = project_by_id(ind["project_id"])
            st.markdown(f"**{ind['name']}** · *{proj['short_name']}* — {f['reason']}")
        if len(flags) > 15:
            st.caption(f"...and {len(flags) - 15} more.")

    st.markdown("---")
    st.subheader("Recent updates")
    recent = df.copy()
    if recent.empty or recent["obs_date"].isna().all():
        st.info("No field updates logged yet.")
        return
    recent["obs_date"] = pd.to_datetime(recent["obs_date"], errors="coerce")
    recent = recent.dropna(subset=["obs_date"]).sort_values("obs_date", ascending=False).head(10)
    for _, row in recent.iterrows():
        ind = next((i for i in INDICATORS if i["id"] == row["indicator"]), None)
        ind_name = ind["name"] if ind else row["indicator"]
        date_str = row["obs_date"].strftime("%d %b %Y")
        if ind and ind["type"] == "percent" and pd.notna(row.get("assessed")):
            val_str = f"{row['improved']:g}/{row['assessed']:g} improved"
        elif ind and ind["type"] == "average":
            val_str = f"avg reading: {row['value']}"
        else:
            val_str = f"{row['value']}"
        where = f" ({row['community']})" if pd.notna(row.get("community")) and str(row.get("community")).strip() else ""
        note = f" — {row['note']}" if pd.notna(row.get("note")) and str(row.get("note")).strip() else ""
        st.markdown(f"**{date_str}** · {ind_name}{where}: **{val_str}**{note}")


# ---------------------------------------------------------------
# PROJECT VIEW
# ---------------------------------------------------------------
def build_trend(df, indicator):
    """Returns a DataFrame of (date, value) showing progress over time,
    suitable for a line chart. The meaning of 'value' depends on type:
    - count/milestone: running cumulative total as entries come in
    - percent: running cumulative % (total improved / total assessed so far)
    - average: raw readings over time (not split by cohort — a quick-glance
      view; the indicator detail above already shows the per-cohort figure)
    """
    sub = _entries_for(df, indicator["id"])
    if sub.empty:
        return pd.DataFrame(columns=["Date", "Value"])

    rows = []
    if indicator["type"] == "percent":
        running_a, running_i = 0.0, 0.0
        for _, row in sub.iterrows():
            a = _to_float(row.get("assessed"))
            i = _to_float(row.get("improved"))
            if a is None:
                continue
            running_a += a
            running_i += (i or 0)
            if running_a > 0:
                rows.append({"Date": row["obs_date"], "Value": running_i / running_a * 100.0})
    elif indicator["type"] == "average":
        for _, row in sub.iterrows():
            v = _to_float(row.get("value"))
            if v is not None:
                rows.append({"Date": row["obs_date"], "Value": v})
    else:  # count / milestone
        running = 0.0
        for _, row in sub.iterrows():
            v = _to_float(row.get("value"))
            if v is None:
                continue
            running = max(running, v) if indicator["type"] == "milestone" else running + v
            rows.append({"Date": row["obs_date"], "Value": running})

    return pd.DataFrame(rows)


def render_trend(df, indicator):
    trend_df = build_trend(df, indicator)
    if len(trend_df) < 2:
        st.caption("Not enough entries yet to show a trend — need at least two logged dates.")
        return
    y_title = "%" if indicator["type"] in ("percent", "average") else indicator["unit"]
    chart = (
        alt.Chart(trend_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Date:T", title=None),
            y=alt.Y("Value:Q", title=y_title),
            tooltip=[alt.Tooltip("Date:T"), alt.Tooltip("Value:Q", format=".1f")],
        )
        .properties(height=180)
    )
    target_line = alt.Chart(pd.DataFrame({"y": [indicator["target"]]})).mark_rule(
        color=STATUS_GOOD, strokeDash=[4, 4]
    ).encode(y="y:Q")
    st.altair_chart(chart + target_line, use_container_width=True)
    st.caption("Dashed line = target.")


def render_indicator_row(ind, df, can_edit):
    cur = current_value(df, ind)
    pct = pct_complete(ind, df)
    label, color = status_of(pct)
    last = last_update_date(df, ind["id"])
    last_str = last.strftime("%d %b %Y") if last is not None else "never"

    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            if ind["type"] == "milestone":
                st.markdown(f"**{ind['name']}**  `milestone`")
                st.caption(f"target: {ind['target']} {ind['unit']} · last update: {last_str}")
            elif ind["type"] == "average":
                avg, n_with_followup, n_baseline_only = average_group_changes(df, ind["id"])
                st.markdown(f"**{ind['name']}**  `average`")
                if n_with_followup == 0 and n_baseline_only == 0:
                    st.caption(f"no readings logged yet · target: {ind['target']:g}% increase · last update: {last_str}")
                else:
                    extra = f" · {n_baseline_only} cohort(s) awaiting a follow-up reading" if n_baseline_only else ""
                    st.caption(f"average change {cur:.1f}% across {n_with_followup} cohort(s){extra} · target {ind['target']:g}% increase · last update: {last_str}")
            else:
                st.markdown(f"**{ind['name']}**")
                unit = "%" if ind["type"] == "percent" else ind["unit"]
                st.caption(f"baseline {ind['baseline']:g} · current {cur:g} · target {ind['target']:g} {unit} · last update: {last_str}")
            st.progress(max(0, min(100, int(pct))) / 100)
            if ind.get("instrument"):
                st.caption(f"\U0001F4CB {ind['instrument']}")
        with c2:
            st.markdown(f"<span style='background:{color}22;color:{color};padding:3px 10px;border-radius:12px;font-size:12px;'>{label} · {round(pct)}%</span>", unsafe_allow_html=True)
        with c3:
            if can_edit and st.button("Log update", key=f"log_{ind['id']}"):
                st.session_state["logging_indicator"] = ind["id"]

        with st.expander("View trend over time"):
            render_trend(df, ind)


def render_log_form(ind, project_id, user):
    st.markdown("---")
    st.subheader(f"Log an update — {ind['name']}")
    if ind.get("instrument"):
        st.info(f"Data source: {ind['instrument']}")

    communities = communities_for(project_id)

    with st.form("log_form"):
        if ind["type"] == "percent":
            c1, c2 = st.columns(2)
            assessed = c1.number_input("How many were assessed?", min_value=0, step=1)
            improved = c2.number_input("How many showed the improvement?", min_value=0, step=1)
            value = None
        elif ind["type"] == "milestone":
            st.caption(f"One-time milestone (target: {ind['target']} {ind['unit']}).")
            value = st.number_input(f"Value ({ind['unit']})", min_value=0.0, value=float(ind["target"]), step=1.0)
            assessed = improved = None
        elif ind["type"] == "average":
            st.caption("The first reading logged for a given community + group becomes that cohort's baseline. Every later reading for the same community + group is compared back to it — so fill in Group below if you're tracking more than one cohort per community.")
            value = st.number_input("Average value observed (raw number, e.g. bags/acre or $ income)", step=0.1)
            assessed = improved = None
        else:
            value = st.number_input(f"New value ({ind['unit']})", step=1.0)
            assessed = improved = None

        community = st.selectbox("Community", communities) if communities else None
        group = st.text_input("Group / cohort (optional)", placeholder="e.g. Group A, if you're running more than one group in this community")
        obs_date = st.date_input("Date", value=datetime.date.today())
        note = st.text_area("Note (what happened, context, evidence)")
        c1, c2 = st.columns(2)
        save = c1.form_submit_button("Save update")
        cancel = c2.form_submit_button("Cancel")

    if save:
        if ind["type"] == "percent" and improved > assessed:
            st.error("The improved count can't be more than the assessed count.")
            return
        append_manual_entry(project_id, ind["id"], obs_date.isoformat(), note, user["name"],
                             value=value, assessed=assessed, improved=improved,
                             community=community, group=group)
        st.session_state["logging_indicator"] = None
        st.success("Update saved.")
        st.rerun()
    if cancel:
        st.session_state["logging_indicator"] = None
        st.rerun()


def render_map_tab(df, project_id):
    proj_ids = {i["id"] for i in indicators_for(project_id)}
    sub = df[df["indicator"].isin(proj_ids)].copy()
    sub["lat"] = pd.to_numeric(sub.get("lat"), errors="coerce")
    sub["lon"] = pd.to_numeric(sub.get("lon"), errors="coerce")
    sub = sub.dropna(subset=["lat", "lon"])
    if sub.empty:
        st.info("No GPS locations recorded yet for this project. GPS is captured automatically when a coordinator submits an entry through the Kobo mobile/web form with location turned on.")
        return
    st.caption(f"{len(sub)} entries with a recorded GPS location.")
    st.map(sub[["lat", "lon"]], size=40)


def render_photos_tab(df, project_id):
    proj_ids = {i["id"] for i in indicators_for(project_id)}
    sub = df[df["indicator"].isin(proj_ids)].copy()
    sub = sub[sub["photo_url"].notna() & (sub["photo_url"].astype(str).str.strip() != "")]
    if sub.empty:
        st.info("No photos recorded yet for this project. Photos are captured when a coordinator attaches one through the Kobo mobile/web form.")
        return

    token = st.secrets.get("KOBO_TOKEN", None) if hasattr(st, "secrets") else None
    if not token:
        st.warning("Photos are stored in Kobo, but KOBO_TOKEN isn't set up in this app's secrets, so they can't be fetched and shown here. See Manage for the Kobo connection.")
        return

    sub["obs_date"] = pd.to_datetime(sub["obs_date"], errors="coerce")
    sub = sub.sort_values("obs_date", ascending=False).head(12)
    st.caption(f"Showing the {len(sub)} most recent photos.")
    cols = st.columns(3)
    for idx, (_, row) in enumerate(sub.iterrows()):
        with cols[idx % 3]:
            try:
                resp = requests.get(row["photo_url"], headers={"Authorization": f"Token {token}"}, timeout=15)
                resp.raise_for_status()
                st.image(resp.content, use_container_width=True)
            except Exception:
                st.caption("(photo could not be loaded)")
            ind = next((i for i in INDICATORS if i["id"] == row["indicator"]), None)
            date_str = row["obs_date"].strftime("%d %b %Y") if pd.notnull(row["obs_date"]) else ""
            st.caption(f"{date_str} · {row.get('community','')}")
            st.caption(ind["name"][:60] if ind else row["indicator"])


def render_project(user, df, project_id):
    p = project_by_id(project_id)
    if not p:
        st.error("Project not found.")
        return
    # Only the admin can log updates directly in the dashboard. Coordinators enter
    # everything through Kobo, which has real, permanent storage — the dashboard's
    # local storage can be wiped when the free hosting sleeps and reboots, so it's
    # not a safe place for coordinators' real field data to live even briefly.
    can_edit = user["role"] == "admin"

    st.title(p["name"])
    st.caption(f"{p['funder']} · {p['locations']}")
    st.markdown(f"> {p['objective']}")

    tab_ind, tab_map, tab_photos = st.tabs(["Indicators", "Map", "Photos"])

    with tab_ind:
        all_inds = indicators_for(project_id)

        c1, c2 = st.columns([2, 1])
        with c1:
            search = st.text_input("Search indicators", placeholder="e.g. 'training' or 'women'", key=f"search_{project_id}")
        with c2:
            status_filter = st.multiselect("Filter by status", ["On track", "At risk", "Behind"],
                                            default=["On track", "At risk", "Behind"], key=f"statusf_{project_id}")

        inds = all_inds
        if search:
            inds = [i for i in inds if search.lower() in i["name"].lower()]
        inds = [i for i in inds if status_of(pct_complete(i, df))[0] in status_filter]

        if not inds:
            st.info("No indicators match your search/filter.")
        else:
            chart_rows = []
            for ind in inds:
                pct = max(0, min(100, pct_complete(ind, df)))
                label, _ = status_of(pct_complete(ind, df))
                short_name = ind["name"] if len(ind["name"]) <= 28 else ind["name"][:25] + "..."
                chart_rows.append({"Indicator": short_name, "Full name": ind["name"], "% complete": round(pct, 1), "Status": label})
            chart_df = pd.DataFrame(chart_rows)
            ind_chart = (
                alt.Chart(chart_df)
                .mark_bar()
                .encode(
                    x=alt.X("Indicator:N", title=None, sort=chart_df["Indicator"].tolist(),
                             axis=alt.Axis(labelAngle=-45, labelLimit=160)),
                    y=alt.Y("% complete:Q", scale=alt.Scale(domain=[0, 100])),
                    color=alt.Color(
                        "Status:N",
                        scale=alt.Scale(domain=["On track", "At risk", "Behind"], range=[STATUS_GOOD, STATUS_WARN, STATUS_BAD]),
                        legend=alt.Legend(title=None, orient="top"),
                    ),
                    tooltip=["Full name", "% complete", "Status"],
                )
                .properties(height=380)
            )
            st.altair_chart(ind_chart, use_container_width=True)

            for ind in inds:
                render_indicator_row(ind, df, can_edit)

        if st.session_state.get("logging_indicator"):
            ind = next((i for i in all_inds if i["id"] == st.session_state["logging_indicator"]), None)
            if ind:
                render_log_form(ind, project_id, user)

    with tab_map:
        render_map_tab(df, project_id)

    with tab_photos:
        render_photos_tab(df, project_id)


# ---------------------------------------------------------------
# COMMUNITY VIEW
# ---------------------------------------------------------------
def all_communities_for(projects):
    seen = []
    for p in projects:
        for c in communities_for(p["id"]):
            if c not in seen:
                seen.append(c)
    return seen


def render_community_view(user, df):
    st.title("Community View")
    st.caption("See everything happening in one community, across every project active there.")
    vp = visible_projects(user)
    communities = all_communities_for(vp)
    if not communities:
        st.info("No communities configured yet.")
        return

    selected = st.selectbox("Community", communities)
    active_projects = [p for p in vp if selected in communities_for(p["id"])]
    st.caption(f"**{selected}** has activity from {len(active_projects)} project(s): " + ", ".join(p["short_name"] for p in active_projects))

    for p in active_projects:
        st.markdown("---")
        st.subheader(p["short_name"])
        local_df = df[df["community"] == selected]
        inds_with_data = [i for i in indicators_for(p["id"]) if not local_df[local_df["indicator"] == i["id"]].empty]

        if not inds_with_data:
            st.info(f"No entries logged in {selected} yet for this project.")
            continue

        for ind in inds_with_data:
            cur = current_value(local_df, ind)
            pct = pct_complete(ind, local_df)
            label, color = status_of(pct)
            unit = "%" if ind["type"] in ("percent", "average") else ind["unit"]
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"{ind['name']} — **{cur:g}{'%' if ind['type'] in ('percent','average') else ''}** of {ind['target']:g} {unit if ind['type']=='count' else ''}")
            with c2:
                st.markdown(f"<span style='background:{color}22;color:{color};padding:2px 8px;border-radius:10px;font-size:12px;'>{label}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(f"Recent notes from {selected}")
    active_ids = {i["id"] for p in active_projects for i in indicators_for(p["id"])}
    notes = df[(df["community"] == selected) & df["indicator"].isin(active_ids)
               & df["note"].notna() & (df["note"].astype(str).str.strip() != "")]
    if notes.empty:
        st.info("No notes recorded yet for this community.")
    else:
        notes = notes.copy()
        notes["obs_date"] = pd.to_datetime(notes["obs_date"], errors="coerce")
        notes = notes.sort_values("obs_date", ascending=False).head(10)
        for _, row in notes.iterrows():
            ind = next((i for i in INDICATORS if i["id"] == row["indicator"]), None)
            date_str = row["obs_date"].strftime("%d %b %Y") if pd.notnull(row["obs_date"]) else ""
            st.markdown(f"**{date_str}** — *{ind['name'] if ind else row['indicator']}*: {row['note']}")


# ---------------------------------------------------------------
# REPORTS
# ---------------------------------------------------------------
def _pdf_safe(text):
    """The built-in PDF font only supports latin-1 characters. Coordinator
    notes, project names, etc. can contain characters outside that (smart
    quotes, em dashes, ...) which would otherwise crash report generation.
    This swaps common cases for plain ASCII and safely drops anything else
    left over, so a report can never fail to generate because of this."""
    if text is None:
        return ""
    text = str(text)
    for bad, good in {
        "\u2014": "-", "\u2013": "-",
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2026": "...", "\u00b7": "-",
    }.items():
        text = text.replace(bad, good)
    return text.encode("latin-1", "replace").decode("latin-1")


def generate_pdf_report(p, inds, df):
    """Builds a donor-ready PDF: header, objective, summary, full indicator
    table with status, and recent field notes. Returns raw PDF bytes."""
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Youth Action Lead Liberia", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Monitoring, Evaluation, Accountability & Learning", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(0, 7, _pdf_safe(p["name"]), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5, _pdf_safe(f"Funder: {p['funder']}"), new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(0, 5, _pdf_safe(f"Location: {p['locations']}"), new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(0, 5, f"Generated: {datetime.date.today().strftime('%d %b %Y')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Objective", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5, _pdf_safe(p["objective"]), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    s = project_summary(p["id"], df)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5, _pdf_safe(f"Overall average progress: {s['avg']}% across {s['total']} indicators - "
                                    f"{s['good']} on track, {s['warn']} at risk, {s['bad']} behind."),
                   new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    status_colors = {"On track": (223, 234, 217), "At risk": (243, 230, 204), "Behind": (241, 218, 216)}

    pdf.set_font("Helvetica", "B", 8)
    with pdf.table(col_widths=(84, 18, 18, 18, 14, 24), text_align=("LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "LEFT")) as table:
        header = table.row()
        for h in ["Indicator", "Baseline", "Current", "Target", "%", "Status"]:
            header.cell(h)
        pdf.set_font("Helvetica", "", 7)
        for ind in inds:
            cur = current_value(df, ind)
            pct = pct_complete(ind, df)
            label, _ = status_of(pct)
            row = table.row()
            row.cell(_pdf_safe(ind["name"])[:58])
            row.cell(f"{ind['baseline']:g}")
            row.cell(f"{cur:.1f}")
            row.cell(f"{ind['target']:g}")
            row.cell(f"{round(pct)}")
            r, g, b = status_colors.get(label, (255, 255, 255))
            row.cell(label, style=FontFace(fill_color=(r, g, b)))

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Recent field notes", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    proj_ids = {i["id"] for i in inds}
    notes = df[df["indicator"].isin(proj_ids) & df["note"].notna() & (df["note"].astype(str).str.strip() != "")]
    if notes.empty:
        pdf.multi_cell(0, 5, "No narrative updates recorded yet.", new_x="LMARGIN", new_y="NEXT")
    else:
        notes = notes.copy()
        notes["obs_date"] = pd.to_datetime(notes["obs_date"], errors="coerce")
        notes = notes.sort_values("obs_date", ascending=False).head(10)
        for _, row in notes.iterrows():
            ind = next((i for i in inds if i["id"] == row["indicator"]), None)
            date_str = row["obs_date"].strftime("%d %b %Y") if pd.notnull(row["obs_date"]) else ""
            ind_name = ind["name"] if ind else row["indicator"]
            pdf.multi_cell(0, 5, _pdf_safe(f"{date_str} - {ind_name}: {row['note']}"), new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


def render_reports(user, df):
    st.title("Reports")
    vp = visible_projects(user)
    ids = [p["id"] for p in vp]
    names = {p["id"]: p["short_name"] for p in vp}
    selected = st.selectbox("Project", ids, format_func=lambda i: names[i]) if len(vp) > 1 else ids[0]
    p = project_by_id(selected)
    inds = indicators_for(selected)

    st.markdown(f"### {p['name']} — Progress Report")
    st.caption(f"Funder: {p['funder']} | Location: {p['locations']} | Generated {datetime.date.today().strftime('%d %b %Y')}")
    st.markdown(f"> {p['objective']}")

    rows = []
    for ind in inds:
        cur = current_value(df, ind)
        pct = pct_complete(ind, df)
        label, _ = status_of(pct)
        unit = "%" if ind["type"] in ("percent", "average") else ind["unit"]
        rows.append({
            "Indicator": ind["name"], "Type": ind["type"],
            "Baseline": ind["baseline"], "Current": round(cur, 1), "Target": ind["target"],
            "Unit": unit, "%": round(pct), "Status": label,
        })
    report_df = pd.DataFrame(rows)
    st.dataframe(report_df, use_container_width=True, hide_index=True)

    csv_bytes = report_df.to_csv(index=False).encode("utf-8")
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button("Download table as CSV", csv_bytes, file_name=f"{selected}_report.csv", mime="text/csv")
    with dl2:
        if st.button("Generate PDF report"):
            with st.spinner("Building PDF..."):
                pdf_bytes = generate_pdf_report(p, inds, df)
            st.download_button("Download PDF report", pdf_bytes, file_name=f"{selected}_report.pdf", mime="application/pdf")

    st.subheader("Recent field updates")
    proj_ids = {i["id"] for i in inds}
    notes = df[df["indicator"].isin(proj_ids) & df["note"].notna() & (df["note"].astype(str).str.strip() != "")]
    if notes.empty:
        st.info("No narrative updates recorded yet for this project.")
    else:
        notes = notes.copy()
        notes["obs_date"] = pd.to_datetime(notes["obs_date"], errors="coerce")
        notes = notes.sort_values("obs_date", ascending=False).head(8)
        for _, row in notes.iterrows():
            ind = next((i for i in inds if i["id"] == row["indicator"]), None)
            date_str = row["obs_date"].strftime("%d %b %Y") if pd.notnull(row["obs_date"]) else ""
            where = f" ({row['community']})" if pd.notna(row.get("community")) and str(row.get("community")).strip() else ""
            st.markdown(f"**{date_str}**{where} — *{ind['name'] if ind else row['indicator']}*: {row['note']}")

    st.caption("Tip: use your browser's Print (Ctrl/Cmd+P) to save this report as a PDF.")


# ---------------------------------------------------------------
# MANAGE (admin)
# ---------------------------------------------------------------
def render_manage(user):
    st.title("Manage")
    if user["role"] != "admin":
        st.warning("Only the MEAL Officer can manage users and refresh Kobo data.")
        return

    st.subheader("Refresh data from Kobo")
    st.caption("Pulls the latest submissions from your Kobo form using KOBO_TOKEN / KOBO_FORM_UID from secrets or environment variables.")
    if st.button("Refresh now"):
        try:
            from kobo.pull_data import run as pull_run
            token = st.secrets.get("KOBO_TOKEN", None) if hasattr(st, "secrets") else None
            form_uid = st.secrets.get("KOBO_FORM_UID", None) if hasattr(st, "secrets") else None
            server = st.secrets.get("KOBO_SERVER", None) if hasattr(st, "secrets") else None
            n = pull_run(server=server, form_uid=form_uid, token=token)
            st.success(f"Pulled {n} submissions from Kobo.")
        except Exception as e:
            st.error(f"Could not refresh from Kobo: {e}")

    st.subheader("Indicators")
    st.caption("Indicators live in config/indicators.py, version-controlled alongside the Kobo form. Edit that file and re-run kobo/generate_xlsform.py to update both the dashboard and the field form together.")
    ind_df = pd.DataFrame(INDICATORS)
    cols = [c for c in ["project_id", "name", "type", "unit", "baseline", "target"] if c in ind_df.columns]
    st.dataframe(ind_df[cols], use_container_width=True, hide_index=True, height=350)

    st.subheader("Users & project access")
    users = auth.load_users()
    for uid, u in users.items():
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{u['name']}** — {u['title']}")
                proj_label = "All projects" if u["project"] == "all" else (project_by_id(u["project"]) or {}).get("short_name", u["project"])
                st.caption(f"{proj_label} · username: {uid}")
                new_name = st.text_input("Rename", key=f"name_{uid}", placeholder="real coordinator name")
                if st.button("Save name", key=f"apply_name_{uid}") and new_name:
                    auth.rename_user(uid, new_name)
                    st.success(f"Renamed to {new_name}.")
                    st.rerun()
                new_title = st.text_input("Edit title", key=f"title_{uid}", placeholder="e.g. Project Coordinator")
                if st.button("Save title", key=f"apply_title_{uid}") and new_title:
                    auth.set_title(uid, new_title)
                    st.success(f"Title updated to {new_title}.")
                    st.rerun()
            with c2:
                new_pin = st.text_input("Reset PIN", key=f"pin_{uid}", type="password", placeholder="new PIN")
                if st.button("Apply", key=f"apply_{uid}") and new_pin:
                    auth.set_pin(uid, new_pin)
                    st.success(f"PIN updated for {u['name']}.")


# ---------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------
def render_settings(user):
    st.title("Settings")
    st.subheader("Change your PIN")
    with st.form("pin_form"):
        new_pin = st.text_input("New PIN", type="password")
        submit = st.form_submit_button("Save PIN")
    if submit and new_pin:
        auth.set_pin(user["username"], new_pin)
        st.success("PIN updated.")


# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------
def main():
    if "user" not in st.session_state:
        render_login()
        return

    user = st.session_state["user"]
    df = load_submissions()

    with st.sidebar:
        st.markdown("**Youth Action Lead Liberia**")
        st.caption("M&E System")
        st.markdown(f"**{user['name']}**")
        st.caption(user["title"])
        st.markdown("---")

        vp = visible_projects(user)
        nav_options = ["Dashboard"] + [p["short_name"] for p in vp] + ["Community View", "Reports"]
        if user["role"] == "admin":
            nav_options.append("Manage")
        nav_options.append("Settings")
        choice = st.radio("Navigate", nav_options, label_visibility="collapsed")

        st.markdown("---")
        if st.button("Sign out"):
            del st.session_state["user"]
            st.rerun()

    if choice == "Dashboard":
        render_dashboard(user, df)
    elif choice == "Community View":
        render_community_view(user, df)
    elif choice == "Reports":
        render_reports(user, df)
    elif choice == "Manage":
        render_manage(user)
    elif choice == "Settings":
        render_settings(user)
    else:
        project_id = next(p["id"] for p in vp if p["short_name"] == choice)
        render_project(user, df, project_id)


if __name__ == "__main__":
    main()
