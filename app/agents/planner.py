import json
from agents.llm import call_llm
from prompts.templates import PLANNER_PROMPT


def plan_query(question: str) -> dict:
    raw = call_llm(
        system_prompt=PLANNER_PROMPT,
        user_message=f"Question: {question}",
    )
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "intent": question,
            "tables": [],
            "columns": [],
            "filters": [],
            "aggregations": [],
            "joins": [],
        }
