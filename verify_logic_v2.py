import logic
import json
import os

def test_matching():
    # Load real recipes
    recipes = logic.load_recipes()
    print(f"Loaded {len(recipes)} recipes.")
    
    # Test Case 3: Mixed Match (Specific + Category)
    # Shredded Pork with Green Pepper (青椒肉丝): Pork (Meat), Pepper (Veg). Also Seasonings.
    # User has: 'Vegetable' (Category) + 'Pork' (Specific) -> Should FULL MATCH (ignoring seasonings)
    
    # Note: In recipes.json:
    # "猪里脊肉" is tag "肉类"
    # "青椒" is tag "蔬菜"
    
    print("\n--- Test Case 3: [Veg Category, Meat Category] for Green Pepper Pork ---")
    user_cats = ["肉类", "蔬菜"]
    user_specs = [] # Empty specifics
    
    can_cook, missing_one = logic.get_recommendations(user_specs, user_cats, recipes)
    matched_names = [r['name'] for r in can_cook]
    print(f"Can Cook with [Meat, Veg]: {matched_names}")
    
    assert "青椒肉丝" in matched_names, "Should match Green Pepper Pork with Meat+Veg categories"
    
    print("\n--- Test Case 4: [Tomato Specific, Meat Category] ---")
    # Tomato (Specific) + Meat (Category).
    # "西红柿炒鸡蛋" needs Tomato + Egg(Egg/Soy). Meat category shouldn't help with Egg.
    # Should partial match usage of Tomato.
    # "土豆烧牛肉": Beef(Meat) + Potato(Veg) + Carrot(Veg) + Onion(Veg).
    # If I only have Meat category... I'm missing Veg.
    
    user_cats_2 = ["肉类"]
    user_specs_2 = ["西红柿"]
    can_cook_2, missing_one_2 = logic.get_recommendations(user_specs_2, user_cats_2, recipes)
    
    print(f"\nUser has Meat + Tomato.")
    can_cook_names_2 = [r['name'] for r in can_cook_2]
    missing_one_names_2 = [r['name'] for r in missing_one_2]
    print(f"Can Cook: {can_cook_names_2}")
    print(f"Missing One: {missing_one_names_2}")
    
    # Tomato Scrambled Eggs:
    # Have: Tomato. Missing: Egg (Egg/Soy). Meat cat doesn't help.
    # Should be in Missing One (missing Egg).
    assert "西红柿炒鸡蛋" in missing_one_names_2, "Should match Tomato Eggs partially (missing Egg)"

    print("\n--- Test Case 5: [Tomato Specific, Meat Category] for Tomato Stir-fry Pork ---")
    # Added "西红柿炒肉片": Pork(Tag: Meat) + Tomato(Tag: Veg).
    # User: Meat + Tomato.
    # Should FULL match.
    
    assert "西红柿炒肉片" in can_cook_names_2, "Should FULL MATCH Tomato Stir-fry Pork with Meat Cat + Tomato Specific"

    print("\nSUCCESS: All mixed logic verification tests passed!")

if __name__ == "__main__":
    test_matching()
