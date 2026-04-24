# pytest cases as guided by professor in sprint 3 md
import pytest
from unit_conversion import normalize_quantity, convert_recipe_unit

def test_weight_normalization():
    # 1kg should return 1000 grams, and None for ml
    g, ml = normalize_quantity(1, "kg", "weight")
    assert g == 1000.0
    assert ml is None

def test_volume_normalization():
    # 1 liter should return None for grams, and 1000 ml
    g, ml = normalize_quantity(1, "liter", "volume")
    assert g is None
    assert ml == 1000.0

def test_recipe_conversions():
    # Recipe units return value and unit type
    val, type_name = convert_recipe_unit(2, "lb")
    assert val == pytest.approx(907.184)
    assert type_name == "grams"
    
    val, type_name = convert_recipe_unit(1, "cup")
    assert val == 240.0
    assert type_name == "ml"

def test_unknown_unit():
    # Unknown units should return count
    val, type_name = convert_recipe_unit(10, "mystery_unit")
    assert val == 10
    assert type_name == "count"