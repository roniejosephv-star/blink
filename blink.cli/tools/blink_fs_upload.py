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

def upload_file(port, local_path, remote_path):
    ndjson_protocol.emit_progress("fs_upload", 0, f"Connecting to {port} to upload {local_path} to {remote_path}...")
    try:
        connection = serial_connection.SerialConnection(port, dtr=False, rts=False)
        manager = bare_metal_target.BareMetalTargetManager(
            connection,
            submit_mode=None, write_block_size=None, write_block_delay=None,
            uses_local_time=False, clean=False, cwd=None, interrupt=True, minny_cache_dir=None,
        )
        manager.start()
        
        ndjson_protocol.emit_progress("fs_upload", 20, f"Reading local file {local_path}...")
        with open(local_path, "rb") as f:
            content = f.read()
            
        ndjson_protocol.emit_progress("fs_upload", 50, f"Writing to {remote_path} on device...")
        
        # Use manager's write_file
        manager.write_file(remote_path, content)
        
        manager.close()
        ndjson_protocol.emit_progress("fs_upload", 100, "Upload complete.")
        
        ndjson_protocol.emit_result({
            "status": "success",
            "port": port,
            "local_path": local_path,
            "remote_path": remote_path,
            "bytes_written": len(content)
        })
        
    except Exception as e:
        ndjson_protocol.emit_error("fs_upload_failed", str(e), recoverable=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Upload file to device")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--local", required=True, help="Local path to upload")
    parser.add_argument("--remote", required=True, help="Remote path to write")
    args = parser.parse_args()
    upload_file(args.port, args.local, args.remote)
