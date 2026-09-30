import os
from functools import lru_cache
from google import genai
from google.genai import types

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your Google AI Studio API key."
        )
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, *, temperature: float = 0.3, max_output_tokens: int = 1200) -> str:
    response = get_client().models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def generate_json(prompt: str, schema: dict, *, temperature: float = 0.2, max_output_tokens: int = 1800):
    response = get_client().models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")
    return text.strip()
