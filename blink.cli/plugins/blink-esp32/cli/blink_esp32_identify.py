#!/usr/bin/env python3
"""
tinkr-esp32-identify — Identify the exact chip on a connected ESP32 port.

NDJSON output on stdout. Streaming-friendly.

Usage:
    tinkr-esp32-identify --port /dev/cu.usbserial-1410
"""
import sys
import os
import argparse
import json

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


# Flash start address by chip family (from Thonny / esptool).
CHIP_TO_ADDRESS = {
    "esp32":   "0x1000",
    "esp32s2": "0x1000",
    "esp8266": "0x0",
    "esp32s3": "0x0",
    "esp32c3": "0x0",
    "esp32c6": "0x0",
    "esp32c2": "0x0",
}


def identify_chip(port: str) -> dict:
    """Run esptool chip_id to identify the chip on the given port."""
    ndjson_protocol.emit_progress("identify", 10, f"Opening {port}...")
    try:
        import esptool  # type: ignore
    except ImportError:
        ndjson_protocol.emit_error(
            "esptool_missing",
            "esptool is required. Install with: pip install esptool>=5.2",
            recoverable=True,
            suggestion="pip install esptool",
        )

    # esptool exposes a high-level API. We invoke it via the CLI in a subprocess
    # to keep this script simple and to match the existing tinkr.cli pattern.
    ndjson_protocol.emit_progress("identify", 30, "Running esptool chip_id...")
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, "-m", "esptool", "--port", port, "chip_id"],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        ndjson_protocol.emit_error(
            "identify_timeout",
            f"esptool chip_id timed out on {port}",
            recoverable=True,
            suggestion="Hold the BOOT button on the device if it hangs.",
        )
    except FileNotFoundError:
        ndjson_protocol.emit_error(
            "esptool_missing",
            "esptool is not installed in this Python environment.",
            recoverable=True,
            suggestion="pip install esptool>=5.2",
        )

    if result.returncode != 0:
        ndjson_protocol.emit_error(
            "identify_failed",
            f"esptool chip_id failed: {result.stderr.strip()}",
            recoverable=True,
            suggestion="Hold the BOOT button or check the cable.",
        )

    # Parse esptool output. Example:
    #   "Chip is ESP32-S3 (revision v0.2)"
    #   "MAC: aa:bb:cc:dd:ee:ff"
    #   "Chip ID: 0x12345678"
    chip = None
    chip_id = None
    mac = None
    flash_size = None
    for line in result.stdout.splitlines():
        if "Chip is" in line:
            # "Chip is ESP32-S3 (revision v0.2)"
            parts = line.split("Chip is ", 1)[1].split(" ")
            chip = parts[0].lower()
        elif "Chip ID:" in line:
            chip_id = line.split("Chip ID: ")[1].strip()
        elif "MAC:" in line:
            mac = line.split("MAC: ")[1].strip()
        elif "Detected flash size:" in line:
            flash_size = line.split("Detected flash size: ")[1].strip()

    if not chip:
        ndjson_protocol.emit_error(
            "unknown_chip",
            f"Could not parse chip from esptool output: {result.stdout!r}",
            recoverable=True,
            suggestion="Update esptool or check the device.",
        )

    family = chip.replace("-", "")  # "esp32-s3" -> "esp32s3"
    flash_address = CHIP_TO_ADDRESS.get(family, "0x0")

    return {
        "chip": chip,
        "family": family,
        "chip_id": chip_id,
        "mac": mac,
        "flash_size": flash_size,
        "flash_address": flash_address,
        "port": port,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Identify an ESP32 chip on a serial port")
    parser.add_argument("--port", required=True, help="Serial port (e.g., /dev/cu.usbserial-1410)")
    args = parser.parse_args()

    ndjson_protocol.emit_progress("identify", 0, f"Identifying chip on {args.port}...")
    info = identify_chip(args.port)
    ndjson_protocol.emit_progress("identify", 100, f"Identified {info['chip']}.")
    ndjson_protocol.emit_result(info)


if __name__ == "__main__":
    main()
