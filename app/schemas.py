from pydantic import BaseModel

class QueryInput(BaseModel):
    question: str
    decomp: dict | None = None

class QueryOutput(BaseModel):
    question: str
    sql: str
    result: list
    columns: list
    status: str
    retry_used: bool
    error: str | None = None
