"""
Single source of truth for YALL's four real projects and their indicators,
taken from the M&E Framework / proposal documents Charles provided.

Edit this file when a project's objectives, indicators, targets, dates, or
communities change. Both the Kobo form generator (kobo/generate_xlsform.py)
and the dashboard (dashboard/app.py) read from here. After editing, re-run:

    python kobo/generate_xlsform.py

and re-upload the resulting .xlsx to Kobo to update the field form.

INDICATOR TYPES
---------------
  "count"     A running number that goes up over time (e.g. "farmers
              trained: 60"). Baseline and target are plain counts.

  "percent"   A percentage from an assessment round (e.g. "70% of trained
              miners aware of mining laws"). Logged as two raw numbers —
              how many were assessed, and how many showed the improvement.
              Baseline and target are percentages (0-100).

  "milestone" A one-time yes/it's-done achievement with a target of 1.

  "average"   Tracks a real average value over time (e.g. "average crop
              yield: 3.2 bags/acre") rather than a headcount or percentage.
              The FIRST entry ever logged for the indicator is treated as
              the baseline reading; every later entry is compared back to
              it to compute a % change, which is then measured against the
              indicator's target (itself a target % increase, e.g. 40%).
              Log a fresh average reading each time you re-measure (e.g.
              each harvest, or every few months for income/sales).

COMMUNITIES: each project lists the real communities it operates in
(used to tag every logged entry with where it happened — important since
several of these communities carry activity from more than one project).
"""

PROJECTS = [
    {
        "id": "uaf_women",
        "name": "Defending Women's Environmental and Human Rights Against Mining-Induced Degradation",
        "short_name": "Women's Rights & Anti-Mining Advocacy",
        "accent": "#B5542A",
        "funder": "Friends of Liberia Small Grants (UAF-Africa Rapid Response Grant)",
        "locations": "Bong & Lofa Counties",
        "objective": (
            "Strengthen women's legal empowerment and evidence-based advocacy against "
            "mining-induced environmental degradation, expand agroecological livelihoods "
            "among women farmers, and build a broader coalition to advance climate justice policy."
        ),
        "start_date": None,
        "end_date": None,
    },
    {
        "id": "agroecology",
        "name": "Agroecology for Resilient Livelihoods in Mining-Affected Communities",
        "short_name": "Agroecology",
        "accent": "#5B7A3A",
        "funder": "Friends of Liberia",
        "locations": "Tormue & Yowee, Bong County",
        "objective": (
            "Establish climate-smart agroecological demonstration sites, train 60 farmers "
            "in resilient farming and agro-entrepreneurship, and build sustainable, "
            "farmer-led systems for income and food security in mining-affected communities."
        ),
        "start_date": "2026-05-15",
        "end_date": "2027-05-14",
    },
    {
        "id": "legal_empowerment",
        "name": "Empowering Communities for Climate Justice through Legal Strategies for Safe Artisanal Mining Practices in Liberia",
        "short_name": "Legal Empowerment & Safe Mining",
        "accent": "#266873",
        "funder": "Fund for Global Human Rights",
        "locations": "Kiliwu, Zolowo, Kponwansanyea-Kpeteyea & Kpayaquelleh New Town (Lofa); Yowee, Gbargonai & David Deans Town (Bong)",
        "objective": (
            "Build a formal partnership with the EPA, train community members and artisanal "
            "miners in legal advocacy and safe mining practices, establish community advocacy "
            "structures and a Climate Justice Hub, and run school climate-change workshops."
        ),
        "start_date": "2025-01-01",
        "end_date": "2026-12-31",
    },
    {
        "id": "women_agri",
        "name": "The Women Agricultural Resilience Initiative",
        "short_name": "Women Agricultural Resilience Initiative",
        "accent": "#8A6D3B",
        "funder": "Mortenson Family Foundation",
        "locations": "Kiliwu, Kponwansanyea-Kpeteyea & Kpayaquelleh New Town (Lofa); Yowee & Tormue (Bong)",
        "objective": (
            "Move 400+ women farmers from subsistence farming into cooperative membership, "
            "mastering regenerative agricultural techniques, increasing yields and household "
            "income, restoring degraded farmland, and establishing community-led platforms "
            "engaging local authorities on land rights and environmental protection."
        ),
        "start_date": "2026-07-01",
        "end_date": "2028-06-30",  # ~24 months from start; confirm exact end date when known
    },
]

# Real communities each project operates in. Used to tag every logged entry
# with where it happened, since several of these towns carry activity from
# more than one project and that needs to stay checkable, not blurred together.
COMMUNITIES = {
    "uaf_women": ["Kiliwu", "Kponwansanyea-Kpeteyea", "Kpayaquelleh New Town", "Yowee", "Tormue"],
    "agroecology": ["Tormue", "Yowee"],
    "legal_empowerment": ["Kiliwu", "Zolowo", "Kponwansanyea-Kpeteyea", "Kpayaquelleh New Town", "Yowee", "Gbargonai", "David Deans Town"],
    "women_agri": ["Kiliwu", "Kponwansanyea-Kpeteyea", "Kpayaquelleh New Town", "Yowee", "Tormue"],
}

INDICATORS = [
    # ---- Project 1: Women's Rights & Anti-Mining Advocacy (uaf_women) ----
    {"id": "i1", "project_id": "uaf_women", "type": "count",
     "name": "Women leaders trained in legal empowerment, water monitoring, evidence gathering",
     "unit": "women leaders", "baseline": 0, "target": 100},
    {"id": "i2", "project_id": "uaf_women", "type": "count",
     "name": "Community dialogue sessions conducted",
     "unit": "sessions", "baseline": 0, "target": 10},
    {"id": "i3", "project_id": "uaf_women", "type": "milestone",
     "name": "Shadow report published",
     "unit": "reports", "baseline": 0, "target": 1},
    {"id": "i4", "project_id": "uaf_women", "type": "count",
     "name": "Copies of shadow report disseminated",
     "unit": "copies", "baseline": 0, "target": 50},
    {"id": "i5", "project_id": "uaf_women", "type": "count",
     "name": "Advocacy meetings held with decision-makers",
     "unit": "meetings", "baseline": 0, "target": 8},
    {"id": "i6", "project_id": "uaf_women", "type": "count",
     "name": "New EPA investigations initiated from community-generated evidence",
     "unit": "investigations", "baseline": 0, "target": 2},
    {"id": "i7", "project_id": "uaf_women", "type": "count",
     "name": "Agroecology demonstration plots established",
     "unit": "plots", "baseline": 0, "target": 5},
    {"id": "i8", "project_id": "uaf_women", "type": "count",
     "name": "Women farmers trained in agroecological practices",
     "unit": "women farmers", "baseline": 0, "target": 200},
    {"id": "i9", "project_id": "uaf_women", "type": "count",
     "name": "Women farmers adopting at least 4 agroecological techniques",
     "unit": "women farmers", "baseline": 0, "target": 200,
     "instrument": "Instrument 1 — Agroecological Technique Adoption Checklist (real farm visit, check off techniques observed; log how many farmers pass ≥4 in each visit round)"},
    {"id": "i10", "project_id": "uaf_women", "type": "count",
     "name": "Radio awareness sessions aired",
     "unit": "sessions", "baseline": 0, "target": 10},
    {"id": "i11", "project_id": "uaf_women", "type": "count",
     "name": "Social media content pieces produced",
     "unit": "content pieces", "baseline": 0, "target": 12},
    {"id": "i12", "project_id": "uaf_women", "type": "count",
     "name": "CSOs participating in the Rural Women Climate Justice Summit",
     "unit": "organizations", "baseline": 0, "target": 10},
    {"id": "i13", "project_id": "uaf_women", "type": "milestone",
     "name": "Policy proposal tabled by coalition",
     "unit": "proposals", "baseline": 0, "target": 1},
    {"id": "i14", "project_id": "uaf_women", "type": "count",
     "name": "Organizations in the coalition tabling the policy proposal",
     "unit": "organizations", "baseline": 0, "target": 5},

    # ---- Project 2: Agroecology (agroecology) ----
    {"id": "i15", "project_id": "agroecology", "type": "count",
     "name": "Agroecological demonstration sites established",
     "unit": "sites", "baseline": 0, "target": 2},
    {"id": "i16", "project_id": "agroecology", "type": "count",
     "name": "Demonstration sites with soil and water conservation structures in place",
     "unit": "sites", "baseline": 0, "target": 2},
    {"id": "i17", "project_id": "agroecology", "type": "count",
     "name": "Tool sheds and storage units constructed",
     "unit": "sheds", "baseline": 0, "target": 2},
    {"id": "i18", "project_id": "agroecology", "type": "count",
     "name": "Farmers trained in climate-smart agroecological practices",
     "unit": "farmers", "baseline": 0, "target": 60},
    {"id": "i19", "project_id": "agroecology", "type": "percent",
     "name": "Female participants among trained farmers",
     "unit": "%", "baseline": 0, "target": 50},
    {"id": "i20", "project_id": "agroecology", "type": "percent",
     "name": "Trained farmers demonstrating knowledge of at least 3 techniques",
     "unit": "%", "baseline": 0, "target": 75,
     "instrument": "Instrument 2 — Pre/Post Knowledge Test (composting, crop rotation, intercropping with mucuna, natural pest management, water conservation/mulching)"},
    {"id": "i21", "project_id": "agroecology", "type": "percent",
     "name": "Trained farmers adopting at least 3 new practices",
     "unit": "%", "baseline": 0, "target": 75,
     "instrument": "Instrument 3 — Farm Observation Checklist (same 5 techniques, checked in the field at mid-term and project end)"},
    {"id": "i22", "project_id": "agroecology", "type": "count",
     "name": "Vegetable crop varieties planted and harvested",
     "unit": "varieties", "baseline": 0, "target": 4},
    {"id": "i23", "project_id": "agroecology", "type": "percent",
     "name": "Harvest consumed by participating households",
     "unit": "%", "baseline": 0, "target": 50,
     "instrument": "Instrument 4 — Harvest Use Tracking Form, Section A (household consumption tally)"},
    {"id": "i24", "project_id": "agroecology", "type": "percent",
     "name": "Harvest sold collectively",
     "unit": "%", "baseline": 0, "target": 50,
     "instrument": "Instrument 4 — Harvest Use Tracking Form, Section B (group sales log)"},
    {"id": "i25", "project_id": "agroecology", "type": "count",
     "name": "Farmers completing agro-entrepreneurship training",
     "unit": "farmers", "baseline": 0, "target": 60},
    {"id": "i26", "project_id": "agroecology", "type": "count",
     "name": "Farmer groups maintaining financial records",
     "unit": "groups", "baseline": 0, "target": 2},
    {"id": "i27", "project_id": "agroecology", "type": "count",
     "name": "Farmer groups with an active susu fund",
     "unit": "groups", "baseline": 0, "target": 2},
    {"id": "i28", "project_id": "agroecology", "type": "average",
     "name": "Increase in average household income from produce sales",
     "unit": "%", "baseline": 0, "target": 25,
     "instrument": "Instrument 5 — Household Income Survey (baseline + periodic follow-up, same sampled households)"},
    {"id": "i29", "project_id": "agroecology", "type": "count",
     "name": "Farmer groups participating in final evaluation workshop",
     "unit": "groups", "baseline": 0, "target": 2},
    {"id": "i30", "project_id": "agroecology", "type": "count",
     "name": "Written sustainability plans produced and adopted",
     "unit": "plans", "baseline": 0, "target": 2},

    # ---- Project 3: Legal Empowerment & Safe Mining (legal_empowerment) ----
    {"id": "i31", "project_id": "legal_empowerment", "type": "milestone",
     "name": "Formal partnership agreement signed with EPA",
     "unit": "agreements", "baseline": 0, "target": 1},
    {"id": "i32", "project_id": "legal_empowerment", "type": "count",
     "name": "Joint activities conducted with EPA",
     "unit": "activities", "baseline": 0, "target": 2},
    {"id": "i33", "project_id": "legal_empowerment", "type": "count",
     "name": "Community members trained on legal advocacy",
     "unit": "people", "baseline": 0, "target": 120},
    {"id": "i34", "project_id": "legal_empowerment", "type": "percent",
     "name": "Trained community members demonstrating improved knowledge of land rights",
     "unit": "%", "baseline": 22.7, "target": 70,
     "instrument": "Instrument 6 — Community Legal Rights Test, Section A (land rights)"},
    {"id": "i35", "project_id": "legal_empowerment", "type": "percent",
     "name": "Trained community members who know where to report environmental damage",
     "unit": "%", "baseline": 21.3, "target": 70,
     "instrument": "Instrument 6 — Community Legal Rights Test, Section B (reporting channels)"},
    {"id": "i36", "project_id": "legal_empowerment", "type": "count",
     "name": "Community members engaged in documented advocacy action post-training",
     "unit": "people", "baseline": 0, "target": 60},
    {"id": "i37", "project_id": "legal_empowerment", "type": "count",
     "name": "Community advocacy associations formed and active",
     "unit": "associations", "baseline": 0, "target": 4},
    {"id": "i38", "project_id": "legal_empowerment", "type": "count",
     "name": "Active members across community advocacy associations",
     "unit": "members", "baseline": 0, "target": 40},
    {"id": "i39", "project_id": "legal_empowerment", "type": "count",
     "name": "Advocacy actions taken by association members",
     "unit": "actions", "baseline": 0, "target": 8},
    {"id": "i40", "project_id": "legal_empowerment", "type": "count",
     "name": "Community members reached through association-led advocacy activities",
     "unit": "people", "baseline": 0, "target": 60},
    {"id": "i41", "project_id": "legal_empowerment", "type": "count",
     "name": "Miners trained on safe mining practices",
     "unit": "miners", "baseline": 0, "target": 120},
    {"id": "i42", "project_id": "legal_empowerment", "type": "percent",
     "name": "Trained miners demonstrating improved knowledge of safety protocols",
     "unit": "%", "baseline": 0, "target": 75,
     "instrument": "Instrument 7 — Miner Safety Knowledge Test, Section A (safety protocols)"},
    {"id": "i43", "project_id": "legal_empowerment", "type": "percent",
     "name": "Trained miners reporting consistent PPE use post-training",
     "unit": "%", "baseline": 13.6, "target": 60,
     "instrument": "Instrument 8 — Miner Follow-up Survey, Section A (PPE use, 3 months post-training)"},
    {"id": "i44", "project_id": "legal_empowerment", "type": "percent",
     "name": "Trained miners aware of mining laws and regulations",
     "unit": "%", "baseline": 0, "target": 70,
     "instrument": "Instrument 7 — Miner Safety Knowledge Test, Section B (mining laws)"},
    {"id": "i45", "project_id": "legal_empowerment", "type": "percent",
     "name": "Miners who fill or cover pits after mining",
     "unit": "%", "baseline": 13.6, "target": 60,
     "instrument": "Instrument 8 — Miner Follow-up Survey, Section B (pit covering)"},
    {"id": "i46", "project_id": "legal_empowerment", "type": "count",
     "name": "Students reached through climate change workshops",
     "unit": "students", "baseline": 0, "target": 80},
    {"id": "i47", "project_id": "legal_empowerment", "type": "count",
     "name": "Schools participating in climate change workshops",
     "unit": "schools", "baseline": 0, "target": 4},
    {"id": "i48", "project_id": "legal_empowerment", "type": "percent",
     "name": "Students demonstrating improved climate change knowledge",
     "unit": "%", "baseline": 12.0, "target": 70,
     "instrument": "Instrument 9 — Student Climate Knowledge Test (pre/post)"},
    {"id": "i49", "project_id": "legal_empowerment", "type": "milestone",
     "name": "Climate Justice Hub established and operational",
     "unit": "hubs", "baseline": 0, "target": 1},
    {"id": "i50", "project_id": "legal_empowerment", "type": "count",
     "name": "Community-led climate-sensitive projects initiated through the hub",
     "unit": "projects", "baseline": 0, "target": 2},
    {"id": "i51", "project_id": "legal_empowerment", "type": "count",
     "name": "Community members engaged through hub activities",
     "unit": "people", "baseline": 0, "target": 50},
    {"id": "i52", "project_id": "legal_empowerment", "type": "count",
     "name": "Training manuals developed",
     "unit": "manuals", "baseline": 0, "target": 4},
    {"id": "i53", "project_id": "legal_empowerment", "type": "percent",
     "name": "Training sessions conducted using the developed manuals",
     "unit": "%", "baseline": 0, "target": 100},
    {"id": "i54", "project_id": "legal_empowerment", "type": "percent",
     "name": "Facilitators rating the training manuals as useful or highly useful",
     "unit": "%", "baseline": 0, "target": 80,
     "instrument": "Instrument 10 — Facilitator Feedback Form"},

    # ---- Project 4: Women Agricultural Resilience Initiative (women_agri) ----
    {"id": "i55", "project_id": "women_agri", "type": "count",
     "name": "Women farmers participating in training",
     "unit": "women farmers", "baseline": 0, "target": 500},
    {"id": "i56", "project_id": "women_agri", "type": "percent",
     "name": "Women farmers who know at least 3 climate-smart techniques",
     "unit": "%", "baseline": 0, "target": 80,
     "instrument": "Instrument 11 — Pre/Post Knowledge Test (biochar production, rainwater harvesting, vegetative filters, agroforestry, conservation agriculture)"},
    {"id": "i57", "project_id": "women_agri", "type": "percent",
     "name": "Women farmers applying at least 3 techniques on their farms",
     "unit": "%", "baseline": 0, "target": 80,
     "instrument": "Instrument 12 — Farm Observation Checklist (same 5 techniques, checked in the field)"},
    {"id": "i58", "project_id": "women_agri", "type": "average",
     "name": "Average crop yield increase",
     "unit": "%", "baseline": 0, "target": 40,
     "instrument": "Instrument 13 — Yield Tracking Form (baseline + follow-up after each harvest)"},
    {"id": "i59", "project_id": "women_agri", "type": "count",
     "name": "Women-led agricultural groups legally registered",
     "unit": "groups", "baseline": 0, "target": 10},
    {"id": "i60", "project_id": "women_agri", "type": "count",
     "name": "Registered groups actively selling produce together",
     "unit": "groups", "baseline": 0, "target": 10},
    {"id": "i61", "project_id": "women_agri", "type": "average",
     "name": "Average increase in group sales revenue",
     "unit": "%", "baseline": 0, "target": 60,
     "instrument": "Instrument 14 — Group Sales Tracking Form (baseline + ongoing group sales log)"},
    {"id": "i62", "project_id": "women_agri", "type": "average",
     "name": "Average increase in household income",
     "unit": "%", "baseline": 0, "target": 50,
     "instrument": "Instrument 15 — Household Income Survey (baseline + periodic follow-up, same sampled households)"},
    {"id": "i63", "project_id": "women_agri", "type": "percent",
     "name": "Households with improved food security (HDDS)",
     "unit": "%", "baseline": 0, "target": 70,
     "instrument": "Instrument 16 — HDDS Food Security Survey (baseline + follow-up, same sampled households)"},
    {"id": "i64", "project_id": "women_agri", "type": "count",
     "name": "Hectares of degraded farmland restored",
     "unit": "hectares", "baseline": 0, "target": 80},
    {"id": "i65", "project_id": "women_agri", "type": "count",
     "name": "Community platforms established, one per clan, engaging local authorities",
     "unit": "platforms", "baseline": 0, "target": 3},
]

# Coordinator roster used to build Kobo's "coordinator" choice list, and to
# seed dashboard accounts. Names here are placeholders — rename them in the
# dashboard's Manage page once you have the real coordinators assigned.
COORDINATORS = [
    {"username": "charles", "name": "Charles Karbedeh Jr.", "project": "all"},
    {"username": "women_coord", "name": "Women's Rights Coordinator", "project": "uaf_women"},
    {"username": "agro_coord", "name": "Agroecology Coordinator", "project": "agroecology"},
    {"username": "legal_coord", "name": "Legal Empowerment Coordinator", "project": "legal_empowerment"},
    {"username": "women_agri_coord", "name": "Women Agricultural Resilience Coordinator", "project": "women_agri"},
]


def project_by_id(pid):
    for p in PROJECTS:
        if p["id"] == pid:
            return p
    return None


def indicators_for(project_id):
    return [i for i in INDICATORS if i["project_id"] == project_id]


def communities_for(project_id):
    return COMMUNITIES.get(project_id, [])
