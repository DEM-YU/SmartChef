import json

def get_all_ingredients_from_data():
    """
    【动态提取】扫描 recipes.json 中所有菜谱，
    提取出所有不重复的食材名称，供前端 multiselect 使用。
    """
    all_ings = set()
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            for recipe in recipes:
                for ing in recipe.get('ingredients', []):
                    # 自动提取每一个食材的名字并去重
                    all_ings.add(ing['name'].strip())
        return sorted(list(all_ings)) # 返回排序后的列表
    except Exception as e:
        print(f"提取食材失败: {e}")
        return []

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