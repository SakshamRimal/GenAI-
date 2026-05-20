from sqlalchemy import text
from db import engine


def execute_query(sql: str) -> list[dict]:
    """
    Execute a validated SELECT query and return results as a list of dicts.
    Raises an exception on failure (caller handles retry logic).
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
