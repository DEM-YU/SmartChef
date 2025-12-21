import json

def get_smart_recommendations(user_ingredients):
    """
    智能加权匹配算法：
    - 主料 (main): 4分
    - 辅料 (side): 1分
    """
    recommendations = []
    # 清理用户输入的空格
    user_set = set([str(i).strip() for i in user_ingredients])

    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            
        for recipe in recipes:
            total_weight = 0
            match_weight = 0
            missing_items = []
            
            # 处理菜谱中的每一个食材
            for ing in recipe.get('ingredients', []):
                # 设定权重：如果是主料给4分，辅料给1分
                # 如果JSON里没写type，默认按主料处理
                weight = 4 if ing.get('type') == 'main' else 1
                total_weight += weight
                
                if ing['name'].strip() in user_set:
                    match_weight += weight
                else:
                    missing_items.append(ing['name'])
            
            # 计算匹配百分比得分 (0-100)
            score = int((match_weight / total_weight) * 100) if total_weight > 0 else 0
            
            # 只要得分大于 0，就显示（即便只中了一样辅料）
            if score > 0:
                recommendations.append({
                    "recipe": recipe,
                    "score": score,
                    "missing": missing_items
                })
        
        # 核心：按照分值从高到低排序，分高者排在最上面
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
    except Exception as e:
        print(f"读取数据失败: {e}")
        
    return recommendations