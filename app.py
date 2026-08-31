import streamlit as st
import pandas as pd
from agents import run_copilot_workflow
from database import execute_query

st.set_page_config(page_title="Enterprise AI Data Copilot", layout="wide")

st.title("🛡️ Enterprise SQL AI Copilot with Governance")
st.write("Ask business questions in natural language and generate/execute safe SQL queries.")

# Sidebar for controls & status
with st.sidebar:
    st.header("⚙️ Copilot Controls")
    st.success("Database Status: Connected")

# User input prompt
prompt = st.text_input("Enter your data question or command:", placeholder="e.g. Show total sales by customer region")

if st.button("Run Query"):
    if prompt:
        with st.spinner("Processing query via Agentic Workflow..."):
            try:
                # FastAPIం
                response = run_copilot_workflow(prompt)
                
                
                if isinstance(response, dict):
                    if response.get("status") == "approval_required":
                        st.warning("⚠️ **Human-in-the-Loop Governance Triggered!**")
                        st.info(f"Generated Query requires Approval: `{response.get('sql_query')}`")
                        
                        # Human Approval 
                        if st.button("Approve & Execute"):
                            df, err = execute_query(response.get('sql_query'))
                            if err:
                                st.error(f"Execution Error: {err}")
                            else:
                                st.success("Query Executed Successfully!")
                                st.dataframe(df)
                    else:
                        st.success("Query Executed Successfully!")
                        if "data" in response:
                            st.dataframe(pd.DataFrame(response["data"]))
                        else:
                            st.write(response)
                else:
                    st.write(response)
                    
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
    else:
                st.warning("Please enter a valid query prompt.")
