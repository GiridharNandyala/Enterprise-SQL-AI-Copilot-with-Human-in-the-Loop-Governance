from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import run_copilot_workflow
from database import init_db

app = FastAPI(title="Enterprise SQL AI Copilot API")

@app.on_event("startup")
def startup_event():
    init_db()

class QueryRequest(BaseModel):
    query: str

@app.post("/api/v1/query")
def process_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return run_copilot_workflow(request.query)