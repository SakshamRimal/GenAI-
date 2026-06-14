import json
from agents.llm import call_llm
from prompts.templates import GENERATOR_PROMPT, FIXER_PROMPT


def generate_sql(plan: dict) -> str:
    plan_str = json.dumps(plan, indent=2)
    prompt = GENERATOR_PROMPT.replace("{plan}", plan_str)
    sql = call_llm(
        system_prompt=prompt,
        user_message="Generate the SQL query for the plan above. Return ONLY raw SQL, nothing else.",
    )
    return _clean_sql(sql)


def fix_sql(question: str, failed_sql: str, error: str) -> str:
    prompt = (
        FIXER_PROMPT
        .replace("{question}", question)
        .replace("{sql}", failed_sql)
        .replace("{error}", error)
    )
    sql = call_llm(
        system_prompt=prompt,
        user_message=(
            "Return ONLY the corrected SQL query. "
            "No explanation, no markdown, no backticks. Just the raw SQL."
        ),
    )
    return _clean_sql(sql)


def _clean_sql(sql: str) -> str:
    sql = sql.strip()
    for fence in ["```sql", "```postgresql", "```"]:
        sql = sql.removeprefix(fence)
    sql = sql.removesuffix("```").strip()
    # If LLM returned explanation instead of SQL, this will still fail validation
    # which is the correct behavior
    return sql
