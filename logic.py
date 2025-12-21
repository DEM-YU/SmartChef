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
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Secrets 中未配置 API Key"

    # 定义 2025 年模型优先级列表
    # 按照“最稳健且配额多”到“最新预览”的顺序排列
    model_candidates = [
        "gemini-2.0-flash",       # 2025 年最推荐的免费层级模型
        "gemini-1.5-flash",       # 极速备选模型
        "gemini-3-pro-preview"    # 你截图中的最新模型（但配额可能受限）
    ]

    try:
        # 使用 2025 年最新的 SDK 客户端
        client = genai.Client(api_key=api_key)
        prompt = f"你是一位创意大厨。我有这些食材：{', '.join(ingredients)}。请给一个创意菜名和简单步骤。"
        
        last_error = ""
        for model_name in model_candidates:
            try:
                response = client.models.generate_content(
                    model=model_name, 
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                continue # 如果当前模型 404 或 429，立即尝试下一个
        
        return f"❌ 所有可用模型均请求失败。最后一次报错: {last_error}"
        
    except Exception as e:
        return f"❌ 客户端初始化失败: {str(e)}"