# YALL Data Collection Instruments

16 real data collection tools needed to feed the indicators that can't just be counted — they need a test, survey, or field visit first. For everything else (simple counts, milestones), a coordinator just tallies and logs the number directly; no instrument needed.

**Important note on Legal Empowerment's instruments (6–10):** the baseline percentages already on file (22.7%, 21.3%, 13.6%, 12.0%) came from an existing "Baseline Report" with its own original survey questions, which wasn't available when these were drafted. These are new instruments, not a reconstruction of the original — so follow-up percentages measured with these won't be a perfect apples-to-apples comparison against those exact baseline figures. Worth keeping in mind if this gets scrutinized closely by the funder.

---

## Project 1: Women's Rights & Anti-Mining Advocacy

### Instrument 1 — Agroecological Technique Adoption Checklist
**Feeds:** Women farmers adopting ≥4 agroecological techniques

A coordinator visits a trained farmer's plot after training and checks off which techniques are visible:
- ☐ Crop diversification (multiple crop types together)
- ☐ Composting / organic matter application
- ☐ Natural pest management (no synthetic pesticides)
- ☐ Water conservation or mulching
- ☐ Cover cropping / green manure
- ☐ Soil conservation structures (contour bunds, terracing)
- ☐ Crop rotation
- ☐ Agroforestry (trees integrated into farmland)

**Record:** farmer ID, community, date, number of techniques checked, pass/fail (≥4). Log the count of farmers who passed in a visit round as a **count** in the dashboard.

---

## Project 2: Agroecology

### Instrument 2 — Pre/Post Knowledge Test
**Feeds:** Trained farmers demonstrating knowledge of ≥3 techniques

Short quiz given right before training starts, and again right after it ends. Same questions both times. Covers the five techniques taught: **composting, crop rotation, intercropping (with mucuna), natural/integrated pest management, water conservation/mulching.** One simple multiple-choice question per technique. ≥3 correct = passing.

**Record:** farmer ID, date, number correct, pass/fail. Log as **assessed / improved** in the dashboard.

### Instrument 3 — Farm Observation Checklist
**Feeds:** Trained farmers adopting ≥3 new practices

Field visit at mid-term and again at project end. Coordinator checks off which of the same five techniques are actually visible in practice on each farmer's plot. ≥3 checked = adopting.

**Record:** farmer ID, date, number observed, pass/fail. Log as **assessed / improved**.

### Instrument 4 — Harvest Use Tracking Form
**Feeds:** Harvest consumed by households (Section A) and Harvest sold collectively (Section B)

**Section A (household level):** ask a sample of households, after each harvest, roughly what share of their harvest they kept for eating vs. sold.
**Section B (group level):** the farmer group's own sales log — how much was sold together through the group.

**Record:** community, date, total harvest amount, amount consumed, amount sold collectively. Log each section as **assessed / improved** (e.g. households consuming / households sampled).

### Instrument 5 — Household Income Survey
**Feeds:** Increase in average household income from produce sales

Ask a sample of households: "How much did your household earn from farming last month?" Once at the very start (baseline reading), then every few months, same households each time.

**Record:** household ID, date, monthly farming income reported. Log each round's **average** income as a single number — the dashboard's `average` indicator type compares it back to the first reading automatically.

---

## Project 3: Legal Empowerment & Safe Mining

### Instrument 6 — Community Legal Rights Test
**Feeds:** Improved knowledge of land rights (Section A) and knowing where to report environmental damage (Section B)

Quiz before and after legal advocacy training. Section A: land rights questions. Section B: "where would you report environmental/mining damage?" Scored separately.

**Record:** participant ID, date, section scores. Log each section as **assessed / improved**.

### Instrument 7 — Miner Safety Knowledge Test
**Feeds:** Improved safety knowledge (Section A) and awareness of mining laws (Section B)

Quiz before and after safe mining training. Section A: safety protocols (protective gear, safe digging practices). Section B: mining laws and regulations.

**Record:** miner ID, date, section scores. Log each section as **assessed / improved**.

### Instrument 8 — Miner Follow-up Survey
**Feeds:** Consistent PPE use (Section A) and pit-covering behavior (Section B)

Conducted 3 months after training — a field visit or interview with the same trained miners. Section A: "Do you consistently use PPE?" Section B: "Do you fill/cover pits after mining?" Both yes/no.

**Record:** miner ID, date, yes/no answers. Log each section as **assessed / improved**.

### Instrument 9 — Student Climate Knowledge Test
**Feeds:** Students demonstrating improved climate change knowledge

Short quiz before and after each school's climate change workshop.

**Record:** student ID (or anonymized), school, date, score. Log as **assessed / improved**.

### Instrument 10 — Facilitator Feedback Form
**Feeds:** Facilitators rating the training manuals as useful/highly useful

After each training session that uses one of the four manuals, the facilitator rates it: not useful / useful / highly useful, plus an optional comment.

**Record:** facilitator name, manual used, date, rating. Log as **assessed / improved** (assessed = facilitators asked, improved = rated useful or highly useful).

---

## Project 4: Women Agricultural Resilience Initiative

### Instrument 11 — Pre/Post Knowledge Test
**Feeds:** Women farmers who know ≥3 climate-smart techniques

Quiz before and after training, covering: **biochar production, rainwater harvesting, vegetative filters (soil/water remediation), agroforestry, conservation agriculture.** ≥3 correct = passing.

**Record:** farmer ID, date, number correct, pass/fail. Log as **assessed / improved**.

### Instrument 12 — Farm Observation Checklist
**Feeds:** Women farmers applying ≥3 techniques on their farms

Field visit checking which of the same five techniques are visible on each woman's plot. ≥3 observed = adopting.

**Record:** farmer ID, date, number observed, pass/fail. Log as **assessed / improved**.

### Instrument 13 — Yield Tracking Form
**Feeds:** Average crop yield increase

Record each participating farmer's typical harvest amount at the start (baseline reading). After each subsequent harvest, record the new amount, same plots.

**Record:** farmer/plot ID, date, harvest amount. Log each round's **average** yield as a single number.

### Instrument 14 — Group Sales Tracking Form
**Feeds:** Average increase in group sales revenue

Each of the 10 registered groups keeps a sales log. Their starting sales level (before cooperating, as individuals) is the baseline reading; ongoing collective sales are tracked from there.

**Record:** group ID, date, sales amount. Log each round's **average** across groups as a single number.

### Instrument 15 — Household Income Survey
**Feeds:** Average increase in household income

Same approach as Instrument 5 (Agroecology) — ask a sample of households their monthly farming income, once at baseline, then periodically.

**Record:** household ID, date, monthly income reported. Log each round's **average** as a single number.

### Instrument 16 — HDDS Food Security Survey
**Feeds:** Households with improved food security

Ask a household what food groups they ate in the last 24 hours, from the standard 8 food groups (grains, legumes, vegetables, fruit, meat/fish, dairy, oils, sugar). More groups = higher score. Done once at baseline, again later, same households.

**Record:** household ID, date, number of food groups eaten. Log as **assessed / improved** (assessed = households surveyed, improved = households whose score went up from baseline).

---

## Quick reference: which type goes with which instrument

| Dashboard type | What you log | Used by |
|---|---|---|
| **assessed / improved** | Two counts — how many checked/tested, how many passed/improved | Instruments 1–4, 6–12, 16 |
| **average** | A single average reading, repeated over time | Instruments 5, 13, 14, 15 |

Everything not listed above (simple counts, one-time milestones) doesn't need an instrument — just count and log the number directly.
