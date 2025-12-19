import streamlit as st
import logic

# Page Configuration
st.set_page_config(page_title="我的智能厨房", page_icon="🍳")

# Title
st.title("🍳 我的智能厨房")

# Load Recipes Once
recipes = logic.load_recipes()

# Extract Ingredients for Selection
all_ingredients_set = set()
for recipe in recipes:
    for ing_obj in recipe.get('ingredients', []):
        all_ingredients_set.add(ing_obj.get('name', '').strip())

# --- Ingredient Library ---
# Defined based on common household items and recipe needs
INGREDIENTS_DB = {
    "🥩 肉类": ["猪肉", "牛肉", "羊肉", "鸡肉", "鸭肉", "五花肉", "排骨", "培根", "猪里脊肉", "鸡胸肉", "猪肉末", "猪肉片"],
    "🥬 蔬菜": ["白菜", "菠菜", "西红柿", "土豆", "青椒", "西兰花", "洋葱", "胡萝卜", "茄子", "木耳", "黄瓜", "包菜", "红椒", "大葱", "葱", "姜", "蒜", "香菜"],
    "🐟 水产": ["大虾", "鱼片", "螃蟹", "鱿鱼", "蛤蜊", "鲫鱼", "咸鱼"],
    "🥚 蛋/豆制品": ["鸡蛋", "豆腐", "嫩豆腐", "牛奶", "奶酪", "腐竹"]
}

# --- Sidebar / Main Selection Area ---
st.markdown("### 🛒 请选择你冰箱里的食材")

selected_meat = st.multiselect("🥩 肉类 (Meat)", INGREDIENTS_DB["🥩 肉类"])
selected_veg = st.multiselect("🥬 蔬菜 (Vegetable)", INGREDIENTS_DB["🥬 蔬菜"])
selected_sea = st.multiselect("🐟 水产 (Seafood)", INGREDIENTS_DB["🐟 水产"])
selected_egg = st.multiselect("🥚 蛋/豆制品 (Egg/Soy)", INGREDIENTS_DB["🥚 蛋/豆制品"])

# Aggregate all selections
final_ingredients = selected_meat + selected_veg + selected_sea + selected_egg

# Matching Logic
if st.button("开始匹配"):
    if not final_ingredients:
        st.warning("请至少选择一种食材！")
    else:
        # Pass empty list for categories since we are doing specific matching now
        # logic.get_recommendations(user_specifics, user_categories, recipes)
        can_cook, missing_one = logic.get_recommendations(final_ingredients, [], recipes)
        
        if not can_cook and not missing_one:
            st.warning("冰箱空空如也，去买点菜吧")
        else:
            # --- 1. Full Match Section ---
            if can_cook:
                st.markdown("## 🍲 可以直接做的菜")
                st.success("🎉 食材准备就绪，马上开动！")
                
                # Create a grid for cards
                cols = st.columns(3)
                for idx, recipe in enumerate(can_cook):
                    with cols[idx % 3]:
                        # Card Container (using simplified styling since border=True is newer, 
                        # but standard markdown works everywhere)
                        with st.container():
                            st.markdown(f"### {recipe['name']}")
                            
                            # Difficulty & Time
                            diff_icon = "⭐" if recipe.get('difficulty') == "简单" else "⭐⭐" if recipe.get('difficulty') == "中等" else "⭐⭐⭐"
                            time_val = recipe.get('time', '??')
                            st.caption(f"⏱️ {time_val} min | {diff_icon} {recipe.get('difficulty', '未知')}")
                            
                            # Category Tag
                            cat = recipe.get('category', '其他')
                            st.markdown(f"**🏷️ {cat}**")
                            
                            # Missing Seasonings Feedback
                            missing_seasoning = recipe.get('missing_seasoning', [])
                            if missing_seasoning:
                                st.markdown(f"<span style='color:orange'>缺少调料: {', '.join(missing_seasoning)}</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("<span style='color:green'>✅ 食材齐全</span>", unsafe_allow_html=True)
                            
                            st.divider()

            # --- 2. Partial Match Section ---
            if missing_one:
                st.markdown("---")  # Gray divider
                st.markdown("## 🛒 差一点就能做")
                st.info("💡 只差一样主料，去楼下便利店补个货？")
                
                cols_missing = st.columns(3)
                for idx, recipe in enumerate(missing_one):
                    with cols_missing[idx % 3]:
                        with st.container():
                            st.markdown(f"### {recipe['name']}")
                            
                            # Difficulty & Time
                            diff_icon = "⭐" if recipe.get('difficulty') == "简单" else "⭐⭐" if recipe.get('difficulty') == "中等" else "⭐⭐⭐"
                            time_val = recipe.get('time', '??')
                            st.caption(f"⏱️ {time_val} min | {diff_icon} {recipe.get('difficulty', '未知')}")
                            
                            # Category Tag
                            cat = recipe.get('category', '其他')
                            st.markdown(f"**🏷️ {cat}**")
                            
                            # Missing Ingredient
                            missing_ing = recipe.get('missing_ingredient', '未知食材')
                            st.markdown(f"🛑 <span style='color:red'>缺: **{missing_ing}**</span>", unsafe_allow_html=True)
                            
                            st.divider()
