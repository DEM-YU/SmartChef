import streamlit as st
from logic import get_smart_recommendations, get_categorized_ingredients

st.set_page_config(page_title="SmartChef 4.0 厨师专业版", page_icon="👨‍🍳", layout="wide")

# --- 侧边栏：分类选择核心食材 ---
st.sidebar.title("👨‍🍳 智能食材柜")
st.sidebar.info("请勾选现有的**核心食材**：")

categorized_data = get_categorized_ingredients()
user_selections = []

if categorized_data:
    for cat_name, items in categorized_data.items():
        if items:
            with st.sidebar.expander(cat_name, expanded=(cat_name == "🥩 肉类")):
                picked = st.multiselect(f"选择{cat_name}", items, key=f"s_{cat_name}", label_visibility="collapsed")
                user_selections.extend(picked)

    st.sidebar.markdown("---")
    match_btn = st.sidebar.button("🚀 寻找今日菜谱", use_container_width=True, type="primary")
else:
    match_btn = False

# --- 主界面：结果渲染 ---
st.title("🍲 冰箱食材精准匹配")

if match_btn and user_selections:
    results = get_smart_recommendations(user_selections)
    
    if not results:
        st.error("抱歉，现有食材无法匹配到任何菜谱。")
    else:
        st.write(f"🔍 已选核心食材：{', '.join([f'**{i}**' for i in user_selections])}")
        
        for item in results:
            recipe = item['recipe']
            score = item['score']
            color = "green" if score >= 80 else "orange" if score >= 40 else "red"
            
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"### :{color}[{recipe['name']}]  `(匹配度: {score}%)`")
                    
                    # 修复渲染 Bug：使用 markdown 渲染颜色
                    if item['missing']:
                        missing_str = ", ".join([f"**{m}**" for m in item['missing']])
                        st.markdown(f"❌ **缺少核心料**: :red[{missing_str}]")
                    else:
                        st.markdown("✅ **核心食材已齐全！**")
                    
                    # 独立展示调料/工具
                    if item['others']:
                        st.markdown(f"🧂 **自备调料/工具**: {', '.join(item['others'])}")
                    
                    with st.expander("📖 查看做菜步骤"):
                        st.info(recipe.get('instructions', '暂无详细步骤。'))
                
                with c2:
                    st.progress(score / 100)
                    st.caption(f"📊 难度: {recipe.get('difficulty')} | ⏱️ {recipe.get('time')}min")
else:
    st.info("👈 请从左侧分类中勾选冰箱里的食材，大厨将为你即刻配菜。")