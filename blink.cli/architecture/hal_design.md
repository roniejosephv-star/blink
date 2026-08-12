# Tinkr HAL — Hardware Abstraction Layer Design v0.1

> The common layer that lets a Tinkr project talk to any device the right way, without the application code knowing which chip it's on. The HAL is the bridge between plugin-specific CLI tools and the project-level abstractions (REPL, filesystem, package manager, flash, serial monitor). It is the single thing that makes "many devices, one workflow" actually work.

---

## 1. Why a HAL is Required

The user said it directly: *"a Common Layer to handle multiple Device Is also required."* Here's why this is structurally non-optional:

- **The application code should not know whether the device is an ESP32 or an RP2040.** A "deploy this project" operation means different things on different chips, but the user's intent is the same: get my code onto the board.
- **The user has multiple devices on their desk.** They want to switch between them in one click.
- **The agent (MCP server) needs a uniform device surface.** When the AI asks "what's the device state?", it should not have to branch on chip family.
- **Plugins should be self-contained.** The `tinkr-esp32` plugin should not have to know about the `tinkr-rp2040` plugin. The HAL coordinates them.

Without a HAL, every consumer (UI, agent, CLI, IDE) re-implements the dispatch logic. With a HAL, there is one dispatch.

---

## 2. The Device: The Unit of the HAL

A **device** is the unit the HAL manages. It is identified by:

```python
@dataclass(frozen=True)
class Device:
    id: str                          # Stable per-project unique ID (e.g., "esp32s3-left")
    vendor: str                      # "Espressif", "Raspberry Pi", "Nordic"
    family: str                      # "esp32s3", "rp2040", "nrf52"
    model: str                       # "ESP32-S3-DevKitC-1"
    serial_number: str | None        # From USB descriptor or REPL `os.uname()`
    port: str | None                 # "/dev/cu.usbserial-1410" (transient)
    transport: str                   # "serial" | "usb-native" | "webrepl" | "ble" | "wifi"
    firmware_type: str | None        # "micropython" | "circuitpython" | "arduino" | ...
    firmware_version: str | None     # "v1.24.1"
    capabilities: frozenset[str]     # {"flash", "repl", "filesystem", "package_manager", ...}
    plugin: str                      # "tinkr-esp32" (the plugin that owns this device)
    metadata: dict[str, Any]         # Plugin-specific extras (MAC, board revision, etc.)
    last_seen: datetime
    connection_status: ConnectionStatus  # Detected | Connected | Flashing | Error(...)
```

A Device is the abstraction. The concrete object is a *device adapter* that wraps a plugin's CLI tools and exposes the standard capability surface.

---

## 3. The Capability Model

The HAL defines a fixed set of **capabilities**. A device's plugin declares which capabilities it supports. The HAL dispatches a capability invocation to the right plugin.

### 3.1 The 12 standard capabilities

| Capability | Description | Returns |
|---|---|---|
| `identify` | Re-identify a device (in case of reboot / re-plug) | `Device` (updated) |
| `flash` | Write firmware to the device | `Result` (streamed progress) |
| `repl.open` | Open an interactive REPL session | `REPLSession` |
| `repl.execute` | Run a snippet of code on the device | `ExecuteResult { stdout, stderr, duration }` |
| `repl.interrupt` | Send Ctrl+C | `Result` |
| `repl.reboot` | Soft reboot (Ctrl+D) | `Result` |
| `filesystem.list` | List a path on the device | `list[FileEntry]` |
| `filesystem.read` | Read a file | `bytes` |
| `filesystem.write` | Write a file | `Result` |
| `filesystem.delete` | Delete a file or directory | `Result` |
| `package.install` | Install a package | `Result` (streamed progress) |
| `package.remove` | Remove a package | `Result` |
| `package.list` | List installed packages | `list[PackageInfo]` |
| `package.freeze` | Export installed packages as `requirements.txt` | `str` |
| `serial.monitor` | Open a raw serial monitor | `SerialStream` |
| `serial.plot` | Open a numeric serial plotter (CSV-keyed) | `PlotStream` |
| `ota.update` | Over-the-air firmware update | `Result` (streamed progress) |
| `gdb.attach` | Attach a GDB stub | `GDBTarget` |
| `power.off` | Cut power to the device (if supported by board) | `Result` |
| `power.read` | Read voltage / current (if supported) | `PowerReading` |
| `wifi.scan` | Scan WiFi networks visible to the device | `list[WiFiNetwork]` |
| `wifi.status` | Read current WiFi connection state | `WiFiStatus` |
| `ble.scan` | Scan BLE advertisements | `list[BLEAdv]` |

Plugins declare a subset. The HAL rejects invocations of capabilities the device's plugin does not support.

### 3.2 Custom capabilities

A plugin can also declare **custom capabilities** (e.g., `esp32-deep-sleep`, `esp32-ulp-coprogram`, `nrf52-softdevice-update`). These are exposed through MCP with the plugin's tool prefix and dispatched to the plugin's CLI tools directly. The HAL does not interpret them; it just routes them.

---

## 4. The Adapter Interface (Python)

Every plugin provides a `DeviceAdapter` class that implements the standard capabilities using the plugin's CLI tools. The interface is one class per plugin.

```python
# In a plugin: tinkr-esp32/adapters/esp32_adapter.py
from tinkr.hal import DeviceAdapter, Capability, Device, Result, REPLSession

class ESP32Adapter(DeviceAdapter):
    """Adapter for ESP32-family devices. Wraps the tinkr-esp32 CLI tools."""

    plugin_name = "tinkr-esp32"

    @classmethod
    def matches(cls, device_info: dict) -> bool:
        """Return True if this adapter handles a device with these port metadata."""
        return device_info.get("vid_pid_family") in {
            "esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32c2",
        }

    @Capability("identify")
    async def identify(self, device: Device) -> Device:
        """Run tinkr-esp32-port-identify; update the device's metadata."""
        info = await self.cli.run("tinkr-esp32-port-identify", ["--port", device.port])
        return device.evolve(
            chip=info["chip"],
            firmware_type=info.get("firmware_type"),
            firmware_version=info.get("firmware_version"),
            serial_number=info.get("serial_number"),
        )

    @Capability("flash")
    async def flash(self, device: Device, firmware: Path, *, erase: bool = False) -> AsyncIterator[ProgressEvent]:
        """Stream flash progress."""
        cmd = ["--port", device.port, "--firmware", str(firmware)]
        if erase:
            cmd.append("--erase")
        async for event in self.cli.stream("tinkr-esp32-flash-firmware", cmd):
            yield event

    @Capability("repl.open")
    async def open_repl(self, device: Device) -> REPLSession:
        """Open an interactive REPL session."""
        return REPLSession(
            send=self.cli.process("tinkr-esp32-repl-execute", ["--port", device.port]),
            interrupt=lambda: self.cli.run("tinkr-esp32-repl-interrupt", ["--port", device.port]),
            reboot=lambda: self.cli.run("tinkr-esp32-repl-soft-reboot", ["--port", device.port]),
        )

    @Capability("filesystem.list")
    async def fs_list(self, device: Device, path: str) -> list[FileEntry]:
        """List a path on the device filesystem."""
        result = await self.cli.run("tinkr-esp32-fs-list", ["--port", device.port, "--path", path])
        return [FileEntry.from_dict(e) for e in result["entries"]]

    # ... and so on for the other capabilities the plugin supports.
```

The adapter is a thin object-oriented wrapper over the CLI tools. The CLI tools are still the source of truth (NDJSON in, NDJSON out). The adapter is a typed Python surface that the rest of Tinkr can use.

### 4.1 Why an adapter and not just direct CLI calls

- **The agent (MCP server) calls adapter methods**, not CLI tools. This gives it a typed, autocompleted, docstringed surface.
- **The UI calls adapter methods**, not CLI tools. This is the same surface; the UI and the agent are interchangeable consumers.
- **The tests use adapter methods**, not CLI tools. Tests can mock the CLI.
- **The CLI tools are still invokable by hand** for debugging, scripting, and CI.

### 4.2 Why the CLI tools are still the contract

- **The CLI is the language boundary.** A future Rust or Tauri UI does not need to reimplement the adapter — it just calls the CLI tools via subprocess.
- **The CLI is the test boundary.** You can `tinkr-esp32-port-scan` from a shell and see the result.
- **The CLI is the human boundary.** A user can `tinkr-esp32-flash-firmware --port /dev/cu.usbserial-1410 --firmware foo.bin` without Tinkr installed.
- **The CLI is the upgrade boundary.** When a plugin adds a new capability, the CLI is the first place it shows up. The adapter is generated (or hand-written) on top.

---

## 5. The HAL Registry

The HAL registry is the in-process catalog of (plugin → adapter class) mappings.

```python
# In Tinkr core, not in plugins
class HAL:
    def __init__(self, plugin_dir: Path):
        self.adapters: dict[str, type[DeviceAdapter]] = {}
        self.discover(plugin_dir)

    def discover(self, plugin_dir: Path) -> None:
        """Scan all installed plugins and load their adapter classes."""
        for plugin_path in plugin_dir.iterdir():
            manifest = tinkr_plugin_toml.load(plugin_path / "tinkr.plugin.toml")
            adapter_module = importlib.import_module(
                f".plugins.{plugin_path.name}.adapters.adapter",
                package="tinkr.hal",
            )
            self.adapters[manifest["plugin"]["name"]] = adapter_module.Adapter

    def find_adapter(self, device: Device) -> DeviceAdapter:
        """Find the adapter for a device, or raise NoAdapterError."""
        for adapter_cls in self.adapters.values():
            if adapter_cls.matches(device.metadata):
                return adapter_cls(device)
        raise NoAdapterError(f"No adapter for device {device.id}")

    def capabilities_for(self, device: Device) -> frozenset[str]:
        """Return the set of capabilities supported by a device's plugin."""
        adapter = self.find_adapter(device)
        return adapter.supported_capabilities
```

The HAL is a small (~200 LoC) module. It does not know anything about ESP32, RP2040, etc. — only about plugins and their adapter classes.

---

## 6. The Device Registry (per project)

A project has its own **device registry** — a list of devices the user has interacted with, persisted in `.tinkr/state/devices.toml`. The HAL uses this to resolve "the device" in commands like `tinkr device scan`, `tinkr repl`, `tinkr flash`.

```toml
# .tinkr/state/devices.toml (auto-managed, gitignored)
[[device]]
id = "esp32s3-left"
plugin = "tinkr-esp32"
port = "/dev/cu.usbserial-1410"
last_chip = "ESP32-S3"
last_firmware = "MicroPython v1.24.1"
last_seen = "2026-08-12T14:32:00Z"
nickname = "kitchen sensor"     # User-set

[[device]]
id = "rp2040-pico"
plugin = "tinkr-rp2040"
port = "/dev/cu.usbmodem14101"
last_chip = "RP2040"
last_firmware = "MicroPython v1.24.1"
last_seen = "2026-08-12T13:00:00Z"
nickname = "robot arm controller"

[default]
device = "esp32s3-left"
```

`tinkr device list` shows them. `tinkr device use esp32s3-left` sets the default. All `tinkr` commands without an explicit `--device` use the default.

### 6.1 The device scan loop

`tinkr device scan` does this:
1. For each installed plugin, run its `port-scan` CLI tool.
2. For each detected port, ask each plugin's adapter: "do you match this port?" (VID/PID, text matching, etc.)
3. The first adapter that matches claims the device.
4. The HAL creates a `Device` object, updates the device registry, and returns the list.

This is the same flow Thonny's `BareMetalMicroPythonProxy._is_potential_port` does — but factored across plugins, not hard-coded.

---

## 7. The Agent Surface (MCP Tools)

The HAL exposes its capability surface to the agent through MCP. Each capability becomes an MCP tool, namespaced by device ID.

### 7.1 MCP tool naming

For each device D with capabilities C, the HAL generates:
- `device.list` — list all known devices
- `device.get` — get metadata for a device by ID
- `<capability>.<device_id>` — e.g., `repl.execute.esp32s3_left`, `flash.esp32s3_left`

The agent sees a uniform tool surface, regardless of which plugin the device uses.

### 7.2 Example MCP session

```python
# Agent via MCP:
mcp.call("device.list")
# → [{id: "esp32s3-left", chip: "ESP32-S3", ...}, {id: "rp2040-pico", chip: "RP2040", ...}]

mcp.call("repl.execute.esp32s3_left", {"code": "import os; print(os.uname())"})
# → {stdout: "(sysname='rp2', ...)", stderr: "", duration_ms: 234}

mcp.call("filesystem.read.esp32s3_left", {"path": "/main.py"})
# → {content: "from machine import Pin\nled = Pin(2, Pin.OUT)\n...", size: 234}

mcp.call("flash.esp32s3_left", {"firmware": "/path/to/firmware.bin", "erase": true})
# → stream of progress events → final result
```

The agent's LLM gets a uniform surface. It does not need to know that one device is an ESP32 and another is an RP2040. The HAL handles the dispatch.

### 7.3 Why this matters for "AI-native"

The "AI-native hardware IDE" promise is satisfied at the HAL level. Once the HAL is in place, any agent (Gemini, Claude, local Ollama, a custom LangGraph agent) can:
- List devices.
- Identify chips.
- Read / write files.
- Execute code.
- Install packages.
- Flash firmware.
- Stream serial output.

All through a uniform MCP tool surface. All backed by a small, well-defined HAL. All without the agent ever needing to know the chip-specific details.

---

## 8. Capability Gating and Safety

The HAL enforces capability gating. A device's plugin declares which capabilities it supports; the HAL rejects invocations of unsupported capabilities with a clear error.

```python
# Example: trying to flash an ESP32 with the wrong firmware type
mcp.call("flash.esp32s3_left", {"firmware": "pico.uf2"})
# → Error: "Device 'esp32s3-left' (ESP32-S3) does not support UF2 flashing. Use the 'tinkr-esp32-uf2-flash' tool for RP2040 UF2 files."
```

Plugins can also declare *invariants* — runtime checks the HAL runs before dispatch:
- "The `flash` capability requires the firmware file to be a `.bin`."
- "The `flash` capability refuses to write to a chip that is currently in deep sleep."
- "The `package.install` capability requires `filesystem.write` to be supported."

This is the same defense-in-depth pattern as the AI tool registry, applied to hardware. It is the project's safety layer.

---

## 9. The HAL and the Three User Personas

| Persona | What they care about | HAL surface they use |
|---|---|---|
| **Hobbyist** | "Just works." Plug in the board, see it in the list, deploy code, see output. | `device.scan`, `device.list`, `repl.execute`, `filesystem.read/write` |
| **Educator** | Multi-student setup, multiple boards, predictable behavior. | `device.list` (with nicknames), `flash` (to known-good firmware), `package.install` (to known-good packages) |
| **Embedded engineer** | REPL + serial monitor + flash + GDB + custom plugin. | Everything. Plus the ability to add a custom plugin and have the HAL pick it up automatically. |

The HAL is the same for all three. The UI and the agent surface the same HAL capabilities to all three. The plugins are the only thing that differs.

---

## 10. Open Questions

1. **Where does the HAL live in the codebase?** Recommendation: in `tinkr.core.hal` (a small module), not in any plugin. Plugins provide adapters that *implement* the HAL; the HAL itself is plugin-agnostic.
2. **Should the HAL be a process boundary (a separate binary) or in-process (a Python module)?** Recommendation: in-process for v1; revisit if a Rust or Tauri UI needs a separate process for perf reasons.
3. **Should the device registry be per-project, per-user, or both?** Recommendation: per-project (`.tinkr/state/devices.toml`) for the project's known devices; per-user (`~/.tinkr/known-devices.toml`) for cross-project nicknames. The project wins on conflict.
4. **Should the HAL support network-attached devices (WiFi, WebREPL, MQTT)?** Yes, but as a "transport" attribute of the device, not a separate concept. The same capability surface works over any transport.
5. **Should the HAL support multiple simultaneous devices for batch operations?** Yes for read-only ops (`device.scan`, `device.list`); opt-in for write ops (`flash all`, `deploy to all`). Recommendation: v2 feature.
6. **Should the HAL be exposed as a Rust crate too?** Yes, eventually. The Rust HAL would be a thin wrapper over the CLI tools (same NDJSON contract). The Python HAL is the reference; the Rust HAL is for performance-critical paths (e.g., the Tauri UI's reactive device list).
