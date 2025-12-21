import logic

def test_ai_fallback():
    print("Testing AI Fallback...")
    
    # recipes.json has common dishes. 
    # Let's pick an ingredient unlikely to have 3 matches to trigger AI.
    # Actually, we can just pass a dummy list of ingredients that won't match anything local exactly,
    # or just one ingredient that might match 1 or 2 things but < 3.
    
    user_ingredients = ["龙虾", "黄金", "钻石"] 
    # "龙虾" might not be in our simple json, "黄金" definitely isn't.
    
    can_cook, missing_one = logic.get_recommendations(user_ingredients, [], [])
    # Pass empty recipes_data? No, we need to load real recipes to ensure they DON'T match.
    
    recipes_data = logic.load_recipes()
    can_cook, missing_one = logic.get_recommendations(user_ingredients, [], recipes_data)
    
    print(f"Found {len(can_cook)} 'can_cook' recipes.")
    
    found_ai = False
    for r in can_cook:
        print(f"- {r['name']} (Category: {r.get('category')})")
        if r.get('is_ai_generated'):
            found_ai = True
            print("  [Confirmed AI Recipe]")
            print(f"  Description: {r.get('description')}")
            
    if found_ai:
        print("SUCCESS: AI Chef was triggered.")
    else:
        print("FAILURE: AI Chef was NOT triggered.")

if __name__ == "__main__":
    test_ai_fallback()
