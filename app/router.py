from app.schemas import QueryInput, QueryOutput
from fastapi import APIRouter
from pydantic import BaseModel

from app.validator import validate_sql
from app.executor import execute_sql
from app.llm_pipeline import extract_decomposition, generate_sql_llm, fix_sql_llm

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/query", response_model=QueryOutput)
def query(input: QueryInput):

    # Step 1: Decompose question if not provided
    if input.decomp is None:
        try:
            decomp = extract_decomposition(input.question)
        except Exception as e:
            return QueryOutput(
                question=input.question,
                sql="",
                result=[],
                columns=[],
                status="failed",
                retry_used=False,
                error=f"Decomposition failed: {e}",
            )
    else:
        decomp = input.decomp

    # Step 2: Generate SQL
    sql = generate_sql_llm(input.question, decomp)

    # Step 3: Validate SQL
    if not validate_sql(sql):
        return QueryOutput(
            question=input.question,
            sql=sql,
            result=[],
            columns=[],
            status="failed",
            retry_used=False,
            error="Generated SQL is not safe or not a SELECT statement.",
        )

    # Step 4: Execute SQL
    result = execute_sql(sql)

    if result["status"] == "success":
        return QueryOutput(
            question=input.question,
            sql=sql,
            result=result["rows"],
            columns=result["columns"],
            status="success",
            retry_used=False,
        )

    # Step 5: Retry once if failed
    fixed_sql = fix_sql_llm(input.question, decomp, sql, result["error"])

    if not validate_sql(fixed_sql):
        return QueryOutput(
            question=input.question,
            sql=fixed_sql,
            result=[],
            columns=[],
            status="failed",
            retry_used=True,
            error="Fixed SQL is still not safe.",
        )

    retry_result = execute_sql(fixed_sql)

    return QueryOutput(
        question=input.question,
        sql=fixed_sql,
        result=retry_result["rows"],
        columns=retry_result["columns"],
        status=retry_result["status"],
        retry_used=True,
        error=retry_result["error"],
    )