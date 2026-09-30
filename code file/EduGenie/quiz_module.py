import json
from gemini_client import generate_json

QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {
                        "type": "array",
                        "minItems": 4,
                        "maxItems": 4,
                        "items": {"type": "string"},
                    },
                    "correct_answer": {"type": "string"},
                    "explanation": {"type": "string"},
                },
                "required": ["question", "options", "correct_answer", "explanation"],
            },
        }
    },
    "required": ["questions"],
}


def generate_quiz(text: str):
    text = text.strip()
    if not text:
        return {"error": "Please enter a topic or passage for the quiz."}

    prompt = f"""
Create exactly 3 multiple-choice questions from the educational input below.
Each question must have exactly 4 options.
The correct_answer must exactly match one option.
Include a short explanation of the correct answer.
Avoid trick questions and keep the questions relevant to the input.

Educational input:
{text}
"""
    try:
        raw = generate_json(prompt, QUIZ_SCHEMA, temperature=0.2, max_output_tokens=1800)
        data = json.loads(raw)
        questions = data.get("questions", [])
        if len(questions) != 3:
            raise ValueError("The model did not return exactly 3 questions.")
        for q in questions:
            if len(q.get("options", [])) != 4:
                raise ValueError("A question did not contain exactly 4 options.")
            if q["correct_answer"] not in q["options"]:
                raise ValueError("A correct answer did not match an option.")
        return data
    except Exception as exc:
        return {"error": f"Quiz generation failed: {exc}"}
