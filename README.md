# 🍳 SmartChef - 你的智能厨房助手 

> **“冰箱里只剩这几样了，我能做点什么菜？”** —— 这是一个专门解决“今天吃什么”终极难题的神器。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![GitHub license](https://img.shields.io/github/license/DEM-YU/SmartChef)](https://github.com/DEM-YU/SmartChef/blob/main/LICENSE)

---

## 🌐 在线体验
🚀 **[点击这里直接访问：SmartChef Live Demo](https://smartchef-xzy5i33ypmhvtqvfapp9vbt.streamlit.app/)**

---

## ✨ 项目亮点

* **分类点选系统**：精心设计的分类界面（肉类、蔬菜、水产、蛋奶），像在餐厅点菜一样勾选你有的食材。
* **智能推荐逻辑**：
    * **✅ 完美匹配**：展示你手头食材可以直接下锅的所有菜谱。
    * **💡 惊喜推荐**：展示只需再多买 1 样食材就能解锁的新菜品，并高亮显示缺少的食材。
* **全方位信息展示**：每道菜都标注了 **难度等级**、**预计耗时** 以及 **菜系分类**。
* **完全响应式设计**：无论是在电脑显示器还是手机屏幕上，都能获得极佳的交互体验。

## 📸 界面预览

![SmartChef Preview](https://raw.githubusercontent.com/DEM-YU/SmartChef/main/screenshot.png)

---

## 🛠️ 技术栈
* **Frontend/Backend**: [Streamlit](https://streamlit.io/) - 强大的 Python 原生 Web 框架。
* **Logic**: Python - 使用高效的集合 (Set) 运算处理食材匹配。
* **Data Source**: JSON - 结构化的菜谱数据库，易于扩展。

---

## 🚀 如何在本地运行

1.  **克隆仓库**
    ```bash
    git clone [https://github.com/DEM-YU/SmartChef.git](https://github.com/DEM-YU/SmartChef.git)
    cd SmartChef
    ```

2.  **安装依赖库**
    ```bash
    pip install -r requirements.txt
    ```

3.  **启动应用**
    ```bash
    streamlit run app.py
    ```

---

## 📈 路线图 (Roadmap)
- [ ] 🤖 **AI 烹饪指南**：接入 LLM API 自动生成每道菜的详细步骤。
- [ ] 🖼️ **诱人视觉**：为每一道菜自动匹配高清美食大图。
- [ ] 📝 **购物清单**：一键导出缺少的食材，直接发到手机微信。

## 🤝 贡献
如果你有有趣的菜谱或更好的匹配逻辑，欢迎提交 Pull Request！

---

**Author**: [DEM-YU](https://github.com/DEM-YU)  
**Project Created via Vibe Coding** 🚀
