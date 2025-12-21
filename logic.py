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
    """2025 版 Gemini 核心调用逻辑 - 避开零配额模型"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Secrets 中未配置 API Key"

    # 重新排列优先级：将配额充足的 Flash 模型放在首位
    # 报错显示 gemini-3-pro 的 limit 是 0，所以我们最后才尝试它
    model_candidates = [
        "gemini-1.5-flash",       # 2025 年最稳定的免费层级“劳模”
        "gemini-2.0-flash",       # 性能平衡的备选模型
        "gemini-3-pro-preview"    # 虽然最新，但你的账号当前配额为 0
    ]

    try:
        # 使用你截图中 2025 年最新的 SDK 语法
        client = genai.Client(api_key=api_key)
        prompt = f"你是一位大厨。食材：{', '.join(ingredients)}。请给一个创意菜名和步骤。"
        
        for model_name in model_candidates:
            try:
                response = client.models.generate_content(
                    model=model_name, 
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                # 如果当前模型报 429 或 404，立即跳过尝试下一个
                continue
        
        return "❌ 2025 免费额度已耗尽。请确认 Google AI Studio 中 Flash 模型的配额状态。"
        
    except Exception as e:
        return f"❌ 2025 接口初始化失败: {str(e)}"