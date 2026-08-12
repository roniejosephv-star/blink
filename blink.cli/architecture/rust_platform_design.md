# Blink Platform — Rust Architecture Design

> **Vision**: Cursor IDE for Edge Devices — a Rust-native platform that dynamically detects, configures, programs, and manages ESP32 and similar microcontrollers via a cluster of Python CLI tools.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    BLINK PLATFORM (Rust)                      │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  USB Hotplug │  │ Device State │  │   UI / Terminal  │    │
│  │  Daemon      │  │ Manager      │  │   Interface      │    │
│  │  (nusb)      │  │ (in-memory)  │  │   (ratatui/TUI)  │    │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘    │
│         │                 │                    │              │
│  ┌──────▼─────────────────▼────────────────────▼──────┐      │
│  │              Tool Orchestrator (Tokio)              │      │
│  │                                                     │      │
│  │  ┌───────────────────────────────────────────┐     │      │
│  │  │         NDJSON IPC Protocol Layer          │     │      │
│  │  │  • Parse stdout → progress/result          │     │      │
│  │  │  • Parse stderr → user_feedback prompts    │     │      │
│  │  │  • Write stdin  → user responses           │     │      │
│  │  └───────────────────────────────────────────┘     │      │
│  └────────────────────────┬───────────────────────────┘      │
│                           │                                   │
│  ┌────────────────────────▼───────────────────────────┐      │
│  │           Native Rust Operations                    │      │
│  │  • espflash (ESP32 firmware flashing)               │      │
│  │  • nusb (USB device enumeration & hotplug)          │      │
│  │  • serialport (raw serial I/O)                      │      │
│  │  • probe-rs (ARM/RP2040 support)                    │      │
│  └────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
                            │
                   subprocess spawn
                            │
┌──────────────────────────▼───────────────────────────────────┐
│                    BLINK CLI CLUSTER (Python)                 │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ blink-   │ │ blink-   │ │ blink-   │ │ blink-   │       │
│  │ port-    │ │ flash-   │ │ repl-    │ │ fs-      │       │
│  │ scan     │ │ firmware │ │ execute  │ │ upload   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ blink-   │ │ blink-   │ │ blink-   │ │ blink-   │       │
│  │ config-  │ │ pkg-     │ │ ai-      │ │ project- │       │
│  │ dtr-rts  │ │ install  │ │ analyze  │ │ deploy   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                               │
│  Dependencies: minny, pyserial, esptool, pipkin, ollama      │
└──────────────────────────────────────────────────────────────┘
```

---

## NDJSON IPC Protocol Specification

### Message Types

| Type | Direction | Channel | Format |
|---|---|---|---|
| `progress` | Python → Rust | stdout | `{"type":"progress","stage":"...","pct":N,"message":"..."}` |
| `result` | Python → Rust | stdout | `{"type":"result","status":"ok"/"error","data":{...}}` |
| `log` | Python → Rust | stdout | `{"type":"log","level":"info"/"warn"/"error","message":"..."}` |
| `user_feedback` | Python → Rust | stderr | `{"type":"user_feedback","id":"...","prompt":"...","options":[...],"default":"..."}` |
| `user_response` | Rust → Python | stdin | `{"id":"...","response":"..."}` |
| `error` | Python → Rust | stdout | `{"type":"error","code":"...","message":"...","recoverable":bool,"suggestion":"..."}` |

### Error Codes

| Code | Meaning | Recoverable |
|---|---|---|
| `PORT_NOT_FOUND` | No device on any port | Yes — check cable |
| `PORT_BUSY` | Port already in use | Yes — close other app |
| `PORT_PERMISSION` | Permission denied | Yes — chmod |
| `DEVICE_UNKNOWN` | Cannot identify device | Yes — manual input |
| `FLASH_FAILED` | Firmware write failed | Maybe — retry |
| `REPL_TIMEOUT` | No REPL prompt found | Maybe — reset device |
| `REPL_BOOT_LOOP` | DTR/RTS reset loop | Yes — change config |
| `FILE_TRANSFER_FAILED` | Upload/download error | Yes — retry |
| `MINNY_NOT_INSTALLED` | minny package missing | Yes — pip install |

---

## Rust Crate Dependencies

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
nusb = "0.1"              # USB hotplug detection
espflash = "4"             # ESP32 native flashing
serialport = "4"           # Serial port access
clap = { version = "4", features = ["derive"] }  # CLI argument parsing
tracing = "0.1"            # Structured logging
tracing-subscriber = "0.3" # Log formatting
anyhow = "1"               # Error handling
```

---

## Device State Model

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeviceState {
    pub port: String,              // /dev/cu.usbserial-XXX
    pub vid: u16,                  // 0x303A
    pub pid: u16,                  // 0x0002
    pub chip_family: ChipFamily,   // ESP32, ESP32S3, RP2040, etc.
    pub board_name: Option<String>,
    pub firmware_type: FirmwareType,  // MicroPython, CircuitPython, None
    pub firmware_version: Option<String>,
    pub connection_status: ConnectionStatus,
    pub dtr_rts_config: DtrRtsConfig,
    pub last_seen: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ChipFamily {
    ESP32, ESP32S2, ESP32S3, ESP32C3, ESP32C6,
    ESP8266, RP2040, RP2350, Unknown,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConnectionStatus {
    Detected,     // USB plugged in
    Connected,    // REPL session active
    Flashing,     // Firmware being written
    Transferring, // File upload/download in progress
    Error(String),
}
```

---

## Tool Manifest Schema

Each Python CLI tool includes a manifest for Rust discovery:

```json
{
    "name": "blink-port-scan",
    "version": "0.1.0",
    "tier": 1,
    "domain": "port",
    "action": "scan",
    "description": "Scan all serial ports and identify connected microcontrollers",
    "requires_device": false,
    "requires_port": false,
    "supports_streaming": true,
    "output_format": "ndjson",
    "python_deps": ["pyserial>=3.4"],
    "args": [],
    "user_feedback_possible": false
}
```

---

## Dynamic Tool Invocation from Rust

```rust
pub async fn invoke_tool(
    tool_name: &str,
    args: &[String],
) -> Result<ToolResult, BlinkError> {
    let mut child = tokio::process::Command::new(tool_name)
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let stdout = BufReader::new(child.stdout.take().unwrap());
    let stderr = BufReader::new(child.stderr.take().unwrap());
    let stdin = child.stdin.take().unwrap();

    // Process NDJSON lines from stdout
    let mut lines = stdout.lines();
    while let Some(line) = lines.next_line().await? {
        let msg: NdjsonMessage = serde_json::from_str(&line)?;
        match msg.msg_type.as_str() {
            "progress" => emit_progress(msg),
            "result" => return Ok(msg.into()),
            "error" => return Err(msg.into()),
            _ => {}
        }
    }

    // Handle user_feedback from stderr
    // ... (bidirectional IO handling)
}
```
