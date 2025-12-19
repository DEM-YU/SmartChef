import logic
import json
import os

def test_matching():
    # Load real recipes
    recipes = logic.load_recipes()
    print(f"Loaded {len(recipes)} recipes.")
    
    # Test Case 1: Tomato Eggs (User has Tomato, Eggs -> Misses Seasonings)
    # West tomatoes Scrambled Eggs needs: Egg, Tomato, Oil, Salt, Scallion, Sugar
    # 'Egg' and 'Tomato' are mains. Others are 'Seeasoning'
    user_ing_1 = ["西红柿", "鸡蛋"]
    can_cook_1, missing_one_1 = logic.get_recommendations(user_ing_1, recipes)
    
    print("\n--- Test Case 1: [Tomato, Egg] ---")
    matched_names = [r['name'] for r in can_cook_1]
    print(f"Can Cook: {matched_names}")
    
    assert "西红柿炒鸡蛋" in matched_names, "Should be able to cook Tomato Eggs (missing only seasonings)"
    
    # Check if it correctly identifies missing seasonings
    te_recipe = next(r for r in can_cook_1 if r['name'] == "西红柿炒鸡蛋")
    print(f"Missing Seasonings for Tomato Eggs: {te_recipe['missing_seasoning']}")
    assert len(te_recipe['missing_seasoning']) > 0, "Should have missing seasonings"
    assert "食用油" in te_recipe['missing_seasoning']

    # Test Case 2: Only Tomato (Missing Egg - Main)
    user_ing_2 = ["西红柿"]
    can_cook_2, missing_one_2 = logic.get_recommendations(user_ing_2, recipes)
    
    print("\n--- Test Case 2: [Tomato] ---")
    partial_names = [r['name'] for r in missing_one_2]
    print(f"Missing One: {partial_names}")
    
    assert "西红柿炒鸡蛋" in partial_names, "Should be partial match for Tomato Eggs"
    te_partial = next(r for r in missing_one_2 if r['name'] == "西红柿炒鸡蛋")
    print(f"Missing Ingredient: {te_partial['missing_ingredient']}")
    assert te_partial['missing_ingredient'] == "鸡蛋", "Should be missing Egg"
    
    print("\nSUCCESS: All logic verification tests passed!")

if __name__ == "__main__":
    test_matching()
