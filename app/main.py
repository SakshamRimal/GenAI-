from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.workflow import run_workflow
from db import test_connection

app = FastAPI(
    title="Mini SQL Agent",
    description="Agentic Text-to-SQL using Claude Haiku",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


class AgentResponse(BaseModel):
    sql: str
    result: list
    summary: str
    status: str
    retry_count: int
    latency_ms: float
    error: str | None = None


@app.get("/health")
def health():
    db_ok = test_connection()
    return {"status": "ok", "db_connected": db_ok}


@app.post("/agent/sql", response_model=AgentResponse)
def agent_sql(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    state = run_workflow(request.question)

    return AgentResponse(
        sql=state.sql,
        result=state.result,
        summary=state.summary,
        status="success" if state.success else "failed",
        retry_count=state.retry_count,
        latency_ms=state.latency_ms,
        error=state.error,
    )
