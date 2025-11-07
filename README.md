# String Analyzer (minimal)

A small FastAPI service that analyzes strings and exposes a simple HTTP API.

Quick start (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn string-analyzer.app.main:app --reload
```

Open http://127.0.0.1:8000/docs to see the API docs.

Project layout:

- `string-analyzer/app/` — FastAPI app and routes
- `string-analyzer/models/` — DB helpers
- `string-analyzer/utils/` — analysis and filter logic
- `tests/` — simple HTTP examples

Notes:
- If you need deployment instructions (Heroku/Railway), re-add them separately.
- Keep `.env` out of source control; use `.env.example` as the template.

License: MIT

