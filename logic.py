import json

def get_recommendations(user_ingredients):
    """纯本地匹配逻辑：100% 稳定，无需联网"""
    can_cook = []
    missing_one = []
    
    try:
        # 读取本地 recipes.json
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
    except FileNotFoundError:
        return [], []

    # 处理用户选择的食材
    user_set = set([str(i).strip() for i in user_ingredients])

    for recipe in recipes:
        # 适配你的字典格式 JSON
        extracted_ingredients = []
        for ing in recipe.get('ingredients', []):
            if isinstance(ing, dict):
                extracted_ingredients.append(ing.get('name', '').strip())
            else:
                extracted_ingredients.append(str(ing).strip())
        
        recipe_set = set(extracted_ingredients)
        actual_missing = recipe_set - user_set
        
        # 逻辑：完全匹配或只差一样
        if len(actual_missing) == 0:
            can_cook.append(recipe)
        elif len(actual_missing) == 1:
            missing_one.append({
                "recipe": recipe,
                "missing": list(actual_missing)[0]
            })
            
    return can_cook, missing_one