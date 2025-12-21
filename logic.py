import json
import os
import streamlit as st
from google import genai # 注意：2025 版引用方式可能已变更为此

def get_recommendations(user_ingredients):
    """保持原来的本地匹配逻辑不变..."""
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
    except FileNotFoundError:
        return [], []
    # ... (此处省略中间的匹配代码)
    return can_cook, missing_one

def call_ai_chef(ingredients):
    # 在 Streamlit 云端，建议直接从 st.secrets 获取 Key
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        return "⚠️ Secrets 中未配置 API Key"

    try:
        # 按照你截图中 2025 年最新的 SDK 写法初始化客户端
        #
        client = genai.Client(api_key=api_key)
        
        prompt = f"你是一位创意大厨。我有这些食材：{', '.join(ingredients)}。请给我一个创意菜名和步骤。"
        
        # 使用你截图中出现的最新预览版模型名称
        #
        response = client.models.generate_content(
            model="gemini-3-pro-preview", 
            contents=prompt
        )
        
        return response.text
    except Exception as e:
        return f"❌ 2025 接口请求失败: {str(e)}"