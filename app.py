import streamlit as st
from logic import get_smart_recommendations

st.set_page_config(page_title="SmartChef 2.0 智能版", page_icon="🍲", layout="wide")

st.title("🍲 SmartChef 智能菜谱匹配")
st.caption("基于食材权重排序：主料匹配度越高，排名越靠前。")

# --- 侧边栏：食材选择 ---
st.sidebar.header("🧊 我的冰箱里有...")
# 这里可以根据你的 recipes.json 动态生成，或者手动列出
all_ingredients = ["西红柿", "鸡蛋", "牛肉", "土豆", "猪肉", "青椒", "白菜", "小葱", "洋葱", "胡萝卜"]
selected_items = st.sidebar.multiselect("点击添加食材:", all_ingredients)

if st.sidebar.button("开始智能匹配", use_container_width=True):
    if not selected_items:
        st.warning("你还没选食材呢，大厨没法开火呀！")
    else:
        results = get_smart_recommendations(selected_items)
        
        if not results:
            st.error("哎呀，选的食材太冷门了，我的菜谱库里找不到相关的。")
        else:
            st.subheader(f"根据你的食材，我们找到了 {len(results)} 个方案：")
            
            # 循环显示结果
            for item in results:
                recipe = item['recipe']
                score = item['score']
                
                # 根据分数决定颜色
                color = "green" if score >= 80 else "orange" if score >= 40 else "gray"
                
                with st.container():
                    col_info, col_chart = st.columns([3, 1])
                    with col_info:
                        st.markdown(f"### :{color}[{recipe['name']}]")
                        st.write(f"⏱️ 预计耗时: {recipe.get('time', '--')} 分钟")
                        
                        if item['missing']:
                            st.write(f"🛒 还缺: {', '.join(item['missing'])}")
                        else:
                            st.write("✨ 食材全齐了！完美！")
                    
                    with col_chart:
                        st.write(f"匹配度: {score}%")
                        st.progress(score / 100)
                    
                    st.divider()