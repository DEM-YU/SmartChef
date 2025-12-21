import json

# List of seasonings, tools, and basic staples that users usually have.
# These items do NOT appear in selection and do NOT penalize the score.
IGNORE_ITEMS = [
    "salt", "pepper", "sugar", "vinegar", "soy sauce", "oil", "garlic", "ginger", 
    "scallion", "green onion", "chili", "star anise", "cumin", "sesame", "oyster sauce",
    "cooking wine", "cornstarch", "toothpick", "water", "honey", "ketchup", "curry powder",
    "black pepper", "cinnamon", "bay leaf", "clove", "maple syrup", "butter"
]

def is_ignore(name):
    return any(key in name.lower() for key in IGNORE_ITEMS)

def get_categorized_ingredients():
    """Dynamically categorizes ingredients from recipes.json into English groups."""
    categories_map = {
        "🥩 Meat": ["beef", "pork", "chicken", "lamb", "bacon", "sausage", "ham", "ribs", "steak"],
        "🥬 Vegetables": ["potato", "tomato", "onion", "carrot", "broccoli", "spinach", "cabbage", "pepper", "cucumber", "mushroom", "lettuce", "eggplant", "celery"],
        "🐟 Seafood": ["fish", "shrimp", "prawn", "crab", "squid", "salmon", "seafood"],
        "🍚 Grains/Staples": ["rice", "pasta", "noodle", "flour", "corn", "bread", "spaghetti"],
        "🥚 Dairy/Eggs/Beans": ["egg", "tofu", "milk", "cheese", "yogurt", "bean"]
    }
    
    categorized = {cat: [] for cat in categories_map.keys()}
    
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            all_ings = set()
            for r in recipes:
                for ing in r.get('ingredients', []):
                    name = ing['name'].strip().lower()
                    if not is_ignore(name):
                        for cat, keywords in categories_map.items():
                            if any(key in name for key in keywords):
                                categorized[cat].append(name)
                                break
        for cat in categorized:
            categorized[cat] = sorted(list(set(categorized[cat])))
        return categorized
    except: return {}

def get_smart_recommendations(user_ingredients):
    """Calculates matching scores with the 'Main Ingredient Penalty' logic."""
    recommendations = []
    user_set = set([str(i).strip().lower() for i in user_ingredients])

    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            
        for recipe in recipes:
            total_weight, match_weight = 0, 0
            has_any_main = False   
            missing_items, others = [], []
            
            for ing in recipe.get('ingredients', []):
                name = ing['name'].strip().lower()
                
                if is_ignore(name):
                    others.append(name)
                    continue
                
                is_main = (ing.get('type') == 'main')
                weight = 4 if is_main else 1
                total_weight += weight
                
                if name in user_set:
                    match_weight += weight
                    if is_main: has_any_main = True
                else:
                    missing_items.append(name)
            
            # Score calculation with core ingredient check
            score = int((match_weight / total_weight) * 100) if has_any_main and total_weight > 0 else 0
            
            if score >= 15:
                recommendations.append({
                    "recipe": recipe,
                    "score": score,
                    "missing": missing_items,
                    "others": others
                })
        recommendations.sort(key=lambda x: x['score'], reverse=True)
    except: pass
    return recommendations