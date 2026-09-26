"""Expose the Flora interpreter through a minimal Flask API."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

app = Flask(__name__, static_folder=None)
PROJECT_DIR = Path(__file__).resolve().parent


@app.get("/")
def index():
    """Serve the static Flora front end."""
    return send_from_directory(PROJECT_DIR, "index.html")


@app.get("/style.css")
def stylesheet():
    """Serve the front-end stylesheet."""
    return send_from_directory(PROJECT_DIR, "style.css", mimetype="text/css")


@app.get("/script.js")
def script():
    """Serve the front-end Run handler."""
    return send_from_directory(PROJECT_DIR, "script.js", mimetype="text/javascript")


@app.get("/assets/<path:filename>")
def asset(filename):
    """Serve visual assets used by the front end."""
    return send_from_directory(PROJECT_DIR / "assets", filename)


@app.get("/sfx/<path:filename>")
def sound_effect(filename):
    """Serve audio files used by the front end."""
    return send_from_directory(PROJECT_DIR / "sfx", filename)


@app.post("/run")
def run_flora():
    """Tokenize, parse, and run Flora source provided as JSON."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("source"), str):
        return jsonify(
            success=False,
            error_type="Runtime Error",
            message="Request JSON must include a string 'source' field.",
        ), 400

    try:
        tokens = Lexer(payload["source"]).tokenize()
    except ValueError as error:
        return jsonify(
            success=False,
            error_type="Syntax Error",
            message=str(error),
        )

    try:
        statements = Parser(tokens).parse()
    except SyntaxError as error:
        return jsonify(
            success=False,
            error_type="Syntax Error",
            message=str(error),
        )

    output = StringIO()
    try:
        with redirect_stdout(output):
            Interpreter(statements).run()
    except (RuntimeError, TypeError, ArithmeticError) as error:
        return jsonify(
            success=False,
            error_type="Runtime Error",
            message=str(error),
        )

    return jsonify(success=True, output=output.getvalue().splitlines())


if __name__ == "__main__":
    app.run(debug=True)