import streamlit as st
from logic import get_smart_recommendations, get_categorized_ingredients

st.set_page_config(page_title="SmartChef 3.0 专业版", page_icon="👨‍🍳", layout="wide")

# --- 侧边栏：分类食材选择 ---
st.sidebar.header("🛒 准备食材")
st.sidebar.markdown("请在下方分类中勾选您拥有的食材：")

categorized_data = get_categorized_ingredients()
user_selections = []

if categorized_data:
    # 遍历每个分类，创建折叠选单
    for cat_name, items in categorized_data.items():
        if items: # 如果该分类下有食材
            with st.sidebar.expander(cat_name, expanded=False):
                # 在每个分类下使用 multiselect
                picked = st.multiselect(f"选择{cat_name}", items, key=cat_name, label_visibility="collapsed")
                user_selections.extend(picked)

    st.sidebar.markdown("---")
    match_btn = st.sidebar.button("🚀 寻找今日菜谱", use_container_width=True)
else:
    st.sidebar.error("数据加载失败，请检查 recipes.json")
    match_btn = False

# --- 主界面 ---
st.title("👨‍🍳 SmartChef: 智能食材管家")
if user_selections:
    st.info(f"当前已选: {', '.join(user_selections)}")

if match_btn:
    if not user_selections:
        st.warning("大厨，请先在左侧选点食材吧！")
    else:
        results = get_smart_recommendations(user_selections)
        
        if not results:
            st.error("抱歉，目前没有找到匹配的菜谱，换几种食材试试？")
        else:
            st.subheader(f"🔍 为您精选了 {len(results)} 道菜谱：")
            
            for item in results:
                recipe = item['recipe']
                score = item['score']
                
                # 颜色区分匹配度
                color = "green" if score >= 80 else "orange" if score >= 40 else "gray"
                
                with st.container():
                    col_info, col_chart = st.columns([3, 1])
                    with col_info:
                        st.markdown(f"### :{color}[{recipe['name']}]")
                        st.caption(f"难度: {recipe.get('difficulty','简单')} | 耗时: {recipe.get('time','--')}min")
                        
                        if item['missing']:
                            st.write(f"🛒 **还缺:** {', '.join(item['missing'])}")
                        else:
                            st.write("✨ **食材全齐了！现在就能做。**")
                        
                        with st.expander("查看烹饪步骤"):
                            st.info(recipe.get('instructions', '暂无具体步骤描述。'))
                    
                    with col_chart:
                        st.write(f"匹配度: {score}%")
                        st.progress(score / 100)
                    
                    st.divider()
else:
    # 初始状态引导
    st.info("👈 请在左侧勾选你现有的食材，点击按钮看看今天能吃什么！")