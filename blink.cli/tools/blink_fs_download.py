#!/usr/bin/env python3
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import ndjson_protocol

try:
    from minny import bare_metal_target, serial_connection
except ImportError:
    ndjson_protocol.emit_error("minny_missing", "minny package is not installed.", recoverable=False)

def download_file(port, remote_path, local_path):
    ndjson_protocol.emit_progress("fs_download", 0, f"Connecting to {port} to download {remote_path} to {local_path}...")
    try:
        connection = serial_connection.SerialConnection(port, dtr=False, rts=False)
        manager = bare_metal_target.BareMetalTargetManager(
            connection,
            submit_mode=None, write_block_size=None, write_block_delay=None,
            uses_local_time=False, clean=False, cwd=None, interrupt=True, minny_cache_dir=None,
        )
        manager.start()
        
        ndjson_protocol.emit_progress("fs_download", 50, f"Reading from {remote_path} on device...")
        
        # Use manager's read_file
        content = manager.read_file(remote_path)
        
        manager.close()
        
        ndjson_protocol.emit_progress("fs_download", 80, f"Writing local file {local_path}...")
        with open(local_path, "wb") as f:
            f.write(content)
            
        ndjson_protocol.emit_progress("fs_download", 100, "Download complete.")
        
        ndjson_protocol.emit_result({
            "status": "success",
            "port": port,
            "remote_path": remote_path,
            "local_path": local_path,
            "bytes_read": len(content)
        })
        
    except Exception as e:
        ndjson_protocol.emit_error("fs_download_failed", str(e), recoverable=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download file from device")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--remote", required=True, help="Remote path to read")
    parser.add_argument("--local", required=True, help="Local path to download to")
    args = parser.parse_args()
    download_file(args.port, args.remote, args.local)
