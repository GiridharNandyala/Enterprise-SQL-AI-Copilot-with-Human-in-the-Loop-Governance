import os
import ast
from typing import TypedDict, Optional, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from database import execute_query

load_dotenv()

# 1. Correct Model Initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

DB_SCHEMA = """
Tables in enterprise.db:
1. customers (customer_id, name, region, join_date)
2. products (product_id, product_name, category, price)
3. orders (order_id, customer_id, product_id, order_date, amount, status)
"""

class AgentState(TypedDict):
    user_query: str
    sql_query: str
    retry_count: int
    error: Optional[str]
    results: Optional[list]
    requires_approval: bool

def generate_sql(state: AgentState) -> AgentState:
    query = state["user_query"]
    error_ctx = f"\nPrevious Error: {state['error']}. Fix the query." if state.get("error") else ""
    
    prompt = f"""
    You are an expert SQLite Data Engineer. Convert the natural language user request into a clean SQL query.
    
    Schema:
    {DB_SCHEMA}
    
    User Query: "{query}"
    {error_ctx}
    
    Return ONLY the raw SQL query string. Do not output JSON or markdown blocks.
    """
    
    try:
        response = llm.invoke(prompt)
        raw_output = response.content if hasattr(response, 'content') else str(response)
        
        # Safe extraction for List / Dict outputs
        if isinstance(raw_output, list) and len(raw_output) > 0:
            first_item = raw_output[0]
            raw_text = first_item.get("text", str(first_item)) if isinstance(first_item, dict) else str(first_item)
        elif isinstance(raw_output, dict):
            raw_text = raw_output.get("text", str(raw_output))
        else:
            raw_text = str(raw_output)

        # Handle stringified dictionaries
        if raw_text.strip().startswith("{") and "'text':" in raw_text:
            try:
                parsed_dict = ast.literal_eval(raw_text)
                if isinstance(parsed_dict, dict) and "text" in parsed_dict:
                    raw_text = parsed_dict["text"]
            except Exception:
                pass

        clean_sql = raw_text.strip().replace("```sql", "").replace("```", "").strip()
    except Exception as e:
        clean_sql = f"-- Error generating SQL: {str(e)}"
    
    return {
        **state,
        "sql_query": clean_sql
    }

def validate_and_execute(state: AgentState) -> AgentState:
    sql = state.get("sql_query", "")
    
    # 1. Security Check for Dangerous Operations
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    if any(kw in sql.upper() for kw in dangerous_keywords):
        return {
            **state,
            "requires_approval": True,
            "error": None,
            "results": None
        }
    
    # 2. Check for SQL Generation Error
    if sql.startswith("-- Error"):
        return {
            **state,
            "error": sql,
            "retry_count": state.get("retry_count", 0) + 1,
            "requires_approval": False,
            "results": None
        }

    # 3. Execute Query on SQLite
    df, err = execute_query(sql)
    
    if err:
        return {
            **state,
            "error": err,
            "retry_count": state.get("retry_count", 0) + 1,
            "results": None
        }
    
    results_json = df.to_dict(orient="records") if df is not None else []
    return {
        **state,
        "results": results_json,
        "error": None,
        "requires_approval": False
    }

def should_retry_or_end(state: AgentState) -> str:
    if state.get("requires_approval"):
        return "end"
    if state.get("error") and state.get("retry_count", 0) < 3:
        return "retry"
    return "end"

builder = StateGraph(AgentState)
builder.add_node("generate_sql", generate_sql)
builder.add_node("validate_and_execute", validate_and_execute)

builder.set_entry_point("generate_sql")
builder.add_edge("generate_sql", "validate_and_execute")

builder.add_conditional_edges(
    "validate_and_execute",
    should_retry_or_end,
    {
        "retry": "generate_sql",
        "end": END
    }
)

app_graph = builder.compile()

def run_copilot_workflow(user_query: str) -> Dict[str, Any]:
    initial_state: AgentState = {
        "user_query": user_query,
        "sql_query": "",
        "retry_count": 0,
        "error": None,
        "results": None,
        "requires_approval": False
    }
    
    final_state = app_graph.invoke(initial_state)
    return dict(final_state)