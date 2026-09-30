import os
from gemini_client import generate_text


_local_pipeline = None


def _local_explain(topic: str) -> str:
    global _local_pipeline
    if _local_pipeline is None:
        from transformers import pipeline
        _local_pipeline = pipeline(
            "text2text-generation",
            model=os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M"),
        )

    prompt = (
        "Explain the following concept to a beginner in simple language. "
        "Use a short definition, an intuitive explanation, an example, and key points.\n\n"
        f"Concept: {topic}"
    )
    result = _local_pipeline(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_concept(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        return "Please enter a topic to explain."

    # The original project specification uses LaMini-Flan-T5 locally.
    # Set USE_LOCAL_EXPLAINER=true and install requirements-local.txt to use it.
    if os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true":
        try:
            return _local_explain(topic)
        except Exception as exc:
            # Fall back to Gemini so the application remains usable.
            fallback_note = f"\n\n(Local explainer unavailable; using Gemini fallback: {exc})"
        else:
            fallback_note = ""
    else:
        fallback_note = ""

    prompt = f"""
You are an educational concept explainer.
Explain the topic below for a beginner.
Structure the response as:
1. Simple definition
2. How it works / why it matters
3. A concrete example
4. Key points to remember

Topic:
{topic}
"""
    try:
        return generate_text(prompt, temperature=0.25, max_output_tokens=1000) + fallback_note
    except Exception as exc:
        return f"Unable to explain the topic right now: {exc}"
