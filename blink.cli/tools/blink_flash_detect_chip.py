#!/usr/bin/env python3
import sys
import os
import subprocess
import json

# Add the lib directory to path to import ndjson_protocol
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import ndjson_protocol

def detect_chip(port):
    """Run esptool chip_id to detect the exact chip family."""
    # Find esptool executable in the same venv or system path
    python_exe = sys.executable
    cmd = [python_exe, "-m", "esptool", "--port", port, "chip_id"]
    
    try:
        ndjson_protocol.emit_progress("detect_chip", 10, f"Running esptool on {port}...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Parse esptool output
        chip_type = "unknown"
        mac = "unknown"
        raw_output = ""
        
        for line in process.stdout:
            raw_output += line
            # Detect manual bootloader requirement
            if "Connecting..." in line or "_____" in line:
                ndjson_protocol.emit_progress("detect_chip", 0, "Connecting to bootloader... (Hold BOOT button if it hangs)")
                ndjson_protocol.emit_result({"action_required": "manual_bootloader", "message": "Please hold the BOOT button on your device"})
                
            if line.startswith("Detecting chip type... "):
                chip_type = line.replace("Detecting chip type... ", "").strip()
            elif line.startswith("MAC: "):
                mac = line.replace("MAC: ", "").strip()
            elif line.startswith("Chip is "):
                chip_type = line.replace("Chip is ", "").split(" ")[0].strip()
                
        process.wait()
        
        if process.returncode == 0:
            ndjson_protocol.emit_progress("detect_chip", 100, "Chip detected successfully.")
            ndjson_protocol.emit_result({
                "port": port,
                "chip_type": chip_type,
                "mac": mac,
                "raw_output": raw_output
            })
        else:
            stderr = process.stderr.read()
            ndjson_protocol.emit_error("esptool_error", f"esptool failed: {stderr}", recoverable=True, suggestion="Ensure the device is in bootloader mode or check the cable.")
            
    except Exception as e:
        ndjson_protocol.emit_error("unknown_error", str(e), recoverable=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Detect ESP chip type via esptool")
    parser.add_argument("--port", required=True, help="Serial port of the device")
    args = parser.parse_args()
    
    detect_chip(args.port)
