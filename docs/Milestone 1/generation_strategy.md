
# Option C: Constraint-guided decoding (lightweight)

### Use a structured JSON output format from LLM.

### Reject outputs failing schema/constraints and regenerate


Our project uses constraint-guided decoding to ensure that all AI‑generated recipes are:
Realistic, using only the user’s actual inventory
The LLM generates a recipe using the user's inventory.
The LLM is required to return the recipe in a structured JSON format that includes the recipe instructions and the ingredients used with their quantities and units.

After the recipe is generated, our program runs a validator that checks several rules:

* JSON must be correctly formatted. If it isn’t, give: Please output strictly in the requested JSON format.
* Expired ingredients cannot be used for generating a recipe. If they are AI responds: Ingredient ‘x’ is expired and cannot be used.
* The LLM response must be generated with the existing ingredient from the user DB. If it doesn’t: Ingredient ‘x’ is not in the pantry.
* The LLM must not exceed the current user’s ingredient Quantity. If there’s not enough, then: Not enough ‘x’. Need 'x’ml, but only have 'x’ml available. Please scale down portions/servings.
* The units must be converted.


Why was option C chosen?
Option C was selected because it is simpler to implement while also preventing.

* inventing ingredients
* using expired food
* requesting unrealistic quantities

These are especially important for our app since:
Recipes must use only items from the user’s inventory
Filters out expired items
Suggests exact quantities for each ingredient









