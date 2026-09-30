from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="Educational assistant with Q&A, explanations, quizzes, summaries and learning paths.",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
  return templates.TemplateResponse(
    request=request,
    name="index.html"
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: dict):
    return {"result": answer_question(payload.get("text", ""))}


@app.post("/explain")
async def explain(payload: dict):
    return {"result": explain_concept(payload.get("text", ""))}


@app.post("/quiz")
async def quiz(payload: dict):
    return {"result": generate_quiz(payload.get("text", ""))}


@app.post("/summarize")
async def summarize(payload: dict):
    return {"result": summarize_text(payload.get("text", ""))}


@app.post("/learn/recommendations")
async def recommendations(payload: dict):
    return {"result": get_learning_recommendations(payload.get("text", ""))}
