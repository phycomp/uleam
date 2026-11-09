"""Direct LLM client (OpenAI-compatible, points at Ollama)."""
from openai import OpenAI

from .config import OLLAMA_V1_URL, OLLAMA_MODEL, TEMPERATURE, MAX_TOKENS


def get_client() -> OpenAI:
    return OpenAI(base_url=OLLAMA_V1_URL, api_key="ollama")


def chat(system: str, user: str, json_mode: bool = False) -> str:
    client = get_client()
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    resp = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        **kwargs,
    )
    return resp.choices[0].message.content or ""