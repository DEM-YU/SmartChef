import json
import os
import streamlit as st
from google import genai # 2025 版最新引用

def get_recommendations(user_ingredients):
    """本地匹配逻辑（保持不变）"""
    can_cook, missing_one = [], []
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
        user_set = set([str(i).strip() for i in user_ingredients])
        for r in recipes:
            extracted = [i.get('name','').strip() if isinstance(i,dict) else str(i).strip() for i in r.get('ingredients',[])]
            actual_missing = set(extracted) - user_set
            if not actual_missing: can_cook.append(r)
            elif len(actual_missing) == 1: missing_one.append({"recipe": r, "missing": list(actual_missing)[0]})
    except: pass
    return can_cook, missing_one

def call_ai_chef(ingredients):
    """2025 年 12 月专用：锁定截图推荐的 Gemini 3 Flash"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Secrets 中未配置 API Key"

    try:
        # 使用你截图中的 2025 最新 Client 语法
        client = genai.Client(api_key=api_key)
        prompt = f"你是创意大厨。食材：{', '.join(ingredients)}。请给一个创意菜名和步骤。"
        
        # 核心修改：使用截图“What's new”里明确标出的模型名
        response = client.models.generate_content(
            model="gemini-3-flash", 
            contents=prompt
        )
        
        if response and response.text:
            return response.text
        return "❌ AI 响应为空，请稍后重试。"

    except Exception as e:
        error_msg = str(e)
        # 如果 3-flash 也报 404，尝试去掉 'models/' 前缀或使用截图里的预览版
        return f"❌ 2025 接口访问失败: {error_msg}"