from gemini_client import generate_text


def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        return "Please enter a question."

    prompt = f"""
You are EduGenie, a helpful educational assistant.
Answer the student's question accurately and concisely.
Use simple language suitable for a learner.
If the question is ambiguous, state the assumption you made.
Do not invent citations or claim that you checked sources you did not check.

Student question:
{question}
"""
    try:
        return generate_text(prompt, temperature=0.2, max_output_tokens=900)
    except Exception as exc:
        return f"Unable to answer right now: {exc}"
