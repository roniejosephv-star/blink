#!/usr/bin/env python3
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

# Add mpypkg to path
mpypkg_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "mpypkg", "src")
if mpypkg_dir not in sys.path:
    sys.path.insert(0, mpypkg_dir)

import ndjson_protocol
import subprocess

def install_package(port, package):
    ndjson_protocol.emit_progress("pkg_install", 0, f"Preparing to install {package} to {port}...")
    try:
        # We invoke mpypkg directly via its CLI entry point for simplicity, 
        # or we could use its python API if we inspect it further.
        # Since mpypkg operates on the device via minny/mpytool, we assume it has a cli.
        # Let's use the pre-built mpypkg-cli or a python script.
        mpypkg_cli = os.path.join(os.path.dirname(mpypkg_dir), "mpypkg-cli")
        if not os.path.exists(mpypkg_cli):
            # Fallback to python module execution
            cmd = [sys.executable, "-m", "mpypkg", "install", package, "--port", port]
        else:
            cmd = [mpypkg_cli, "install", package, "--port", port]
            
        ndjson_protocol.emit_progress("pkg_install", 50, f"Running mpypkg install {package}...")
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if res.returncode == 0:
            ndjson_protocol.emit_progress("pkg_install", 100, "Installation complete.")
            ndjson_protocol.emit_result({
                "status": "success",
                "package": package,
                "port": port,
                "output": res.stdout
            })
        else:
            ndjson_protocol.emit_error("pkg_install_failed", f"Failed to install {package}:\n{res.stderr}", recoverable=True)
            
    except Exception as e:
        ndjson_protocol.emit_error("pkg_install_error", str(e), recoverable=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Install MicroPython package to device")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--package", required=True, help="Package name (e.g. micropython-uasyncio)")
    args = parser.parse_args()
    install_package(args.port, args.package)
