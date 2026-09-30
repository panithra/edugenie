# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS learning assistant implementing the project specification:

- Q&A
- Beginner-friendly concept explanation
- 3-question / 4-option quiz generation
- Educational passage summarization
- Beginner-to-advanced learning recommendations

## Architecture

```text
EduGenie/
├── main.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── tests/
│   └── test_api.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
└── .gitignore
```

The supplied project document describes FastAPI, HTML/CSS, Gemini for Q&A/quiz/summary/learning paths, and LaMini-Flan-T5 for concept explanation. This implementation keeps that modular architecture. Because local transformer models are large, the default setup uses Gemini for explanations; `USE_LOCAL_EXPLAINER=true` enables the LaMini path after installing `requirements-local.txt`.

## 1. Open in VS Code

Open this `EduGenie` folder in VS Code and open **Terminal → New Terminal**.

## 2. Create a virtual environment (Windows PowerShell)

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

If `py` is unavailable, use:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and set:

```env
GEMINI_API_KEY=your_real_api_key
```

Do not commit `.env` to Git.

## 5. Run

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API health check:

```text
http://127.0.0.1:8000/health
```

## 6. Test

Run:

```powershell
pytest -q
```

Then manually test all five UI tasks:

1. Ask a question — `Which is the largest ocean?`
2. Explain — `Pythagoras theorem`
3. Quiz — paste a short passage or topic
4. Summarize — paste a paragraph
5. Learning path — `SQL`

## API examples

### Q&A

```powershell
Invoke-RestMethod http://127.0.0.1:8000/qa `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"What is photosynthesis?"}'
```

### Explanation

```powershell
Invoke-RestMethod http://127.0.0.1:8000/explain `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Explain the Pythagoras theorem"}'
```

### Quiz

```powershell
Invoke-RestMethod http://127.0.0.1:8000/quiz `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Photosynthesis is the process by which plants convert light energy into chemical energy."}'
```

### Summary

```powershell
Invoke-RestMethod http://127.0.0.1:8000/summarize `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Paste your educational passage here."}'
```

### Learning path

```powershell
Invoke-RestMethod http://127.0.0.1:8000/learn/recommendations `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"SQL"}'
```

## Optional LaMini-Flan-T5 local explanation

The original specification names `MBZUAI/LaMini-Flan-T5-783M` for the explanation module.

Install the additional packages:

```powershell
pip install -r requirements-local.txt
```

Then change `.env`:

```env
USE_LOCAL_EXPLAINER=true
```

The first local explanation can take time because the model needs to be downloaded. If local loading fails, the application automatically falls back to Gemini.

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Make sure `.env` exists in the project root and contains a valid key. Restart Uvicorn after changing environment settings.

### `python` command not found
Install Python 3.10+ and enable **Add Python to PATH**, then reopen VS Code.

### PowerShell blocks activation
Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again.

### Gemini model error
Set `GEMINI_MODEL` in `.env` to a Gemini model currently available to your API key.

### Port 8000 is busy
Run:

```powershell
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Security notes

- Never put the Gemini API key in `index.html` or JavaScript.
- Keep the key only in `.env`.
- Do not commit `.env`.
- For production, add authentication, rate limiting, logging controls, request-size limits, and a proper secret manager.

## Source alignment

The project follows the supplied EduGenie document's stated modules and endpoints while updating the Gemini integration to the current `google-genai` Python SDK style.
