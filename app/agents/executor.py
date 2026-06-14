from agents.validator import validate_sql, ValidationError
from agents.sql_generator import fix_sql
from tools.db_tools import execute_query
from config import MAX_RETRIES


def execute_with_retry(question: str, sql: str) -> dict:
    current_sql = sql
    last_error = None

    # First validate — if it fails here, try to fix once before looping
    try:
        validated_sql = validate_sql(current_sql)
    except ValidationError as e:
        last_error = str(e)
        current_sql = fix_sql(question, current_sql, last_error)
        try:
            validated_sql = validate_sql(current_sql)
        except ValidationError as e2:
            return {
                "sql": current_sql,
                "result": [],
                "error": str(e2),
                "retry_count": 1,
                "success": False,
            }

    # Now try executing, with retry on DB errors only
    for attempt in range(MAX_RETRIES + 1):
        try:
            rows = execute_query(validated_sql)
            return {
                "sql": validated_sql,
                "result": rows,
                "error": None,
                "retry_count": attempt,
                "success": True,
            }
        except Exception as e:
            last_error = str(e)

        if attempt < MAX_RETRIES:
            fixed = fix_sql(question, validated_sql, last_error)
            try:
                validated_sql = validate_sql(fixed)
            except ValidationError as ve:
                last_error = str(ve)
                continue

    return {
        "sql": validated_sql,
        "result": [],
        "error": last_error,
        "retry_count": MAX_RETRIES,
        "success": False,
    }
