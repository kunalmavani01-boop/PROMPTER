# PROMPTER

PROMPTER is a lightweight prompt optimization and management toolkit with a FastAPI backend and a simple browser UI.

## What is included

- Prompt enhancement endpoint with structured improvement suggestions
- Prompt templates for common workflows
- Version tracking for saved prompts
- Lightweight analytics for prompt improvement runs
- Static dashboard served directly by the API

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## API

- `GET /health`
- `POST /api/enhance`
- `GET /api/templates`
- `GET /api/versions`
- `POST /api/versions`
- `GET /api/versions/{version_id}`
- `GET /api/analytics`

## Project structure

```text
PROMPTER/
|-- docs/
|-- examples/
|-- static/
|-- tests/
|-- main.py
|-- requirements.txt
```

See [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md) and [docs/API.md](./docs/API.md) for usage details.
