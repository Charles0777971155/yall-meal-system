"""
Pulls submissions from your Kobo form via the API and saves them to
data/submissions.csv, which the dashboard reads.

Setup (one time):
  1. In Kobo, open your form -> Settings -> find the form's UID in the URL,
     e.g. kf.kobotoolbox.org/#/forms/aAbBcCdD1234  ->  UID is "aAbBcCdD1234"
  2. Get your API token: Kobo account settings -> "API key" (or visit
     https://kf.kobotoolbox.org/token/?format=json while logged in)
  3. Set these as environment variables, or put them in .streamlit/secrets.toml
     (see .streamlit/secrets.toml.example) if running through the dashboard:
        KOBO_TOKEN=your_token_here
        KOBO_FORM_UID=your_form_uid_here
        KOBO_SERVER=https://kf.kobotoolbox.org   (default, change if self-hosted)

Run manually with:
    python kobo/pull_data.py

Or click "Refresh data from Kobo" inside the dashboard (admin only), which
calls the same function.
"""

import os
import csv

import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUT_CSV = os.path.join(DATA_DIR, "submissions.csv")

FIELDS = ["project", "indicator", "value", "assessed", "improved",
          "community", "group", "obs_date", "note", "coordinator", "_submission_time"]


def fetch_submissions(server, form_uid, token):
    """Fetch all submissions for a form, following pagination."""
    headers = {"Authorization": f"Token {token}"}
    url = f"{server.rstrip('/')}/api/v2/assets/{form_uid}/data.json"
    all_results = []

    while url:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        all_results.extend(payload.get("results", []))
        url = payload.get("next")  # Kobo paginates; None when done

    return all_results


def to_rows(submissions):
    rows = []
    for s in submissions:
        rows.append({
            "project": s.get("project", ""),
            "indicator": s.get("indicator", ""),
            "value": s.get("value", ""),
            "assessed": s.get("assessed", ""),
            "improved": s.get("improved", ""),
            "community": s.get("community", ""),
            "group": s.get("group", ""),
            "obs_date": s.get("obs_date", ""),
            "note": s.get("note", ""),
            "coordinator": s.get("coordinator", ""),
            "_submission_time": s.get("_submission_time", ""),
        })
    return rows


def save_csv(rows, path=OUT_CSV):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def run(server=None, form_uid=None, token=None):
    server = server or os.environ.get("KOBO_SERVER", "https://kf.kobotoolbox.org")
    form_uid = form_uid or os.environ.get("KOBO_FORM_UID")
    token = token or os.environ.get("KOBO_TOKEN")

    if not form_uid or not token:
        raise SystemExit(
            "Missing KOBO_FORM_UID and/or KOBO_TOKEN.\n"
            "Set them as environment variables, or pass them to run(), or\n"
            "fill in .streamlit/secrets.toml if calling this from the dashboard.\n"
            "See the docstring at the top of this file for how to find them."
        )

    submissions = fetch_submissions(server, form_uid, token)
    rows = to_rows(submissions)
    save_csv(rows)
    print(f"Pulled {len(rows)} submissions -> {OUT_CSV}")
    return len(rows)


if __name__ == "__main__":
    run()
