# 🛡️ Enterprise SQL AI Copilot with Human-in-the-Loop Governance

An enterprise-grade Agentic SQL AI Copilot powered by **LangGraph**, **FastAPI**, **Streamlit**, and **Google Gemini 3.6 Flash**. This system converts natural language business queries into executed SQLite queries while enforcing security guardrails and human approval mechanisms for high-risk operations.

[![Live API Demo](https://img.shields.io/badge/Render-Live_API_Docs-00C7B7?style=for-the-badge&logo=render&logoColor=white)](https://enterprise-sql-ai-copilot-with-human-in.onrender.com/docs)

---

## ✨ Features
* **Natural Language to SQL**: Translates business questions directly into SQLite queries using Google Gemini 3.6 Flash.
* **Human-in-the-Loop Governance**: Flags dangerous data manipulation queries (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`) requiring explicit approval before execution.
* **Self-Correction & Retry**: Automatic iterative loop up to 3 retries if a generated SQL query encounters execution errors.
* **Dual Interface**: Exposes a FastAPI production backend (with Swagger UI) and a Streamlit interactive frontend.
* **Multi-Table Enterprise Schema**: Built-in support for `customers`, `products`, `orders`, and `employees`.

---

## 🗄️ Database Schema (`enterprise.db`)
* **`customers`**: `customer_id`, `name`, `region`, `join_date`
* **`products`**: `product_id`, `product_name`, `category`, `price`
* **`orders`**: `order_id`, `customer_id`, `product_id`, `order_date`, `amount`, `status`
* **`employees`**: `employee_id`, `name`, `department`, `role`, `salary`

---

## 🚀 Local Setup Instructions

### 1. Prerequisites & Virtual Environment
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

2. Install Dependencies
pip install -r requirements.txt

3. Environment Variables
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

4. Running the FastAPI Backend
python -m uvicorn main:app --reload

5. Running the Streamlit Frontend
streamlit run app.py

🌐 Live Deployment
The API is deployed on Render and accessible via Swagger UI:
👉 https://enterprise-sql-ai-copilot-with-human-in.onrender.com/docs
