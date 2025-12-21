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
    """2025 专用版：避开 0 配额，锁定 Flash 路径"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return "⚠️ 未配置 API Key"

    try:
        # 使用你截图中的 Client 语法
        client = genai.Client(api_key=api_key)
        prompt = f"你是大厨。食材：{', '.join(ingredients)}。请给一个创意菜名和做法。"
        
        # 强制使用 gemini-1.5-flash。
        # 报错显示你的 gemini-3-pro 配额是 0，而 1.5 系列通常有免费额度。
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ 2025 接口访问失败: {str(e)}"