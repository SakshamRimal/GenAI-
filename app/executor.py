from app.database import get_connection
from app.logger import log_query

def execute_sql(sql: str) -> dict:
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []

        conn.commit()
        log_query(sql, "SUCCESS")

        return {
            "status": "success",
            "rows": rows,
            "columns": columns,
            "error": None,
        }

    except Exception as e:
        conn.rollback()
        log_query(sql, "FAILED", str(e))

        return {
            "status": "failed",
            "rows": [],
            "columns": [],
            "error": str(e),
        }

    finally:
        conn.close()