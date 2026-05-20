FORBIDDEN_KEYWORDS = {"delete", "drop", "update", "insert", "alter", "truncate"}

def validate_sql(sql: str) -> bool:
    cleaned = sql.lower().strip()

    # Must start with SELECT
    if not cleaned.startswith("select"):
        return False

    # Must not contain dangerous keywords
    for word in FORBIDDEN_KEYWORDS:
        if word in cleaned:
            return False

    return True