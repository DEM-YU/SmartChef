import streamlit as st
from logic import get_smart_recommendations, get_categorized_ingredients

st.set_page_config(page_title="SmartChef 4.0 Pro", page_icon="👨‍🍳", layout="wide")

# --- Sidebar: Ingredient Selection ---
st.sidebar.title("👨‍🍳 Ingredient Cabinet")
st.sidebar.info("Select the **core ingredients** you have:")

categorized_data = get_categorized_ingredients()
user_selections = []

if categorized_data:
    for cat_name, items in categorized_data.items():
        if items:
            with st.sidebar.expander(cat_name, expanded=(cat_name == "🥩 Meat")):
                picked = st.multiselect(f"Select {cat_name}", items, key=f"s_{cat_name}", label_visibility="collapsed")
                user_selections.extend(picked)

    st.sidebar.markdown("---")
    match_btn = st.sidebar.button("🚀 Find Recipes", use_container_width=True, type="primary")
else:
    match_btn = False

# --- Main Page: Results ---
st.title("🍲 Smart Recipe Matcher")

if match_btn and user_selections:
    results = get_smart_recommendations(user_selections)
    
    if not results:
        st.error("No recipes found for these ingredients.")
    else:
        st.write(f"🔍 Selected Ingredients: {', '.join([f'**{i}**' for i in user_selections])}")
        
        for item in results:
            recipe = item['recipe']
            score = item['score']
            color = "green" if score >= 80 else "orange" if score >= 40 else "red"
            
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"### :{color}[{recipe['name']}]  `(Match: {score}%)`")
                    
                    if item['missing']:
                        missing_str = ", ".join([f"**{m}**" for m in item['missing']])
                        st.markdown(f"❌ **Missing**: :red[{missing_str}]")
                    else:
                        st.markdown("✅ **All core ingredients ready!**")
                    
                    if item['others']:
                        st.markdown(f"🧂 **Pantry Staples**: {', '.join(item['others'])}")
                    
                    with st.expander("📖 View Cooking Steps"):
                        st.info(recipe.get('instructions', 'No instructions provided.'))
                
                with c2:
                    st.progress(score / 100)
                    st.caption(f"📊 Difficulty: {recipe.get('difficulty')} | ⏱️ {recipe.get('time')}min")
else:
    st.info("👈 Select ingredients from the sidebar to see what you can cook today!")