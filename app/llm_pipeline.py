import os
import json
from app.llm_client import call_llm

PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts", "llm_prompts.json")

def _load_prompts() -> dict:
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _extract_json(text: str) -> dict:
    text = text.strip()

    # Try direct parse
    if text.startswith("{"):
        return json.loads(text)

    # Try to find JSON block inside text
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end + 1])

    raise ValueError(f"No JSON found in response: {text}")

def extract_decomposition(question: str) -> dict:
    prompts = _load_prompts()
    system = prompts["extract_decomp_system"]
    user = prompts["extract_decomp_user"].format(question=question)
    response = call_llm(system, user)
    return _extract_json(response)

def generate_sql_llm(question: str, decomp: dict) -> str:
    prompts = _load_prompts()
    system = prompts["generate_sql_system"]
    user = prompts["generate_sql_user"].format(
        question=question,
        decomp=json.dumps(decomp),
    )
    return call_llm(system, user).strip()

def fix_sql_llm(question: str, decomp: dict, sql: str, error: str) -> str:
    prompts = _load_prompts()
    system = prompts["fix_sql_system"]
    user = prompts["fix_sql_user"].format(
        question=question,
        decomp=json.dumps(decomp),
        sql=sql,
        error=error,
    )
    return call_llm(system, user).strip()