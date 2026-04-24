# Sprint 2 Plan — Venture 4: Krusty Compost Crew (Binny & Bloom)

**Sprint Duration:** April 8 – April 14, 2026
**Sprint Goal:** Fix unit conversion failures, create .env.example, improve demo script, and address known bugs.
**Final Demo:** April 29, 2026

---

## Context

After Milestone 2, Binny & Bloom has a working pantry-aware recipe system with login, inventory management, AI generation, and validation — both CLI and web versions. The main issues are unit conversion failures (6/20 test cases), missing `.env.example`, a weak demo script, and several code bugs. Sprint 2 stabilizes the system and prepares for a polished final demo.

---

## Sprint 2 Tasks

### P0 — Critical Fixes (Days 1–2)

| Task | Owner | Description |
|---|---|---|
| Create .env.example | Luis | Create `.env.example` with `OPENROUTER_API_KEY=your_key_here`. This was a "must fix" item from Milestone 2 |
| Fix unit conversion | Emma | Address the 6 failing test cases. Focus on tbsp↔ml, cup↔ml, oz↔g conversions. Add missing conversion factors to `unit_conversion.py` |
| Fix sort_inventory player_id | Luis | `sort_inventory()` in `expiry.py` queries ALL inventory — add player_id filter |
| Remove dead API key line | Luis | Remove `OPENROUTER_API_KEY=""` hardcoded at top of `app.py` |

### P1 — Demo Preparation (Days 2–4)

| Task | Owner | Description |
|---|---|---|
| Rewrite demo script | Jay | Rewrite `milestone2_demo_script.md` with clear, non-contradictory scenarios. Include exact steps, expected outputs, and failure cases |
| Populate generator.py | Emma | Either move generation logic into `generator.py` (from `openrouterllm.py`) or remove the empty file |
| Add refusal demo case | Abigail | Create a clear demo scenario showing the system refusing when pantry has insufficient/incompatible ingredients |
| Fix chat window closing | Luis | Address the known issue where chat window closes after recipe generation |

### P2 — Evaluation & Metrics (Days 3–5)

| Task | Owner | Description |
|---|---|---|
| Report missing metrics | Taja | Calculate and document expiry utilization rate and validator rejection rate |
| Reconcile test results | Abigail | MVP test cases (10, all passing) contradict evaluation results (6/20 failing). Reconcile and produce honest, consistent results |
| Add edge case tests | Taja | Test with: empty pantry, all items expired, single ingredient, conflicting dietary restrictions |

### P3 — UI Polish & Features (Days 5–7)

| Task | Owner | Description |
|---|---|---|
| Improve inventory display | Jay | Clean up the inventory table (currently has many columns). Prioritize key info: name, quantity, unit, expiry, status |
| Expiry notification UI | Taja | Make 3-day expiry alerts more prominent on dashboard |
| Waste reduction dashboard | Emma | Display the waste reduction score formula results on the user dashboard |
| Demo rehearsal | All | Full team demo run-through with both success and failure cases |

---

## Definition of Done (Sprint 2)

- [x] `.env.example` exists in the repo 
- [x] Unit conversion passes at least 17/20 test cases (up from 14/20)
- [x] `sort_inventory()` filters by current player_id 
- [x] Demo script has clear, consistent scenarios with expected outputs
- [x] Missing metrics (expiry utilization, validator rejection) are documented
- [x] Chat window stays open after recipe generation 
- [x] Each team member has code commits this sprint

---

## Contribution Expectations

Luis (143) and Abigail (138) carried the bulk. **Emma** (10 commits), **Taja** (18), and **Jay** (21) need to increase their code contributions. Sprint 2 tasks are distributed to ensure everyone works on substantive items.

---

## Remaining Sprints Overview

| Sprint | Dates | Focus |
|---|---|---|
| Sprint 2 (this sprint) | Apr 8–14 | Unit conversion, .env.example, demo script, bug fixes |
| Sprint 3 | Apr 15–21 | UI polish, waste dashboard, demo rehearsal |
| Sprint 4 | Apr 22–28 | Final integration, presentation prep, final deliverables |
| **Final Demo** | **Apr 29** | **Presentation and live demo** |
| Final Deliverables Due | May 3 | All documentation and code finalized |
