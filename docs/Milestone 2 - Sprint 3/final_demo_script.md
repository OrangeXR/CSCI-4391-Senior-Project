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
### Global Setup (~ 1 minute)
**Before demo starts:**
- Backend server is running
- database is seeded with demo users
- AI and validator services are active
- inventory system is connected
- .env file has API key present


*Browser is open on the login screen*

---



# Scenario 1: Login Failure (1 minute)

Purpose: Demonstrate form validation and rejection of incomplete credentials.
| Step | Action | What to say |
|------|--------|-------------|
| 1 | Leave username + password blank | “We’ll test login validation with missing credentials.” |
| 2 | Click Login | "By attempting to login with no credentials.” |
| 3 | Observe error message | “The system correctly blocks login when fields are empty.” |

**Expected Output:**
- Login rejected  
- Error message displayed "Fill out field"  
- User remains on login screen  
- No inventory or AI access 

**Requirements Verified:**
- System must *NOT* log the user in
- System must *NOT* load inventory or expose AI features.

---

# Scenario 2: Login Success (1 minute)

| Step | Action | What to say |
|------|--------|-------------|
| 1 | Enter demo credentials | “Now we login with valid credentials.” |
| 2 | Click Login | “Authentication should succeed.” |
| 3 | Home page loads | “User is redirected to homepage” |

**Expected Output:**
- User logged in  
- Inventory + AI accessible  

**Expected Output:**
- User is redirected to home page
- User can access inventory, AI and other features



# Scenario 3A: Happy Path (~ 4 minutes)


| steps | actions                                 | what to say                       |
|-------|-----------------------------------------|-----------------------------------|
| 1     |   Navigate to the **Check Inventory page** | "Lets see what we have in our inventory" (look for penne pasta) |
| 2 | Click on **Chat with Binny** if not already open | "Now we will ask for a recipe from binny with penne pasta  " |
| 3  | Type: I want a recipe with penne pasta | |
| 4| Click **Submit** | |
| 5| Observe recipe output | "The validator confirmed penne pasta exist, the quantities are realistic, no ingredients are expired and validator passed (via terminal). The recipe that came back uses what's actually in our pantry" | 


***NOTE: May require regeneration and may have to delete garlic or other expired item it keeps generating with***
  
**Expected Output**
- AI generates a recipe using *available pantry ingredients* in valid JSON format
- Validator checks: ingredients existence, realistic proportions, no expired items 
- Validator passes- recipe is displayed


---

# Scenario 3B: Failure Path (~ 5 minutes)

Starting state:

- User is logged in as expired or demo, inventory *MUST* contain expired chicken breast 

| Step | Action | What to say |
|------|--------|-------------|
|  1 | Navigate to **Check Inventory** |“We will now test for expired ingredient detection.”|
| 2| Ensure expired chicken exists | “We will use chicken breast for testing" |
| 3 | Click on **Chat with Binny**  if not opened ||
| 4|  Enter prompt: I would like a recipe with chicken breast | “This prompt should trigger expiration validation.” |
| 5 | Submit |  |
| 6 | Observe response | “Validator correctly rejects expired ingredient.” |

**Expected Output:**
- Error message: Ingredient chicken breast is expired and cannot be used.
- Recipe rejected  

**Requirements Verified**
- System must *NOT* accept expired ingredients
- User is clearly notified with the hard fail mesage

---

# Gamification options 

---

## Scenario 4A: Compost (~ 3 minutes)
Starting state:
- User is logged in as demo

***NOTE: Demonstrating AI suggestions for compost***


| Step | Action | What to say |
|------|--------|-------------|
| 1 | Select compostable item | “Let's test the compost functionality.” |
| 2 | Click on **Chat with Binny** if not open|| 
| 3 | Ask compost prompt: How can i compost _(item)_ |  |
| 4 | Submit | “AI will return compost suggestion” |
| 5 | Click compost button | “Manually composting item.” |
| 6 | Observe update | “Item is now composted and score updates.” |


**Expected Output**
- AI will generate a suggested how to compost item, like the following: 

  "Avocado — home compost
      Remove hard pit before composting, chop skin into small pieces."

  "Carrot — home compost
      Chop into small pieces, both flesh and peel break down quickly"

- Score notification should display 
- Status of carrot should update to composted 

---

## Scenario 4B: Donate (~1 minute)
Starting state:
- User is logged in as demo


| steps | actions                                 | what to say                       |
|-------|-----------------------------------------|-----------------------------------|
| 1| Navigate to any item in the pantry that is not expired and active  | "Lets test donation functionality" | 
|2 | Click **Donate** | "We will donate this item"|
| 3 | Observe status of item update | Read message display|


**Expected Output**

- Score notification displayed and score reduced
- Status of item updated to donated

---

## Scenario: 4C: Use (~2 minutes)

| steps | actions                                 | what to say                       |
|-------|-----------------------------------------|-----------------------------------|
| 1| Navigate to any item in the pantry that is not expired and active  | "Lets look at the use fuctionality"| 
|2 | Click **Use** | |
| 3 | Observe message update and deleted from inventory | Read message and confirm item is removed |

**Expected Output:**
- Score notification display and score reduction
- Inventory updated 

----


## Scenario 5: Empty (~ 3 minutes)
Starting state:
- user is logged in as empty
- pantry contains no ingredients

| Steps | Actions                                 | What to say                       |
|-------|-----------------------------------------|-----------------------------------|
| 1| Login to empty account using credentials | "We will now test an empty inventory" | 
| 2 | Navigate to **Check Inventory page** | "As you can see there is no items in the inventory"|
|3 |Click **Chat with Binny** if not already open| "Lets ask for a recipe "|
| 3| Enter prompt : I would like a recipe please ||
| 4| Click **Submit** | | 
| 5| Click show steps and Read message out loud | "No recipe available, Sorry, I can't create a recipe because there are no food items in your inventory. Please add ingredients to your inventory first." | 

 **Expected Output**
- Validator detects no items in inventory
- Hard fail AI will generate output in chatbox of "No recipe available, Sorry, I can't create a recipe because there are no food items in your inventory. Please add ingredients to your inventory first." 

---

## Scenario 6: Dietary user (~ 3 minutes)
Starting state: 
- User is logged in as vegeterian 
- pantry contains valid items in inventory 



| Steps | Actions                                 | What to say                       |
|-------|-----------------------------------------|-----------------------------------|
| 1| Login to vegetarian account using credentials | "We will now test the vegetarian dietary needs " | 
| 2 | Navigate to **Check Inventory page** | "inventory contains same items as demo account"|
|3 |Click **Chat with Binny** if not already open| "Lets ask for a recipe using with ground beef "|
| 3| Enter prompt : I would like a recipe with ground beef ||
| 4| Click **Submit** | | 
| 5| Read message out loud | "HEADS UP: I tried to make a recipe with your current inventory. 'ground beef' violates vegetarian requirement." | 

 **Expected Output**
- Validator detects dietary needs 
- Validator detects ground beef as violation to dietary needs
- Hard fail AI will generate output in chatbox of "I tried to make a recipe with your current inventory. 'ground beef' violates vegetarian requirement."



  


