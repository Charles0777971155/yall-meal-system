# YALL M&E System (Kobo + Python + Streamlit)

A free, code-based M&E system for YALL's four real projects:

1. **Women's Rights & Anti-Mining Advocacy** — Defending Women's Environmental
   and Human Rights Against Mining-Induced Degradation (UAF-Africa Rapid
   Response Grant, via Friends of Liberia) — 14 indicators
2. **Agroecology** — Agroecology for Resilient Livelihoods in Mining-Affected
   Communities (Friends of Liberia) — 16 indicators
3. **Legal Empowerment & Safe Mining** — Empowering Communities for Climate
   Justice through Legal Strategies for Safe Artisanal Mining Practices
   (Fund for Global Human Rights) — 24 indicators
4. **Women Agricultural Resilience Initiative** — Mortenson Family Foundation — 11 indicators

65 indicators total, taken directly from the four M&E Framework / proposal
documents. Coordinators collect field data in Kobo. A Python script pulls it
in. A Streamlit dashboard shows progress per project, with its own login per
coordinator, flags indicators that need attention, and generates reports.
Everything here is free — no Power BI, no paid hosting.

## Indicator types

Each indicator is one of four types, and it changes what gets logged:

- **count** — a running number (e.g. "farmers trained: 60"). Log a single value.
- **percent** — a percentage from an assessment (e.g. "70% of trained miners
  aware of mining laws"). You log two raw numbers — how many were assessed,
  and how many showed the improvement — and the dashboard calculates the
  percentage.
- **milestone** — a one-time achievement with a target of 1 (e.g. "shadow
  report published"). Logged once as done.
- **average** — tracks a real average value over time (e.g. "average crop
  yield: 3.2 bags/acre") rather than a headcount. The first entry you ever
  log becomes the baseline reading; every later entry is compared back to
  it to compute a % change, measured against the indicator's target
  (itself a target % increase).

**16 of these indicators need real data collection first** (a knowledge
test, a follow-up survey, a farm visit) before a number can be logged — see
`YALL_Data_Collection_Instruments.md` for exactly what to do for each one.

## Communities & groups

Every logged entry records which **community** it happened in (from that
project's real community list) and, optionally, which **group/cohort** —
several of YALL's communities now carry activity from more than one
project, so this keeps entries checkable rather than blurred together.
See `YALL_Indicator_Reference.md` for the full breakdown of which projects
share which communities.

## "Needs attention" on the dashboard home

Rather than scanning all 54 indicators yourself, the dashboard home lists
indicators that either have no field data logged yet, or haven't been
updated in 60+ days (and aren't already at target) — so the ones that need
your attention surface on their own.

## How the pieces fit together

```
Kobo (field data collection)
   -> kobo/pull_data.py  (pulls submissions via Kobo API)
   -> data/submissions.csv
   -> dashboard/app.py   (Streamlit dashboard: login, progress, reports)
```

`config/indicators.py` is the single source of truth for both the Kobo form
and the dashboard — projects, indicators, baselines and targets all live
there, so the field form and the dashboard never drift apart.

## 1. Open this in VS Code and install dependencies

You need Python 3.10+ installed. Then, in a VS Code terminal:

```bash
cd yall-meal-vscode
python3 -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Try the dashboard right now, with sample data

No Kobo needed yet — there's sample data in `data/submissions_sample.csv`
so you can see it working immediately:

```bash
streamlit run dashboard/app.py
```

It opens in your browser. Log in as:
- **Charles Karbedeh Jr.** (sees all three projects) — PIN `1234`
- **Women's Rights Coordinator**, **Agroecology Coordinator**, **Legal
  Empowerment Coordinator**, **Women Agricultural Resilience Coordinator**
  (each sees only their project) — PIN `1234`

These coordinator names are placeholders — rename them to the real people
in the dashboard's **Manage** page whenever you're ready.

Change these PINs before real use (see step 6).

## 3. Set up Kobo

1. Create a free account at [kobotoolbox.org](https://www.kobotoolbox.org).
2. In Kobo, click **New** -> **Upload an XLSForm**, and upload
   `kobo/YALL_MEAL_Indicator_Update.xlsx` (already generated for you from
   your current indicators).
3. **Preview the form before deploying it** (Kobo has a built-in preview).
   Pick a project, then an indicator, and confirm that count/milestone
   indicators show a single "value" field, while percent indicators show
   "assessed" and "improved" fields instead. This conditional logic depends
   on how Kobo's form engine evaluates it — worth a quick check before
   coordinators start using it, and an easy fix in `kobo/generate_xlsform.py`
   if anything looks off.
4. **Deploy** the form. Coordinators can now open it in the Kobo web
   interface or the **KoboCollect** mobile app to log field updates.

If you ever change indicators in `config/indicators.py`, regenerate the
form and re-upload it:

```bash
python kobo/generate_xlsform.py
```

## 4. Connect the dashboard to your live Kobo data

1. Find your form's UID: open the form in Kobo, look at the URL —
   `kf.kobotoolbox.org/#/forms/aAbBcCdD1234`, the UID is `aAbBcCdD1234`.
2. Get your API token: while logged in, visit
   `https://kf.kobotoolbox.org/token/?format=json`.
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and
   fill in your token, form UID, and server URL. This file is git-ignored
   — it never gets committed or uploaded anywhere public.
4. Pull data manually any time with:
   ```bash
   python kobo/pull_data.py
   ```
   Or, as the admin (Charles), click **Refresh data from Kobo** inside the
   dashboard's **Manage** page — same effect, no terminal needed.

Coordinators can also log an update directly inside the dashboard (each
project page has a **Log update** button) — handy between Kobo syncs, or
if someone doesn't have the Kobo app open.

## 5. Deploy the dashboard online for free, with real logins

So coordinators can open it from a browser link rather than your laptop:

1. Push this project to a GitHub repository (make it **private** — it's
   free on GitHub, and keeps your data out of public view).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, click **New app**, point it at your repo and
   `dashboard/app.py`.
3. In the app's **Settings -> Secrets**, paste the same three lines from
   your local `secrets.toml` (KOBO_TOKEN, KOBO_FORM_UID, KOBO_SERVER).
4. Deploy. You'll get a URL like `yall-meal.streamlit.app` — share that
   with your coordinators. They log in with their own account and PIN,
   same as locally.

This hosting is entirely free on Streamlit Community Cloud.

## 6. Change PINs before real use

Two ways:
- Each person: log in, go to **Settings**, set a new PIN.
- Admin (Charles): **Manage** page, **Reset PIN** next to any account.

## Security note

This uses simple PIN-based login suited to a small internal team (a
handful of coordinators), not public internet exposure of sensitive data.
PINs are stored as SHA-256 hashes in `dashboard/users.yaml`, never in
plain text — but this is not bank-grade security. Keep your GitHub repo
private, and if this ever needs to hold more sensitive data or serve a
larger audience, it's worth upgrading to a proper auth library (e.g.
`streamlit-authenticator`) or Google/Microsoft login.

## Project layout

```
config/indicators.py          Projects, indicators, types, baselines & targets (edit here)
kobo/generate_xlsform.py      Builds the Kobo form from config/indicators.py
kobo/YALL_MEAL_Indicator_Update.xlsx   The generated form — upload to Kobo
kobo/pull_data.py             Pulls Kobo submissions into data/submissions.csv
dashboard/app.py              The Streamlit dashboard
dashboard/auth.py             Login / PIN handling
dashboard/users.yaml          Accounts and PIN hashes
data/submissions_sample.csv   Sample data so the dashboard works before Kobo is connected
data/submissions.csv          Real pulled data (created once you connect Kobo; git-ignored)
```
