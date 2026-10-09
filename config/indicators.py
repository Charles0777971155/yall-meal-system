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
    # ---- Project: legal_empowerment ----
    {"id": "i31", "project_id": "legal_empowerment", "type": "milestone", "name": "Formal partnership agreement signed with EPA", "unit": "agreements", "baseline": 0, "target": 1, "mov": "Signed partnership agreement document"},
    {"id": "i32", "project_id": "legal_empowerment", "type": "count", "name": "Joint activities conducted with EPA (trainings, monitoring visits, compliance sessions)", "unit": "activities", "baseline": 0, "target": 2, "mov": "Joint activity reports and meeting minutes"},
    {"id": "i33", "project_id": "legal_empowerment", "type": "count", "name": "Community members trained on legal advocacy", "unit": "people", "baseline": 0, "target": 120, "mov": "Training attendance registers", "gender_disagg": True},
    {"id": "i34", "project_id": "legal_empowerment", "type": "percent", "name": "Trained community members aware of land rights", "unit": "%", "baseline": 22.7, "target": 70, "mov": "Pre- and post-test scores", "instrument": "Instrument 6 — Community Legal Rights Test, Section A (land rights)"},
    {"id": "i35", "project_id": "legal_empowerment", "type": "percent", "name": "Trained community members who know where to report environmental damage", "unit": "%", "baseline": 21.3, "target": 70, "mov": "Pre- and post-test scores", "instrument": "Instrument 6 — Community Legal Rights Test, Section B (reporting channels)"},
    {"id": "i36", "project_id": "legal_empowerment", "type": "count", "name": "Community members engaged in documented advocacy action post-training", "unit": "people", "baseline": 0, "target": 60, "mov": "Post-training follow-up survey", "gender_disagg": True},
    {"id": "i37", "project_id": "legal_empowerment", "type": "count", "name": "Community advocacy associations (Community Advocacy Hub) formed and active", "unit": "associations", "baseline": 0, "target": 4, "mov": "Association formation documentation and meeting minutes"},
    {"id": "i38", "project_id": "legal_empowerment", "type": "count", "name": "Active members across community advocacy associations (at least 10 per community)", "unit": "members", "baseline": 0, "target": 40, "mov": "Association membership register", "gender_disagg": True},
    {"id": "i39", "project_id": "legal_empowerment", "type": "count", "name": "Advocacy actions taken by association members (at least 2 per community)", "unit": "actions", "baseline": 0, "target": 8, "mov": "Advocacy activity reports and meeting minutes"},
    {"id": "i40", "project_id": "legal_empowerment", "type": "count", "name": "Community members reached through association-led advocacy activities", "unit": "people", "baseline": 0, "target": 60, "mov": "Attendance records from association-led activities", "gender_disagg": True},
    {"id": "i41", "project_id": "legal_empowerment", "type": "count", "name": "Miners trained on safe mining practices", "unit": "miners", "baseline": 0, "target": 120, "mov": "Training attendance registers", "gender_disagg": True},
    {"id": "i42", "project_id": "legal_empowerment", "type": "percent", "name": "Trained miners demonstrating improved knowledge of safety protocols", "unit": "%", "baseline": 0, "target": 75, "mov": "Pre- and post-test scores", "instrument": "Instrument 7 — Miner Safety Knowledge Test, Section A (safety protocols)"},
    {"id": "i43", "project_id": "legal_empowerment", "type": "percent", "name": "Trained miners reporting consistent PPE use at 3-month follow-up", "unit": "%", "baseline": 13.6, "target": 60, "mov": "3-month post-training follow-up survey", "instrument": "Instrument 8 — Miner Follow-up Survey, Section A (PPE use, 3 months post-training)"},
    {"id": "i44", "project_id": "legal_empowerment", "type": "percent", "name": "Trained miners aware of mining laws and regulations", "unit": "%", "baseline": 0, "target": 70, "mov": "Pre- and post-test scores", "instrument": "Instrument 7 — Miner Safety Knowledge Test, Section B (mining laws)"},
    {"id": "i45", "project_id": "legal_empowerment", "type": "percent", "name": "Trained miners who fill or cover pits after mining", "unit": "%", "baseline": 13.6, "target": 60, "mov": "Post-training follow-up survey", "instrument": "Instrument 8 — Miner Follow-up Survey, Section B (pit covering)"},
    {"id": "i46", "project_id": "legal_empowerment", "type": "count", "name": "Students reached through climate change workshops (the student hub ambassadors)", "unit": "students", "baseline": 0, "target": 80, "mov": "Workshop attendance registers", "gender_disagg": True},
    {"id": "i47", "project_id": "legal_empowerment", "type": "count", "name": "Schools participating in climate change workshops", "unit": "schools", "baseline": 0, "target": 4, "mov": "School participation records"},
    {"id": "i48", "project_id": "legal_empowerment", "type": "percent", "name": "Students demonstrating improved climate change knowledge after workshops", "unit": "%", "baseline": 0, "target": 70, "mov": "Pre- and post-test scores", "instrument": "Instrument 9 — Student Climate Knowledge Test (pre/post)", "reference_value": 34, "reference_unit": "% mean pre-test score", "reference_note": "Improved = post-test score at least 20 percentage points above own pre-test score. Use same test at post-test."},
    {"id": "i50", "project_id": "legal_empowerment", "type": "count", "name": "Community-led climate-sensitive projects initiated through the hub", "unit": "projects", "baseline": 0, "target": 2, "mov": "Project documentation and activity logs"},
    {"id": "i70", "project_id": "legal_empowerment", "type": "count", "name": "Student-led climate justice initiatives implemented on campuses through the hub", "unit": "initiatives", "baseline": 0, "target": 5, "mov": "Project documentation and activity logs; school records of implemented initiatives"},
    {"id": "i51", "project_id": "legal_empowerment", "type": "count", "name": "Community members engaged through hub activities", "unit": "people", "baseline": 0, "target": 50, "mov": "Participant records and visitor logs", "gender_disagg": True},
    {"id": "i52", "project_id": "legal_empowerment", "type": "count", "name": "Training manuals developed (legal advocacy, safe mining, climate change, hub management)", "unit": "manuals", "baseline": 0, "target": 4, "mov": "Completed manual documents"},
    {"id": "i53", "project_id": "legal_empowerment", "type": "percent", "name": "Planned training sessions delivered using the developed manuals", "unit": "%", "baseline": 0, "target": 100, "mov": "Training session reports"},
    {"id": "i54", "project_id": "legal_empowerment", "type": "percent", "name": "Facilitators rating the training manuals as useful or highly useful", "unit": "%", "baseline": 0, "target": 80, "mov": "Facilitator feedback forms", "instrument": "Instrument 10 — Facilitator Feedback Form"},
    # ---- Project: agroecology ----
    {"id": "i15", "project_id": "agroecology", "type": "count", "name": "Agroecological demonstration sites established", "unit": "sites", "baseline": 0, "target": 2, "mov": "Mapping; photographic evidence; site visit reports; community meeting minutes"},
    {"id": "i16", "project_id": "agroecology", "type": "count", "name": "Demonstration sites with soil and water conservation structures in place", "unit": "sites", "baseline": 0, "target": 2, "mov": "Site visit reports and photographic documentation"},
    {"id": "i17", "project_id": "agroecology", "type": "count", "name": "Tool sheds and storage units constructed", "unit": "sheds", "baseline": 0, "target": 2, "mov": "Physical inspection and photographic evidence"},
    {"id": "i18", "project_id": "agroecology", "type": "count", "name": "Farmers trained in climate-smart agroecological practices", "unit": "farmers", "baseline": 0, "target": 60, "mov": "Training attendance sheets", "gender_disagg": True},
    {"id": "i19", "project_id": "agroecology", "type": "percent", "name": "Female participants among trained farmers", "unit": "%", "baseline": 0, "target": 50, "mov": "Training attendance sheets disaggregated by gender"},
    {"id": "i20", "project_id": "agroecology", "type": "percent", "name": "Trained farmers demonstrating knowledge of at least 3 techniques", "unit": "%", "baseline": 0, "target": 75, "mov": "Pre- and post-training knowledge assessments", "instrument": "Instrument 2 — Pre/Post Knowledge Test (composting, crop rotation, intercropping with mucuna, natural pest management, water conservation/mulching)"},
    {"id": "i21", "project_id": "agroecology", "type": "percent", "name": "Trained farmers adopting at least 3 new practices", "unit": "%", "baseline": 0, "target": 75, "mov": "Farm observation checklists; focus group discussions", "instrument": "Instrument 3 — Farm Observation Checklist (same 5 techniques, checked in the field at mid-term and project end)"},
    {"id": "i22", "project_id": "agroecology", "type": "count", "name": "Vegetable crop varieties planted and harvested", "unit": "varieties", "baseline": 0, "target": 4, "mov": "Harvest record logs maintained by farmer groups; site visit reports"},
    {"id": "i23", "project_id": "agroecology", "type": "percent", "name": "Harvest consumed by participating households", "unit": "%", "baseline": 0, "target": 50, "mov": "Household consumption surveys", "instrument": "Instrument 4 — Harvest Use Tracking Form, Section A (household consumption tally)"},
    {"id": "i24", "project_id": "agroecology", "type": "percent", "name": "Harvest sold collectively", "unit": "%", "baseline": 0, "target": 50, "mov": "Sales receipts; group record books", "instrument": "Instrument 4 — Harvest Use Tracking Form, Section B (group sales log)"},
    {"id": "i25", "project_id": "agroecology", "type": "count", "name": "Farmers completing agro-entrepreneurship training", "unit": "farmers", "baseline": 0, "target": 60, "mov": "Training attendance sheets", "gender_disagg": True},
    {"id": "i26", "project_id": "agroecology", "type": "count", "name": "Farmer groups maintaining financial records", "unit": "groups", "baseline": 0, "target": 2, "mov": "Review of group record books and sales receipts"},
    {"id": "i27", "project_id": "agroecology", "type": "count", "name": "Farmer groups with an active susu fund", "unit": "groups", "baseline": 0, "target": 2, "mov": "Review of group savings records and meeting minutes"},
    {"id": "i28", "project_id": "agroecology", "type": "average", "name": "Increase in average household income from produce sales", "unit": "%", "baseline": 0, "target": 25, "mov": "Household income surveys, baseline vs. follow-up", "instrument": "Instrument 5 — Household Income Survey (baseline + periodic follow-up, same sampled households)", "reference_value": 2839, "reference_unit": "LD per household per year", "reference_note": "Baseline survey, 14 households, band midpoints; top band valued at 10,000. +25% = about LD 3,549."},
    {"id": "i29", "project_id": "agroecology", "type": "count", "name": "Farmer groups participating in final evaluation workshop", "unit": "groups", "baseline": 0, "target": 2, "mov": "Workshop attendance sheets and meeting minutes"},
    {"id": "i30", "project_id": "agroecology", "type": "count", "name": "Written sustainability plans produced and adopted", "unit": "plans", "baseline": 0, "target": 2, "mov": "Review of final sustainability plan documents"},
    # ---- Project: uaf_women ----
    {"id": "i1", "project_id": "uaf_women", "type": "count", "name": "Women leaders trained in legal empowerment, water monitoring, evidence gathering", "unit": "women leaders", "baseline": 0, "target": 100, "mov": "Training attendance registers; pre/post assessments; workshop reports"},
    {"id": "i2", "project_id": "uaf_women", "type": "count", "name": "Community dialogue sessions conducted", "unit": "sessions", "baseline": 0, "target": 10, "mov": "Session reports; testimony records; photo/video/audio documentation"},
    {"id": "i3", "project_id": "uaf_women", "type": "milestone", "name": "Shadow report published", "unit": "reports", "baseline": 0, "target": 1, "mov": "Published report; distribution list; media coverage log"},
    {"id": "i4", "project_id": "uaf_women", "type": "count", "name": "Copies of shadow report disseminated", "unit": "copies", "baseline": 0, "target": 50, "mov": "Distribution/dissemination list"},
    {"id": "i5", "project_id": "uaf_women", "type": "count", "name": "Advocacy meetings held with decision-makers", "unit": "meetings", "baseline": 0, "target": 8, "mov": "Meeting minutes/attendance sheets; official correspondence"},
    {"id": "i6", "project_id": "uaf_women", "type": "count", "name": "New EPA investigations initiated from community-generated evidence", "unit": "investigations", "baseline": 0, "target": 2, "mov": "EPA public statements/reports; official correspondence"},
    {"id": "i7", "project_id": "uaf_women", "type": "count", "name": "Agroecology demonstration plots established", "unit": "plots", "baseline": 0, "target": 5, "mov": "Plot establishment reports; site visit records"},
    {"id": "i8", "project_id": "uaf_women", "type": "count", "name": "Women farmers trained in agroecological practices", "unit": "women farmers", "baseline": 0, "target": 200, "mov": "Training attendance records"},
    {"id": "i9", "project_id": "uaf_women", "type": "count", "name": "Women farmers adopting at least 4 agroecological techniques", "unit": "women farmers", "baseline": 0, "target": 200, "mov": "Follow-up farmer surveys; field observation reports", "instrument": "Instrument 1 — Agroecological Technique Adoption Checklist (real farm visit, check off techniques observed; log how many farmers pass ≥4 in each visit round)"},
    {"id": "i10", "project_id": "uaf_women", "type": "count", "name": "Radio awareness sessions aired", "unit": "sessions", "baseline": 0, "target": 10, "mov": "Radio station broadcast logs"},
    {"id": "i11", "project_id": "uaf_women", "type": "count", "name": "Social media content pieces produced", "unit": "content pieces", "baseline": 0, "target": 12, "mov": "Social media analytics/screenshots"},
    {"id": "i12", "project_id": "uaf_women", "type": "count", "name": "CSOs, women's rights organizations and environmental justice networks participating in the Rural Women Climate Justice Summit", "unit": "organizations", "baseline": 0, "target": 10, "mov": "Summit attendance list"},
    {"id": "i13", "project_id": "uaf_women", "type": "milestone", "name": "Policy proposal on environmental and land tenure clauses in mining concession agreements tabled by the coalition", "unit": "proposals", "baseline": 0, "target": 1, "mov": "Coalition MOU; submitted policy proposal document"},
    {"id": "i14", "project_id": "uaf_women", "type": "count", "name": "Community-based CSOs in the coalition tabling the policy proposal", "unit": "organizations", "baseline": 0, "target": 5, "mov": "Coalition MOU; membership list"},
    {"id": "i66", "project_id": "uaf_women", "type": "count", "name": "EPA investigations with initial findings publicly reported", "unit": "investigations", "baseline": 0, "target": 2, "mov": "EPA public statements/reports; official correspondence"},
    {"id": "i67", "project_id": "uaf_women", "type": "count", "name": "Evidence submissions (water test results, photo and video documentation, testimonies) by trained women leaders to the EPA (at least 2 per community)", "unit": "submissions", "baseline": 0, "target": 10, "mov": "Submission records; copies of water test results, photo/video documentation, and testimonies submitted to the EPA"},
    {"id": "i68", "project_id": "uaf_women", "type": "percent", "name": "Adopting women farmers reporting improved soil health and crop diversity and growth", "unit": "%", "baseline": 0, "target": 70, "mov": "Follow-up farmer surveys; field observation of soil health and crop diversity"},
    {"id": "i69", "project_id": "uaf_women", "type": "percent", "name": "Adopting women farmers reporting improved food security and economic independence", "unit": "%", "baseline": 0, "target": 70, "mov": "Household survey; follow-up interviews with adopting women farmers"},
    # ---- Project: women_agri ----
    {"id": "i55", "project_id": "women_agri", "type": "count", "name": "Women farmers participating in training", "unit": "women farmers", "baseline": 0, "target": 500, "mov": "Training attendance registers"},
    {"id": "i56", "project_id": "women_agri", "type": "percent", "name": "Trained women farmers who know at least 3 climate-smart techniques", "unit": "%", "baseline": 7.5, "target": 80, "mov": "Pre/post knowledge assessment", "instrument": "Instrument 11 — Pre/Post Knowledge Test (biochar production, rainwater harvesting, vegetative filters, agroforestry, conservation agriculture)"},
    {"id": "i57", "project_id": "women_agri", "type": "percent", "name": "Trained women farmers applying at least 3 techniques on their farms", "unit": "%", "baseline": 0, "target": 80, "mov": "Farm observation / follow-up survey", "instrument": "Instrument 12 — Farm Observation Checklist (same 5 techniques, checked in the field)"},
    {"id": "i58", "project_id": "women_agri", "type": "average", "name": "Average crop yield increase", "unit": "%", "baseline": 0, "target": 40, "mov": "Harvest records, baseline vs. follow-up", "instrument": "Instrument 13 — Yield Tracking Form (baseline + follow-up after each harvest)", "reference_unit": "kg per sample square", "reference_note": "Pending: set from sample squares measured at harvest, same farmers at endline."},
    {"id": "i59", "project_id": "women_agri", "type": "count", "name": "Women-led agricultural groups legally registered (by end of project)", "unit": "groups", "baseline": 0, "target": 10, "mov": "Registration certificates"},
    {"id": "i60", "project_id": "women_agri", "type": "count", "name": "Registered groups actively selling produce together", "unit": "groups", "baseline": 0, "target": 10, "mov": "Group sales records"},
    {"id": "i61", "project_id": "women_agri", "type": "average", "name": "Average increase in group sales revenue", "unit": "%", "baseline": 0, "target": 60, "mov": "Group sales record books, baseline vs. follow-up", "instrument": "Instrument 14 — Group Sales Tracking Form (baseline + ongoing group sales log)", "reference_unit": "LD per group", "reference_note": "Pending: set from each group first marketing season sales."},
    {"id": "i62", "project_id": "women_agri", "type": "average", "name": "Average increase in household income", "unit": "%", "baseline": 0, "target": 50, "mov": "Household economy survey, baseline vs. follow-up", "instrument": "Instrument 15 — Household Income Survey (baseline + periodic follow-up, same sampled households)", "reference_value": 7482, "reference_unit": "LD per household per year", "reference_note": "Produce plus palm oil income only, baseline survey, 14 households. +50% = about LD 11,223. Use same sources at endline."},
    {"id": "i63", "project_id": "women_agri", "type": "percent", "name": "Women-headed households facing severe food insecurity (measured by HDDS)", "unit": "%", "baseline": 75, "target": 22.5, "mov": "HDDS survey, baseline vs. follow-up", "instrument": "Instrument 16 — HDDS Food Security Survey (baseline + follow-up, same sampled households)"},
    {"id": "i64", "project_id": "women_agri", "type": "count", "name": "Hectares of degraded farmland restored", "unit": "hectares", "baseline": 0, "target": 80, "mov": "Land restoration site records / mapping"},
    {"id": "i65", "project_id": "women_agri", "type": "count", "name": "Community platforms established, one per clan, engaging local authorities on land rights and environmental protection", "unit": "platforms", "baseline": 0, "target": 3, "mov": "Platform documentation; meeting records with authorities"},
    {"id": "i71", "project_id": "women_agri", "type": "count", "name": "Women-led agricultural groups that are financially literate", "unit": "groups", "baseline": 0, "target": 10, "mov": "Financial literacy training completion records; group assessment results"},
    {"id": "i72", "project_id": "women_agri", "type": "count", "name": "Community platforms with women leaders in key roles", "unit": "platforms", "baseline": 0, "target": 3, "mov": "Platform leadership documentation; meeting minutes identifying officer roles"},
]


# Gantt-supported timing windows for status interpretation.
# These are implementation/measurement windows derived from Gantt.docx.
# They are intentionally windows, not invented monthly achievement targets.
GANTT_TIMING = {
    # Legal Empowerment project: Jan 2025-Dec 2026
    "i31": ("2025-04-01", "2025-09-30", "EPA partnership building and engagement"),
    "i32": ("2025-04-01", "2025-09-30", "EPA partnership building / joint activities"),
    "i33": ("2025-07-01", "2025-12-31", "Training community members on legal advocacy"),
    "i34": ("2025-07-01", "2025-12-31", "Post-training legal rights assessment"),
    "i35": ("2025-07-01", "2025-12-31", "Post-training reporting-channel assessment"),
    "i36": ("2026-07-01", "2026-12-31", "Post-training follow-up monitoring"),
    "i37": ("2025-07-01", "2025-12-31", "Establishing advocacy hub"),
    "i38": ("2025-07-01", "2026-06-30", "Advocacy hub membership / activity"),
    "i39": ("2025-07-01", "2026-12-31", "Advocacy hub activities"),
    "i40": ("2025-07-01", "2026-12-31", "Association-led advocacy activities"),
    "i41": ("2025-07-01", "2025-12-31", "Training miners on safe mining practices"),
    "i42": ("2025-07-01", "2025-12-31", "Miner training / post-test"),
    "i43": ("2026-07-01", "2026-12-31", "Post-training follow-up monitoring"),
    "i44": ("2025-07-01", "2025-12-31", "Miner training / post-test"),
    "i45": ("2026-07-01", "2026-12-31", "Post-training follow-up monitoring"),
    "i46": ("2025-07-01", "2025-12-31", "Workshops for students on climate change"),
    "i47": ("2025-07-01", "2025-12-31", "Workshops for students on climate change"),
    "i48": ("2025-07-01", "2025-12-31", "Student climate workshop post-test"),
    "i50": ("2025-10-01", "2026-06-30", "Establishing Climate Justice Hub"),
    "i70": ("2025-10-01", "2026-06-30", "Climate Justice Hub activities"),
    "i51": ("2025-10-01", "2026-06-30", "Climate Justice Hub activities"),
    "i52": ("2025-04-01", "2025-09-30", "Develop training manuals"),
    "i53": ("2025-07-01", "2026-12-31", "Training sessions using developed manuals"),
    "i54": ("2025-07-01", "2026-12-31", "Facilitator feedback after manual use"),

    # Agroecology project: 15 May 2026-14 May 2027
    "i15": ("2026-06-01", "2026-09-30", "Demonstration sites / land preparation"),
    "i16": ("2026-06-01", "2026-09-30", "Land preparation / soil and water conservation"),
    "i17": ("2026-06-01", "2026-07-31", "Construction of tool sheds and seed storage units"),
    "i18": ("2026-08-01", "2026-09-30", "Launch of Climate-Smart Agroecology Training"),
    "i19": ("2026-08-01", "2026-09-30", "Launch of Climate-Smart Agroecology Training"),
    "i20": ("2026-08-01", "2026-09-30", "Training knowledge assessment"),
    "i21": ("2026-08-01", "2027-04-30", "Continuous technical mentorship / farm observation"),
    "i22": ("2026-08-01", "2027-03-31", "Planting and harvesting primary vegetable crops"),
    "i23": ("2026-11-01", "2027-03-31", "Harvesting and post-harvest handling"),
    "i24": ("2026-11-01", "2027-03-31", "Harvesting / market connections"),
    "i25": ("2026-10-01", "2026-12-31", "Agro-Entrepreneurship and Market Facilitation Workshops"),
    "i26": ("2026-10-01", "2027-03-31", "Bookkeeping / group financial management"),
    "i27": ("2026-11-01", "2027-01-31", "Group savings (susu) fund establishment"),
    "i28": ("2027-03-01", "2027-04-30", "Endline household income survey"),
    "i29": ("2027-03-01", "2027-04-30", "Participatory final evaluation workshop"),
    "i30": ("2027-03-01", "2027-04-30", "Community sustainability plans"),

    # Women's Environmental and Human Rights project: Aug 2026-Aug 2027
    "i1": ("2026-09-01", "2026-10-31", "Capacity-building workshops"),
    "i2": ("2026-10-01", "2026-11-30", "Community dialogue sessions"),
    "i3": ("2026-10-01", "2026-11-30", "Shadow report development"),
    "i4": ("2026-12-01", "2027-01-31", "Shadow report dissemination"),
    "i5": ("2026-12-01", "2027-04-30", "Direct advocacy meetings"),
    "i6": ("2026-12-01", "2027-04-30", "Direct advocacy / EPA engagement"),
    "i7": ("2026-10-01", "2026-11-30", "Establishment of agroecology demonstration plots"),
    "i8": ("2026-11-01", "2027-06-30", "Agroecology training and technical support"),
    "i9": ("2027-01-01", "2027-06-30", "Agroecology training / farmer adoption follow-up"),
    "i10": ("2026-11-01", "2027-05-31", "Local radio awareness sessions"),
    "i11": ("2026-08-01", "2027-06-30", "Social media campaign"),
    "i12": ("2027-06-01", "2027-07-31", "Rural Women Climate Justice Summit"),
    "i13": ("2027-06-01", "2027-08-31", "Coalition policy development / summit"),
    "i14": ("2027-06-01", "2027-08-31", "Coalition policy development / summit"),
    "i66": ("2026-12-01", "2027-04-30", "Direct advocacy / EPA engagement"),
    "i67": ("2026-12-01", "2027-04-30", "Direct advocacy / evidence submissions"),
    "i68": ("2027-01-01", "2027-08-31", "Agroecology training / farmer outcome follow-up"),
    "i69": ("2027-01-01", "2027-08-31", "Agroecology training / farmer outcome follow-up"),

    # Women Agricultural Resilience Initiative: Sep 2026-Aug 2028
    "i55": ("2026-11-01", "2027-10-31", "Training of women farmers in regenerative techniques"),
    "i56": ("2026-11-01", "2027-10-31", "Women farmer training / knowledge assessment"),
    "i57": ("2027-03-01", "2028-04-30", "Farm application follow-up / restoration"),
    "i58": ("2028-07-01", "2028-08-31", "Endline crop yield measurement"),
    "i59": ("2027-05-01", "2028-04-30", "Legal registration of women-led groups"),
    "i60": ("2027-05-01", "2028-06-30", "Collective marketing and market linkages"),
    "i61": ("2027-05-01", "2028-06-30", "Collective marketing / sales tracking"),
    "i62": ("2028-07-01", "2028-08-31", "Endline household income measurement"),
    "i63": ("2028-07-01", "2028-08-31", "Endline HDDS data collection"),
    "i64": ("2026-11-01", "2028-06-30", "Demonstration plots / restoration of degraded farmland"),
    "i65": ("2027-01-01", "2028-06-30", "Establishment of community-led platforms"),
    "i71": ("2027-05-01", "2028-06-30", "Financial literacy and VSLA training"),
    "i72": ("2027-01-01", "2028-06-30", "Community-led platforms / leadership"),
}

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
