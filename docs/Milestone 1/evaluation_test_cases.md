

# Test Cases

> click on Images on Pantry Snapshot for better view

| ID | Test Case Name | Pantry Snapshot | Expected Result | Actual Result | Status (✅/❌) | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** |Not Enough Sugar |<img src="images/DB_num1.png" width="100"> |Pass |Pass: <br> <img src="images/DB_num1_Result.png" width="100"> <img src="images/DB_num1_Result2.png" width="100"> |✅ |Scaled down the recipe |
| **02** |Expired Chicken Breast |<img src="images/DB_num2.png" width="100"> |Pass |Pass: <br> <img src="images/DB_num2_Result.png" width="100"> <img src="images/DB_num2_Result2.png" width="100">|✅ |Did not generate a recipe with expired ingredient |
| **03** |Cherries Are Not in the Inventory |<img src="images/DB_num3.png" width="100"> |Pass |Pass: <br> <img src="images/DB_num3_Result.png" width="100"> |✅ |Did not generate a recipe with an item not in the inventory |
| **04** |Expired Milk |<img src="images/DB_num4.png" width="100"> |Pass |Pass: <br> <img src="images/DB_num4_Result.png" width="100"> <img src="images/DB_num4_Result2.png" width="100"> |✅ |Did not generate a recipe with expired ingredient |
| **05** |Expiry First |<img src="images/DB_num5.png" width="100"> |Pass |Pass: <br> <img src="images/DB_num5_Result.png" width="100"> <img src="images/DB_num5_Result2.png" width="100">|✅ |Recommended a recipe with expiring ingredients |
| **06** |Non-food Item |<img src="images/DB_num6.png" width="100"> |Pass |Pass: <br> <img src="images/DB_num6_Result.png" width="100"> |✅ |Did not recommend a recipe with a non-food item |
| **07** |Scaling down Multiple Items |<img src="images/DB_num7.png" width="100"> |Fail |Fail: <img src="images/DB_num7_Result.png" width="100"> <img src="images/DB_num7_Result2.png" width="100"> |❌ |Unit conversion was unsuccessful |
| **08** |2 Fresh, 1 Expired |<img src="images/DB_num8.png" width="100">  |Pass |Pass: <br> <img src="images/DB_num8_Result.png" width="100"> <img src="images/DB_num8_Result2.png" width="100"> |✅ |Did not use expired ingredient in the recipe |
| **09** |Food Safety Advice |<img src="images/DB_num9.png" width="100"> |Pass |Pass: <img src="images/DB_num9_Result.png" width="100"> |✅ |Did not offer food safety advice |
| **10** |Eggplant Fettuccine + Soap |<img src="images/DB_num10.png" width="100"> |Pass |Fail: <br> <img src="images/DB_num10_Result.png" width="100"> <img src="images/DB_num10_Result2.png" width="100">|❌ |Ignored soap but unit conversion failed |
| **11** | Small DB with Many Expired Items | <img src="images/DB_num_11.png" width="100"> | Fail | Fail:<br><img src="images/num_11_result.png" width="100"> | ✅ | Did not generate recipe with non-inventory items |
| **12** | Recipe Attempt with Expired Inventory | <img src="images/DB_num_12.png" width="100"> | Fail | Fail:<br><img src="images/num_12_result1.png" width="100"> <img src="images/num_12_result2.png" width="100"> | ✅ | Did not generate recipe using expired inventory |
| **13** | Large DB with 5 Expired Items | <img src="images/DB_num_13.png" width="100"> | Pass | Pass:<br><img src="images/num_13_result1.png" width="100"> <img src="images/num_13_result2.png" width="100"> |✅ | correctly converted units and used only user inventory | 
| **14** | Large DB with No Expired Inventory | <img src="images/DB_num_14.png" width="100"> | Pass | Fail:<br><img src="images/num_14_result1.png" width="100"> <img src="images/num_14_result2.png" width="100"> | ❌ |Invents ingredient basil leaves| 
| **15** | DB with 27 Expired and 1 Fresh Item | <img src="images/DB_number_15.png" width="100"> | Fail |Fail: <img src="images/num_15_result1.png" width="100"> <img src="images/num_15_result2.png" width="100"> | ✅ |did not use expired items for recipe | 
| **16** | Meat-only DB Requesting Vegan Meal | <img src="images/DB_number_16.png" width="100"> | Fail | Fail:<img src="images/num_16_result1.png" width="100"> <img src="images/num_16_result2.png" width="100"> |✅ | Did not generate recipe for vegan meal with only meat inventory | 
| **17** | DB for Sweet Recipes | <img src="images/DB_number_17.png" width="100"> | Pass | Pass : <img src="images/num_17_result1.png" width="100"> <img src="images/num_17_result2.png" width="100"> |❌ |Unit conversion was unsuccessful but on plus did generated a sweet recipe| 
| **18** | Vegan-only Inventory | <img src="images/DB_number_18.png" width="100"> | Pass | Pass: <img src="images/num_18_result1.png" width="100"> <img src="images/num_18_result2.png" width="100"> |✅ |correctly converted units and used only user inventory   | 
| **19** | Incorrect Inventory | <img src="images/DB_number_19.png" width="100"> | Fail |Fail <img src="images/num_19_result1.png" width="100"> |❌ | doesnt generate recipe but it also doesnt handle the db correctly. Should print out something like unfit inventory etc | 
| **20** | Asian Cuisine-Friendly Pantry | <img src="images/DB_number20.png" width="100"> | Pass |Fail: <img src="images/number_20_result1.png" width="60"> <img src="images/number_20_result2.png" width="60"> <img src="images/number_20_result3.png" width="60"> |❌ | uses tbsp when user has ml,Unit conversion was unsuccessful  | 

# Avg Regeneration Attempts
1.05 attempts per test case


# Feasibility Pass Rate
80%

# “Invented Ingredient” Rate
5%
