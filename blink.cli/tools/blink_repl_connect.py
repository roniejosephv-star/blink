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
    ndjson_protocol.emit_error("minny_missing", "minny package is not installed in the environment.", recoverable=False)

def connect_repl(port):
    """
    Connect to the MicroPython REPL to verify device health.
    Handles DTR/RTS boot loops internally via minny.
    """
    ndjson_protocol.emit_progress("repl_connect", 0, f"Opening serial connection to {port}...")
    
    try:
        # 1. Initialize serial connection
        # Setting dtr=False, rts=False prevents the ESP32 from entering a bootloop
        connection = serial_connection.SerialConnection(port, dtr=False, rts=False)
        
        # 2. Initialize target manager
        manager = bare_metal_target.BareMetalTargetManager(
            connection,
            submit_mode=None,
            write_block_size=None,
            write_block_delay=None,
            uses_local_time=False,
            clean=False,
            cwd=None,
            interrupt=True,
            minny_cache_dir=None,
        )
        
        ndjson_protocol.emit_progress("repl_connect", 50, "Synchronizing with REPL state machine...")
        
        # Optionally, run a quick command to get the version
        out, err = manager._execute("import sys; import os; print(sys.implementation.name, sys.version, os.uname().machine)", capture_output=True)
        
        ndjson_protocol.emit_progress("repl_connect", 100, "REPL connected successfully.")
        
        ndjson_protocol.emit_result({
            "status": "connected",
            "port": port,
            "sys_info": out.strip()
        })
        
    except Exception as e:
        ndjson_protocol.emit_error("repl_failed", f"Failed to connect to REPL: {str(e)}", recoverable=True, suggestion="Ensure firmware is flashed and device is not in bootloop.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Verify REPL connection to ESP device")
    parser.add_argument("--port", required=True, help="Serial port")
    args = parser.parse_args()
    
    connect_repl(args.port)
