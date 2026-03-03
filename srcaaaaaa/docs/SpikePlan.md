# Binny & Bloom
## CSCI 4391 - Senior Project - Spring 2026
## Abigail Rodriguez Vazquez, Emma Whitehead, Jay Vega, Luis Morales, Taja Hicks

## Engineering Spike Plan

### Your spike must answer:
- What is the hardest technical risk?
  - I believe the hardest technical risk will be the actual AI integration into our application.  From reading and interpreting the data contained in our database to actually using that information to create recommendations that are both useful and correct for meal prep, donations, and composting.  We have been working to provide relevant data for the AI to go through and we must figure out the best way to have it digest that data and provide valid outputs that we can trust.
- Can we make a 2–3 minute demo that proves it works?
Timebox: 3–5 days (max 1 week)
  - Yes, we can make a 2-3 minute demo that proves it works. 
- Riskiest assumption (1 sentence)
  - I believe the riskiest assumption is that the recommendations the user receives will be helpful and accurate. 
- Spike goal (what “success” means)
  - Passing this class.  Success would mean that our application takes into account the inventory and makes accurate recommendations for meal prep, donations, and composting. 

- Inputs → Outputs (what data goes in, what comes out)
#### Inputs
- Item name 
- Category
- quantity 
- best_by date
#### Outputs
- Meal prep
  - Recipes and meal ideas using items that are expiring soon first. 
  - Ingredient substitutions if available
- Donations
  - Item there are a surplus of
- Composting
  - Items past best-by date
  - Items not suitable for donation(opened Items)


### Demo plan (2–3 min) (what you will show live)s
- Inventory - show how items are input into the database and how they are stored
- AI
  - (AI) Meal ideas starting with the oldest items in the inventory first.
  - (AI) Reasoning(maybe it recognizes carrots + onions + broth = soup)
  - (AI) Donation arrangements
  - (AI) Composting guidance
- Explain that AI can actually get the items in the inventory and produce actions that are meaningful.
- What we will keep working on with the app
### Owner(s) + tasks (who is responsible for what)
- AI: Everybody
- Team DB: Emma, Jay, Luis, and Taja.
- Team Front End dev:  Abigail Rodriguez Vazquez , Luis, and Taja
### Exit criteria (clear pass/fail checks)
#### PASS
- Meal suggestions use items that are actually present
- Donation suggestions use items in surplus
- Compost suggestions use expired items
- Consistent results between runs
#### FAIL
- AI recommendations do not make sense
- The out varies too much between runs
- Ai only recommends Compost from day one.
- Inconsistent results from AI responds 


### If it fails… (Plan B / fallback approach)
- Plan B:  If AI cannot use the data provided reliably we hard code rules for expiration, donations, and composting and only use AI for meal ideas.  This will still allow us to deliver an application that delivers value.
