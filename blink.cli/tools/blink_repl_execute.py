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

def execute_code(port, code):
    """
    Connect to REPL and execute Python code using raw paste mode.
    """
    ndjson_protocol.emit_progress("repl_execute", 0, f"Connecting to {port} for execution...")
    
    try:
        # Setting dtr=False, rts=False prevents the ESP32 from entering a bootloop
        connection = serial_connection.SerialConnection(port, dtr=False, rts=False)
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
        ndjson_protocol.emit_progress("repl_execute", 50, "Executing code payload...")
        
        # Execute code
        out, err = manager._execute(code, capture_output=True)
        
        ndjson_protocol.emit_progress("repl_execute", 100, "Execution complete.")
        
        ndjson_protocol.emit_result({
            "status": "success",
            "port": port,
            "stdout": out,
            "stderr": err,
            "error": None
        })
        
    except Exception as e:
        ndjson_protocol.emit_error("execution_failed", f"Failed to execute code: {str(e)}", recoverable=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Execute Python code on ESP device via REPL")
    parser.add_argument("--port", required=True, help="Serial port")
    parser.add_argument("--code", required=True, help="Python code to execute")
    args = parser.parse_args()
    
    execute_code(args.port, args.code)
