#!/usr/bin/env python3
import sys
import os

# Add the lib directory to path to import ndjson_protocol
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import ndjson_protocol
from serial.tools.list_ports import comports

def scan_ports():
    ports = []
    for p in comports():
        if p.vid is None:
            continue
        # macOS: prefer cu.* over tty.* (doesn't wait for DCD signal)
        if sys.platform == "darwin" and p.device.startswith("/dev/tty."):
            continue
            
        port_data = {
            "port": p.device,
            "vid": p.vid,
            "pid": p.pid,
            "description": p.description,
            "manufacturer": p.manufacturer,
            "product": p.product,
            "serial_number": p.serial_number
        }
        
        # Simple heuristic mapping for known chip families
        if p.vid == 0x303A:
            port_data["chip_family"] = "esp32"
            port_data["board_type"] = "Espressif Native USB"
        elif p.vid == 0x2E8A:
            port_data["chip_family"] = "rp2040"
            port_data["board_type"] = "Raspberry Pi Pico"
        elif p.vid == 0x10C4 and p.pid == 0xEA60:
            port_data["chip_family"] = "esp32/esp8266" # Common for external bridges
            port_data["board_type"] = "CP210x Bridge"
        elif p.vid == 0x1A86 and p.pid == 0x7523:
            port_data["chip_family"] = "esp32/esp8266"
            port_data["board_type"] = "CH340 Bridge"
            
        ports.append(port_data)
        
    ndjson_protocol.emit_result(ports)

if __name__ == "__main__":
    scan_ports()
