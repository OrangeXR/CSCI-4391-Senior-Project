# Milestone 2 Deliverables
## Team: Binny & Bloom
### Focus: MVP of Pantry-Aware, Constraint-Validated Recipe Generation

Milestone 2 is due **one week after the Sprint 1 review meeting**. This is the **MVP milestone**.

At Milestone 1, you demonstrated important pieces of the system: pantry schema, unit normalization, validator logic, evaluation cases, and an early UI.  
At Milestone 2, the expectation is different:

> The system must work as **one coherent MVP flow**, not as separate parts that only work in isolation.

---

# Milestone 2 Objective

By Milestone 2, your team must demonstrate a usable MVP in which a user can:

1. log in
2. view pantry inventory with quantities and expiry
3. request a recipe
4. receive either:
   - a **validated feasible recipe**, or
   - a **clear refusal / validation failure reason**
5. see that the system is prioritizing near-expiration inventory when possible
6. Minimum functioning GUI

This milestone is about **integration, reliability, and demo readiness**.

---

# 1. MVP Definition

Your MVP must satisfy all of the following:

## Required MVP behavior

- Pantry inventory is stored as structured data with:
  - ingredient name
  - quantity
  - unit
  - measurement type
  - expiration date
- The recipe generation flow uses pantry context only by default
- The system checks recipe feasibility before presenting final output
- The final user-facing result clearly distinguishes:
  - successful validated recipe
  - failed validation / refusal / scaled-down retry
- The MVP must support at least:
  - one successful case
  - one failure or refusal case

## Non-negotiable MVP constraints

- Default mode remains **no new ingredients**
- Recipes must include exact amounts
- Quantities must not exceed available inventory
- Expired ingredients must not be used
- Validation must be part of the actual demo path, not only a console-only side path

---

# 2. Required Demo Path

During Milestone 2, your live demo must show this full path:

1. User logs in
2. User opens pantry/inventory
3. Pantry data visibly includes quantity, unit, and expiry
4. User asks for a recipe
5. System generates a candidate recipe
6. Validator runs
7. UI clearly shows:
   - validated pass result and final recipe, or
   - rejection/failure reason and any retry/refusal behavior
8. Show one second scenario where the recipe is rejected or scaled down

Console-only validation is not enough by itself for the MVP. The core product path must demonstrate this end to end.

---

# 3. Deliverables to Submit

Your repository must include the following by Milestone 2:

## Required repository artifacts

- `/docs/Milestone 2 Demo Script.md`
- `/docs/MVP Test Cases.md`
- `/docs/MVP Known Issues.md`
- `/docs/MVP Retrospective.md`
- `/docs/demo_video.mp4` or a markdown file linking to the video
- updated `/docs/PRD.md` if MVP scope changed
- updated `/README.md`
- `.env.example`

## Required source expectations

- web app route that runs generation and validation in the same user flow
- validator integrated into the user-facing path
- improved ingredient matching logic
- resolved or clearly documented handling for failing test scenarios

---

# 4. Required Written Documents

## A. `/docs/Milestone 2 Demo Script.md`

Provide the exact sequence your team will show in class:

- starting state
- login credentials used for demo
- pantry state used in happy path
- prompt used in happy path
- expected validator pass behavior
- pantry state used in failure path
- prompt used in failure path
- expected validator fail/refusal behavior

This should read like a checklist for a reliable live demo.

## B. `/docs/MVP Test Cases.md`

Provide at least **10 focused MVP test cases** that directly exercise the integrated product path.

For each case include:

- test name
- pantry state
- user prompt
- expected result
- actual result
- pass/fail
- notes

These should be smaller and more MVP-focused than the Milestone 1 exploratory evaluation set.

## C. `/docs/MVP Known Issues.md`

List the remaining issues honestly.

Required categories:

- ingredient matching edge cases
- unit conversion edge cases
- UI limitations
- data quality assumptions
- anything the team would fix next with one more sprint

## D. `/docs/MVP Retrospective.md`

In 1 to 2 pages, explain:

- what changed from Milestone 1 to Milestone 2
- what was cut from scope
- what is now truly MVP-ready
- what still needs work after MVP

---

# 5. Required Metrics

Report updated metrics from your current integrated system:

- feasibility pass rate
- invented ingredient rate
- expiry utilization rate
- validator rejection rate
- average regeneration attempts
- number of known failing edge cases still unresolved

If a metric got worse, explain why.

---

# 6. MVP Expectations for This Team

Based on your current Sprint 1 status, I expect the following to be complete next week:

## Must be fixed before Milestone 2

- validator integrated into the Flask/web path
- UI explicitly displays validation outcome
- improved ingredient matching beyond simple substring-only confidence
- `.env.example` added
- `README.md` updated to reflect the actual MVP flow

## Strongly recommended

- move generation logic into a clearly named module or document why it remains elsewhere
- re-run and improve the Milestone 1 failing cases
- reduce cases where units mismatch or ingredients are invented

## Scope to de-emphasize if needed

If time is tight, prioritize the validated recipe MVP over extra features such as:

- scoreboard polish
- broader lifestyle features
- donation/compost expansion
- cosmetic UI refinement

---

# 7. Required Live Demo Video for Milestone 2

You must demonstrate:

1. a user logging in
2. a pantry with quantities and expiration dates
3. a recipe request from the UI
4. a validator-backed successful output
5. a validator-backed failure/refusal case
6. evidence that near-expiration items are preferred when feasible

---

# 8. Not Acceptable for Milestone 2

- Showing only raw LLM output without validation status
- Keeping validation only in a separate console demo path
- Claiming ingredient matching is fixed without demonstrating edge cases
- Adding new features while the core validated MVP path is still unreliable
- Presenting a polished UI without a dependable pass/fail product flow

---

# Final Advice

Milestone 2 is not about proving that you have many ideas. It is about proving that the core idea works reliably enough to count as an MVP.

For this week, build one narrow path that is defensible, repeatable, and easy to demo.
