# Blink CLI

Blink CLI is a robust, Python-based edge integration cluster designed for seamless interaction with microcontrollers and edge devices (primarily targeting ESP32 ecosystems). 

This repository currently houses the stable **Command Line Interface (CLI) Tools**, which serve as the foundational, pluggable modules for device identification, firmware management, filesystem operations, and REPL communication.

## Tool Cluster (`blink.cli/tools`)

All CLI scripts output strictly formatted NDJSON (Newline Delimited JSON), making them highly suitable for programmatic parsing by orchestrators, CI/CD pipelines, or desktop IDE frontends.

### 1. Port & Device Identification
- `blink_port_scan.py`: Scans available serial ports for connected devices.
- `blink_port_identify.py`: Identifies the specific edge device connected to a given port.
- `blink_flash_detect_chip.py`: Detects the exact chip model (e.g., ESP32-S3, ESP8266) via the bootloader.

### 2. Firmware Management
- `blink_firmware_fetch.py`: Downloads specific firmware binaries for the target device.
- `blink_flash_address.py`: Determines the correct flash address for a given chip and firmware type.
- `blink_flash_firmware.py`: Erases and flashes new firmware binaries to the microcontroller.

### 3. File System (FS) Operations
- `blink_fs_list.py`: Lists the contents of the device's internal filesystem.
- `blink_fs_upload.py`: Uploads local files to the device's filesystem.
- `blink_fs_download.py`: Downloads files from the device to the local machine.

### 4. REPL & Execution
- `blink_repl_connect.py`: Validates and establishes a connection to the device's Python REPL.
- `blink_repl_execute.py`: Sends and executes Python code directly on the target device via the REPL.
- `blink_pkg_install.py`: Installs MicroPython/CircuitPython packages directly onto the edge device.

## Architecture & Integration

The CLI tools are designed as independent, pluggable scripts. They do not maintain long-lived state. Instead, they expect inputs as arguments and stream their progress and final results as NDJSON to `stdout`.

*(Note: The Desktop IDE orchestration layer, visual Breadboard interface, and AI integrations are actively in development and will be introduced in subsequent stages).*
