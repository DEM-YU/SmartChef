import json
import os
import streamlit as st
from google import genai # 2025 版 SDK 引用

def get_recommendations(user_ingredients):
    """本地数据库匹配逻辑"""
    # 1. 必须在函数开头就初始化变量，防止 NameError
    can_cook = []
    missing_one = []
    
    try:
        # 确保 recipes.json 路径正确
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
    except Exception:
        # 如果找不到文件或读取失败，直接返回空列表
        return [], []

    # 2. 处理用户食材
    user_set = set([str(i).strip() for i in user_ingredients])

    # 3. 循环匹配
    for recipe in recipes:
        # 兼容你的 JSON 对象格式
        extracted = []
        for ing in recipe.get('ingredients', []):
            if isinstance(ing, dict):
                extracted.append(ing.get('name', '').strip())
            else:
                extracted.append(str(ing).strip())
        
        recipe_set = set(extracted)
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
    """2025 版 Gemini 3 调用逻辑"""
    # 从 Streamlit Cloud 的 Secrets 读取
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        return "⚠️ Secrets 中未配置 API Key"

    try:
        # 按照 2025 年最新 SDK 初始化客户端
        client = genai.Client(api_key=api_key)
        
        prompt = f"你是一位大厨。我有这些食材：{', '.join(ingredients)}。请给我一个创意菜名和简单做法。"
        
        # 使用你截图中出现的 2025 预览版模型
        response = client.models.generate_content(
            model="gemini-3-pro-preview", 
            contents=prompt
        )
        
        return response.text
    except Exception as e:
        return f"❌ 2025 接口请求失败: {str(e)}"