import streamlit as st
from logic import get_smart_recommendations, get_categorized_ingredients

st.set_page_config(page_title="SmartChef 3.0 全分类版", page_icon="👨‍🍳", layout="wide")

# --- 侧边栏样式优化 ---
st.sidebar.title("👨‍🍳 智能食材柜")
st.sidebar.info("请打开下方分类勾选你的食材：")

categorized_data = get_categorized_ingredients()
user_selections = []

if categorized_data:
    # 按照我们定义的 6 大类进行渲染
    for cat_name, items in categorized_data.items():
        if items: # 只显示有内容的分类
            with st.sidebar.expander(cat_name, expanded=(cat_name == "🥩 肉类")):
                # 使用 checkbox 或者 multiselect。多选框在分类里更高效
                picked = st.multiselect(
                    f"选择{cat_name}", 
                    items, 
                    key=f"select_{cat_name}",
                    label_visibility="collapsed"
                )
                user_selections.extend(picked)

    st.sidebar.markdown("---")
    if st.sidebar.button("🍳 开始智能配菜", use_container_width=True, type="primary"):
        if not user_selections:
            st.sidebar.warning("请至少选一样食材！")
        else:
            st.session_state.do_match = True
    else:
        if 'do_match' not in st.session_state:
            st.session_state.do_match = False

# --- 主界面结果展示 ---
st.title("🍲 你的私人大厨推荐")

if st.session_state.do_match and user_selections:
    st.write(f"已选食材：{', '.join([f'**{i}**' for i in user_selections])}")
    results = get_smart_recommendations(user_selections)
    
    if not results:
        st.error("这些食材太有个性了，凑不出一道菜，建议多选两样配料？")
    else:
        for item in results:
            recipe = item['recipe']
            score = item['score']
            color = "green" if score >= 80 else "orange" if score >= 40 else "gray"
            
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"### :{color}[{recipe['name']}]  `匹配度: {score}%`")
                    st.write(f"🕒 **耗时**: {recipe.get('time')}min | 📊 **难度**: {recipe.get('difficulty')}")
                    if item['missing']:
                        st.write(f"🛒 **缺货**: {', '.join(item['missing'])}")
                    else:
                        st.write("✅ **食材完美契合！**")
                    
                    with st.expander("📖 查看做菜步骤"):
                        st.write(recipe.get('instructions'))
                with c2:
                    st.progress(score / 100)
                st.write("") 
else:
    st.info("👈 请从左侧勾选你现有的食材，开启你的美食发现之旅。")