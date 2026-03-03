# Pantry Database Shema
Documentation describes the structure, constraints, and data normalization rules for the pantry inventory system.

The system will track:<br>
- players (users)<br>
- inventory items <br>
- quantity normalization (grams /milliliters) <br>
- measurement type and unit policies <br><br>


# Player Table
| Name | Type    | Required | Description |
|------|---------|-------------|---------|
| id   | INTEGER(PK)| Yes |unique user id | 
| name | TEXT | Yes | name of user|
| username | TEXT | Yes | unique login username  |
| password_hash | TEXT | Yes | hashed password |
| profile_picture | TEXT | No| path to uploaded profile image |
| score| INTEGER | Yes | user |

# Inventory Table
| Name | Type    | Description | Example |
|------|---------|-------------|---------|
| id   | INTEGER(PK) | auto-generated item number | 1 | 
| player_id | INTEGER | player item belongs to | 1 |
| name | TEXT | item name | tomato |
| category | TEXT | item category type | produce|
| quantity | INTEGER | how many items | 1 |
| unit | TEXT | unit of measurement for item | g |
| measurment_type | TEXT | how was item measured | weight |
| quantity_grams | REAL | how many grams | 100.0 |
| quantity_ml | REAL | how many ml | 10.0 |
| purchase_date | TEXT | date item was purchased | 2026-02-10 |
| best_by | TEXT | expiry date | 2026-02-15 |
| raw_meat | BOOLEAN | is item raw | 1 |
| perishable | BOOLEAN | is item perishable | 1 |
| opened | BOOLEAN | is item open | 0 |
| donation_allowed | BOOLEAN | is item eligible for donation | 1 |
| price | REAL | price item purchased for | 2.49 |
| status | TEXT | status of item | active |

<br><br>

# Measurement types
System supports 3 measurement types:
count , stored directly no normalization
- weight, normalized to grams
- volume, normalized to milliliters
<br><br>
# Unit policy 
The listed units below are supported in normalize_quantity():
<br><br>
## weight units

| Unit | Converts to | Conversion Formula        |
|------|-------------|---------------------------|
| g    | grams       | grams = quantity          |
| kg   | grams       | grams = quantity * 1000   |
| lb   | grams       | grams = quantity * 453.592|
| oz   | grams       | grams = quantity * 28.3495|
| mg   | grams       | grams = quantity / 1000   |

if measurement_type == "weight":
- grams is populated, ml is NULL

## volume units
| Unit        | Converts to | Conversion Formula        |
|-------------|-------------|---------------------------|
| ml          | ml          | ml = quantity             |
| l/liter     | ml          | ml = quantity * 1000      |
| fl_oz.      | ml          | ml = quantity * 29.5735   |
| cup         | ml          | ml = quantity * 240       |
| tbsp        | ml          | ml = quantity * 15        |
| tsp         | ml          | ml = quantity * 5         |
| gallon      | ml          | ml = quantity * 3785.41   |
| half_gallon | ml          | ml = quantity * 1892.7    |
<br>

if measurement_type == "volume": <br>
- mL is populated <br>
- grams is NULL <br>


## Each Unit
if unit == "each" and  measurement_type == "count" <br>
- quantity is stored directly
- grams = NULL
- mL = NULL

# Canonicalization:<br>
When item values are case normalized(all lowercase) when entered into database.<br><br>
# Allowed units:<br>
kg, lb, oz, mg, g, ml,fl oz, cup, tbsp, tsp, gallon, half gallon, <br><br>

# Expiration storage format:<br>
YYYY-MM-DD<br><br>

# Example Records
## User Example 1
User enter: 
- **Item:** 2lb chicken breast 

Stored as:<br>
    - **Quantity** = 2 <br>
    - **Unit:** lb <br>
    - **Grams** = 907.184 <br>
    - **Milliliters (mL)** = NULL <br>

## User Example 2
User enter: 
- **Item:** 1 gallon Milk

Stored as: <br>
    - **Quantity** = 1 <br>
    - **Unit:** gallon <br>
    - **Milliliters (mL)** = 3785.41 <br>
    - **Grams** = NULL<br>

## User Example 2
User enter: 
- **Item:** 6 eggs

Stored as:<br>
    - **Quantity** = 6 <br>
    - **Unit:** count
    - **Milliliters (mL)** = 3785.41 <br>
    - **Grams** = NULL <br>






