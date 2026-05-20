import json
from agents.llm import call_llm
from prompts.templates import SUMMARIZER_PROMPT


def summarize(question: str, sql: str, result: list[dict]) -> str:
    result_str = json.dumps(result[:50], indent=2, default=str)
    prompt = SUMMARIZER_PROMPT.format(
        question=question,
        sql=sql,
        result=result_str,
    )
    return call_llm(
        system_prompt="You are a concise data analyst.",
        user_message=prompt,
        max_tokens=256,
    )
