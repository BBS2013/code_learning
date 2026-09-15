"""A tiny Flask starter app for the code_learning sandbox.

Serves a small "Learning Notes" web page backed by an in-memory store, plus a
JSON API so the environment can be exercised end to end (create + list records).
"""
from __future__ import annotations

from datetime import datetime, timezone
from itertools import count
from threading import Lock

from flask import Flask, jsonify, render_template, request


def create_app() -> Flask:
    app = Flask(__name__)

    # In-memory note store. Kept simple on purpose: this is a learning sandbox,
    # not a production service, so there is no database dependency to configure.
    notes: list[dict] = []
    ids = count(1)
    lock = Lock()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/notes")
    def list_notes():
        with lock:
            return jsonify(notes=list(notes))

    @app.post("/api/notes")
    def add_note():
        payload = request.get_json(silent=True) or {}
        text = (payload.get("text") or "").strip()
        if not text:
            return jsonify(error="'text' is required"), 400

        note = {
            "id": next(ids),
            "text": text,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with lock:
            notes.append(note)
        return jsonify(note=note), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
