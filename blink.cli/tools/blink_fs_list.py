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

def list_fs(port, remote_path="/"):
    ndjson_protocol.emit_progress("fs_list", 0, f"Connecting to {port} to list {remote_path}...")
    try:
        connection = serial_connection.SerialConnection(port, dtr=False, rts=False)
        manager = bare_metal_target.BareMetalTargetManager(
            connection,
            submit_mode=None, write_block_size=None, write_block_delay=None,
            uses_local_time=False, clean=False, cwd=None, interrupt=True, minny_cache_dir=None,
        )
        manager.start()
        
        ndjson_protocol.emit_progress("fs_list", 50, "Reading filesystem...")
        
        # We can use minny's fs functions if available, or just execute code.
        # execute os.listdir() and os.stat()
        code = f"""
import os
import ujson
res = []
try:
    for f in os.listdir('{remote_path}'):
        st = os.stat('{remote_path}/' + f if '{remote_path}' != '/' else '/' + f)
        res.append({{"name": f, "size": st[6], "is_dir": st[0] & 0x4000 != 0}})
except OSError as e:
    pass
print(ujson.dumps(res))
"""
        res = manager.submit_code(code)
        manager.close()
        
        import json
        files = []
        if res.out.strip():
            try:
                files = json.loads(res.out.strip())
            except json.JSONDecodeError:
                pass
                
        ndjson_protocol.emit_progress("fs_list", 100, "Filesystem read.")
        ndjson_protocol.emit_result({
            "port": port,
            "path": remote_path,
            "files": files
        })
        
    except Exception as e:
        ndjson_protocol.emit_error("fs_list_failed", str(e), recoverable=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="List files on device")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--path", default="/", help="Remote path to list")
    args = parser.parse_args()
    list_fs(args.port, args.path)
