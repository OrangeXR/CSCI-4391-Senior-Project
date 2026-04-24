# Sprint 2 Grade — Venture 4: Krusty Compost Crew (Binny & Bloom)

**Graded:** April 15, 2026
**Sprint Window:** April 8 – April 14, 2026
**Graded Against:** `docs/Sprint 2.md`

---

## Overall Grade: 93/100

Binny & Bloom had one of the strongest Sprint 2s of the cohort. Every P0 item is done, all four P1 items are done, all three P2 items are done, and one of four P3 items is complete (chat window already addressed in Sprint 2; inventory table cleanup also landed). The team cleared the full critical list and most of the polish list, with code from every team member. The main things keeping this out of the high 90s are: the Definition of Done checklist in `Sprint 2.md` is out of date (two items are marked unchecked even though the work shipped), the waste reduction dashboard is not yet implemented, and Sprint 2's reported evaluation results still leave a small gap (3 of 20 reconciled cases fail, 1 of 4 edge cases fails) that needs to be acknowledged in the final demo.

---

## Category Breakdown

### 1. Task Completion (38/40)

**P0 — Critical Fixes (all complete):**
- `src/.env.example` created with `OPENROUTER_API_KEY=your_key_here` (commits b812242, f04bacf, Luis). ✓
- Unit conversion coverage expanded in `src/unit_conversion.py`: oz→g, mg→g, cup→ml, tbsp→ml, tsp→ml, liter→ml, gallon→ml (seven Emma commits on 4/11). ✓
- `sort_inventory()` in `src/expiry.py` now takes `player_id` and filters the SQL with `WHERE player_id = ?`. All three callers (`validator.py`, `main.py`, `openrouterllm.py`) updated (commit 2c809bd, Luis). ✓
- Hardcoded `OPENROUTER_API_KEY=""` removed from top of `src/app.py`; only a commented Authorization header remains (commit 1541ab4, Luis). ✓

**P1 — Demo Preparation (all complete):**
- `docs/Milestone 2/milestone2_demo_script.md` rewritten with Global Setup, Login Failure, Happy Path, and Failure Path scenarios, each with exact steps and expected behavior (three Jay commits). ✓
- `src/generator.py` removed rather than populated (commit 5cb3b15, Emma). This matches the plan's "either populate or remove" option. ✓
- `docs/Milestone 2 - Sprint 2/refusal_demo_case.md` documents two clean refusal scenarios (vegetarian user asks for chicken stew; empty user asks for chicken taco) with validator screenshots (Abigail). ✓
- Chat window closing bug fixed in `src/templates/InventoryPage.html` (commit cf7d550, Luis), closing the UX bug the demo video exposed. ✓

**P2 — Evaluation & Metrics (all complete):**
- `edge_case_tests.md` added with four edge cases (empty pantry, all expired, single ingredient, conflicting dietary restrictions) plus feasibility rate (75%) (Taja). ✓
- `Reconcile_test_results.md` merges the original 10 MVP cases and 10 Flask cases into a single 20-case table with honest ✓/✗ marks (17 pass, 3 fail), 85% feasibility pass rate, 1.95 avg regeneration attempts. Contradicts the earlier "all passing" MVP table and is the honest reconciliation the plan asked for (Abigail). ✓
- Missing metrics reported: feasibility pass rate 85%, avg regen 1.95 (Reconcile doc). Notification/expiry UX enhancements landed via commit 46ab936 (Taja). ✓

**P3 — UI Polish & Features (2 of 4):**
- Inventory display cleaned up: wider table, smaller buttons, spaced buttons (commits 54a3600, 3a56094, 539cb4c, Luis). ✓
- Notification/expiry prominence enhancements (commit 46ab936, Taja). ✓ (counts as partial credit for the "expiry notification UI" item.)
- Waste reduction dashboard: Emma added a score breakdown + dashboard logic (commits 2d96c9e, 8ac5f48), which is adjacent to the waste score work but not a full waste reduction dashboard with formula results. Partial. 
- Full team demo rehearsal: no evidence in commits or docs. Not done.

### 2. Code Quality (18/20)

- `src/expiry.py::sort_inventory` signature and SQL both updated, callers all pass `player_id` consistently. Clean fix.
- `src/unit_conversion.py` gained eight new conversions. The `normalize_quantity` and `convert_recipe_unit` functions are now duplicated in coverage (two parallel tables) — worth consolidating in Sprint 3 but not blocking.
- Dead `OPENROUTER_API_KEY=""` line in `app.py` removed cleanly.
- New allergy/diet-check code added (commit 3e1926f, Luis) including re-adding food-allergy fields on registration and profile.
- New users seeded: `demo`, `demo2`, `empty`, `expired`, `vegetarian` (commit a3e6837) which directly supports the refusal demo scenarios.
- Minor concern: several "Add files via upload" commits from GitHub web UI make it harder to review individual diffs. Not a correctness issue.

### 3. Documentation (14/15)

- `docs/Milestone 2 - Sprint 2/` folder created and populated: `edge_case_tests.md`, `Reconcile_test_results.md`, `refusal_demo_case.md`, `README.md`, plus image folders `EdgeCaseImages/` and `reconsileImages/`.
- Demo script rewrite lands in `docs/Milestone 2/milestone2_demo_script.md`.
- Docs folder reorganization: Milestone 1 and Milestone 2 content properly moved into subfolders (Luis, Taja).
- **Minor issue:** `docs/Sprint 2.md` Definition of Done still has `sort_inventory()` filter and chat window unchecked even though both shipped. Checklist drift.

### 4. Testing / Evaluation (13/15)

- 20-case reconciled evaluation table with screenshots: 17 pass, 3 fail (85%). Honest numbers replace the earlier all-green MVP table.
- 4 edge-case tests added with screenshots: 3 pass, 1 fail (single-ingredient case hallucinated butter/oil).
- Unit conversion coverage expanded, but: the docs do not show a re-run of the original 6/20 failing unit-conversion test cases to prove they now pass. Code evidence strongly suggests the fix works, but the evaluation report was not re-run to confirm "14/20 → 17+/20" as the plan's Definition of Done promised.
- No unit tests for the new conversion factors.

### 5. Team Contribution (10/10)

Every team member has code or doc commits this sprint. Emma (nerevar) in particular went from 10 commits at Milestone 2 to shipping the entire unit conversion fix plus dashboard score integration, which was the biggest individual flag from Milestone 2. Luis still leads by volume but the distribution is much healthier.

**Commit counts (April 8–14, instructor commits excluded):**

| Team Member | Sprint 2 Commits | Notes |
|---|---|---|
| Luis M (OrangeXR) | 34 | P0 fixes, UI table redesign, allergy/diet checks, seeded demo users, folder reorg |
| Taja Hicks (AlexandriaTH) | 19 | Edge case tests + images, notification enhancements, folder reorg |
| Abigail Rodriguez Vazquez | 15 | Reconciled test results, refusal demo doc, loading indicator JS/CSS |
| nerevar (Emma) | 10 | All seven new unit conversions, dashboard score breakdown |
| Jaylynn Vega | 4 | Demo script rewrite (3 commits), inventory column display |

Per the individual-grades policy, everyone receives the venture-level grade. No red flags surfaced this sprint — Emma cleared the Milestone 2 concern decisively. Jay's commit count is still the lowest; the Sprint 3 plan keeps a substantive task assigned to her.

---

## Definition of Done Scorecard

| Item | Status |
|---|---|
| `.env.example` exists | Done (`src/.env.example`) |
| Unit conversion passes 17/20 | Code complete, evaluation not re-run against the original 20 cases |
| `sort_inventory()` filters by player_id | Done (commit 2c809bd) |
| Demo script has clear, consistent scenarios | Done |
| Missing metrics documented | Done (Reconcile doc, edge case doc) |
| Chat window stays open after generation | Done (commit cf7d550) |
| Each team member has commits | Done (all 5 members committed) |

The Sprint 2 plan's DoD checklist is two boxes out of date. Not a grading deduction on its own, but worth cleaning up.

---

## What Is Missing / Carried to Sprint 3

1. **Re-run the 20-case evaluation** against the new unit conversion factors and publish the before/after in the Sprint 3 docs (expected: 17+/20).
2. **Waste reduction dashboard** — formula results visible on the dashboard, not just a score number. Emma started the plumbing; finish the UI.
3. **Full team demo rehearsal** — not done. Needs at least one dry run before April 29.
4. **Edge case 03 (single ingredient)** — model hallucinated butter/oil. Fix is either prompt engineering or validator tightening.
5. **Consolidate `normalize_quantity` and `convert_recipe_unit`** — both cover the same units now, should be one source of truth.
6. **Loading indicator for validator wait** — the Milestone 2 video flagged awkward wait times; Abigail started `showLoading` work, wire it into the chat submit flow.
7. **Update `Sprint 2.md` DoD checklist** to match reality.

---

## Per-Task Completion Summary

| Priority | Task | Owner | Status |
|---|---|---|---|
| P0 | Create `.env.example` | Luis | Done |
| P0 | Fix unit conversion (6 failing cases) | Emma | Code done, re-evaluation pending |
| P0 | Fix `sort_inventory` player_id | Luis | Done |
| P0 | Remove dead API key line | Luis | Done |
| P1 | Rewrite demo script | Jay | Done |
| P1 | Populate or remove `generator.py` | Emma | Done (removed) |
| P1 | Add refusal demo case | Abigail | Done |
| P1 | Fix chat window closing | Luis | Done |
| P2 | Report missing metrics | Taja | Done |
| P2 | Reconcile test results | Abigail | Done |
| P2 | Add edge case tests | Taja | Done |
| P3 | Improve inventory display | Jay/Luis | Done |
| P3 | Expiry notification UI | Taja | Partial (notification enhancements landed) |
| P3 | Waste reduction dashboard | Emma | Partial (score plumbing landed, UI not finished) |
| P3 | Demo rehearsal | All | Not done |
