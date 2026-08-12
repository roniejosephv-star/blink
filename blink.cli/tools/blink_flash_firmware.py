#!/usr/bin/env python3
import sys
import os
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import ndjson_protocol

def flash_firmware(port, firmware_path, address=None, erase=False):
    """
    Run esptool write_flash to flash the firmware.
    """
    if not address:
        # We need to detect chip and look up address
        python_exe = sys.executable
        # 1. Detect chip
        try:
            cmd_detect = [python_exe, os.path.join(current_dir, "blink_flash_detect_chip.py"), "--port", port]
            res_detect = subprocess.run(cmd_detect, capture_output=True, text=True, check=True)
            chip_type = "ESP32" # fallback
            import json
            for line in res_detect.stdout.splitlines():
                try:
                    data = json.loads(line)
                    if data.get("type") == "result":
                        chip_type = data.get("data", {}).get("chip_type", "ESP32")
                except:
                    pass
            
            # 2. Get address
            cmd_addr = [python_exe, os.path.join(current_dir, "blink_flash_address.py"), "--chip", chip_type]
            res_addr = subprocess.run(cmd_addr, capture_output=True, text=True, check=True)
            address = "0x1000" # fallback
            for line in res_addr.stdout.splitlines():
                try:
                    data = json.loads(line)
                    if data.get("type") == "result":
                        address = data.get("data", {}).get("flash_address", "0x1000")
                except:
                    pass
        except subprocess.CalledProcessError as e:
            ndjson_protocol.emit_error("detect_failed", "Failed to detect chip for address lookup", recoverable=True)
            return

    cmd = [
        sys.executable, "-m", "esptool",
        "--port", port,
        "--baud", "460800"
    ]
    
    if erase:
        # Erase flash first
        erase_cmd = cmd + ["erase_flash"]
        try:
            ndjson_protocol.emit_progress("flash_erase", 0, f"Erasing flash on {port}...")
            subprocess.run(erase_cmd, capture_output=True, text=True, check=True)
            ndjson_protocol.emit_progress("flash_erase", 100, "Flash erased successfully.")
        except subprocess.CalledProcessError as e:
            ndjson_protocol.emit_error("erase_failed", f"esptool erase failed: {e.stderr}", recoverable=True)
            return
            
    # Write flash
    write_cmd = cmd + [
        "write_flash",
        "-z",
        "--flash_mode", "keep",
        "--flash_size", "detect",
        "--flash_freq", "keep",
        address, firmware_path
    ]
    
    try:
        ndjson_protocol.emit_progress("flash_write", 0, f"Flashing {os.path.basename(firmware_path)} to {address}...")
        
        # Use Popen to stream output
        process = subprocess.Popen(write_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            # Detect manual bootloader requirement
            if "Connecting..." in line or "_____" in line:
                ndjson_protocol.emit_progress("flash_write", 0, "Connecting to bootloader... (Hold BOOT button if it hangs)")
                ndjson_protocol.emit_result({"action_required": "manual_bootloader", "message": "Please hold the BOOT button on your device"})
            # Simple progress estimation based on percentage in esptool output
            elif "%" in line:
                try:
                    pct_str = line.split("%")[0].split()[-1]
                    pct = int(pct_str)
                    ndjson_protocol.emit_progress("flash_write", pct, f"Writing... {pct}%")
                except:
                    pass
                    
        process.wait()
        
        if process.returncode == 0:
            ndjson_protocol.emit_result({"status": "success", "port": port})
        else:
            stderr = process.stderr.read()
            ndjson_protocol.emit_error("flash_failed", f"esptool write failed: {stderr}", recoverable=True)
            
    except Exception as e:
        ndjson_protocol.emit_error("unknown_error", str(e), recoverable=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Flash firmware to ESP device")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--firmware", required=True, help="Path to .bin file")
    parser.add_argument("--address", help="Start address (default: auto)")
    parser.add_argument("--erase", action="store_true", help="Erase flash before writing")
    args = parser.parse_args()
    
    flash_firmware(args.port, args.firmware, args.address, args.erase)
