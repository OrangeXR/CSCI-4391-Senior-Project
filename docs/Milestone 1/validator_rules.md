
# Validator Rules 
* JSON must be correctly formatted. If it isn't, give: Please output strictly in the requested JSON format
*  Expired ingredients cannot be used for generating a recipe. If they are AI responds: Ingredient 'x' is expired and cannot be used.
*  The LLM response must be generated with the existing ingredient from the user DB. If it doesn't: Ingredient 'x' is not in the pantry.
* The LLM must not exceed the current user's ingredient Quantity. If there's not enough, then: Not enough 'x'. Need 'x'ml, but only have 'x'ml available. Please scale down portions/servings.
* The units must be converted. 
   






