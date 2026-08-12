import json
import sys

def emit_progress(stage, pct, message):
    """Emit a progress update to stdout in NDJSON format."""
    payload = {
        "type": "progress",
        "stage": stage,
        "pct": pct,
        "message": message
    }
    print(json.dumps(payload))
    sys.stdout.flush()

def emit_result(data):
    """Emit a successful result to stdout in NDJSON format."""
    payload = {
        "type": "result",
        "status": "ok",
        "data": data
    }
    print(json.dumps(payload))
    sys.stdout.flush()

def emit_error(code, message, recoverable=False, suggestion=""):
    """Emit an error to stdout in NDJSON format and exit."""
    payload = {
        "type": "error",
        "code": code,
        "message": message,
        "recoverable": recoverable,
        "suggestion": suggestion
    }
    print(json.dumps(payload))
    sys.stdout.flush()
    sys.exit(1)

def request_feedback(prompt_id, prompt_message, options=None, default=None):
    """
    Emit a user feedback request to stderr in NDJSON format.
    The Rust orchestrator captures this and presents it to the user.
    """
    payload = {
        "type": "user_feedback",
        "id": prompt_id,
        "prompt": prompt_message,
        "options": options or [],
        "default": default
    }
    print(json.dumps(payload), file=sys.stderr)
    sys.stderr.flush()

def read_user_response():
    """
    Wait for and read the user's response from stdin (provided by the Rust orchestrator).
    Expects a single JSON line.
    """
    line = sys.stdin.readline()
    if not line:
        return None
    try:
        return json.loads(line.strip())
    except json.JSONDecodeError:
        return None
