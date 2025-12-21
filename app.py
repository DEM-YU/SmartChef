import streamlit as st
from logic import get_recommendations, call_ai_chef

st.set_page_config(page_title="SmartChef AI", page_icon="👨‍🍳", layout="wide")

st.title("👨‍🍳 SmartChef AI: 你的私人智能大厨")
st.markdown("---")

# 1. 食材分类字典 (你可以根据需要继续添加)
categories = {
    "🥩 肉类": ["牛肉", "猪肉", "羊肉", "鸡肉", "五花肉", "培根"],
    "🥬 蔬菜": ["白菜", "菠菜", "西红柿", "土豆", "青椒", "西兰花", "茄子", "洋葱", "胡萝卜"],
    "🦐 水产": ["大虾", "鱼片", "螃蟹", "鱿鱼"],
    "🥚 蛋奶豆制品": ["鸡蛋", "豆腐", "奶酪"]
}

# 2. 侧边栏或主界面选择
st.sidebar.header("🛒 冰箱里有什么？")
selected_items = []
for cat, items in categories.items():
    picked = st.sidebar.multiselect(f"{cat}", items)
    selected_items.extend(picked)

# 3. 匹配逻辑
if st.sidebar.button("🚀 开始匹配菜谱", use_container_width=True):
    if not selected_items:
        st.warning("请先在左侧勾选一些食材哦！")
    else:
        # 第一部分：本地数据库结果
        st.header("🍱 本地经典菜谱")
        can_cook, missing_one = get_recommendations(selected_items)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ 现在就能做")
            if can_cook:
                for recipe in can_cook:
                    with st.expander(f"📖 {recipe['name']}"):
                        st.write(f"**难度:** {recipe.get('difficulty', '简单')}")
                        st.write(f"**耗时:** {recipe.get('time', '20')}min")
                        st.write(f"**所需食材:** {', '.join(recipe['ingredients'])}")
            else:
                st.info("本地库里暂时没有完全匹配的菜。")

        with col2:
            st.subheader("💡 差一点就能做")
            if missing_one:
                for item in missing_one:
                    recipe = item['recipe']
                    with st.expander(f"⚠️ {recipe['name']}"):
                        st.write(f"**只差这一样:** :red[{item['missing']}]")
                        st.write(f"**其他食材:** {', '.join(recipe['ingredients'])}")
            else:
                st.info("没有只差一样的菜谱。")

        # 第二部分：AI 创意生成 (重头戏)
        st.markdown("---")
        st.header("🤖 AI 大厨的突发奇想")
        with st.spinner('AI 正在翻看私房菜谱，请稍候...'):
            ai_suggestion = call_ai_chef(selected_items)
            st.success("创意菜谱生成成功！")
            st.markdown(ai_suggestion)
            st.balloons() # 撒花庆祝
else:
    st.info("请从左侧选择食材并点击“开始匹配”按钮。")