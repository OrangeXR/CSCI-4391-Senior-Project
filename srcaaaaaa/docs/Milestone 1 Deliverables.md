# Milestone 1 Deliverables  
## Team: Binny & Bloom
### Focus: Constraint-Satisfying “Cook What You Have” Recipe Generator (No New Ingredients by Default)

---

## Context (What you already proved in Spike)

From your spike demo, the core concept is working:

- A pantry database with ingredients + quantity + expiration date  
- An LLM (Trinity via OpenRouter) generates recipes using *only* what is available  

Your README positions the app around **minimizing waste while maximizing utility**, including **Pantry Inventory Control, Meal Planning, Donation Guide, Composting Advice, and AI integration**.  

Milestone 1 must elevate this from “LLM writes a generic recipe” to an **engineered, verifiable constraint system** where quantities/expiry actually matter.

---

# Milestone 1 Objective

By Milestone 1, your team must demonstrate:

- Pantry inventory as structured data (units, quantities, expiry)
- A **constraint layer** that enforces “use only what’s available” (and how much)
- A recipe generation approach that is not purely “call LLM and hope”
- Automated validation that the produced recipe is feasible under constraints
- Measurable evaluation (not just screenshots)
- Clean GitHub structure + technical walkthrough video (no UI required)

---

# 1. Updated PRD-Lite (1–2 pages)

Update PRD to clearly define the product as:

> A pantry-aware recipe assistant that generates feasible recipes that use only available ingredients (amount-aware), prioritizing near-expiration items to reduce waste.

## Required additions to the PRD

### A. Must-have Value Proposition (Make it non-generic)
Pick 1–2 of the following and commit to it (define measurable success metrics):

- ```**Expiry-first planning**: recipes prioritize ingredients expiring within N days```  (picked)
- ```**Waste reduction score**: quantify “how much inventory was consumed” ```            (picked)
- **Feasibility guarantee**: recipes are always possible given inventory + units  
- **Time/skill constraints**: “15-min recipe”, “beginner-friendly” options

### B. Non-negotiable constraints (explicit)
- Default mode: **no new ingredients added**
- Recipe must specify **exact amounts** per ingredient
- Quantities must not exceed what is available (with unit conversion)
- If constraints cannot be met, system must refuse or propose a smaller portion size

### C. Acceptance Criteria (testable)
Examples (you can revise, but must be testable):
- 100% of outputs pass the feasibility validator
- 0 invented ingredients in default mode
- ```≥ 70% of test cases use at least one “expiring soon” item (if expiry-first is chosen)``` (picked)

---

# 2. Pantry Schema + Unit Normalization (Engineering Component)
(Jay) (Luis)
Create or finalize a pantry schema that supports validation.

## Requirements
- Canonical ingredient names (e.g., “tomato” not “tomatoes”)
- Units normalized (grams/ml/cups, etc.)
- Quantity stored as numeric + unit
- Expiration date stored as ISO date

Create:
- /docs/pantry_schema.md (fields, examples, units policy) 
- /src/unit_conversion.py (or equivalent) 

---

# 3. Constraint & Feasibility Validator (Required)
(Emma) (Taja) (Abby)
This is the “not just an API call” part.

Implement a validator that checks the generated recipe against the pantry state.

## Must validate
- Every ingredient in recipe exists in pantry (default mode)
- Amount required ≤ amount available (with unit conversion)
- Portion scaling supported (optional but encouraged)
- Missing/insufficient ingredient triggers refusal or “reduce servings” suggestion

Create:
- /src/validator.py  
- /docs/validator_rules.md (bullet list of rules)

If validation fails, the system must:
- Regenerate with stricter constraints, OR
- Refuse with a clear reason

Manual checking does not count.

---

# 4. Recipe Generation Approach (Must be more than “generic prompt”)
(everybody)
You must implement at least one structured approach that makes quantities meaningful.

Choose one (or combine):

### Option A: Two-stage plan (recommended) (picked)
1) ```Deterministic planner selects a feasible ingredient subset + target dish type```  
2) ```LLM writes the recipe using only the selected subset + exact amounts```  

### Option B: Retrieval-grounded recipes
- Build a small recipe KB (JSON is fine)
- Retrieve a recipe template that matches inventory overlap
- LLM adapts template to available quantities

### Option C: Constraint-guided decoding (lightweight)
- Use structured JSON output format from LLM
- Reject outputs failing schema/constraints and regenerate

Create:
- /docs/generation_strategy.md (which option you used and why)

---

# 5. Evaluation Starter Kit (Minimum 20 Test Cases)
(Taja)(Abby)
Create:
- /docs/evaluation_test_cases.md

Include 20 scenarios with:
- Pantry snapshot (ingredients + quantities + expiry)
- Expected feasibility result (Pass/Fail)
- Generated recipe output
- Validator output
- Notes (what failed and why, if fail)

## Required metrics
- Feasibility pass rate
- “Invented ingredient” rate (should be 0 in default mode)
- Expiry utilization rate (if you claim expiry-first)
- Average regeneration attempts (if using regenerate-on-fail)

---

# 6. Architecture Diagram (1 page)
(Abby)
Create:
- /docs/architecture.png

Must show:
Pantry DB → Planner/Retriever → LLM → Validator → Final Output (+ logging)

Label deterministic vs LLM components clearly.

---

# 7. Required Technical Walkthrough Video (No UI Required)
(everybody)
Submit a 5–8 minute technical walkthrough video showing:

- Pantry DB format and example records  
- Unit normalization / conversion  
- Generation strategy (planner or retrieval)  
- The validator running and rejecting/accepting outputs  
- One success case and one failure/refusal case

A polished UI is NOT required. Console/log demonstration is acceptable.

Include link in README or store at:
- /docs/demo_video.mp4 (or link to external host)

---

# 8. GitHub Repository Requirements

Your repository must include:

- /docs/PRD.md  
- /docs/pantry_schema.md  
- /docs/validator_rules.md  
- /docs/generation_strategy.md  
- /docs/evaluation_test_cases.md  
- /docs/architecture.png  
- /src/generator.py  
- /src/validator.py  
- /src/unit_conversion.py (or equivalent)

Additionally:
(Luis)
- Updated README with setup + run instructions
- requirements.txt
- .env.example (no keys committed)
- At least one meaningful commit per team member
- Issue board / sprint tasks with owners

---

# Required Live Demo for Milestone 1

You must demonstrate:

1) A pantry state with quantities + expiry  
2) Recipe generation using only available ingredients  
3) Output includes exact amounts  
4) Validator output shown (Pass)  
5) A failure case: insufficient ingredient → refusal or scaled-down serving plan  

---

# Not Acceptable for Milestone 1

- Generic recipes that ignore inventory quantities  
- Adding new ingredients without labeling them as optional (default must be “no new ingredients”)  
- No validator / no unit normalization  
- Manual feasibility checking only  
- No evaluation dataset

---

# Milestone 1 Standard

Your project must evolve from:

“We store pantry items and call an LLM for a recipe.”

To:

“We engineered a constraint-satisfying recipe generator with validation, measurable feasibility, and waste-reduction logic.”
