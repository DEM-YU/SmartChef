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
    
    # 定义模型尝试列表，从最新到最稳
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    prompt = f"你是一位大厨。我有这些食材：{', '.join(ingredients)}。请给我一个创意菜名和简单做法。"
    
    for m_name in model_names:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # 如果当前模型报错，继续尝试下一个
            continue
            
    return "❌ 尝试了所有模型均失败，请检查 API Key 权限或稍后再试。"