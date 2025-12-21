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
    """2025 年末版：自动探测可用模型，解决 404 和 429 报错"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Secrets 中未配置 API Key"

    try:
        # 使用你截图中的 2025 最新 SDK 语法
        client = genai.Client(api_key=api_key)
        prompt = f"你是创意大厨。食材：{', '.join(ingredients)}。请给一个创意菜名和步骤。"
        
        # 2025 年模型尝试列表（去掉了 'models/' 前缀，这是新版 SDK 的标准格式）
        #
        model_list = [
            "gemini-2.0-flash",       # 2025 年最稳、配额最多的免费层级模型
            "gemini-1.5-flash",       # 经典极速模型
            "gemini-3-pro-preview"    # 你截图示例中的最新模型
        ]
        
        for m_name in model_list:
            try:
                response = client.models.generate_content(
                    model=m_name, 
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                # 如果当前模型报 404 或 429，立即切换下一个
                continue
                
        return "❌ 2025 年所有可用模型均无法访问，请检查 Google AI Studio 的配额状态。"

    except Exception as e:
        return f"❌ 2025 接口访问失败: {str(e)}"