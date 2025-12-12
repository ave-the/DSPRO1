import ast
import re
import pandas as pd

INPUT_CSV = "./Datasets/13k-recipes.csv"
OUTPUT_CSV = "recipe_ingredient_matrix.csv"

COLUMNS = [
    "Recipe",
    "Duck liver (gr)", "Goose liver (gr)", "Beef kidney (gr)",
    "Chicken Broilers (gr)", "Turkey (gr)", "Trout (gr)", "Sardine (gr)",
    "Tofu (gr)", "Soybeans (gr)", "Black beans (gr)", "Lentils (gr)",
    "Pinto beans (gr)", "Chickpea flour (gr)", "Seaweed (gr)",
    "Taro (gr)", "Cassava (gr)", "Thyme (gr)", "Vinegar (ml)",
    "Flour wheat (gr)", "Pasta (gr)", "white Rice (gr)", "Potatoes (gr)",
    "Milk (ml)", "Soy milk (ml)", "Salt (gr)", "Water (ml)"
]
'''
def parse_ingredient_string(s):
    """
    Expect something like: '1 cup whole milk', '2 Tbsp. olive oil', '1 (3½–4-lb.) whole chicken'
    Returns (amount_float, unit/string, name_string)
    """
    s = s.lower()
    # Replace unicode fractions with decimal approximations
    frac_map = {
        "½": "1/2",
        "¼": "1/4",
        "¾": "3/4",
        "⅓": "1/3",
        "⅔": "2/3",
        "⅛": "1/8",
    }
    for k, v in frac_map.items():
        s = s.replace(k, " " + v + " ")

    s = s.replace("–", "-")

    # Extract a leading quantity like "1 1/2", "3-4", "1", "2 3/4"
    m = re.match(r"\s*([\d/\.]+(?:\s+[\d/\.]+)?(?:\s*-\s*[\d/\.]+)?)\s+(.*)", s)
    if not m:
        # No explicit leading quantity; treat as 1 unit if it is countable like "1 onion" type,
        # but here just return None amount and full string as name
        return None, None, s.strip()

    qty_str = m.group(1)
    rest = m.group(2).strip()

    # If range like "3-4", take average
    if "-" in qty_str:
        a, b = qty_str.split("-", 1)
        try:
            qty = (float(eval(a)) + float(eval(b))) / 2.0
        except Exception:
            qty = float(eval(a))
    else:
        try:
            qty = float(eval(qty_str))
        except Exception:
            qty = None

    # Now split rest into a possible unit + name
    parts = rest.split()
    if not parts:
        return qty, None, ""

    possible_unit = parts[0]
    # Normalize some units
    unit_aliases = {
        "tbsp": "tbsp",
        "tbsp.": "tbsp",
        "tablespoon": "tbsp",
        "tablespoons": "tbsp",
        "tsp": "tsp",
        "tsp.": "tsp",
        "teaspoon": "tsp",
        "teaspoons": "tsp",
        "cup": "cup",
        "cups": "cup",
        "pound": "lb",
        "pounds": "lb",
        "lb.": "lb",
        "lb": "lb",
        "oz": "oz",
        "ounce": "oz",
        "ounces": "oz",
        "can": "can",
        "cans": "can",
    }
    unit = unit_aliases.get(possible_unit, None)

    if unit is not None:
        name = " ".join(parts[1:]).strip()
    else:
        unit = None
        name = rest

    return qty, unit, name
    
    
'''

import re

# Put this near the top of your file
FRACTION_MAP = {
    "½": "1/2",
    "¼": "1/4",
    "¾": "3/4",
    "⅓": "1/3",
    "⅔": "2/3",
    "⅛": "1/8",
}

def parse_fraction(token: str) -> float:
    """
    Parse a token like '1', '1/2', '3/4' into a float.
    """
    token = token.strip()
    if "/" in token:
        num, den = token.split("/", 1)
        return float(num) / float(den)
    return float(token)

def parse_quantity(qty_str: str) -> float | None:
    """
    Parse a quantity string that may be:
    - '2'
    - '1/2'
    - '2 1/2' (mixed number)
    - '2-3'
    - '2 1/2-3'
    - '2 1/2 - 3 1/2'
    Returns a single float (averaging ranges).
    """
    qty_str = qty_str.strip()
    # Normalize multiple spaces
    qty_str = re.sub(r"\s+", " ", qty_str)

    # Handle ranges 'a-b'
    if "-" in qty_str:
        left, right = [p.strip() for p in qty_str.split("-", 1)]
        return (parse_quantity(left) + parse_quantity(right)) / 2.0

    # Mixed number 'a b/c'
    parts = qty_str.split(" ")
    if len(parts) == 2 and "/" in parts[1]:
        whole = parse_fraction(parts[0])
        frac = parse_fraction(parts[1])
        return whole + frac

    # Simple number or fraction
    return parse_fraction(qty_str)

def parse_ingredient_string(s):
    """
    Expect something like: '1 cup whole milk', '2 Tbsp. olive oil', '2 1/2-3 cups milk'
    Returns (amount_float, unit/string, name_string)
    """
    s = s.lower()

    # Replace unicode fractions with ascii
    for k, v in FRACTION_MAP.items():
        s = s.replace(k, " " + v + " ")

    s = s.replace("–", "-")  # en dash to hyphen

    # Regex: quantity (possibly with spaces and / and -) + whitespace + rest
    m = re.match(r"\s*([\d\s\/\.\-]+)\s+(.+)", s)
    if not m:
        # No explicit leading quantity; return None amount, treat full string as name
        return None, None, s.strip()

    qty_str = m.group(1)
    rest = m.group(2).strip()

    try:
        qty = parse_quantity(qty_str)
    except Exception:
        qty = None

    # Split rest into possible unit + name
    parts = rest.split()
    if not parts:
        return qty, None, ""

    possible_unit = parts[0]
    unit_aliases = {
        "tbsp": "tbsp",
        "tbsp.": "tbsp",
        "tablespoon": "tbsp",
        "tablespoons": "tbsp",
        "tsp": "tsp",
        "tsp.": "tsp",
        "teaspoon": "tsp",
        "teaspoons": "tsp",
        "cup": "cup",
        "cups": "cup",
        "pound": "lb",
        "pounds": "lb",
        "lb.": "lb",
        "lb": "lb",
        "oz": "oz",
        "ounce": "oz",
        "ounces": "oz",
        "can": "can",
        "cans": "can",
    }
    unit = unit_aliases.get(possible_unit, None)

    if unit is not None:
        name = " ".join(parts[1:]).strip()
    else:
        unit = None
        name = rest

    return qty, unit, name


def to_grams_or_ml(qty, unit, name):
    """
    Apply Option 1 conversions.
    Returns numeric amount in grams or ml (treat ml ~ grams for water-like liquids).
    If no unit, handle special cases like '1 onion', '1 egg', '1 potato', '1 can beans'.
    """
    if qty is None:
        # Try heuristics for things like "1 onion", "1 egg"
        # Very rough: look for 'onion', 'egg', 'potato', 'can'
        if "onion" in name:
            return 150.0
        if "egg" in name:
            # 1 egg = 50 g; final mapping to yolk is 18 g, handled later
            return 50.0
        if "potato" in name:
            return 150.0
        if "can" in name and "bean" in name:
            return 425.0
        return 0.0

    if unit is None:
        # E.g., "2 onions"
        if "onion" in name:
            return qty * 150.0
        if "egg" in name:
            return qty * 50.0
        if "potato" in name:
            return qty * 150.0
        if "can" in name and "bean" in name:
            return qty * 425.0
        # Fallback: treat as grams
        return qty

    if unit == "cup":
        # 1 cup milk = 240 ml, 1 cup solids ~ 120 g (rough generic)
        if "milk" in name or "broth" in name or "stock" in name or "water" in name:
            return qty * 240.0
        else:
            return qty * 120.0
    if unit == "tbsp":
        # 1 tbsp liquid = 14 g/ml
        return qty * 14.0
    if unit == "tsp":
        # 1 tsp = 5 g
        return qty * 5.0
    if unit == "lb":
        return qty * 454.0
    if unit == "oz":
        return qty * 28.35
    if unit == "can":
        # Only beans specified
        if "bean" in name:
            return qty * 425.0
        return qty * 425.0  # generic can
    return qty

def map_to_fixed(name, amount):
    """
    Apply Option A approximate mapping rules to map ingredient name + amount
    onto one of the fixed columns. Returns dict {column_name: amount_to_add}.
    Unmapped -> {} (treated as zeros).
    """

    name = name.lower()

    # Helpers
    def add(col, amt):
        return {col: amt}

    # Organs / livers
    if "liver" in name:
        if "goose" in name:
            return add("Goose liver (gr)", amount)
        if "duck" in name:
            return add("Duck liver (gr)", amount)
        # any other liver
        return add("Duck liver (gr)", amount)
    if "kidney" in name or "offal" in name or "giblet" in name:
        return add("Beef kidney (gr)", amount)

    # Protein: specific meats
    if any(x in name for x in ["chicken", "broiler", "thigh", "drumstick", "wing", "breast"]):
        return add("Chicken Broilers (gr)", amount)
    if "turkey" in name:
        return add("Turkey (gr)", amount)
    if any(x in name for x in ["salmon", "cod", "fish", "trout", "tuna"]):
        return add("Trout (gr)", amount)
    if "shrimp" in name or "prawn" in name:
        return add("Sardine (gr)", amount)
    if any(x in name for x in ["pork", "bacon", "ham", "prosciutto"]):
        return add("Beef kidney (gr)", amount)
    if any(x in name for x in ["beef", "lamb", "mutton", "steak"]):
        return add("Beef kidney (gr)", amount)
    if "tofu" in name:
        return add("Tofu (gr)", amount)
    if "edamame" in name or "soybean" in name or "soy bean" in name:
        return add("Soybeans (gr)", amount)
    if "black bean" in name:
        return add("Black beans (gr)", amount)
    if "lentil" in name:
        return add("Lentils (gr)", amount)
    if "pinto bean" in name:
        return add("Pinto beans (gr)", amount)
    if "chickpea" in name or "garbanzo" in name:
        return add("Chickpea flour (gr)", amount)
    if "egg" in name:
        # 1 egg = 50 g total -> 18 g yolk per egg
        # amount currently in grams; convert to yolk grams in proportion
        # eggs = amount / 50, yolk = eggs * 18
        eggs = amount / 50.0
        yolk_g = eggs * 18.0
        return add("Duck liver (gr)", yolk_g)  # mapped to egg yolk placeholder? adjust if you change column
    if "cheese" in name or "cream cheese" in name or "evaporated milk" in name:
        # Cheese/milk solids → Milk
        return add("Milk (ml)", amount)

    # Carbs / starches
    if "rice" in name:
        return add("white Rice (gr)", amount)
    if "pasta" in name or "spaghetti" in name or "macaroni" in name or "noodle" in name:
        return add("Pasta (gr)", amount)
    if "potato" in name:
        return add("Potatoes (gr)", amount)
    if any(x in name for x in ["bread", "flatbread", "roti", "pita", "tortilla"]):
        return add("Pasta (gr)", amount)
    if any(x in name for x in ["quinoa", "barley", "farro", "bulgur", "millet"]):
        return add("white Rice (gr)", amount)
    if "flour" in name and "wheat" in name or "all-purpose flour" in name or "all purpose flour" in name:
        return add("Flour wheat (gr)", amount)
    if "masa" in name:
        # corn masa as carb -> map to Pasta arbitrarily, or white Rice; choose Pasta per bread/flatbread
        return add("Pasta (gr)", amount)
    if "cassava" in name or "yuca" in name:
        return add("Cassava (gr)", amount)
    if "taro" in name:
        return add("Taro (gr)", amount)

    # Veg / flavors
    if "seaweed" in name or "nori" in name or "kombu" in name:
        return add("Seaweed (gr)", amount)
    if any(x in name for x in ["onion", "garlic", "herb", "oregano", "basil", "sage",
                               "rosemary", "parsley", "cilantro", "chive", "thyme", "spice"]):
        return add("Thyme (gr)", amount)
    if any(x in name for x in ["tomato", "mushroom"]) or "fruit" in name or "vegetable" in name:
        # Fruit/vegetables, tomatoes, mushrooms -> 0
        return {}

    # Liquids
    if any(x in name for x in ["milk", "cream", "half-and-half", "half and half"]) and "soy" not in name and "coconut" not in name:
        return add("Milk (ml)", amount)
    if "soy milk" in name or "soymilk" in name:
        return add("Soy milk (ml)", amount)
    if "coconut milk" in name:
        # Map to Soy milk but keep original volume
        return add("Soy milk (ml)", amount)
    if "broth" in name or "stock" in name:
        return add("Milk (ml)", amount)
    if any(x in name for x in ["vinegar", "cider vinegar", "wine vinegar"]):
        return add("Vinegar (ml)", amount)
    if any(x in name for x in ["water"]):
        return add("Water (ml)", amount)
    if any(x in name for x in ["oil", "butter", "lard", "shortening", "ghee"]):
        # Oils/butter -> 0
        return {}

    # Salt
    if "salt" in name and "kosher" in name or "sea salt" in name or "salt," in name:
        return add("Salt (gr)", amount)

    # Fallback: unmapped
    return {}

def process_row(cleaned_ingredients_str):
    try:
        ing_list = ast.literal_eval(cleaned_ingredients_str)
        if not isinstance(ing_list, list):
            return []
    except Exception:
        return []

    parsed = []
    for raw in ing_list:
        if not isinstance(raw, str):
            continue
        qty, unit, name = parse_ingredient_string(raw)
        amount = to_grams_or_ml(qty, unit, name)
        parsed.append((amount, name))
    return parsed

def build_matrix(df):
    rows = []
    for _, row in df.iterrows():
        title = row["Title"]
        cleaned = row.get("Cleaned_Ingredients", row.get("Ingredients"))

        amounts = {col: 0.0 for col in COLUMNS}
        amounts["Recipe"] = title

        parsed = process_row(cleaned)
        for amount, name in parsed:
            mapping = map_to_fixed(name, amount)
            for col, val in mapping.items():
                if col in amounts:
                    amounts[col] += val
        rows.append(amounts)

    return pd.DataFrame(rows, columns=COLUMNS)

def main():
    df = pd.read_csv(INPUT_CSV)
    matrix = build_matrix(df)
    matrix.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(matrix)} recipes to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
    