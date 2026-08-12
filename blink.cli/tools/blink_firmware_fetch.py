#!/usr/bin/env python3
import sys
import os
import urllib.request

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import ndjson_protocol

def download_firmware(url, dest_path):
    ndjson_protocol.emit_progress("firmware_fetch", 0, f"Starting download from {url}...")
    try:
        req = urllib.request.urlopen(url)
        total_size = req.info().get('Content-Length')
        
        if total_size is not None:
            total_size = int(total_size)
            
        downloaded = 0
        chunk_size = 8192
        
        with open(dest_path, 'wb') as f:
            while True:
                buffer = req.read(chunk_size)
                if not buffer:
                    break
                f.write(buffer)
                downloaded += len(buffer)
                if total_size:
                    pct = int((downloaded / total_size) * 100)
                    ndjson_protocol.emit_progress("firmware_fetch", pct, f"Downloading... {pct}% ({downloaded}/{total_size} bytes)")
                else:
                    ndjson_protocol.emit_progress("firmware_fetch", 50, f"Downloading... {downloaded} bytes")
                    
        ndjson_protocol.emit_progress("firmware_fetch", 100, "Download complete.")
        ndjson_protocol.emit_result({
            "status": "success",
            "file_path": dest_path,
            "bytes_downloaded": downloaded
        })
        
    except Exception as e:
        ndjson_protocol.emit_error("download_error", f"Failed to download firmware: {str(e)}", recoverable=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download firmware to local path")
    parser.add_argument("--url", required=True, help="URL to download from")
    parser.add_argument("--dest", required=True, help="Destination path for .bin file")
    args = parser.parse_args()
    
    download_firmware(args.url, args.dest)
