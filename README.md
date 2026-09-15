# code_learning

A small Python + Flask starter app used as a learning sandbox. It serves a
"Learning Notes" page backed by an in-memory store plus a small JSON API, so the
development environment can be exercised end to end.

## Requirements

- Python 3.12+

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

## Run

```bash
.venv/bin/flask --app app run --host 0.0.0.0 --port 5000
```

Then open http://localhost:5000.

## Test

```bash
.venv/bin/pytest
```

## API

| Method | Path          | Description                      |
| ------ | ------------- | -------------------------------- |
| GET    | `/`           | Learning Notes web page          |
| GET    | `/api/health` | Health check (`{"status":"ok"}`) |
| GET    | `/api/notes`  | List all notes                   |
| POST   | `/api/notes`  | Create a note (`{"text": "..."}`)|

## Cloud Agent environment

`.cursor/environment.json` configures the Cursor Cloud Agent environment:

- `install` creates a virtualenv and installs dependencies.
- `terminals.web` starts the Flask dev server on port 5000.
