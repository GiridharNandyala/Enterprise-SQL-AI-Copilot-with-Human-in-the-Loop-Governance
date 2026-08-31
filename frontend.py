import streamlit as st
import pandas as pd
import plotly.express as px
from agents import run_copilot_workflow
from database import execute_query

st.set_page_config(
    page_title="Enterprise AI Data Copilot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("<h1 style='color: #4F46E5;'>🤖 Enterprise AI Data Copilot</h1>", unsafe_allow_html=True)
st.caption("Multi-Agent Governance & Live Execution System Powered by LangGraph & Gemini")

st.divider()

st.sidebar.header("⚙️ Copilot Controls")
st.sidebar.success("Database Status: Connected (enterprise.db)")

# Session State for User Input Prompt
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = ""

# Sample Suggestions Buttons
st.markdown("**💡 Try sample queries:**")
col1, col2, col3 = st.columns(3)

if col1.button("Show total sales by region"):
    st.session_state.active_prompt = "Show total sales by customer region"
if col2.button("Top 5 customers by spent"):
    st.session_state.active_prompt = "Top 5 customers by total order amount"
if col3.button("Delete all customers (Safety Test)"):
    st.session_state.active_prompt = "DELETE FROM customers WHERE customer_id = 101"

# Text input synced with active prompt
user_query = st.text_input(
    "Enter your data question or command:", 
    value=st.session_state.active_prompt,
    placeholder="e.g., What are our top-selling software products?"
)

# Function to execute Agent Workflow directly (No FastAPI needed)
def run_copilot(query):
    with st.spinner("Multi-Agent Graph is processing your request..."):
        try:
            # Direct python function call instead of requests.post
            data = run_copilot_workflow(query)

            if isinstance(data, dict) and data.get("sql_query"):
                st.subheader("📝 Generated SQL Query")
                st.code(data.get("sql_query"), language="sql")

            # Governance Alert / Approval Required
            if isinstance(data, dict) and (data.get("requires_approval") or data.get("status") == "approval_required"):
                st.error("⚠️ Governance Alert: Destructive SQL command detected!")
                st.warning("This operation requires Human-in-the-Loop authorization before execution.")
                
                if st.button("Approve & Execute Command"):
                    sql_to_run = data.get("sql_query")
                    df_res, err = execute_query(sql_to_run)
                    if err:
                        st.error(f"Execution Error: {err}")
                    else:
                        st.success("Action Executed Successfully!")
                        st.dataframe(df_res, use_container_width=True)

            # Output Data & Plots
            elif isinstance(data, dict) and "results" in data:
                st.subheader("📊 Results Data")
                df = pd.DataFrame(data["results"])
                st.dataframe(df, use_container_width=True)

                numeric_cols = df.select_dtypes(include=['number']).columns
                string_cols = df.select_dtypes(include=['object']).columns

                if len(numeric_cols) > 0 and len(string_cols) > 0:
                    st.subheader("📈 Automated Visual Insights")
                    fig = px.bar(df, x=string_cols[0], y=numeric_cols[0], title=f"{numeric_cols[0]} by {string_cols[0]}")
                    st.plotly_chart(fig, use_container_width=True)

            elif isinstance(data, dict) and "data" in data:
                st.subheader("📊 Results Data")
                df = pd.DataFrame(data["data"])
                st.dataframe(df, use_container_width=True)

            elif isinstance(data, dict) and data.get("error"):
                st.error(f"Execution Error: {data['error']}")
            else:
                st.write(data)

        except Exception as e:
            st.error(f"Execution Error: {e}")

# Run when 'Run Query' is clicked OR if a sample button was pressed
if st.button("Run Query") or st.session_state.active_prompt:
    query_to_send = user_query if user_query else st.session_state.active_prompt
    if query_to_send:
        run_copilot(query_to_send)
        st.session_state.active_prompt = ""
