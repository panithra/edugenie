from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        return "Please enter a topic for the learning path."

    prompt = f"""
Create a personalized learning path for the topic below.
Assume the learner is starting from beginner level.
Organize it from beginner to intermediate to advanced.
For each stage, include:
- concepts to learn
- a suggested timeline
- a small practice activity
- resource types such as documentation, videos, articles, or books

Keep it practical and concise. Do not invent specific URLs.
Topic:
{topic}
"""
    try:
        return generate_text(prompt, temperature=0.35, max_output_tokens=1500)
    except Exception as exc:
        return f"Unable to generate a learning path right now: {exc}"
