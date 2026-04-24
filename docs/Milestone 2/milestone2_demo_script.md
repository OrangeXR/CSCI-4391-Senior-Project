# Demo Script

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

---
### Global Setup
Before demo starts:
- Backend server is running
- database is seeded with demo users
- AI and validator services are active
- inventory system is connected
- .env file has API key present

---
### Scenario: Login Failure 
Starting state: 
- The application opened on login screen, no user is authenticated.

Steps:
1. Leave username and login blank
2. click **Login**

   **Expected Output**
   - Login is rejected and error message is displayed of "invalid username or password".
   - User remains on login screen
  
     **Failure Case Behavior**
     - System must ***NOT***: Log the user in, load inventory or access AI features.

---

### Scenario: Happy Path

Starting state:
- user is logged in as demo
- panty contains valid ingredients

  Pantry state:
    - Chicken breast (fresh)
    - rice
    - garlic
    - salt
    - pepper
    - onion
 
  Steps:
  1. Login using valid demo credentials
  2. open AI recipe generator
  3. enter prompt:
       I want a recipe with chicken breast
  4. Submit prompt

     **Expected Output**
     - AI generates a recipe using *available pantry ingredients*
     - validator checks: ingredient existence, realistic proportions, no expired items
     - validator passes

     **Expected Behavior**
     - Recipe is displayed and ingredients align with pantry
    
---

### Scenario: Failure Path 

Starting state:
- User is logged in as demo

Pantry status: contains expiry item 

EX: 
  - Chicken breast (expired)
  - rice
  - garlic

Steps: 
1. ensure pantry contains expired chicken:
2. enter prompt:
   I want a recipe with chicken breast
3. Submit prompt

   **Expected Output**
   - Validator detects chicken breast is expired
   - System rejects the recipe
  
    **Expected Validator Behavior**
   - Hard fail: "Ingredient chicken breast is expired and cannot be used."

  **Failure Case Requirements**
  - System must ***NOT accept expired ingredients***
  - Must clearly notify the user.

---


