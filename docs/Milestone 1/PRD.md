Binny & Bloom
CSCI 4391 - Senior Project - Spring 2026
Abigail Rodriguez Vazquez, Emma Whitehead, Jay Vega, Luis Morales, Taja Hicks
PRD: Product Requirements Document
1 Problem + Target Users
Write 2–4 sentences covering:

What problem exists today?

About 40% of all food produced globally by weight is wasted between farm and fork. That 40% could feed every food-insecure person three full meals a day, everyday for a year with leftovers. If the current trends persist, this waste will double by 2050 (World Resources Institute, 2019).
Who experiences it (target users)?

The target users are anyone who wants to reduce food waste but struggle to track expiration dates and plan meals efficiently.
Why it matters (social good impact / urgency)?

Binny & Bloom is a pantry-aware recipe assistant that generates feasible recipes that use only available ingredients (amount-aware) that prioritizes near-expiration items to reduce waste.
2 Goal / Success Metrics
1–3 measurable outcomes, such as: accuracy / quality improvement, time saved per user task, reduction in errors / friction, user satisfaction (survey score), adoption/usage in a small pilot

Reduction in Waste Score over time, User improve waste score by at least 20% after 3 weeks.
Relevance of LLM-generated recipes
Percentage of expiring items utilized
Expiry-First Planning
Greater than or equal to 70% of generated recipes include at least one near-expiration time when such items exist.
Greater than or equal to 25% in expired unused inventory during testing.
Waste Reduction score
Waste reduction score = 0.6 * expiration usage + 0.4 * inventory usage (draft)
Expiration usage = expiring items used in recipe / total expiring items in inventory
Inventory usage = ingredients used in recipes/ total ingredients in inventory

Example Calculations
Example of how well the recipes uses ingredients close to expiring (expiration usage):

Expiring Items	Used
milk	Yes
spinach	Yes
Yogurt	No
2/3 = 0.67

Example of how much of the pantry is actually use (inventory usage):

Inventory item	Used
milk	Yes
spinach	Yes
rice	Yes
eggs	No
cheese	No
3/5= 0.6 inventory usage
Waste Reduction Score: 0.6(0.67) + 0.4(0.60) = 0.642 - rounded would be .064 or 64%

3 MVP User Stories
Include 5–8 user stories. Required format: As a [user], I want [action], so that [benefit].

As a user, I want to add food items with expiration dates, so that I can keep track of what I have and when it expires.
As a user, I want Binny and Bloom to flag items that are expiring soon, so I can use them before they go to waste.
As a user, I want to be able to view my food inventory, so I can see available ingredients and quantities.
As a user, I want to receive recipe suggestions based on expiring items, so that I can decide what to cook.
As a user, I want to receive alerts about expiration, so that I’m reminded in a clear and understandable way.
As a user, I want to see nearby donation options for excess food, so that I can avoid wasting food items.
As a user, I want to see suggestions for repurposing food waste, so I can help with the environment.
4 MVP Scope vs. non-goals
Clarify what you will build for the MVP, and what you will not build. You must include: Must-have features (3–6)

User Login/Logout. Set encryptions/hashed for user data security/protection
Binny and Bloom must have an add/delete/edit for food inventory
Notifications for expiring food inventory with roughly a 3-day expiry alerts.
Ai generated composting Guidance
Ai generated meal suggestions to prevent waste(amount-aware)
Aid generated for sorting items for the donations:​
Nice-to-have features (optional)
Waste reduction score dashboard
Barcode scanning Explicit non-goals (what you will not build)
Medical history, and health conditions.
No real-time continuous monitoring
Not a replacement for human decision making
5 Acceptance Criteria
Define clear, testable bullets describing what “done” means. What the user can do end-to-end; What the system must output; What counts as pass/fail When our product is completed, it must:

Allow the user to login with their credentials successfully
Correctly handle situations when the user inputs data incorrectly
Allow the user to add/delete a food item
Save expiration date correctly
Expiry Suggestion Notifications trigger correctly for the right food item
Track food waste & food saved
AI provides safe recommendations
Default Mode: No new ingredients
Recipes must ONLY use ingredients currently in inventory
Exact Quantities Required:
Every ingredient must have exact amounts (unit conversion)
Quantity Feasibility:
Quantities must not exceed available inventory
Failure Handling: If constraints cannot be satisfied
System will propose smaller portion or refuse generation with explanation.
6 Assumptions + Constraints
List assumptions and constraints such as:

Data access (what data you do/don’t have)

For user data we would have username, password (hashed), score and name. For food inventory data we will have food name, category, quantity, grams/mL of products, purchase date and expiration dates.For system logic we would have the expiring soon status, days remaining until expiration, donation(based on expiration date/item category/food bank policies), decompose and perishable eligibility. AI generated suggestions of recipes, waste reduction tips and composting instructions. We will also have food allergies IF user inputs that data otherwise, it is not accessed or known.
We will NOT have whether the food has actually spoiled, if stored properly, if it has mold or contamination. We will NOT have calorie tracking and medical history.


Time constraints (what can be done by Milestone 2)
Basic GUI & Database

Ethics/privacy limits (safety boundaries, consent)

We will assume that users will provide accurate food data, consent to their data being collected, and understand how their data is being used. The users will have to be a certain legal age to consent to this. Some constraints include allowing users to delete their data if they wish, obtaining consent before collecting data, and collecting only the data we need. We must also ensure the passwords are encrypted.

Platform constraints (APIs, cost limits, deployment limits)

Some platform constraints that we may have include push/email notifications, privacy & data constraints such as data deletion, secure storage, consent/age restrictions, updates for near-expiry items, AI model costs, and legal liability (food safety).
