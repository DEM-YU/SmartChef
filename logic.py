import json
import os

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
            
    return can_cook, missing_one
