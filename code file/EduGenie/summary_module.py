from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text.strip()
    if not text:
        return "Please enter text to summarize."

    prompt = f"""
Summarize the educational passage below for quick revision.
Keep the important facts and relationships.
Use clear language and bullet points where useful.
Do not add information that is not supported by the passage.

Passage:
{text}
"""
    try:
        return generate_text(prompt, temperature=0.2, max_output_tokens=1000)
    except Exception as exc:
        return f"Unable to summarize right now: {exc}"
