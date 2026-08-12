#!/usr/bin/env python3
"""
tinkr-esp32-flash-firmware — Flash firmware to an ESP32-family device.

NDJSON output on stdout. Streams progress events parsed from esptool's output.

Usage:
    tinkr-esp32-flash-firmware --port /dev/cu.usbserial-1410 --firmware ./firmware.bin
    tinkr-esp32-flash-firmware --port /dev/cu.usbserial-1410 --firmware ./firmware.bin --erase
"""
import sys
import os
import argparse
import re
import subprocess

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

    @staticmethod
    def _unused():
        pass

    ndjson_protocol = _Fallback()


_PERCENT_RE = re.compile(r"(\d{1,3})\s*%")


def _parse_pct(line: str) -> int | None:
    """Extract a percentage from an esptool line if present."""
    m = _PERCENT_RE.search(line)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return None
    return None


def flash_firmware(port: str, firmware_path: str, address: str = None,
                   erase: bool = False, baud: int = 460800) -> None:
    """Stream esptool write_flash with progress events."""
    if not os.path.isfile(firmware_path):
        ndjson_protocol.emit_error(
            "firmware_not_found",
            f"Firmware file not found: {firmware_path}",
            recoverable=True,
            suggestion="Check the path. Run `tinkr firmware list` for known variants.",
        )

    if not address:
        # Default to 0x0; the caller can override by running identify first.
        address = "0x0"

    cmd = [
        sys.executable, "-m", "esptool",
        "--port", port,
        "--baud", str(baud),
    ]

    if erase:
        ndjson_protocol.emit_progress("flash_erase", 0, f"Erasing flash on {port}...")
        erase_cmd = cmd + ["erase_flash"]
        try:
            subprocess.run(erase_cmd, capture_output=True, text=True, check=True, timeout=120)
            ndjson_protocol.emit_progress("flash_erase", 100, "Flash erased.")
        except subprocess.CalledProcessError as e:
            ndjson_protocol.emit_error(
                "erase_failed",
                f"esptool erase_flash failed: {e.stderr.strip()}",
                recoverable=True,
                suggestion="Hold the BOOT button if the device is unresponsive.",
            )
        except FileNotFoundError:
            ndjson_protocol.emit_error(
                "esptool_missing",
                "esptool is not installed. pip install esptool>=5.2",
                recoverable=True,
            )

    ndjson_protocol.emit_progress("flash_write", 0, f"Flashing {os.path.basename(firmware_path)} at {address}...")
    write_cmd = cmd + [
        "write_flash",
        "-z",
        "--flash_mode", "keep",
        "--flash_size", "detect",
        "--flash_freq", "keep",
        address, firmware_path,
    ]

    try:
        process = subprocess.Popen(
            write_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        ndjson_protocol.emit_error(
            "esptool_missing",
            "esptool is not installed. pip install esptool>=5.2",
            recoverable=True,
        )

    last_pct = 0
    for line in process.stdout:
        # Detect manual bootloader requirement.
        if "Connecting..." in line or "_____" in line:
            ndjson_protocol.emit_progress("flash_write", last_pct, "Connecting to bootloader... (hold BOOT if it hangs)")
        pct = _parse_pct(line)
        if pct is not None and pct != last_pct:
            last_pct = pct
            ndjson_protocol.emit_progress("flash_write", pct, f"Writing... {pct}%")

    process.wait()
    if process.returncode == 0:
        ndjson_protocol.emit_progress("flash_write", 100, "Flash complete.")
        ndjson_protocol.emit_result({
            "status": "success",
            "port": port,
            "firmware": firmware_path,
            "address": address,
        })
    else:
        stderr = process.stderr.read()
        ndjson_protocol.emit_error(
            "flash_failed",
            f"esptool write_flash failed: {stderr.strip()}",
            recoverable=True,
            suggestion="Check the cable, hold BOOT, or try a lower baud rate.",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Flash firmware to an ESP32")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--firmware", required=True, help="Path to .bin firmware file")
    parser.add_argument("--address", help="Flash start address (default: auto-detect)")
    parser.add_argument("--erase", action="store_true", help="Erase flash before writing")
    parser.add_argument("--baud", type=int, default=460800, help="Baud rate (default: 460800)")
    args = parser.parse_args()

    flash_firmware(args.port, args.firmware, args.address, args.erase, args.baud)


if __name__ == "__main__":
    main()
