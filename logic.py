import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. 加载环境变量
load_dotenv()

# 2. 配置 Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_recommendations(user_ingredients):
    """本地数据库匹配逻辑 - 兼容对象格式"""
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
    except FileNotFoundError:
        return [], []

    user_set = set([str(i).strip() for i in user_ingredients])
    can_cook = []
    missing_one = []

    for recipe in recipes:
        # 提取食材名称，增强容错性
        extracted_ingredients = []
        for ing in recipe.get('ingredients', []):
            if isinstance(ing, dict):
                extracted_ingredients.append(ing.get('name', '').strip())
            else:
                extracted_ingredients.append(str(ing).strip())
        
        recipe_set = set(extracted_ingredients)
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
    if not api_key:
        return "⚠️ Secrets 中未配置 API Key"
    
    # 根据你 2025 年的后台截图，这些是现在最强的模型名称
    model_names = [
        'gemini-3-flash',          # 2025 最新的快手模型
        'gemini-2.0-flash',        # 2025 的稳定版模型
        'gemini-3-pro-preview'     # 你截图中出现的最新预览版
    ]
    
    prompt = f"你是一位大厨。我有这些食材：{', '.join(ingredients)}。请给我一个创意菜名和简单做法。"
    
    for m_name in model_names:
        try:
            # 强制指定较新的模型名称
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            # 如果报错，继续尝试下一个
            continue
            
    return "❌ 2025 所有的模型请求都失败了。请检查 Google AI Studio 的 API 状态。"