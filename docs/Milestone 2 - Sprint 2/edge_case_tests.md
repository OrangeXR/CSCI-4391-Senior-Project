# Edge Test Cases
Test with: empty pantry, all items expired, single ingredient, conflicting dietary restrictions

| ID | Test Case Name | Pantry State | User Prompt | Expected Result | Actual Result | Status (✅/❌) | Notes | Image |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Empty Pantry | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/emptyPantry.png" width="100"> | "What can I make for lunch?" | The user will recieve a response saying there are no ingredients in the pantry and recommend that the user adds some to get started. | AI detects no ingredients in the user's inventory and asks them to add some to get started. | ✅ | This test case worked as expected, no ingredients were hallucinated. | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/emptyPantry2.png" width="100"> |
| **02** | All ingredients are expired | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/expiredPantry.png" width="100"> | "What can I make for dinner?" | No recipe will be generated and the user will be told that the ingredients are expired and cannot be used. | The AI did not generate any meal recommendations and explained why. | ✅ | This test case was successful, no meal was generated with the entire pantry being filled with expired ingredients. | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/expiredPantry2.png" width="100"> |
| **03** | Single ingredient in the pantry | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/SingleIngredient.png" width="100"> | "What meals can I make?" | The user will recieve a response saying there is not enough ingredients to make a meal OR a simple 1 ingredient meal will be generated. | AI generated a meal with ingredients such as butter/oil which are not in the pantry. | ❌ | AI generated a meal assuming butter and oil were available. This test case was not successful. | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/SingleIngredient2.png" width="100"> |
| **04** | Conflicting dietary restrictions | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/Vegeratian.png" width="100"> | "Give me a vegetarian recipe that includes tomato paste and chicken breast." | AI will detect the conflict OR no recipe will be generated with an explanation. | AI did not generate a recipe because it detected a conflict with the user's dietary needs. | ✅ | AI successfully detected a conflict concerning the user's dietary needs.  | <img src="/docs/Milestone 2 - Sprint 2/EdgeCaseImages/Vegetarian2.png" width="100"> |

# Avg Regeneration Attempts
0 attempts per test case

# Feasibility Pass Rate
75%
