# 🛡️ Enterprise SQL AI Copilot with Human-in-the-Loop Governance

An enterprise-ready Text-to-SQL AI Agent featuring dynamic database schema inspection, query validation guardrails, and a **Human-in-the-Loop (HITL)** governance workflow to safely translate natural language queries into executable SQL commands.

---
[![Live App Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://enterprise-sql-ai-copilot-with-human-in-the-loop-governance.streamlit.app/)
[![LinkedIn Post](https://img.shields.io/badge/🔗_LinkedIn-Post_&_Demo-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/giridhar-nandyala-5758662b2_agenticai-langgraph-genai-ugcPost-7500058210687610882-HjRs/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEs70akBeCLfAOvC2nnAC0kHj16JNBTXqJM)
---
## 🌟 Key Features

- 🧠 **Natural Language to SQL**: Converts complex business questions into optimized SQL queries using LLM tool-calling.
- 🛑 **Human-in-the-Loop (HITL) Governance**: Utilizes **LangGraph Interrupt Checkpoints** to pause execution and require explicit human approval/review for critical database actions.
- 🛡️ **SQL Safety Guardrails**: Prevents destructive operations (e.g., unauthorized `DROP`, `DELETE`, `TRUNCATE`) via regex and AST parsing before execution.
- 📊 **Dynamic Data Rendering**: Returns query results in interactive Pandas DataFrames and visualization-ready formats using Streamlit.
- 🔍 **Schema Awareness**: Automatically inspects table structures, relationships, and data types without hardcoding SQL prompts.

---

## 🏗️ Architecture & Workflow

1. **User Query Input**: Business user asks a question in plain English via Streamlit UI.
2. **Schema Context Retrieval**: System dynamically fetches current DB schema.
3. **SQL Generation Agent**: LLM drafts an optimized SQL query based on user intent and schema.
4. **Safety Verification Check**: Guardrails scan for unsafe DML/DDL commands.
5. **Human Approval Interrupt (LangGraph)**: If sensitive tables or operations are detected, state freezes until human admin reviews and approves/edits the query.
6. **Execution & Visualization**: Query runs safely on SQL Engine; results render in tabular and graphical formats.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Agentic Orchestration**: LangGraph, LangChain
- **LLM Engine**: Google Gemini API / OpenAI GPT-4o
- **Database**: SQLite / PostgreSQL / MySQL
- **Web UI**: Streamlit
- **Data Handling**: Pandas, SQLAlechmy

---

## 🚀 Quick Start & Installation

```bash
# Clone the repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/enterprise-sql-ai-copilot.git](https://github.com/YOUR_GITHUB_USERNAME/enterprise-sql-ai-copilot.git)

# Navigate into project directory
cd enterprise-sql-ai-copilot

# Install dependencies
pip install -r requirements.txt

# Set up Environment Variables (.env)
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///sample_enterprise.db

# Run Streamlit App
streamlit run app.py
