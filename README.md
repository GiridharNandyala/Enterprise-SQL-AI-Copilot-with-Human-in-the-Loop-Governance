# 🛡️ Enterprise SQL AI Copilot with Human-in-the-Loop Governance

An enterprise-grade Agentic SQL AI Copilot powered by **LangGraph**, **FastAPI**, **Streamlit**, and **Google Gemini 1.5 Flash**. This system converts natural language business queries into executed SQLite queries while enforcing security guardrails and human approval mechanisms for high-risk operations.

[![Live API Demo](https://img.shields.io/badge/Render-Live_API_Docs-00C7B7?style=for-the-badge&logo=render&logoColor=white)](https://enterprise-sql-ai-copilot-with-human-in.onrender.com/docs)
[![Streamlit App](https://img.shields.io/badge/Streamlit-RAG_PDF_Chat-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://giridhar-rag-pdf-chat.streamlit.app/)
[![LinkedIn Post](https://img.shields.io/badge/LinkedIn-Project_Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/giridhar-nandyala-5758662b2_generativeai-rag-machinelearning-ugcPost-7485951006032285696-w0Kj/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEs70akBeCLfAOvC2nnAC0kHj16JNBTXqJM)

---

## 🛠️ Tech Stack
* **LLM Engine**: Google Gemini 1.5 Flash
* **Agentic Framework**: LangGraph & LangChain
* **Backend Framework**: FastAPI (Uvicorn)
* **Frontend**: Streamlit
* **Observability & Tracing**: LangSmith
* **Database**: SQLite (`enterprise.db`)
* **Containerization & Deployment**: Docker, Render Cloud Deployment

---

## ✨ Features
* **Natural Language to SQL**: Translates business questions directly into SQLite queries using Google Gemini 1.5 Flash.
* **Human-in-the-Loop Governance**: Flags dangerous data manipulation queries (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`) requiring explicit approval before execution.
* **Self-Correction & Retry**: Automatic iterative loop up to 3 retries if a generated SQL query encounters execution errors.
* **Dual Interface**: Exposes a FastAPI production backend (with Swagger UI) and a Streamlit interactive frontend.
* **Multi-Table Enterprise Schema**: Built-in support for `customers`, `products`, `orders`, and `employees`.

---

## 📊 LangSmith Observability & Tracing
The application integrates **LangSmith** for full-stack observability, agent execution tracing, LLM prompt evaluation, and error tracking.

![LangSmith Tracing Dashboard](<img width="1530" height="776" alt="langsmith_tracing" src="https://github.com/user-attachments/assets/98bd3883-a1ea-4e69-a1cd-7523c7a0e82a" />
)

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
👉 Live API Documentation (Render): Swagger UI

    Streamlit Demo Application: RAG PDF Chat App

    Project Showcase: LinkedIn Post
