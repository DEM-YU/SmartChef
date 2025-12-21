import json

def get_categorized_ingredients():
    """
    【升级版】全覆盖分类逻辑：确保 50+ 菜谱中的每一个食材都有家可归。
    """
    # 建立极其详尽的关键字映射
    categories_map = {
        "🥩 肉类": ["肉", "排骨", "鸡", "鸭", "羊", "牛", "里脊", "五花", "瘦肉", "培根", "香肠", "火腿", "肝", "蹄"],
        "🥬 蔬菜": ["菜", "土豆", "茄", "椒", "胡萝卜", "洋葱", "黄瓜", "苦瓜", "冬瓜", "丝瓜", "莲藕", "蒜苗", "蒜苔", "韭菜", "蘑菇", "菌", "笋", "芹菜", "西兰花", "百合", "豆芽", "木耳", "银耳", "西红柿", "番茄"],
        "🐟 海鲜": ["鱼", "虾", "鱿", "蟹", "海鲜", "鲈鱼", "草鱼", "鲫鱼", "鱼片"],
        "🍚 主食/粉面": ["米", "面", "粉", "面条", "意面", "通心粉", "红薯", "玉米", "淀粉"],
        "🥚 蛋奶豆制品": ["蛋", "豆腐", "豆", "皮蛋", "腐竹", "香干", "奶", "黄油", "芝士"],
        "🧂 调料/香料/其他": ["葱", "姜", "蒜", "辣椒", "花椒", "八角", "香叶", "孜然", "芝麻", "酱", "油", "盐", "醋", "糖", "蚝油", "生抽", "老抽", "豉油", "料酒", "咖喱", "黑胡椒", "可乐", "啤酒", "冰糖", "蜂蜜", "香菜", "九层塔", "枸杞", "红枣"]
    }
    
    # 初始化分类容器
    categorized = {cat: [] for cat in categories_map.keys()}
    
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            all_ings = set()
            for r in recipes:
                for ing in r.get('ingredients', []):
                    all_ings.add(ing['name'].strip())
            
            # 核心分拣逻辑
            for ing_name in all_ings:
                found = False
                for cat, keywords in categories_map.items():
                    if any(key in ing_name for key in keywords):
                        categorized[cat].append(ing_name)
                        found = True
                        break
                
                # 如果依然没找到（保险措施），强行塞入“调料/其他”类，确保“其他”栏消失
                if not found:
                    categorized["🧂 调料/香料/其他"].append(ing_name)
                    
        # 组内排序
        for cat in categorized:
            categorized[cat] = sorted(list(set(categorized[cat])))
            
        return categorized
    except Exception:
        return {}

def get_smart_recommendations(user_ingredients):
    """
    【智能匹配】基于权重和缺失惩罚的匹配算法
    - 主料 (main): 4分
    - 辅料 (side): 1分
    """
    recommendations = []
    user_set = set([str(i).strip() for i in user_ingredients])

    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            
        for recipe in recipes:
            total_weight = 0
            match_weight = 0
            has_any_main = False   # 检查是否包含至少一个主料
            missing_main_count = 0  # 缺失的主料数量
            missing_items = []
            
            for ing in recipe.get('ingredients', []):
                is_main = (ing.get('type') == 'main')
                weight = 4 if is_main else 1
                total_weight += weight
                
                if ing['name'].strip() in user_set:
                    match_weight += weight
                    if is_main:
                        has_any_main = True
                else:
                    missing_items.append(ing['name'])
                    if is_main:
                        missing_main_count += 1
            
            # --- 智能得分计算 ---
            if not has_any_main:
                # 连一个主料都没有，直接判定为不匹配 (0分)
                score = 0
            else:
                base_score = (match_weight / total_weight) * 100
                # 【惩罚机制】每缺一个主料，匹配度得分直接减半
                # 例如：原本50分，缺1个主料变25，缺2个变12.5
                penalty = 0.5 ** missing_main_count
                score = int(base_score * penalty)
            
            # 只要得分超过 15分（说明有核心食材且缺失不多），就推荐
            if score >= 15:
                recommendations.append({
                    "recipe": recipe,
                    "score": score,
                    "missing": missing_items
                })
        
        # 按照匹配得分从高到低排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
    except Exception as e:
        print(f"匹配失败: {e}")
        
    return recommendations