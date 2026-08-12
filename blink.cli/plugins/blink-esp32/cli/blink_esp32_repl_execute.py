#!/usr/bin/env python3
"""
tinkr-esp32-repl-execute — Execute Python code on an ESP32 via raw paste mode.

NDJSON output on stdout. Streams progress events.

Usage:
    tinkr-esp32-repl-execute --port /dev/cu.usbserial-1410 --code "print('hello')"
    tinkr-esp32-repl-execute --port /dev/cu.usbserial-1410 --file script.py
"""
import sys
import os
import argparse
import time

_PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PLUGIN_LIB = os.path.join(_PLUGIN_ROOT, "..", "..", "..", "lib")
if os.path.isdir(_PLUGIN_LIB) and _PLUGIN_LIB not in sys.path:
    sys.path.insert(0, _PLUGIN_LIB)
elif os.path.isdir(os.path.join(_PLUGIN_ROOT, "lib")) and os.path.join(_PLUGIN_ROOT, "lib") not in sys.path:
    sys.path.insert(0, os.path.join(_PLUGIN_ROOT, "lib"))

try:
    import ndjson_protocol
except ImportError:
    import json as _json

    class _Fallback:
        @staticmethod
        def emit_result(data):
            print(_json.dumps({"type": "result", "status": "ok", "data": data}))
            sys.stdout.flush()

        @staticmethod
        def emit_progress(stage, pct, message):
            print(_json.dumps({"type": "progress", "stage": stage, "pct": pct, "message": message}))
            sys.stdout.flush()

        @staticmethod
        def emit_error(code, message, recoverable=True, suggestion=""):
            print(_json.dumps({
                "type": "error", "code": code, "message": message,
                "recoverable": recoverable, "suggestion": suggestion,
            }))
            sys.stdout.flush()
            sys.exit(1)

    ndjson_protocol = _Fallback()


def execute_code(port: str, code: str) -> dict:
    """Execute a snippet of Python code on the device using minny's raw paste mode."""
    try:
        from minny import bare_metal_target, serial_connection  # type: ignore
    except ImportError:
        ndjson_protocol.emit_error(
            "minny_missing",
            "minny is required for REPL execution. Install with: pip install minny>=0.13",
            recoverable=True,
            suggestion="pip install minny",
        )

    ndjson_protocol.emit_progress("repl_open", 0, f"Opening serial connection to {port}...")
    try:
        connection = serial_connection.SerialConnection(port, dtr=False, rts=False)
    except Exception as e:
        ndjson_protocol.emit_error(
            "repl_open_failed",
            f"Failed to open {port}: {e}",
            recoverable=True,
            suggestion="Check the cable, port permissions, and that no other app has the port open.",
        )

    manager = bare_metal_target.BareMetalTargetManager(
        connection,
        submit_mode=None,
        write_block_size=None,
        write_block_delay=None,
        uses_local_time=False,
        clean=False,
        cwd=None,
        interrupt=True,
        minny_cache_dir=None,
    )

    ndjson_protocol.emit_progress("repl_execute", 50, "Sending code via raw paste mode...")
    start_ms = int(time.time() * 1000)
    try:
        out, err = manager._execute(code, capture_output=True)
    except Exception as e:
        ndjson_protocol.emit_error(
            "repl_execute_failed",
            f"Failed to execute code: {e}",
            recoverable=True,
            suggestion="Try sending Ctrl+C first, or reset the device.",
        )
    duration_ms = int(time.time() * 1000) - start_ms

    ndjson_protocol.emit_progress("repl_execute", 100, "Execution complete.")
    return {
        "stdout": out,
        "stderr": err,
        "duration_ms": duration_ms,
        "port": port,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute Python code on an ESP32")
    parser.add_argument("--port", required=True, help="Serial port")
    code_group = parser.add_mutually_exclusive_group(required=True)
    code_group.add_argument("--code", help="Inline Python code")
    code_group.add_argument("--file", help="Path to a .py file")
    args = parser.parse_args()

    if args.code:
        code = args.code
    else:
        with open(args.file) as f:
            code = f.read()

    result = execute_code(args.port, code)
    ndjson_protocol.emit_result(result)


if __name__ == "__main__":
    main()
