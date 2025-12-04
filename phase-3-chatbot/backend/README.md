# Todo Backend

FastAPI backend for Evolution of Todo Phase 2.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Run

```bash
uvicorn src.main:app --reload --port 8000
```

## Test

```bash
pytest -v
```
