import json

# 定义哪些属于“调料/香料”
SEASONING_KEYWORDS = [
    "葱", "姜", "蒜", "辣椒", "花椒", "八角", "香叶", "孜然", "芝麻", 
    "酱", "油", "盐", "醋", "糖", "蚝油", "生抽", "老抽", "豉油", 
    "料酒", "咖喱", "黑胡椒", "可乐", "啤酒", "冰糖", "蜂蜜", "香菜", 
    "九层塔", "枸杞", "红枣", "味精", "鸡精", "豆豉", "豆瓣酱", "番茄酱", "淀粉"
]

def is_seasoning(name):
    return any(key in name for key in SEASONING_KEYWORDS)

def get_categorized_ingredients():
    """分类展示：剔除所有调料项"""
    categories_map = {
        "🥩 肉类": ["肉", "排骨", "鸡", "鸭", "羊", "牛", "里脊", "五花", "瘦肉", "培根", "香肠", "火腿", "肝", "蹄"],
        "🥬 蔬菜": ["菜", "土豆", "茄", "椒", "胡萝卜", "洋葱", "黄瓜", "苦瓜", "冬瓜", "丝瓜", "莲藕", "蒜苗", "蒜苔", "韭菜", "蘑菇", "菌", "笋", "芹菜", "西兰花", "百合", "豆芽", "木耳", "银耳", "西红柿", "番茄"],
        "🐟 海鲜": ["鱼", "虾", "鱿", "蟹", "海鲜", "鲈鱼", "草鱼", "鲫鱼", "鱼片"],
        "🍚 主食/粉面": ["米", "面", "粉", "面条", "意面", "通心粉", "红薯", "玉米"],
        "🥚 蛋奶豆制品": ["蛋", "豆腐", "豆", "皮蛋", "腐竹", "香干", "奶", "黄油", "芝士"]
    }
    
    categorized = {cat: [] for cat in categories_map.keys()}
    
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            all_ings = set()
            for r in recipes:
                for ing in r.get('ingredients', []):
                    name = ing['name'].strip()
                    # 关键修改：如果是调料，直接跳过，不给用户选
                    if not is_seasoning(name):
                        all_ings.add(name)
            
            for ing_name in all_ings:
                for cat, keywords in categories_map.items():
                    if any(key in ing_name for key in keywords):
                        categorized[cat].append(ing_name)
                        break
        
        for cat in categorized:
            categorized[cat] = sorted(list(set(categorized[cat])))
        return categorized
    except Exception: return {}

def get_smart_recommendations(user_ingredients):
    """智能匹配：调料不计入缺失，不参与评分"""
    recommendations = []
    user_set = set([str(i).strip() for i in user_ingredients])

    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            
        for recipe in recipes:
            total_weight = 0
            match_weight = 0
            has_any_main = False   
            missing_items = []
            required_seasonings = [] # 专门存放调料
            
            for ing in recipe.get('ingredients', []):
                name = ing['name'].strip()
                
                # 如果是调料：归类到调料区，不参与评分计算
                if is_seasoning(name):
                    required_seasonings.append(name)
                    continue 
                
                # 如果是硬核食材：
                is_main = (ing.get('type') == 'main')
                weight = 4 if is_main else 1
                total_weight += weight
                
                if name in user_set:
                    match_weight += weight
                    if is_main: has_any_main = True
                else:
                    missing_items.append(name)
            
            if not has_any_main:
                score = 0
            else:
                score = int((match_weight / total_weight) * 100) if total_weight > 0 else 0
            
            if score >= 15:
                recommendations.append({
                    "recipe": recipe,
                    "score": score,
                    "missing": missing_items,
                    "seasonings": required_seasonings # 传给前端显示
                })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
    except Exception: pass
    return recommendations