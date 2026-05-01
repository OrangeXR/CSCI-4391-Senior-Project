# ==========================================
# Converts units to canonical grams or ml
# ==========================================

UNIT_FACTORS={ # unit conversion dict as instructed
    # weight (base unit: grams)
    "g": {"factor": 1.0, "type": "grams"},
    "kg": {"factor": 1000.0, "type": "grams"},
    "lb": {"factor": 453.592, "type": "grams"},
    "oz": {"factor": 28.3495, "type": "grams"},
    "mg": {"factor": 0.001, "type": "grams"},

    # volume (base unit: ml)
    "ml": {"factor": 1.0, "type": "ml"},
    "l": {"factor": 1000.0, "type": "ml"},
    "liter": {"factor": 1000.0, "type": "ml"},
    "fl_oz": {"factor": 29.5735, "type": "ml"},
    "cup": {"factor": 240.0, "type": "ml"},
    "tbsp": {"factor": 15.0, "type": "ml"},
    "tsp": {"factor": 5.0, "type": "ml"},
    "gallon": {"factor": 3785.41, "type": "ml"},
    "half_gallon": {"factor": 1892.7, "type": "ml"}
}

def normalize_quantity(quantity, unit, measurement_type):
    # converts input quantity/unit into standardized grams or ml
    data = UNIT_FACTORS.get(unit.lower()) 

    if not data:
        return None, None # unknown unit
    
    converted = quantity * data["factor"] # convert to grams or ml based on factor

    if data["type"] == "grams":
        return converted, None # return grams with no unit for weight
    elif data["type"] == "ml":
        return None, converted # return ml with no unit for volume
    
    return None, None # fallback for unknown types

def convert_recipe_unit(amount, unit):
    # converts recipe to normalized standard (g/ml/count)
    data = UNIT_FACTORS.get(unit.lower())

    if not data:
        return amount, "count"
    
    return amount * data["factor"], data["type"] # convert and return type (grams/ml)