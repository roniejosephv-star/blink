#!/usr/bin/env python3
"""
tinkr-esp32-port-scan — Scan all serial ports for ESP32-family devices.

NDJSON output on stdout, following the Tinkr protocol (see
architecture/plugin_spec.md#4-cli-tool-contract and lib/ndjson_protocol.py).

Invokable by hand:
    tinkr-esp32-port-scan

Invokable via the Tinkr runtime:
    tinkr runtime tool invoke tinkr-esp32-port-scan

Invokable via MCP (auto-derived):
    esp32.port_scan()
"""
import sys
import os

# Make the plugin's lib directory importable for ndjson_protocol.
# In a packaged install, Tinkr core's ndjson_protocol is used instead.
_PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PLUGIN_LIB = os.path.join(_PLUGIN_ROOT, "..", "..", "..", "lib")
if os.path.isdir(_PLUGIN_LIB) and _PLUGIN_LIB not in sys.path:
    sys.path.insert(0, _PLUGIN_LIB)
# Fallback: a local copy of the NDJSON emitter for offline use.
elif os.path.isdir(os.path.join(_PLUGIN_ROOT, "lib")) and os.path.join(_PLUGIN_ROOT, "lib") not in sys.path:
    sys.path.insert(0, os.path.join(_PLUGIN_ROOT, "lib"))

try:
    import ndjson_protocol
except ImportError:
    # Minimal fallback so the script remains self-contained.
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


# Espressif and common USB-to-UART bridge VID/PIDs (from Thonny's esp/__init__.py).
ESP32_VIDS_PIDS = {
    (0x303A, None),    # Espressif native USB (ESP32-S2/S3/C3/C6)
    (0x10C4, 0xEA60),  # Silicon Labs CP210x
    (0x1A86, 0x7523),  # WCH CH340/CH341
    (0x0403, None),    # FTDI (any PID)
    (0x2E8A, None),    # Raspberry Pi Pico (RP2040)
}

# Text-matching keywords from Thonny's is_potential_port().
TEXT_KEYWORDS = ("usb", "serial", "uart", "daplink", "stlink", "python",
                 "m5stack", "esp32", "micropython")
EXCLUDE_KEYWORDS = ("circuitpython cdc2",)  # CDC2 is the CircuitPython data interface, not REPL.


def is_esp32_port(port) -> bool:
    """Return True if a pyserial port looks like an ESP32-family device."""
    desc = (port.description or "").lower()
    manuf = (port.manufacturer or "").lower()
    interface = (port.interface or "").lower()

    # 1. Exclude known non-REPL interfaces.
    for ex in EXCLUDE_KEYWORDS:
        if ex in interface:
            return False

    # 2. VID/PID match.
    if hasattr(port, "vid") and hasattr(port, "pid"):
        if (port.vid, port.pid) in ESP32_VIDS_PIDS:
            return True
        if (port.vid, None) in ESP32_VIDS_PIDS:
            return True

    # 3. Text matching.
    for kw in TEXT_KEYWORDS:
        if kw in desc or kw in manuf:
            return True
    if "circuitpython" in desc:
        return False  # CircuitPython boards are not ESP32-family.
    return False


def scan_ports() -> list[dict]:
    """Enumerate serial ports and return the list that look like ESP32-family devices."""
    try:
        from serial.tools import list_ports
    except ImportError:
        ndjson_protocol.emit_error(
            "pyserial_missing",
            "pyserial is required. Install with: pip install pyserial>=3.4",
            recoverable=True,
            suggestion="pip install pyserial",
        )

    detected = []
    for port in list_ports.comports():
        if is_esp32_port(port):
            detected.append({
                "port": port.device,
                "vid": f"0x{port.vid:04X}" if port.vid else None,
                "pid": f"0x{port.pid:04X}" if port.pid else None,
                "description": port.description,
                "manufacturer": port.manufacturer,
                "interface": port.interface,
            })
    return detected


def main() -> None:
    ndjson_protocol.emit_progress("port_scan", 0, "Scanning serial ports for ESP32-family devices...")
    detected = scan_ports()
    ndjson_protocol.emit_progress("port_scan", 100, f"Found {len(detected)} ESP32 device(s).")
    ndjson_protocol.emit_result({
        "count": len(detected),
        "devices": detected,
    })


if __name__ == "__main__":
    main()
