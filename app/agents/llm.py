import anthropic
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def call_llm(system_prompt: str, user_message: str, max_tokens: int = 1024) -> str:
    client = get_client()
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return message.content[0].text.strip()
