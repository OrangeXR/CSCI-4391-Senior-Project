# Binny & Bloom
## CSCI 4391 - Senior Project - Spring 2026
## Abigail Rodriguez Vazquez, Emma Whitehead, Jay Vega, Luis Morales, Taja Hicks

## PRD: Product Requirements Document

### 1  Problem + Target Users
Write 2–4 sentences covering:
#### What problem exists today?
#### Who experiences it (target users)?
#### Why it matters (social good impact / urgency)?
About 40% of all food produced globally by weight is wasted between farm and fork. That 40% could feed every food-insecure person three full meals a day, everyday for a year with leftovers. If the current trends persist, this waste will double by 2050 (World Resources Institute, 2019). The target users are anyone interested in learning how to properly dispose of or recycle food waste because the goal of this product is to help improve society by reducing waste one at a time.
### 2  Goal / Success Metrics 
1–3 measurable outcomes, such as: accuracy / quality improvement, time saved per user task, reduction in errors / friction, user satisfaction (survey score), adoption/usage in a small pilot
- Reduction in Waste Score over time
- Relevance of LLM-generated recipes
- Percentage of expiring items utilized 
### 3  MVP User Stories
Include 5–8 user stories. Required format: As a [user], I want [action], so that [benefit].
- As a user, I want to add food items with expiration dates, so that I can keep track of what I have and when it expires.
- As a user, I want Binny and Bloom to flag items that are expiring soon, so I can use them before they go to waste.
- As a user, I want to be able to view my food inventory, so I can see available ingredients and quantities.
- As a user, I want to receive recipe suggestions based on expiring items, so that I can decide what to cook.
- As a user, I want to receive alerts about expiration, so that I’m reminded in a clear and understandable way.
- As a user, I want to see nearby donation options for excess food, so that I can avoid wasting food items.
- As a user, I want to see suggestions for repurposing food waste, so I can help with the environment.  

### 4  MVP Scope vs. non-goals
Clarify what you will build for the MVP, and what you will not build.
You must include:
Must-have features (3–6)
- User Login/Logout. Set encryptions/hashed for user data security/protection  
- Binny and Bloom must have an add/delete/edit for food inventory 
- Notifications for expiring food inventory.
- Ai generated composting Guidance 
- Ai generated  meal suggestions to prevent waste 
- Aid generated for sorting items for the donations:​
- Nice-to-have features (optional)
- Waste reduction score dashboard
- Barcode scanning 
- a virtual farm.
Explicit non-goals (what you will not build)
- Spoiling detection: whether the food has actually spoiled, if stored properly, if it has mold or contamination. 
- Medical history, allergies, calorie tracking and health conditions.
- No real-time continuous monitoring
- Not a replacement for human decision making

### 5  Acceptance Criteria
Define clear, testable bullets describing what “done” means.
What the user can do end-to-end; What the system must output; What counts as pass/fail
When our product is completed, it must:
- Allow the user to login with their credentials successfully
- Correctly handle situations when the user inputs data incorrectly
- Allow the user to add/delete a food item
- Save expiration date correctly
- Expiry Suggestion Notifications trigger correctly for the right food item
- Track food waste & food saved
- AI provides safe recommendations
### 6  Assumptions + Constraints
List assumptions and constraints such as:
- Data access (what data you do/don’t have)
- For user data we would have email address, password (hashed), score and name. For food inventory data we will have food name, category, quantity and expiration dates.For system logic we would have the expiring soon status, days remaining until expiration, donation eligibility (based on expiration date/item category/food bank policies). AI generated suggestions of recipes, waste reduction tips and composting instructions. External API data would be food bank names, location data and donation policies. 
- We will NOT have whether the food has actually spoiled, if stored properly, if it has mold or contamination. We will NOT have medical history, allergies, calorie tracking and health conditions.
- Time constraints (what can be done by Milestone 2)
- Basic GUI & Database
- Ethics/privacy limits (safety boundaries, consent)
- We will assume that users will provide accurate food data, consent to their data being collected, and understand how their data is being used. The users will have to be a certain legal age to consent to this. Some constraints include allowing users to delete their data if they wish, obtaining consent before collecting data, and collecting only the data we need. We must also ensure the passwords are encrypted.
- Platform constraints (APIs, cost limits, deployment limits)
- Some platform constraints that we may have include push/email notifications, privacy & data constraints such as data deletion, secure storage, consent/age restrictions, updates for near-expiry items, AI model costs, and legal liability (food safety).
