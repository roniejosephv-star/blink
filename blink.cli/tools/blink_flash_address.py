#!/usr/bin/env python3
import sys
import os

# Add the lib directory to path to import ndjson_protocol
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import ndjson_protocol

def get_flash_address(chip_type):
    """
    Get the default flash address for a given ESP chip type.
    Mappings based on Thonny's esptool_dialog.py logic.
    """
    chip = chip_type.lower()
    address = "0x1000" # Default for ESP32 and ESP32-S3
    
    if "esp8266" in chip:
        address = "0x0"
    elif "esp32-s2" in chip or "esp32s2" in chip:
        address = "0x1000"
    elif "esp32-s3" in chip or "esp32s3" in chip:
        address = "0x0"
    elif "esp32-c2" in chip or "esp32c2" in chip:
        address = "0x0"
    elif "esp32-c3" in chip or "esp32c3" in chip:
        address = "0x0"
    elif "esp32-c6" in chip or "esp32c6" in chip:
        address = "0x0"
    elif "esp32" in chip: # Catch-all for standard ESP32
        address = "0x1000"
    
    ndjson_protocol.emit_result({
        "chip_type": chip_type,
        "flash_address": address
    })

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Get default flash address for ESP chip type")
    parser.add_argument("--chip", required=True, help="Chip type (e.g., ESP32, ESP32-S3)")
    args = parser.parse_args()
    
    get_flash_address(args.chip)
