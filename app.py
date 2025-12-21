import streamlit as st
from logic import get_recommendations

st.set_page_config(page_title="SmartChef 本地版", page_icon="👨‍🍳", layout="wide")

st.title("👨‍🍳 SmartChef: 你的冰箱管家")
st.markdown("---")

# 食材分类
categories = {
    "🥩 肉类": ["牛肉", "猪肉", "羊肉", "鸡肉", "五花肉", "培根"],
    "🥬 蔬菜": ["白菜", "菠菜", "西红柿", "土豆", "青椒", "西兰花", "茄子", "洋葱", "胡萝卜", "黄瓜"],
    "🦐 水产": ["大虾", "鱼片", "螃蟹", "鱿鱼"],
    "🥚 蛋奶豆制品": ["鸡蛋", "豆腐", "奶酪"]
}

st.sidebar.header("🛒 冰箱食材清单")
selected_items = []
for cat, items in categories.items():
    picked = st.sidebar.multiselect(f"{cat}", items)
    selected_items.extend(picked)

if st.sidebar.button("🚀 寻找匹配菜谱", use_container_width=True):
    if not selected_items:
        st.warning("请先在左侧勾选一些食材哦！")
    else:
        st.header("🍱 推荐菜谱结果")
        can_cook, missing_one = get_recommendations(selected_items)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ 现在就能做")
            if can_cook:
                for recipe in can_cook:
                    with st.expander(f"📖 {recipe['name']}"):
                        st.write(f"**难度:** {recipe.get('difficulty', '简单')}")
                        st.write(f"**耗时:** {recipe.get('time', '20')}min")
                        # 兼容显示食材列表
                        ing_names = [i['name'] if isinstance(i, dict) else i for i in recipe['ingredients']]
                        st.write(f"**清单:** {', '.join(ing_names)}")
            else:
                st.info("暂时没有完全匹配的菜谱。")

        with col2:
            st.subheader("💡 差一样食材")
            if missing_one:
                for item in missing_one:
                    recipe = item['recipe']
                    with st.expander(f"⚠️ {recipe['name']}"):
                        st.write(f"**只差:** :red[{item['missing']}]")
                        ing_names = [i['name'] if isinstance(i, dict) else i for i in recipe['ingredients']]
                        st.write(f"**清单:** {', '.join(ing_names)}")
            else:
                st.info("没有只差一样的菜谱。")
else:
    st.info("请从左侧选择食材并点击按钮开始匹配。")