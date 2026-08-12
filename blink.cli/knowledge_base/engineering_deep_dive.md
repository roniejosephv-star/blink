# Tinkr CLI — Engineering Deep-Dive Knowledge Base

> **Source**: Compiled from 4 specialized engineering research agents analyzing the Thonny codebase.
> **Date**: 2026-08-11

---

## 1. The `minny` Library — Critical Dependency

### What Is It?
`minny` is a standalone Python library created by Aivar Annamaa (Thonny's author) that encapsulates ALL low-level device communication:
- Serial REPL connection management
- Raw paste mode state machine
- File transfer (read/write with chunking)
- Device filesystem operations
- RTC synchronization
- WebREPL connection
- Project management & compilation

### Key Classes & Modules

| Module | Class | Purpose |
|---|---|---|
| `minny.bare_metal_target` | `BareMetalTargetManager` | Main interface for serial-connected devices |
| `minny.serial_connection` | `SerialConnection` | Serial port connection handler |
| `minny.webrepl_connection` | `WebReplConnection` | WebSocket WebREPL handler |
| `minny.connection` | `MicroPythonConnection` | Abstract connection interface |
| `minny.target` | `ProperTargetManager` | Base target manager |
| `minny.target` | `RAW_PASTE_SUBMIT_MODE` | Raw paste mode constant |
| `minny.target` | `EOT, FIRST_RAW_PROMPT, NORMAL_PROMPT` | Protocol constants |
| `minny.target` | `STAT_KIND_INDEX, STAT_MTIME_INDEX, STAT_SIZE_INDEX` | Stat field indices |
| `minny.common` | `ManagementError` | Error type for management operations |
| `minny.project` | `ProjectManager` | MicroPython project management |
| `minny.tracking` | `Tracker` | File tracking for projects |
| `minny.compiling` | `Compiler` | MicroPython cross-compilation |
| `minny.os_target` | `LocalOsTargetManager` | OS-level MicroPython target |

### Installation
```bash
pip install minny
# OR clone from GitHub:
# git clone https://github.com/aivarannamaa/minny.git
```

### Status in Our Workspace
- `../minny` directory does NOT exist in workspace
- Must install from PyPI or clone the repo
- **ACTION REQUIRED**: `pip install minny` or `git clone` the repo into `/Users/mindflow/Projects/Tinkr/minny`

---

## 2. Serial Port Detection — Exact Implementation

### VID/PID Database (from Thonny source)

```python
# ESP32 (esp/__init__.py)
ESP32_VIDS_PIDS = {
    (0x303A, None),  # Espressif native USB (ESP32-S2/S3/C3/C6)
}

# Raspberry Pi Pico (rpi_pico/__init__.py)
PICO_VIDS_PIDS = {
    (0x2E8A, 0x0005),  # Raspberry Pi Pico MicroPython
}

# Common USB-to-UART bridges (get_uart_adapter_vids_pids)
UART_ADAPTER_VIDS_PIDS = {
    (0x10C4, 0xEA60),  # Silicon Labs CP210x
    (0x1A86, 0x7523),  # WCH CH340/CH341
    (0x0403, None),     # FTDI (any PID)
    # ... additional adapters
}
```

### Detection Algorithm (Pseudocode)
```python
def is_potential_port(port):
    # Step 1: Exclude known non-REPL interfaces
    if "CircuitPython CDC2" in port.interface:
        return False
    
    # Step 2: Check VID/PID against known database
    if (port.vid, port.pid) in known_vids_pids:
        return True
    if (port.vid, None) in known_vids_pids:
        return True
    
    # Step 3: Text-match on description/manufacturer
    desc_lower = port.description.lower()
    if "usb" in desc_lower and "serial" in desc_lower:
        return True
    for keyword in ["uart", "daplink", "stlink", "python"]:
        if keyword in desc_lower:
            return True
    if "MicroPython" in port.manufacturer:
        return True
    
    # ESP32-specific text matching
    if "m5stack" in desc_lower or "esp32" in desc_lower:
        if "circuitpython" not in desc_lower:
            return True
    
    return False
```

---

## 3. REPL Connection — Exact Protocol

### Connection Constants
```python
BAUDRATE = 115200
FIRST_RAW_PROMPT = b"raw REPL; CTRL-B to exit\r\n>"
W600_FIRST_RAW_PROMPT = b"raw REPL; CTRL-B to exit\r\r\n>"
RAW_PROMPT = b">"
NORMAL_PROMPT = b">>> "
```

### Raw Paste Mode Protocol
```python
RAW_PASTE_COMMAND = b"\x05A\x01"      # Enter raw paste mode
RAW_PASTE_CONFIRMATION = b"R\x01"     # Device accepted
RAW_PASTE_REFUSAL = b"R\x00"          # Device refused (fallback to normal)
RAW_PASTE_CONTINUE = b"\x01"          # Continue sending chunks
EOT = b"\x04"                          # Execute (Ctrl+D)
INTERRUPT = b"\x03"                    # Interrupt (Ctrl+C)
```

### Connection Flow
```
1. Open serial port (pyserial) with baud=115200
2. Set DTR/RTS per config (True/False)
3. Send \x03 (interrupt) to halt any running code
4. Send \x01 (Ctrl+A) to enter raw REPL mode
5. Wait for FIRST_RAW_PROMPT
6. Connection established → inject __minny_helper
7. Ready for commands
```

### DTR/RTS Configuration
| Setting | Effect | Best For |
|---|---|---|
| DTR=True, RTS=True | Default, may reset ESP on Windows | Most boards |
| DTR=True, RTS=False | Avoids reset loop | Some ESP32 boards |
| DTR=False, RTS=False | Manual control | Problematic boards |

---

## 4. Firmware Flashing — Exact esptool Command Construction

### Command Template
```bash
esptool --port <port> \
        --chip <family> \
        --baud <speed> \
        [--no-stub] \
        write_flash \
        --flash_mode <mode> \
        --flash_size <size> \
        [--erase-all] \
        <address> <firmware_file>
```

### Parameter Derivation
```python
def compute_start_address(family, firmware_type):
    if firmware_type == "circuitpython":
        return "0x0"
    if family in ("esp32", "esp32s2"):
        return "0x1000"
    else:  # esp8266, esp32s3, esp32c3, esp32c6
        return "0x0"

# Defaults
BAUD_OPTIONS = [115200, 230400, 460800]
FLASH_MODE_OPTIONS = ["keep", "dio", "qio", "dout", "qout"]
FLASH_SIZE_OPTIONS = ["keep", "detect", "2MB", "4MB", "8MB", "16MB"]
```

---

## 5. Device-Side MicroPython Code Snippets

### Filesystem Info
```python
__thonny_stat = __minny_helper.os.statvfs('{path}')
__thonny_total = __thonny_stat[2] * __thonny_stat[0]
__thonny_free = __thonny_stat[3] * __thonny_stat[0]
__minny_helper.print_mgmt_value({
    "total": __thonny_total,
    "used": __thonny_total - __thonny_free,
    "free": __thonny_free,
})
del __thonny_stat, __thonny_total, __thonny_free
```

### Directory Listing
```python
__thonny_result = {}
try:
    __thonny_names = __minny_helper.listdir('{path}')
except __minny_helper.builtins.OSError:
    __minny_helper.print_mgmt_value(None)
else:
    for __thonny_name in __thonny_names:
        if not __thonny_name.startswith(".") or {include_hidden}:
            try:
                __thonny_result[__thonny_name] = __minny_helper.os.stat(
                    '{path}' + __thonny_name
                )
            except __minny_helper.builtins.OSError as e:
                __thonny_result[__thonny_name] = __minny_helper.builtins.str(e)
    __minny_helper.print_mgmt_value(__thonny_result)
```

### Helper Code Injection (EXTRA_HELPER_CODE)
```python
last_non_none_repl_value = None
inspector_values = builtins.dict()

@builtins.classmethod
def print_repl_value(cls, obj):
    if obj is not None:
        cls.builtins.print(
            {start_marker!r} % cls.builtins.id(obj),
            cls.builtins.repr(obj),
            {end_marker!r}, sep=''
        )
        cls.last_non_none_repl_value = obj

@builtins.classmethod
def repr(cls, obj):
    try:
        s = cls.builtins.repr(obj)
        if cls.builtins.len(s) > 50:
            s = s[:50] + "..."
        return s
    except cls.builtins.Exception as e:
        return "<could not serialize: " + __minny_helper.builtins.str(e) + ">"
```

### Global Variable Listing
```python
{name: (__minny_helper.repr(value), __minny_helper.builtins.id(value))
 for (name, value) in __minny_helper.builtins.globals().items()
 if not name.startswith('__')}
```

---

## 6. Firmware Variant Database Structure

### JSON Schema
```json
{
    "vendor": "Espressif",
    "model": "ESP32 / WROOM",
    "family": "esp32",
    "info_url": "https://micropython.org/download/ESP32_GENERIC",
    "downloads": [
        {
            "version": "1.28.0",
            "url": "https://micropython.org/resources/firmware/ESP32_GENERIC-20260406-v1.28.0.bin"
        }
    ],
    "latest_prerelease_regex": "\\d{8}-v1.29.0-preview\\.\\d+\\.[a-z0-9]{10}"
}
```

### Database Files
| File | Content |
|---|---|
| `micropython-variants-esptool.json` | MicroPython firmware for ESP chips |
| `micropython-variants-uf2.json` | MicroPython firmware for UF2 boards |
| `micropython-variants-daplink.json` | MicroPython firmware for DAPLink boards |
| `circuitpython-variants-esptool.json` | CircuitPython for ESP chips |
| `circuitpython-variants-uf2.json` | CircuitPython for UF2 boards |
| `circuitpython-variants-daplink.json` | CircuitPython for DAPLink boards |

### MCU Families Supported
`esp8266, esp32, esp32s2, esp32s3, esp32c2, esp32c3, esp32c5, esp32c6, esp32p4, rp2040, rp2350, samd21, samd51, nrf51, nrf52`

---

## 7. Rust Platform Architecture

### Recommended Crates

| Crate | Purpose | Why |
|---|---|---|
| `nusb` | USB hotplug detection | Pure Rust, native macOS IOKit, async stream API |
| `espflash` | ESP32 flashing from Rust | Mature, pure Rust, library + CLI |
| `probe-rs` | ARM/RP2040 debugging | Industry standard for SWD/JTAG |
| `tokio-serial` | Async serial communication | Integrates with Tokio runtime |
| `serialport` | Sync serial communication | Simple, battle-tested |
| `serde_json` | JSON parsing | NDJSON parsing for CLI tool output |
| `tokio` | Async runtime | Foundation for concurrent device management |
| `tonic` | gRPC | For long-running daemon communication |

### Architecture Decision: Hybrid Approach

```
┌─────────────────────────────────────────────────┐
│             RUST BLINK PLATFORM                  │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   nusb   │  │ espflash │  │ tokio-   │      │
│  │  hotplug │  │  flash   │  │ serial   │      │
│  │  detect  │  │  native  │  │  REPL    │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│       │              │              │            │
│  ┌────▼──────────────▼──────────────▼────┐      │
│  │         State Manager (Rust)          │      │
│  │   Connected devices, sessions, cache  │      │
│  └────────────────┬──────────────────────┘      │
│                   │                              │
│  ┌────────────────▼──────────────────────┐      │
│  │     Python CLI Tool Orchestrator      │      │
│  │  (for minny-dependent operations)     │      │
│  │  - tinkr-repl-execute (via minny)     │      │
│  │  - tinkr-fs-upload (via minny)        │      │
│  │  - tinkr-pkg-install (via pipkin)     │      │
│  │  - tinkr-ai-analyze (via ollama)      │      │
│  └───────────────────────────────────────┘      │
│                                                  │
│  ┌───────────────────────────────────────┐      │
│  │      NDJSON IPC Protocol              │      │
│  │  stdout: progress, results            │      │
│  │  stderr: user_feedback prompts        │      │
│  │  stdin: user responses                │      │
│  └───────────────────────────────────────┘      │
└─────────────────────────────────────────────────┘
```

### Tradeoffs: Pure Rust vs Python CLI Tools

| Aspect | Pure Rust | Python CLI (via minny) |
|---|---|---|
| **Distribution** | Single binary, no dependencies | Requires Python + pip |
| **Flashing** | `espflash` crate — excellent | `esptool` — proven but Python |
| **REPL Interaction** | Must reimplement paste mode | `minny` handles everything |
| **File Transfer** | Must reimplement chunking | `minny` handles everything |
| **Latency** | Lower | Subprocess overhead |
| **Maintenance** | Own code to maintain | Upstream minny/esptool updates |

**Recommendation**: Use Rust native for USB detection + flashing (`nusb` + `espflash`). Use Python/minny CLI tools for REPL, file transfer, and device operations (too complex to reimplement).

---

## 8. Package Management

- Thonny uses `pipkin` (not `upip`/`mip` directly) for device package installation
- `pipkin` is invoked via `_perform_pipkin_operation_and_list` in `mp_back.py`
- Search integration uses PyPI API directly
- MicroPython-lib packages are also searchable

---

## 9. Tool Discovery Pattern

### Manifest-Based Discovery (Recommended)
```json
// ~/.tinkr/tools/tinkr-port-scan/manifest.json
{
    "name": "tinkr-port-scan",
    "entrypoint": "main.py",
    "version": "0.1.0",
    "tier": 1,
    "domain": "port",
    "action": "scan",
    "supported_vids": ["0x303A", "0x2E8A"],
    "requires_device": false,
    "output_format": "ndjson"
}
```

### Alternative: PATH Scanning
```bash
# Rust discovers tools by scanning PATH for tinkr-* executables
# Each tool responds to --capabilities with a JSON manifest
tinkr-port-scan --capabilities
```
