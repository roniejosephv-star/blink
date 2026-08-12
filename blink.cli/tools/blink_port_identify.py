#!/usr/bin/env python3
import sys
import os
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import ndjson_protocol
from blink_port_scan import scan_ports
from blink_flash_detect_chip import detect_chip

def identify_port(port):
    """
    Run esptool chip_id on the port and return the full device profile.
    """
    # Just call detect_chip and rely on its NDJSON output.
    # In a full flow, Rust handles the JSON, but since this is a CLI tool,
    # we can invoke esptool natively.
    try:
        python_exe = sys.executable
        cmd = [python_exe, os.path.join(current_dir, "blink_flash_detect_chip.py"), "--port", port]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # For simplicity, we just passthrough the output of blink_flash_detect_chip.
        # It already outputs NDJSON format.
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Identify full device context on a port")
    parser.add_argument("--port", required=True, help="Serial port to identify")
    args = parser.parse_args()
    
    identify_port(args.port)
