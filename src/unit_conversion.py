# ==========================================
# Converts units to canonical grams or ml
# ==========================================


def normalize_quantity(quantity, unit, measurement_type):
    grams = None
    ml = None
    unit = unit.lower()

    if measurement_type == "weight":
        if unit == "kg":
            grams = quantity * 1000
        elif unit == "lb":
            grams = quantity * 453.592
        elif unit == "oz":
            grams = quantity * 28.3495
        elif unit == "mg":
            grams = quantity / 1000
        elif unit == "g":
            grams = quantity

    elif measurement_type == "volume":
        if unit == "ml":
            ml = quantity
        elif unit in ["l", "liter"]:
            ml = quantity * 1000
        elif unit == "fl_oz":
            ml = quantity * 29.5735
        elif unit == "cup":
            ml = quantity * 240
        elif unit == "tbsp":
            ml = quantity * 15
        elif unit == "tsp":
            ml = quantity * 5
        elif unit == "gallon":
            ml = quantity * 3785.41
        elif unit == "half_gallon":
            ml =quantity * 1892.7

    return grams, ml

def convert_recipe_unit(amount, unit):
    # converts recipe ingredient units to normalized form so validator can compare 
  
    if unit in ["g"]:
        return amount, "grams"

    if unit in ["kg"]:
        return amount * 1000, "grams"

    if unit in ["lb"]:
        return amount * 453.592, "grams"

    if unit in ["ml"]:
        return amount, "ml"

    if unit in ["fl_oz"]:
        return amount * 29.5735, "ml"

    return amount, "count"