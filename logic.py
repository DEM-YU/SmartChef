import json
import os
import random  # Added for AI simulation

def load_recipes():
    """
    Load recipes from recipes.json.
    """
    # Assuming recipes.json is in the same directory as logic.py
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'recipes.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: recipes.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error: recipes.json is not valid JSON.")
        return []

def ask_ai_chef(ingredients):
    """
    Simulate an AI Chef that creates a creative recipe based on provided ingredients.
    This acts as a fallback when local matches are insufficient.
    
    Prompt Concept: "You are a senior chef... [List]"
    """
    # In a real scenario, this would call an API (e.g., OpenAI, Gemini).
    # Here we simulate the response structure.
    
    # Constructing a 'creative' name
    main_ing = ingredients[0] if ingredients else "神秘食材"
    creative_names = [
        f"五星级{main_ing}特调",
        f"甚至不用火的{main_ing}料理",
        f"AI大厨的{main_ing}狂想曲",
        f"未来派{main_ing}盖饭"
    ]
    
    recipe_name = random.choice(creative_names)
    
    # Return a recipe object matching recipes.json structure
    return {
        "name": recipe_name,
        "category": "AI 创意菜",
        "difficulty": "未知",
        "time": "??",
        "ingredients": [{"name": ing, "tag": "AI配料"} for ing in ingredients],
        "missing_seasoning": [],
        "missing_critical": [], 
        "is_ai_generated": True,
        "description": f"（AI模拟响应）这里是为您定制的{recipe_name}烹饪逻辑：\n1. 准备好{', '.join(ingredients)}\n2. 发挥你的想象力，大火爆炒！\n3. 出锅！"
    }

def get_recommendations(user_ingredients, user_categories, recipes_data):
    """
    Recommend recipes based on user ingredients and category wildcards.
    
    Args:
        user_ingredients (list): List of specific ingredient names user has.
        user_categories (list): List of category tags user has (e.g., "肉类", "蔬菜").
        recipes_data (list): List of recipe dictionaries loaded from JSON.
        
    Returns:
        tuple: (can_cook, missing_one)
            can_cook: List of recipes where all MAIN ingredients are present (via specific or category match).
            missing_one: List of recipes missing exactly one MAIN ingredient.
    """
    # Normalize user ingredients
    normalized_user_ingredients = [ing.strip() for ing in user_ingredients if ing.strip()]
    normalized_user_categories = [cat.strip() for cat in user_categories if cat.strip()]
    
    can_cook = []
    missing_one = []
    
    for recipe in recipes_data:
        recipe_ingredients = recipe.get('ingredients', [])
        
        missing_critical = []
        missing_seasoning = []
        
        for r_ing in recipe_ingredients:
            ing_name = r_ing.get('name', '').strip()
            ing_tag = r_ing.get('tag', '')
            
            found = False
            
            # Check specific ingredients (Fuzzy match)
            for u_ing in normalized_user_ingredients:
                if u_ing in ing_name or ing_name in u_ing:
                    found = True
                    break
            
            # Check category wildcard
            # If the ingredient's tag is in the user's selected categories, it counts as found
            if not found and ing_tag in normalized_user_categories:
                found = True
            
            if not found:
                if ing_tag == '调料':
                    missing_seasoning.append(ing_name)
                else:
                    missing_critical.append(ing_name)
        
        # Logic Decision
        recipe_result = recipe.copy()
        recipe_result['missing_seasoning'] = missing_seasoning
        recipe_result['missing_critical'] = missing_critical
        
    
        if len(missing_critical) == 0:
            # Full match (seasonings optional)
            can_cook.append(recipe_result)
        elif len(missing_critical) == 1:
            # Partial match (missing 1 main ingredient)
            recipe_result['missing_ingredient'] = missing_critical[0] 
            missing_one.append(recipe_result)
            
    # --- AI Implementation ---
    # If matches are fewer than 3, call AI Chef
    if len(can_cook) < 3 and normalized_user_ingredients:
        ai_recipe = ask_ai_chef(normalized_user_ingredients)
        can_cook.append(ai_recipe)
            
    return can_cook, missing_one
