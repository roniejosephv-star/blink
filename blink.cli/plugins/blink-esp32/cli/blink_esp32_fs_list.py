#!/usr/bin/env python3
"""
tinkr-esp32-fs-list — List files on the ESP32's internal filesystem.

NDJSON output on stdout.

Usage:
    tinkr-esp32-fs-list --port /dev/cu.usbserial-1410 --path /
    tinkr-esp32-fs-list --port /dev/cu.usbserial-1410 --path /lib
"""
import sys
import os
import argparse

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


def fs_list(port: str, path: str) -> list[dict]:
    """List files on the device's filesystem at the given path."""
    try:
        from minny import bare_metal_target, serial_connection  # type: ignore
    except ImportError:
        ndjson_protocol.emit_error(
            "minny_missing",
            "minny is required. Install with: pip install minny>=0.13",
            recoverable=True,
            suggestion="pip install minny",
        )

    ndjson_protocol.emit_progress("fs_list", 0, f"Opening {port}...")
    connection = serial_connection.SerialConnection(port, dtr=False, rts=False)
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

    # Device-side code: listdir + stat each entry, print as JSON.
    code = f"""
import json as _json
import os as _os
try:
    _names = _os.listdir({path!r})
    _entries = []
    for _n in _names:
        try:
            _st = _os.stat({path!r} + _n if {path!r} != '/' else '/' + _n)
            _entries.append({{
                "name": _n,
                "type": "dir" if (_st[0] & 0o170000) == 0o040000 else "file",
                "size": _st[6] if len(_st) > 6 else 0,
            }})
        except Exception as _e:
            _entries.append({{"name": _n, "type": "unknown", "error": str(_e)}})
    print(_json.dumps({{"type": "result", "status": "ok", "data": _entries}}))
except Exception as _e:
    print(_json.dumps({{"type": "error", "code": "fs_list_failed", "message": str(_e)}}))
"""

    ndjson_protocol.emit_progress("fs_list", 50, f"Listing {path} on {port}...")
    out, err = manager._execute(code, capture_output=True)

    import json as _json
    entries = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msg = _json.loads(line)
            if msg.get("type") == "result":
                entries = msg.get("data", [])
                break
            elif msg.get("type") == "error":
                ndjson_protocol.emit_error(
                    msg.get("code", "fs_list_failed"),
                    msg.get("message", "Unknown error"),
                    recoverable=True,
                )
        except _json.JSONDecodeError:
            continue

    ndjson_protocol.emit_progress("fs_list", 100, f"Found {len(entries)} entries.")
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="List files on an ESP32's filesystem")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--path", default="/", help="Path on the device (default: /)")
    args = parser.parse_args()

    entries = fs_list(args.port, args.path)
    ndjson_protocol.emit_result({
        "path": args.path,
        "port": args.port,
        "entries": entries,
    })


if __name__ == "__main__":
    main()
