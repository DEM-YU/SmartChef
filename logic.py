import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 加载环境变量
load_dotenv()

# 配置 Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_recommendations(user_ingredients):
    """本地数据库匹配逻辑 - 已兼容对象格式的 JSON"""
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
    except FileNotFoundError:
        return [], []

    # 处理用户输入的食材（确保是干净的字符串列表）
    user_set = set([str(i).strip() for i in user_ingredients])
    
    can_cook = []
    missing_one = []

    for recipe in recipes:
        # --- 核心修复部分 ---
        # 从 JSON 的字典对象中提取食材名称
        extracted_ingredients = []
        for ing in recipe['ingredients']:
            if isinstance(ing, dict):
                # 如果是字典，取 "name" 字段
                extracted_ingredients.append(ing.get('name', '').strip())
            else:
                # 如果是字符串，直接取值
                extracted_ingredients.append(str(ing).strip())
        
        recipe_set = set(extracted_ingredients)
        # ------------------

        actual_missing = recipe_set - user_set
        
        if len(actual_missing) == 0:
            can_cook.append(recipe)
        elif len(actual_missing) == 1:
            missing_one.append({
                "recipe": recipe,
                "missing": list(actual_missing)[0]
            })
            
    return can_cook, missing_one

def call_ai_chef(ingredients):
    """调用 AI 大厨生成创意菜谱"""
    if not api_key:
        return "⚠️ 未检测到 API Key，请检查 Secrets 或 .env 设置。"

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    你是一位世界顶级的创意大厨。用户现在手里只有这些食材：{', '.join(ingredients)}。
    请根据这些食材：
    1. 构思一个非常有创意的菜名。
    2. 提供一个简单的烹饪逻辑（分步骤）。
    3. 如果食材组合很奇怪，请用幽默的语言解释为什么这样搭配。
    
    请直接用 Markdown 格式输出。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI 大厨罢工了: {str(e)}"