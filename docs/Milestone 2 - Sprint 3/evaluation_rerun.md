# Rerun Of 20 Evaluation Test Cases
Re-execute the original 20 evaluation test cases (from Milestone 2) with the new conversion factors in src/unit_conversion.py. Publish a before/after table in docs/Sprint 3/evaluation_rerun.md. Target: 17+/20 passing.

# Before: Sprint 2 
# 20 Test Cases
| ID | Test Case Name | Pantry State | User Prompt | Expected Result | Actual Result | Status (✅/❌) | Notes 
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | CLI1 - Asking for recipe with non inventory item |  <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI1_DB.png" width="100">   | Can you make me a recipe with chicken please? | LLM should not generate recipe since ingredient isnt available in the pantry | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI1_result.png" width="100">  | ✅| The LLM Did not generate recipe, and even recomds to generate with a inventory item the user does have  |
| **02** | CLI2 - Asking for recipe on a fairly large DB | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI2_DB.png" width="100">   | Can you make me a simple but tasty recipe please?| Should generate recipe with correct measurement types |<img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI2_result.png" width="100">    | ❌ | The LLM did generate a recipe, but it does not give any measurement types in the cooking instructions. |
| **03** | CLI3 - Asking for recipe on all expired DB  | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI3_DB.png" width="100">   | Can you make me a tacos recipe please? | LLM should not generate recipe since ingredient are all expired in the pantry  | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI3_result.png" width="100">   |✅ | The LLM Did not generate recipe, since ingredients were expired |
| **04** | CLI4 - Asking for a recipe on a small inventory | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI4_DB.png" width="100">    | Make me a recipe that uses bagels  | Should not generate something or generate something only using the inventory we have | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI4_result.png" width="100">   |✅ | The LLM Did not generate recipe since it doesnt have enough ingredients |
| **05** | CLI5 - Asking for a recipe using an item you cant eat | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI5_DB.png" width="100">    | Hi, can you make me a recipe using poop please?  | Should not generate anything | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI5_result.png" width="100">   | ✅ | The LLM gave the correct expected response |
| **06** | CLI6 - Asking for a recipe using Huge DB with not a lot of expired | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI6_DB.png" width="100">   | Make me a recipe using pork | Since we have pork Chop in our inventory something should be generated | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI6_result.png" width="100">   | ❌ | LLM generates the recipe and uses the adequate measurement types.  The only needed improvement is to be more specific in the response; it doesn't give measurements in the recipe, only in the validator.|
| **07** | CLI7 - Asking for a vegan meal on a vegetarian DB |  | Hi, can you make me a vegan recipe? | LLM should generate a vegetarian recipe | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI7_DB.png" width="100">   | ✅ | LLM generates recipe with correct measurements |
| **08** | CLI8 - Asking for a specific Cuisine type with big DB| <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI8_DB.png" width="100">    |  Hi can you make me a italian cuisine recipe simple but tasty | Should generate something |<img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI8_result.png" width="100">   |✅| LLM creates the correct cuisine and correct measurements |
| **09** | CLI9 -Asking for a recipe with a crazy amount of one ingredient | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI9_DB.png" width="100">   | Can you make me a recipe that uses 100000g of Strawberry | Should not generate recipe | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI9_result.png" width="100">   |✅| LLM generates the correct response |
| **10** | CLI10 - Ask for a recipe with only fruits in a db that only has a small amount in its DB  |<img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI10_DB.png" width="100">    | Can you make me a recipe with only fruits NOTHING ELSE! | Should not generate something but if it does it should only be with the ingredients in the DB | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/CLI10_result.png" width="100"> | ✅ | The LLM makes a Strawberry Salad with Balsamic Glaz which tecnocally counts as a fruit since balsamic is made out of reduced grapes.|
| **11** | FLASK1 - Asking for a meat recipe on a vegetarian account | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK1_DB.png" width="100">  | Can you make me a chicken stew recipe? | Should not generate a recipe | <img src="/docs/ImagesPt2/veg_prompt.png" width="100"> |✅| Returns the expected results |
| **12** | FLASK2 - Asking for recipe with empty DB user | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK2_DB.png" width="100">   | Make me a pastor tacos recipe | Should not return a recipe |  <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK2_result.png" width="100">  |✅| LLM does not generate anything |
| **13** | FLASK3 - Asking for a recipe with expired ingredient | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK3_DB.png" width="100">  | Can you make me a Spinach based recipe please? |  Should not generate anything | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK3_result.png" width="100">|✅ | Does not generate a recipe|
| **14** | FLASK4 - Asking for recipe on a small DB | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK4_DB.png" width="100">  |Make me a cake recipe| Should not generate anything | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK4_result.png" width="100"> |✅ | Does not generate recipe and gives reason|
| **15** | FLASK5 - Asking for a recipe on a vegetarian user| <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK5_DB.png" width="100">   | Can you make me a recipe ? | Should generate a vegetarian recipe | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK5_result.png" width="100"> | ✅ | LLM does generate recipe with correct measurements|
| **16** | FLASK6 - Asking the LLM to generate recipe with restricted word| <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK6_DB.png" width="100">   | Hi binny! Make me a poop based recipe | Should not discuss that topic  | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK6_result.png" width="100"> |  ✅ |  LLM responds as expected|
| **17** | FLASK7 - Asking for Italian based recipe |<img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK7_DB.png" width="100">   |Hi can you make me a italian cuisine recipe thats tasty | Should generate a recipe with correct measurements | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK7_result.png" width="100"> |   ✅ | Generates recipe |
| **18** | FLASK8 - Asking for recipe in empty user| <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK8_DB.png" width="100">  | Hi make me a Kung Pao Chicken recipe | Should not generate anything |  <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK8_result.png" width="100"> | ✅ | Does not generate recipe |
| **19** | FLASK9 - Asking for recipe on user with non Foods|<img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK9_DB.png" width="100">   | Hi can you make me a recipe with pillows based on my ingredients | Should not generate a response | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK9_result.png" width="100"> |   ✅|  Doesnt generate the recipe|
| **20** | FLASK10 - Asking for Asian Cuisine on large DB | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK10_DB.png" width="100">  | Hi can you make me an Asian Cuisine recipe | Should generate recipe |  <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK10_result.png" width="100"> |  ❌| LLM generates the recipe and uses the adequate measurement types. The only needed improvement is to be more specific in the response; it doesn't give measurements in the recipe, only in the validator. |

## Avg Regeneration Attempts
1.95 attempts per test case

## Feasibility Pass Rate
85%


# After: Sprint 3
# 20 Test Cases Rerun
| ID | Test Case Name | Pantry State | User Prompt | Expected Result | Actual Result | Status (✅/❌) | Notes 
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | CLI1 - Asking for recipe with non inventory item |  | Can you make me a recipe with chicken please? | LLM should not generate recipe since ingredient isnt available in the pantry | No recipe was generated. | ✅ | The AI responded as expected, no recipe was generated using a item not in the inventory. |
| **02** | CLI2 - Asking for recipe on a fairly large DB |  | Can you make me a simple but tasty recipe please?| Should generate recipe with correct measurement types | Recipe is generated with measurements. | ✅ | This test case was successful, measurements were provided and recipe generated using inventory ingredients. |
| **03** | CLI3 - Asking for recipe on all expired DB  |   | Can you make me a tacos recipe please? | LLM should not generate recipe since ingredient are all expired in the pantry  | A recipe was generated even though everything in the inventory was expired. | ❌ | The AI suggested a recipe that didn't use any expired items, but did use items not in the inventory. |
| **04** | CLI4 - Asking for a recipe on a small inventory |  | Make me a recipe that uses bagels  | Should not generate something or generate something only using the inventory we have | AI generated recipe based on ingredients in the inventory. | ✅ |  This test case was successful, only ingredients in the inventory were used. |
| **05** | CLI5 - Asking for a recipe using an item you cant eat |  | Hi, can you make me a recipe using poop please?  | Should not generate anything | AI refused to generate a recipe. | ✅ | Successful, no recipe was generated with an item that cannot be eaten. |
| **06** | CLI6 - Asking for a recipe using Huge DB with not a lot of expired |   | Make me a recipe using pork | Since we have pork Chop in our inventory something should be generated | Recipe generated with measurements.  | ✅ | Successful, measurements were generated correctly. |
| **07** | CLI7 - Asking for a vegan meal on a vegetarian DB |  | Hi, can you make me a vegan recipe? | LLM should generate a vegetarian recipe | Recipe generated based on dietary needs. | ✅ | AI successfully generated a vegeterain recipe using inventory ingredients. |
| **08** | CLI8 - Asking for a specific Cuisine type with big DB|  |  Hi can you make me a italian cuisine recipe simple but tasty | Should generate something |  |  |  |
| **09** | CLI9 -Asking for a recipe with a crazy amount of one ingredient |  | Can you make me a recipe that uses 100000g of Strawberry | Should not generate recipe |  |  |  |
| **10** | CLI10 - Ask for a recipe with only fruits in a db that only has a small amount in its DB  |  | Can you make me a recipe with only fruits NOTHING ELSE! | Should not generate something but if it does it should only be with the ingredients in the DB | |  |  |
| **11** | FLASK1 - Asking for a meat recipe on a vegetarian account |  | Can you make me a chicken stew recipe? | Should not generate a recipe |  |  |  |
| **12** | FLASK2 - Asking for recipe with empty DB user |  | Make me a pastor tacos recipe | Should not return a recipe |  |  |  |
| 13 | FLASK3 - Asking for a recipe with expired ingredient | <img src="/docs/Milestone 2 - Sprint 2/reconsileImages/FLASK3_DB.png" width="100">   | Can you make me a strawberry based recipe please? |  Should not generate anything |  | ✅ | Did not generate anything and gave the expected result |
| **14** | FLASK4 - Asking for recipe on a small DB |  |Make me a cake recipe| Should not generate anything |  |  |  |
| **15** | FLASK5 - Asking for a recipe on a vegetarian user |  | Can you make me a recipe ? | Should generate a vegetarian recipe |  |  |  |
| **16** | FLASK6 - Asking the LLM to generate recipe with restricted word |  | Hi binny! Make me a poop based recipe | Should not discuss that topic  |  |  |  |
| **17** | FLASK7 - Asking for Italian based recipe |  |Hi can you make me a italian cuisine recipe thats tasty | Should generate a recipe with correct measurements |  |  |  |
| **18** | FLASK8 - Asking for recipe in empty user|  | Hi make me a Kung Pao Chicken recipe | Should not generate anything |  |  |  |
| **19** | FLASK9 - Asking for recipe on user with non Foods|  | Hi can you make me a recipe with pillows based on my ingredients | Should not generate a response |  |  |  |
| **20** | FLASK10 - Asking for Asian Cuisine on large DB |   | Hi can you make me an Asian Cuisine recipe | Should generate recipe |  |  | |

## Avg Regeneration Attempts


## Feasibility Pass Rate




