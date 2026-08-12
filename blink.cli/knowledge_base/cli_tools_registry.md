# Blink CLI — Complete Tool Registry & Knowledge Base

> **What is Blink CLI?**: A cluster of purpose-built CLI tools that expose every capability of Thonny IDE as headless, automatable commands. Each tool is named after the exact process it handles, making it trivial for the Rust Blink Platform to discover, invoke, and display tool calls to the user.

> **Design Principle**: Each CLI tool is a self-contained Python script that wraps a specific Thonny module. The Rust platform calls these tools via subprocess, parsing structured JSON output. User feedback is communicated via a standardized JSON protocol on stdout.

---

## Tool Naming Convention

```
blink-<domain>-<action>
```

Examples: `blink-port-scan`, `blink-flash-firmware`, `blink-repl-connect`

---

## Complete CLI Tool Registry

### 🔴 TIER 1: Device Detection & Connection (Critical Path)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-port-scan` | `mpytool/utils.py`, `minny/bare_metal_target.py` | Scan all serial ports, identify devices by VID/PID and text matching | None (auto-detect) | JSON: `[{port, vid, pid, chip_family, board_type, description}]` |
| `blink-port-select` | Interactive Rust TUI | Auto-connect if single device, else prompt user to select target board | None or `--prompt` | JSON: `{selected_port, vid_pid, backend}` |
| `blink-port-identify` | `minny` target modules | Given a port, identify exact device type and backend | `--port /dev/cu.usbserial-XXX` | JSON: `{chip, family, backend, firmware_type}` |
| `blink-port-monitor` | `pyserial` + USB hotplug | Watch for USB device connect/disconnect events | `--watch` (daemon mode) | JSON stream: `{event: "connected"/"disconnected", port, vid, pid, timestamp}` |
| `blink-port-cache-get` | `serial.last_backend_per_vid_pid` | Retrieve cached port-to-backend mappings | None | JSON: `{vid_pid: backend_name}` map |
| `blink-port-cache-set` | Config system | Store a successful port-to-backend mapping | `--vid-pid 0x303A:0x0002 --backend ESP32` | JSON: `{status: "ok"}` |

### 🔴 TIER 1: Firmware Management (Critical Path)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-flash-firmware` | `esptool_dialog.py` | Flash firmware to ESP32/ESP8266 via esptool | `--port --chip --firmware --baud --flash-mode --flash-size --erase-all --no-stub` | JSON stream: `{progress_pct, stage, message}` |
| `blink-flash-uf2` | `uf2dialog.py` | Copy UF2 firmware to mounted volume (RP2040/CircuitPython) | `--firmware path.uf2 --volume /Volumes/RPI-RP2` | JSON: `{status, bytes_written}` |
| `blink-flash-detect-chip` | `esptool.py chip_id` | Detect chip type on connected device | `--port` | JSON: `{chip, chip_id, mac, flash_size}` |
| `blink-flash-erase` | `esptool.py erase_flash` | Erase entire flash memory | `--port --chip` | JSON: `{status, duration_ms}` |
| `blink-flash-address` | Chip-to-address map | Get correct start address for chip family | `--chip esp32s3` | JSON: `{start_address: "0x0"}` |
| `blink-firmware-list` | `data/*-variants-*.json` | List available firmware variants for a board | `--board "ESP32-S3" --type micropython` | JSON: `[{name, url, version, variant}]` |
| `blink-firmware-download` | Variant URLs | Download firmware binary from official source | `--url --output` | JSON: `{path, size, sha256}` |
| `blink-firmware-update-db` | `data/update_*_variants.py` | Refresh firmware variant database from upstream | `--type micropython/circuitpython` | JSON: `{variants_added, variants_updated}` |

### 🔴 TIER 1: Serial Connection & REPL (Critical Path)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-repl-connect` | `minny/serial_connection.py` | Establish serial REPL connection | `--port --baud 115200 --dtr true --rts false` | JSON: `{status: "connected", prompt_found: true}` |
| `blink-repl-execute` | `mp_back.py` + raw paste mode | Execute Python code on device via raw paste | `--port --code "print('hello')"` or `--file script.py` | JSON: `{stdout, stderr, duration_ms}` |
| `blink-repl-interactive` | Shell system | Start interactive REPL session (stdin/stdout passthrough) | `--port` | Raw terminal I/O |
| `blink-repl-interrupt` | `\x03` (Ctrl+C) | Send interrupt signal to device | `--port` | JSON: `{status: "interrupted"}` |
| `blink-repl-soft-reboot` | `\x04` (Ctrl+D / EOT) | Trigger MicroPython soft reboot | `--port` | JSON: `{status: "rebooted", prompt_found: true}` |
| `blink-repl-inject-helper` | `EXTRA_HELPER_CODE` in `mp_back.py` | Inject minny helper class into REPL | `--port` | JSON: `{status: "injected"}` |

### 🟡 TIER 2: File Operations (High Priority)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-fs-list` | `_get_dir_children_info` | List files/dirs on device filesystem | `--port --path /` | JSON: `[{name, type, size, mtime}]` |
| `blink-fs-read` | `InlineCommand("read_file")` | Read file from device | `--port --path /main.py` | JSON: `{content, size, encoding}` |
| `blink-fs-write` | `InlineCommand("write_file")` | Write file to device | `--port --path /main.py --content "..." --chunk-size 127 --chunk-delay 0.01` | JSON: `{status, bytes_written}` |
| `blink-fs-upload` | `UploadDownloadMixin` | Upload local file(s) to device | `--port --local ./src/ --remote / --recursive` | JSON stream: `{file, progress_pct, status}` |
| `blink-fs-download` | `UploadDownloadMixin` | Download file(s) from device | `--port --remote /data/ --local ./backup/ --recursive` | JSON stream: `{file, progress_pct, status}` |
| `blink-fs-delete` | `os.remove()` / `os.rmdir()` | Delete file or directory on device | `--port --path /old_file.py` | JSON: `{status: "deleted"}` |
| `blink-fs-info` | `os.statvfs("/")` | Get device filesystem info (total/free space) | `--port` | JSON: `{total_bytes, free_bytes, used_pct}` |
| `blink-fs-mkdir` | `os.mkdir()` | Create directory on device | `--port --path /lib` | JSON: `{status: "created"}` |

### 🟡 TIER 2: Device Configuration (High Priority)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-config-dtr-rts` | DTR/RTS config options | Set DTR/RTS pin states for connection | `--port --dtr false --rts false` | JSON: `{status: "applied"}` |
| `blink-config-rtc-sync` | `sync_time` / `local_rtc` | Sync host clock to device RTC | `--port --timezone local` | JSON: `{device_time, host_time, drift_ms}` |
| `blink-config-get` | `ConfigurationManager` | Read a Blink CLI config value | `--key serial.baud` | JSON: `{key, value}` |
| `blink-config-set` | `ConfigurationManager` | Set a Blink CLI config value | `--key serial.baud --value 115200` | JSON: `{status: "saved"}` |
| `blink-config-list` | Config system | List all configuration keys and values | None | JSON: `[{key, value, default, description}]` |
| `blink-config-reset` | Config system | Reset configuration to defaults | `--key serial.baud` or `--all` | JSON: `{status: "reset"}` |

### 🟢 TIER 3: Package Management (Medium Priority)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-pkg-search` | `mpypkg/mpypkg.py` / PyPI API | Search for packages available for device | `--query "mqtt" --target micropython` | JSON: `[{name, version, summary}]` |
| `blink-pkg-install` | `mpypkg/cli.py` / `minny` | Install package on device following `pyproject.toml` specs | `--port --package umqtt.simple` | JSON stream: `{stage, message}` |
| `blink-pkg-uninstall` | Device filesystem delete | Remove package from device | `--port --package umqtt` | JSON: `{status: "removed"}` |
| `blink-pkg-list` | Device `/lib/` listing | List installed packages on device | `--port` | JSON: `[{name, path, size}]` |
| `blink-pkg-freeze` | `micropython.freeze()` or dir scan | Export installed packages as requirements | `--port --output requirements.txt` | JSON: `{packages: [...]}` |

### 🟢 TIER 3: AI / LLM Integration (Medium Priority)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-ai-analyze` | `chat.py` context tags | Analyze code/output with LLM | `--input "crash log..." --context-file main.py` | JSON: `{analysis, suggestions: [...]}` |
| `blink-ai-generate` | Chat system | Generate code for device | `--prompt "blink LED on GPIO2" --target esp32` | JSON: `{code, explanation}` |
| `blink-ai-debug` | `#lastRun` + `#selectedOutput` | Send last run output to LLM for debugging | `--port --last-output "..."` | JSON: `{diagnosis, fix_code}` |
| `blink-ai-config` | Ollama/OpenAI config | Configure AI backend | `--provider ollama --model codellama:7b-instruct --endpoint http://localhost:11434` | JSON: `{status: "configured"}` |

### 🟢 TIER 3: Project Management (Medium Priority)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-project-init` | Editor + file structure | Initialize a new Blink project locally | `--name my-sensor --template esp32-micropython` | JSON: `{path, files_created: [...]}` |
| `blink-project-deploy` | Upload + soft reboot | Deploy entire project to device | `--port --project ./my-sensor/` | JSON stream: `{stage, file, progress_pct}` |
| `blink-project-build` | Compile check | Validate/compile project before deploy | `--project ./my-sensor/` | JSON: `{errors: [...], warnings: [...]}` |
| `blink-project-monitor` | Serial monitor | Watch device serial output in real-time | `--port --baud 115200` | Raw stdout stream |
| `blink-project-snapshot` | Download all files | Backup entire device filesystem to local dir | `--port --output ./backup/` | JSON stream: `{file, progress_pct}` |

### 🔵 TIER 4: Diagnostics & Utilities (Lower Priority)

| Tool Name | Thonny Source | Purpose | Input | Output |
|---|---|---|---|---|
| `blink-diag-health` | Multiple checks | Run full device health check | `--port` | JSON: `{memory_free, flash_free, firmware_version, uptime}` |
| `blink-diag-driver` | USB driver check | Verify required USB drivers are installed on host | None | JSON: `{drivers: [{name, installed, version}]}` |
| `blink-diag-deps` | requirements check | Verify all Python dependencies are installed | None | JSON: `{deps: [{name, required, installed, status}]}` |
| `blink-diag-webrepl` | WebREPL config | Check/configure WebREPL on device | `--port --enable --password "secret"` | JSON: `{status, url}` |
| `blink-version` | VERSION file | Show Blink CLI version | None | JSON: `{version, thonny_version, esptool_version}` |

---

## Rust Platform Integration Protocol

### Subprocess Call Pattern

```rust
use std::process::Command;

let output = Command::new("blink-port-scan")
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()?;

// Parse JSON from stdout
// Display progress from streaming JSON lines
// Surface user-feedback prompts from stderr
```

### User Feedback Protocol

When a CLI tool needs user input/confirmation, it emits a special JSON line on **stderr**:

```json
{"type": "user_feedback", "id": "confirm_erase", "prompt": "This will erase all flash data. Continue?", "options": ["yes", "no"], "default": "no"}
```

The Rust platform renders this as a UI dialog/prompt. The user's response is sent back via **stdin**:

```json
{"id": "confirm_erase", "response": "yes"}
```

### Progress Reporting Protocol

Long-running tools emit progress on stdout as newline-delimited JSON:

```json
{"type": "progress", "stage": "erasing", "pct": 45, "message": "Erasing flash sector 23/51..."}
{"type": "progress", "stage": "writing", "pct": 72, "message": "Writing firmware at 0x10000..."}
{"type": "result", "status": "ok", "data": {...}}
```

### Error Reporting Protocol

```json
{"type": "error", "code": "PORT_NOT_FOUND", "message": "No ESP32 device detected on any serial port", "recoverable": true, "suggestion": "Check USB cable and driver installation"}
```

---

## Pain Points & User Feedback Requirements

| Pain Point | Which Tool(s) | User Action Required | Feedback Protocol |
|---|---|---|---|
| **DTR/RTS Boot Loop** | `blink-repl-connect` | User must toggle DTR/RTS settings | `user_feedback: "Device appears to be in reset loop. Try DTR=false, RTS=false?"` |
| **Multiple Devices / Auto-Connect Ambiguity** | `blink-port-select` | User must select which device | `user_feedback: "Multiple devices found. Select: [1] ESP32, [2] Pico"` |
| **Erase Confirmation** | `blink-flash-firmware` | User must confirm destructive action | `user_feedback: "Erase all flash before writing? This destroys all data."` |
| **Firmware Selection** | `blink-firmware-list` | User picks variant for their board | `user_feedback: "Select firmware: [1] ESP32-GENERIC, [2] ESP32-SPIRAM"` |
| **Unknown Board** | `blink-port-identify` | User provides board info manually | `user_feedback: "Could not auto-identify board. Enter chip type."` |
| **Permission Denied** | `blink-repl-connect` | User needs to fix port permissions | `user_feedback: "Permission denied. Run: sudo chmod 666 /dev/cu.usbserial-0001"` |
| **Overwrite Files** | `blink-fs-upload` | User confirms overwrite | `user_feedback: "File /main.py exists on device. Overwrite?"` |

---

## Total Tool Count Summary

| Tier | Count | Domain |
|---|---|---|
| 🔴 Tier 1 (Critical) | 19 | Port Detection (5) + Firmware (8) + REPL (6) |
| 🟡 Tier 2 (High) | 14 | File Operations (8) + Device Config (6) |
| 🟢 Tier 3 (Medium) | 14 | Packages (5) + AI (4) + Project (5) |
| 🔵 Tier 4 (Utility) | 5 | Diagnostics (4) + Version (1) |
| **TOTAL** | **52 CLI tools** | |
