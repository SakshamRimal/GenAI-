import re

BLOCKED_KEYWORDS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bTRUNCATE\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bREPLACE\b",
    r"\bMERGE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
]


class ValidationError(Exception):
    pass


def validate_sql(sql: str) -> str:
    """
    Validates that the SQL is a safe SELECT-only query.
    Returns the cleaned SQL or raises ValidationError.
    """
    if not sql or not sql.strip():
        raise ValidationError("SQL query is empty.")

    upper = sql.upper().strip()

    if not upper.startswith("SELECT"):
        raise ValidationError(
            f"Only SELECT queries are allowed. Query starts with: {sql[:30]}"
        )

    for pattern in BLOCKED_KEYWORDS:
        if re.search(pattern, upper):
            keyword = pattern.replace(r"\b", "")
            raise ValidationError(f"Blocked keyword detected: {keyword}")

    # Prevent multiple statements
    # Strip string literals before checking for semicolons in the middle
    no_strings = re.sub(r"'[^']*'", "''", sql)
    statements = [s.strip() for s in no_strings.split(";") if s.strip()]
    if len(statements) > 1:
        raise ValidationError("Multiple SQL statements are not allowed.")

    return sql.strip().rstrip(";")
