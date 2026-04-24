# Sprint 3 Plan — Venture 4: Krusty Compost Crew (Binny & Bloom)

**Sprint Duration:** April 15 – April 21, 2026
**Sprint Goal:** Re-run the evaluation suite to prove the unit conversion fix, finish the waste reduction dashboard, polish the live-demo experience (loading indicator, rehearsal), and close the remaining edge cases. This sprint exists to leave Sprint 4 free for final integration and presentation prep.
**Final Demo:** April 29, 2026

---

## Context

Sprint 2 closed the critical Milestone 2 gaps: `.env.example`, `sort_inventory(player_id)`, unit conversion factors, dead API key line, chat window fix, demo script rewrite, refusal demo doc, 20-case reconciled evaluation, and 4 edge case tests. Sprint 2 grade: 93/100. Three things remain before the final demo is presentation-ready: (1) the unit conversion work needs a new evaluation pass to confirm the numbers, (2) the waste reduction dashboard is not visible yet, and (3) the team has not done a full dry run. Sprint 3 also cleans up small paper cuts (loading indicator during validator wait, the single-ingredient hallucination edge case, and a duplicate unit conversion table in code).

---

## Sprint 3 Tasks

### P0 — Must Finish Before the Final Demo (Days 1–3)

| Task | Owner | Description |
|---|---|---|
| Re-run 20-case evaluation | Taja | Re-execute the original 20 evaluation test cases (from Milestone 2) with the new conversion factors in `src/unit_conversion.py`. Publish a before/after table in `docs/Sprint 3/evaluation_rerun.md`. Target: 17+/20 passing. |
| Waste reduction dashboard UI | Emma | Display waste reduction score + formula breakdown on the dashboard (not just a single number). Use the score breakdown work from commits 2d96c9e / 8ac5f48 as the backend; finish the template + CSS. |
| Full team demo rehearsal (dry run 1) | All | End-to-end walkthrough of the Apr 29 demo script against live `demo`, `empty`, `expired`, and `vegetarian` accounts. Record timing. Capture bugs in `docs/Sprint 3/rehearsal_notes.md`. |
| Wire loading indicator into chat | Abigail | Finish the `showLoading` function started in commits c1f7a8b / 1f899cd / 3fbcea3 and trigger it on recipe-generation submit in `InventoryPage.html`. Fixes the "awkward wait" feedback from the Milestone 2 video. |

### P1 — Demo Polish (Days 3–5)

| Task | Owner | Description |
|---|---|---|
| Fix single-ingredient hallucination | Emma | Edge case 03 in `edge_case_tests.md`: model invents butter/oil. Either tighten the system prompt in `openrouterllm.py` or add a "invented ingredient" check in `validator.py`. Re-run the 4 edge cases and update the doc. |
| Consolidate unit conversion tables | Emma | `normalize_quantity` and `convert_recipe_unit` in `src/unit_conversion.py` both cover the same units. Refactor into one source of truth with a single lookup dict. Add a small pytest (or unittest) file with at least one assertion per unit. |
| Tighten demo script timings | Jay | Add expected timings and a "what to say" column to `milestone2_demo_script.md`. Rename the file to `final_demo_script.md` and move to `docs/Sprint 3/`. |
| Update `Sprint 2.md` DoD | Luis | Check the two boxes that are now true (`sort_inventory` filter, chat window stays open). Small cleanup. |

### P2 — UX & Visibility (Days 4–6)

| Task | Owner | Description |
|---|---|---|
| Expiry notification prominence | Taja | Continue the Sprint 2 notification enhancements. Make 3-day expiry alerts prominent on the dashboard (banner or colored card), not just list items. |
| Use / donate / compost on camera | Jay | Milestone 2 video never showed the gamification actions. Build a short demo segment (in the script) that triggers use, donate, compost, and delete and shows the score update. |
| Gamification score visibility | Emma | Once the dashboard formula is live, make sure the score from use/donate/compost actions updates in real time on the dashboard for the demo. |

### P3 — Quality of Life (Days 5–7)

| Task | Owner | Description |
|---|---|---|
| Dry run 2 + video capture | All | Second team rehearsal. Capture a 5 minute unedited recording to check pacing and catch bugs. Save under `docs/Sprint 3/rehearsal2.md`. |
| Screenshot refresh | Abigail | Replace any `docs/images` / `docs/ImagesPt2` screenshots that no longer match the current UI (new inventory table, new notification banner). |
| README pass | Luis | Quick sweep of `README.md` to make sure installation steps work from a clean clone (including `.env.example` usage). |

---

## Definition of Done (Sprint 3)

- [ ] `docs/Sprint 3/evaluation_rerun.md` shows 17+/20 feasibility pass on the original evaluation set.
- [x] Waste reduction dashboard visible on user dashboard with formula breakdown.
- [x] Loading indicator appears when the user submits a chat prompt and disappears when the response renders.
- [ ] At least one full team demo rehearsal completed with notes.
- [ ] Single-ingredient edge case either passes or is explicitly flagged as a known limitation in the script.
- [x] `normalize_quantity` and `convert_recipe_unit` share a single source of truth.
- [ ] Final demo script has per-step timings and speaker notes.
- [x] Every team member has commits this sprint.

---

## Contribution Expectations

Sprint 2 was Emma's turnaround sprint (unit conversion + dashboard plumbing), which cleared the biggest Milestone 2 flag. Sprint 3 keeps Emma on the dashboard UI and validator-side hallucination work, keeps Jay on the demo script and gamification segment (her Sprint 2 commit count was the lowest), and gives Taja the critical re-evaluation task. Luis and Abigail continue to anchor Flask/UI work but the sprint is designed so that the P0 critical-path work is distributed across four different people, not just Luis.

---

## Remaining Sprints Overview

| Sprint | Dates | Focus |
|---|---|---|
| Sprint 2 | Apr 8–14 | Unit conversion, .env.example, demo script, bug fixes (graded 93/100) |
| Sprint 3 (this sprint) | Apr 15–21 | Re-evaluation, waste dashboard UI, loading indicator, demo rehearsals |
| Sprint 4 | Apr 22–28 | Final polish, presentation prep, final deliverables |
| **Final Demo** | **Apr 29** | **Presentation and live demo** |
| Final Deliverables Due | May 3 | All documentation and code finalized |

---

## Final Demo Day Heads-Up (April 29)

Two weeks out. Rehearse toward this format during Sprint 3 and Sprint 4.

**12 minutes per team, hard cap.** I will cut you off at 12:00 to keep all 8 teams on schedule, so rehearse to 10:30 or 11:00 to leave margin. Suggested split:

1. **About 3 min: overall design.** What the product does, the core pipeline, and the architectural decisions that matter (retrieval strategy, validator or grounding approach, refusal policy). No code walkthroughs.
2. **About 4 min: individual contributions.** Every team member speaks briefly about what they personally owned this semester. Plan what you will say, roughly 45 to 60 seconds each.
3. **About 4 min: live demo of the highlights.** Pick 2 or 3 scenarios from your existing demo script. Required: at least one refusal or failure case and at least one end-to-end grounded answer. Do not spend this time on UI polish.
4. **About 1 min: Q&A**, included in the 12 minutes.

**Running order** is Venture 1 through Venture 8 in order, so Krusty Compost presents fourth.

**Backup plan:** have a prerecorded screen capture of the working path ready in case the live demo fails. Internet or API hiccups are not an excuse on demo day.

**Slides and runbook:** not due before the presentation, but both are required artifacts in the final deliverables package due May 3. Save them under `docs/Final_Demo/` in your repo.

**Avoid:** narrating code, reading slides verbatim, skipping the refusal case, opening with missing features. Present the version you are proud of.

Rehearse the full 12 minutes end to end at least twice, at least once with a timer.
