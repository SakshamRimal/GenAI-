import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def call_llm(system_prompt: str, user_prompt: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in .env")

    client = Anthropic(api_key=api_key)
    model = os.getenv("LLM_MODEL", "claude-haiku-4-5")

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    if not response.content:
        return ""

    return response.content[0].text