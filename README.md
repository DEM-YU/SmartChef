# 👨‍🍳 SmartChef 4.0 Pro: Intelligent Fridge Manager

**SmartChef** is a Python-based intelligent recipe matching application built with Streamlit. It solves the "what should I cook?" dilemma by matching ingredients in your fridge with a database of 100+ recipes using a weighted scoring algorithm.

---

## 🌟 Key Features

* **Weighted Matching Algorithm**: Categorizes ingredients into "Main" and "Side" to prioritize core proteins and vegetables.
* **Core Missing Penalty**: Automatically penalizes recipes missing essential main ingredients, ensuring realistic cooking suggestions.
* **Automated Categorization**: Scans the database to group ingredients into Meat, Veggies, Seafood, etc., for easy selection.
* **Pantry Staple Filtering**: Intelligently ignores seasonings (salt, oil, pepper) and tools (toothpicks) in the selection process to reduce clutter.
* **Dynamic Visuals**: Real-time progress bars and color-coded status (Green/Orange/Red) based on matching accuracy.

---

## 📂 Project Structure

* `app.py`: UI rendering and sidebar categorization.
* `logic.py`: Core logic including the matching algorithm and pantry filters.
* `recipes.json`: Structured database containing recipe metadata.
* `requirements.txt`: Minimal dependencies for easy deployment.

---

## 🚀 Quick Start

1.  **Install Dependencies**:
    ```bash
    pip install streamlit
    ```
2.  **Run Application**:
    ```bash
    streamlit run app.py
    ```

---

**Developer**: Brooks (Computer Science, University of Alberta)
**Location**: Edmonton, Alberta, Canada
**Last Updated**: Dec 21, 2025, 06:20 AM MST
