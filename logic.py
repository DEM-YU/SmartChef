import json

# 1. 定义需要忽略的“非核心”项：这些项不出现在勾选框，也不参与匹配分计算
IGNORE_ITEMS = [
    "葱", "姜", "蒜", "辣椒", "花椒", "八角", "香叶", "孜然", "芝麻", 
    "酱", "油", "盐", "醋", "糖", "蚝油", "生抽", "老抽", "豉油", 
    "料酒", "咖喱", "黑胡椒", "可乐", "啤酒", "冰糖", "蜂蜜", "香菜", 
    "九层塔", "枸杞", "红枣", "味精", "鸡精", "豆豉", "豆瓣酱", "番茄酱", 
    "淀粉", "牙签", "水", "温水", "开水", "保鲜膜", "竹签", "海鲜酱"
]

def is_ignore(name):
    """检查是否为调料或工具"""
    return any(key in name for key in IGNORE_ITEMS)

def get_categorized_ingredients():
    """动态分类：100% 自动分拣 50+ 菜谱中的核心食材"""
    categories_map = {
        "🥩 肉类": ["肉", "排骨", "鸡", "鸭", "羊", "牛", "里脊", "五花", "瘦肉", "培根", "香肠", "火腿", "蹄"],
        "🥬 蔬菜": ["菜", "土豆", "茄", "椒", "胡萝卜", "洋葱", "黄瓜", "苦瓜", "冬瓜", "丝瓜", "莲藕", "蒜苗", "蒜苔", "韭菜", "蘑菇", "菌", "笋", "芹菜", "西兰花", "百合", "豆芽", "木耳", "银耳", "西红柿", "番茄", "金针菇"],
        "🐟 海鲜": ["鱼", "虾", "鱿", "蟹", "海鲜", "鲈鱼", "草鱼", "鲫鱼", "鱼片"],
        "🍚 主食/粉面": ["米", "面", "粉", "面条", "意面", "通心粉", "红薯", "玉米"],
        "🥚 蛋奶豆制品": ["蛋", "豆腐", "豆", "皮蛋", "腐竹", "香干", "奶", "黄油", "芝士"]
    }
    
    categorized = {cat: [] for cat in categories_map.keys()}
    
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            for r in recipes:
                for ing in r.get('ingredients', []):
                    name = ing['name'].strip()
                    # 如果不是调料或工具，则进行分类归口
                    if not is_ignore(name):
                        for cat, keywords in categories_map.items():
                            if any(key in name for key in keywords):
                                categorized[cat].append(name)
                                break
        for cat in categorized:
            categorized[cat] = sorted(list(set(categorized[cat])))
        return categorized
    except: return {}

def get_smart_recommendations(user_ingredients):
    """匹配算法：调料和工具不扣分，核心食材缺失则惩罚"""
    recommendations = []
    user_set = set([str(i).strip() for i in user_ingredients])

    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            
        for recipe in recipes:
            total_weight, match_weight = 0, 0
            has_any_main = False   
            missing_items, seasonings_tools = [], []
            
            for ing in recipe.get('ingredients', []):
                name = ing['name'].strip()
                
                # 情况A：调料/工具 -> 记录但不参与评分
                if is_ignore(name):
                    seasonings_tools.append(name)
                    continue
                
                # 情况B：核心食材 -> 参与匹配度计算
                is_main = (ing.get('type') == 'main')
                weight = 4 if is_main else 1
                total_weight += weight
                
                if name in user_set:
                    match_weight += weight
                    if is_main: has_any_main = True
                else:
                    missing_items.append(name)
            
            # 只有拥有至少一个主料才推荐
            score = int((match_weight / total_weight) * 100) if has_any_main and total_weight > 0 else 0
            
            if score >= 15:
                recommendations.append({
                    "recipe": recipe,
                    "score": score,
                    "missing": missing_items,
                    "others": seasonings_tools # 调料单传给前端
                })
        recommendations.sort(key=lambda x: x['score'], reverse=True)
    except: pass
    return recommendations