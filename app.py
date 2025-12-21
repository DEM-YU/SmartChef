import streamlit as st
from logic import get_smart_recommendations, get_categorized_ingredients

st.set_page_config(page_title="SmartChef 4.0 厨师专业版", page_icon="🍳", layout="wide")

# --- 侧边栏 ---
st.sidebar.title("🍳 智能食材柜")
st.sidebar.info("勾选你拥有的**核心食材**（调料默认已有）：")

categorized_data = get_categorized_ingredients()
user_selections = []

if categorized_data:
    for cat_name, items in categorized_data.items():
        if items:
            with st.sidebar.expander(cat_name, expanded=(cat_name == "🥩 肉类")):
                picked = st.multiselect(f"选择{cat_name}", items, key=f"s_{cat_name}", label_visibility="collapsed")
                user_selections.extend(picked)

    st.sidebar.markdown("---")
    match_btn = st.sidebar.button("👨‍🍳 开始配菜", use_container_width=True, type="primary")
else:
    match_btn = False

# --- 主界面 ---
st.title("🍲 冰箱食材匹配结果")

if match_btn and user_selections:
    results = get_smart_recommendations(user_selections)
    
    if not results:
        st.error("没找到匹配的菜谱。")
    else:
        for item in results:
            recipe = item['recipe']
            score = item['score']
            color = "green" if score >= 85 else "orange" if score >= 40 else "gray"
            
            with st.container(border=True):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"### :{color}[{recipe['name']}]")
                    
                    # 第一行：显示缺少的硬核食材
                    if item['missing']:
                        st.write(f"🚫 **还缺硬菜**: {', '.join([f'`:red[{m}]`' for m in item['missing']])}")
                    else:
                        st.write("✅ **核心食材已找齐！**")
                    
                    # 第二行：旁边/下方写上需要的调料
                    if item['seasonings']:
                        st.markdown(f"🧂 **自备调料**: {', '.join(item['seasonings'])}")
                    
                    with st.expander("📖 查看步骤"):
                        st.write(recipe.get('instructions'))
                
                with c2:
                    st.write(f"匹配度: {score}%")
                    st.progress(score / 100)
                    st.caption(f"难度: {recipe.get('difficulty')} | 耗时: {recipe.get('time')}min")
else:
    st.info("👈 请从左侧勾选你现有的核心食材。")