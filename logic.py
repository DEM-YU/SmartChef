def call_ai_chef(ingredients):
    """调用 AI 大厨生成创意菜谱"""
    if not api_key:
        return "⚠️ 未检测到 API Key，请检查 Secrets 或 .env 设置。"

    # 修改点：确保模型名称正确
    try:
        # 尝试使用 gemini-1.5-flash，这是目前最快且免费额度高的模型
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        你是一位世界顶级的创意大厨。用户现在手里只有这些食材：{', '.join(ingredients)}。
        请根据这些食材：
        1. 构思一个非常有创意的菜名。
        2. 提供一个简单的烹饪逻辑（分步骤）。
        3. 如果食材组合很奇怪，请用幽默的语言解释为什么这样搭配。
        
        请直接用 Markdown 格式输出。
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 如果 flash 报错，自动切换到 gemini-pro 备用
        try:
            model_backup = genai.GenerativeModel('gemini-pro')
            response = model_backup.generate_content(prompt)
            return response.text
        except:
            return f"❌ AI 大厨罢工了: {str(e)}"