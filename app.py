import streamlit as st
from logic import get_smart_recommendations, get_all_ingredients_from_data

st.set_page_config(page_title="SmartChef 2.0 智能版", page_icon="🍲", layout="wide")

# 侧边栏：动态提取 100 道菜的所有食材
st.sidebar.header("🧊 我的冰箱里有...")
available_ings = get_all_ingredients_from_data()

if available_ings:
    selected_items = st.sidebar.multiselect(
        "搜索并添加食材:", 
        available_ings,
        help="支持输入关键词搜索，如'肉'、'土豆'"
    )
    
    match_btn = st.sidebar.button("🚀 开始智能匹配", use_container_width=True)
else:
    st.sidebar.error("请先确保 recipes.json 中有数据")
    match_btn = False

# 主界面显示
st.title("🍲 SmartChef 智能匹配系统")
st.markdown("---")

if match_btn:
    if not selected_items:
        st.warning("大厨，请先在左侧选点食材吧！")
    else:
        results = get_smart_recommendations(selected_items)
        
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