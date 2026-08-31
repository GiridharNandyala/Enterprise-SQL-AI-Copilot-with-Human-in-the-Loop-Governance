from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import run_copilot_workflow
from database import execute_query

app = FastAPI(title="Enterprise AI Data Copilot API")

class QueryRequest(BaseModel):
    prompt: str

class ApprovalRequest(BaseModel):
    sql_query: str

@app.get("/")
def root():
    return {"status": "Enterprise AI Copilot API is running smoothly!"}

@app.post("/query")
def process_query(req: QueryRequest):
    try:
        response = run_copilot_workflow(req.prompt)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/approve-execution")
def approve_query(req: ApprovalRequest):
    df, err = execute_query(req.sql_query)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return {"status": "Success", "data": df.to_dict(orient="records")}