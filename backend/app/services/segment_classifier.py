from typing import Optional

FOOD_SEGMENTS = {
    "grains": {
        "label": "Grains & Cereals",
        "icon": "🌾",
        "keywords": ["wheat", "grain", "barley", "oats", "maize", "corn", "sorghum",
                     "millet", "rye", "cereal grain", "crop", "harvest", "field crop"],
    },
    "rice": {
        "label": "Paddy & Rice",
        "icon": "🍚",
        "keywords": ["rice", "paddy", "basmati", "jasmine rice", "parboil",
                     "arborio", "brown rice", "white rice", "long grain"],
    },
    "flour_milling": {
        "label": "Flour Milling",
        "icon": "🌀",
        "keywords": ["flour", "milling", "mill", "semolina", "bran", "starch",
                     "grinding", "roller mill", "stone mill", "wheat flour"],
    },
    "cocoa": {
        "label": "Cocoa & Chocolate",
        "icon": "🍫",
        "keywords": ["cocoa", "cacao", "chocolate", "confectionery", "compound chocolate",
                     "dark chocolate", "milk chocolate", "white chocolate", "praline",
                     "barry callebaut", "mondelez", "ferrero"],
    },
    "coffee": {
        "label": "Coffee Speciality",
        "icon": "☕",
        "keywords": ["coffee", "espresso", "roast", "arabica", "robusta", "cold brew",
                     "specialty coffee", "barista", "cappuccino", "latte", "caffeine"],
    },
    "dairy": {
        "label": "Dairy & Alternatives",
        "icon": "🥛",
        "keywords": ["dairy", "milk", "cheese", "butter", "yogurt", "cream", "whey",
                     "lactose", "oat milk", "almond milk", "plant-based milk",
                     "ice cream", "gelato", "kefir", "casein"],
    },
    "meat_poultry": {
        "label": "Meat & Poultry",
        "icon": "🥩",
        "keywords": ["meat", "beef", "poultry", "chicken", "pork", "lamb", "turkey",
                     "sausage", "deli", "cold cut", "slaughterhouse", "abattoir",
                     "processed meat", "cured meat", "tyson"],
    },
    "seafood": {
        "label": "Seafood & Aquaculture",
        "icon": "🐟",
        "keywords": ["seafood", "fish", "aquaculture", "salmon", "tuna", "shrimp",
                     "prawn", "shellfish", "lobster", "crab", "tilapia", "cod",
                     "fishery", "marine harvest"],
    },
    "fruits_vegetables": {
        "label": "Fruits & Vegetables",
        "icon": "🥦",
        "keywords": ["fruit", "vegetable", "produce", "fresh cut", "avocado", "tomato",
                     "potato", "onion", "berry", "citrus", "apple", "banana",
                     "salad", "fresh produce", "horticulture"],
    },
    "beverages": {
        "label": "Beverages",
        "icon": "🥤",
        "keywords": ["beverage", "juice", "soft drink", "energy drink", "water",
                     "tea", "beer", "wine", "spirits", "alcohol", "kombucha",
                     "cola", "pepsi", "coca-cola", "red bull"],
    },
    "snacks_bakery": {
        "label": "Snacks & Bakery",
        "icon": "🍞",
        "keywords": ["snack", "bakery", "bread", "biscuit", "cookie", "cracker",
                     "cake", "pastry", "muffin", "donut", "chip", "crisp",
                     "pretzel", "popcorn", "granola bar", "protein bar"],
    },
    "alt_protein": {
        "label": "Alt-Protein & Novel Foods",
        "icon": "🌱",
        "keywords": ["alt-protein", "plant-based", "vegan", "cultivated meat",
                     "fermentation", "insect protein", "mycoprotein", "pea protein",
                     "soy protein", "beyond meat", "impossible", "lab-grown",
                     "precision fermentation", "novel food"],
    },
    "oils_fats": {
        "label": "Oils & Fats",
        "icon": "🫒",
        "keywords": ["oil", "fat", "palm oil", "olive oil", "sunflower oil",
                     "canola", "rapeseed", "soybean oil", "margarine", "shortening",
                     "hydrogenated", "omega-3", "fatty acid"],
    },
    "spices_flavours": {
        "label": "Spices & Flavours",
        "icon": "🌶️",
        "keywords": ["spice", "flavour", "flavor", "seasoning", "herb", "pepper",
                     "cumin", "turmeric", "cinnamon", "vanilla", "extract",
                     "aroma", "taste", "givaudan", "firmenich", "iff"],
    },
    "packaging": {
        "label": "Food Packaging",
        "icon": "📦",
        "keywords": ["packaging", "pack", "label", "container", "bottle", "can",
                     "pouch", "film", "wrap", "sustainable packaging", "recyclable",
                     "biodegradable", "tetra pak", "plastic-free"],
    },
    "food_safety": {
        "label": "Food Safety & Regulation",
        "icon": "✅",
        "keywords": ["food safety", "regulation", "fda", "efsa", "haccp", "recall",
                     "contamination", "allergen", "labelling", "certification",
                     "organic", "halal", "kosher", "iso 22000", "brc"],
    },
    "food_tech": {
        "label": "Food Technology",
        "icon": "🔬",
        "keywords": ["food tech", "innovation", "automation", "robot", "ai",
                     "3d print food", "blockchain", "iot", "smart factory",
                     "digitisation", "machine learning food", "sensor", "tech"],
    },
    "storage_logistics": {
        "label": "Storage & Logistics",
        "icon": "🏭",
        "keywords": ["storage", "logistics", "cold chain", "warehouse", "silo",
                     "supply chain", "distribution", "transport", "refrigeration",
                     "bulk handling", "inventory", "port", "shipping food"],
    },
}

def classify_segment(title: str, summary: str) -> Optional[str]:
    text = f"{title} {summary}".lower()
    scores = {}
    for seg_key, seg_data in FOOD_SEGMENTS.items():
        score = sum(1 for kw in seg_data["keywords"] if kw in text)
        if score > 0:
            scores[seg_key] = score
    if not scores:
        return None
    return max(scores, key=scores.get)

def get_all_segments():
    return [
        {"key": k, "label": v["label"], "icon": v["icon"]}
        for k, v in FOOD_SEGMENTS.items()
    ]
