# Tinkr Plugin Package Specification — v0.1

> The contract for hardware-specific Tinkr plugins. A plugin is a small, versioned, installable unit that adds support for a new chip family, board, or device class to a Tinkr project. Plugins are pure data + CLI tools + knowledge files — not native code, not AI-written, not auto-executed. Humans build them, ship them via git, and the community shares them.

---

## 1. What a Plugin Is

A **Tinkr plugin** is a directory (or git repo, or `.tar.gz`) that contains:

- A `tinkr.plugin.toml` manifest declaring what the plugin provides
- One or more **CLI tools** (Python or Rust) that talk to the device
- A **knowledge bundle** — datasheets, chip DBs, pin maps, register references, example projects
- An optional **MCP server** entry (auto-derived from CLI tools if absent)
- **Tests** using `socat` virtual serial ports
- A `README.md` and `LICENSE`

A plugin is the **only** way to add new hardware support to Tinkr. There is no other extension point. This is intentional: one way to do it, well-documented, versioned, and shareable.

### 1.1 Design principles

| Principle | Meaning |
|---|---|
| **Stateless** | The plugin owns no runtime state. All state lives in the user's project repo. |
| **Lightweight** | A plugin is small (KB to low-MB). It does not bundle runtimes or models. |
| **Composable** | Multiple plugins can be installed in one project. They do not conflict. |
| **Local-first** | A plugin works fully offline. Network is only used for updates. |
| **Human-authored** | A plugin is written by a human. The "self-growing" loop is community + user, not AI. |
| **Open by default** | The plugin registry is a public git repo (or set of repos). MIT-licensed reference plugins. |
| **Verifiable** | `tinkr plugin validate` checks the manifest, the tools, the knowledge, the tests. |
| **Reversible** | `tinkr plugin remove` deletes the plugin's files from `.tinkr/`. The project repo is unchanged. |

### 1.2 What a plugin is NOT

- Not a fork of Tinkr. Plugins live in user projects, not the Tinkr repo.
- Not a runtime. Plugins are not processes. They are *invoked* by Tinkr's runtime.
- Not AI-generated. A plugin is a human artifact with a human-readable manifest and a human-readable changelog. (The "AI-native" claim applies to Tinkr's *use* of plugins, not to plugin *creation*.)
- Not a vendor lock-in. A plugin's CLI tools can be invoked by hand: `tinkr-esp32-port-scan --port /dev/cu.usbserial-XXX`. No Tinkr required.

---

## 2. Plugin Package Layout

```
my-tinkr-plugin/
├── tinkr.plugin.toml          # Required: manifest
├── README.md                  # Required: human-readable description
├── LICENSE                    # Required: SPDX identifier (MIT, Apache-2.0, etc.)
├── CHANGELOG.md               # Required: version history
├── cli/                       # Required: one or more CLI tools
│   ├── tinkr-<domain>-<action>.py
│   └── ...
├── knowledge/                 # Optional: datasheets, chip DBs, etc.
│   ├── chips/
│   │   └── esp32.json
│   ├── pinouts/
│   │   └── esp32-devkitc.json
│   ├── datasheets/
│   │   └── esp32-datasheet.pdf
│   └── references/
│       └── micropython-stdlib.md
├── mcp/                       # Optional: explicit MCP server
│   └── server.py              # If absent, Tinkr auto-derives from CLI tools
├── examples/                  # Optional: sample projects
│   └── tinkr-led/
│       ├── tinkr.toml
│       └── main.py
├── tests/                     # Required: at least one test
│   ├── test_port_scan.py
│   ├── test_repl.py
│   └── fixtures/
│       └── virtual-serial.sock
└── schemas/                   # Optional: Pydantic models for plugin-specific data
    └── device_state.py
```

### 2.1 Required files

| File | Required | Purpose |
|---|---|---|
| `tinkr.plugin.toml` | Yes | Manifest: name, version, capabilities, dependencies, tools |
| `README.md` | Yes | Human description, install instructions, supported devices |
| `LICENSE` | Yes | SPDX identifier |
| `CHANGELOG.md` | Yes | SemVer version history |
| `cli/` | Yes | At least one CLI tool |
| `tests/` | Yes | At least one passing test |

### 2.2 Optional files

| File | Purpose |
|---|---|
| `knowledge/` | Datasheets, chip DBs, pin maps, reference docs |
| `mcp/server.py` | Explicit MCP server (auto-derived if absent) |
| `examples/` | Sample projects that demonstrate the plugin |
| `schemas/` | Pydantic models for plugin-specific data shapes |

---

## 3. The Manifest: `tinkr.plugin.toml`

### 3.1 Schema

```toml
# Plugin identity
[plugin]
name = "tinkr-esp32"                # Required. Unique. "tinkr-<vendor>-<family>"
display_name = "ESP32 Family Support"
version = "0.4.2"                   # Required. SemVer.
description = "ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6 support via esptool and minny"
authors = ["ronie joseph <ronie@example.com>"]
license = "MIT"                     # Required. SPDX.
homepage = "https://github.com/tinkr-esp32/tinkr-esp32"
repository = "https://github.com/tinkr-esp32/tinkr-esp32.git"

# What this plugin provides
[provides]
families = ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32c2"]
boards = ["ESP32-DevKitC", "ESP32-S3-DevKitC-1", "M5Stack-CoreS3", "NodeMCU-32S"]
firmware_types = ["micropython", "circuitpython", "arduino", "esp-idf"]
transports = ["serial", "usb-native", "webrepl"]

# What the plugin can do
[capabilities]
flash = true                        # Can write firmware
repl = true                         # Can open interactive REPL
filesystem = true                   # Can read/write device filesystem
package_manager = true              # Can install/remove packages
gdb = false                         # GDB debugging support
wifi_sim = false                    # WiFi simulation
logic_analyzer = false              # Virtual logic analyzer
ota_update = false                  # Over-the-air firmware update
serial_plotter = true               # Real-time numeric stream
custom_capabilities = ["esp32-deep-sleep", "esp32-ulp-coprogram"]

# Plugin dependencies
[dependencies]
tinkr = ">=0.2.0,<0.4.0"            # Tinkr core version range
python = ">=3.11"
packages = [
    "esptool>=5.2",
    "minny>=0.13",
    "pyserial>=3.4",
    "pydantic>=2.0",
]
optional_packages = [
    "ngspice>=40",                  # Only needed for analog sim
]
plugins = [
    "tinkr-micropython-runtime@^0.3",  # Other Tinkr plugins
]

# CLI tools provided
[[tools]]
name = "tinkr-esp32-port-scan"
entry = "cli/tinkr_esp32_port_scan.py"
runtime = "python"                  # python | rust
description = "Scan for ESP32 devices on all serial ports"
tier = 1

[[tools]]
name = "tinkr-esp32-flash-firmware"
entry = "cli/tinkr_esp32_flash_firmware.py"
runtime = "python"
description = "Flash ESP32 firmware via esptool"
tier = 1
requires_device = true
requires_port = true
streaming = true

# MCP exposure (optional override)
[mcp]
# If absent, Tinkr auto-derives MCP tools from [[tools]] entries
entry = "mcp/server.py"             # Optional explicit server
tool_prefix = "esp32"               # MCP tools become esp32.port_scan, esp32.flash_firmware, etc.

# Knowledge bundle
[knowledge]
chips = ["knowledge/chips/*.json"]
pinouts = ["knowledge/pinouts/*.json"]
datasheets = ["knowledge/datasheets/*.pdf"]
references = ["knowledge/references/*.md"]
# When the plugin is installed, these files are referenced by their
# absolute path in the project's .tinkr/knowledge/<plugin>/ directory.

# Build / publish metadata
[build]
build_command = "python -m build"   # Optional: pre-publish validation step
test_command = "pytest tests/"      # Required: must pass before publish
entry_test = "tests/test_smoke.py"

# Compatibility
[compatibility]
tested_tinkr_versions = ["0.2.0", "0.3.0"]
tested_platforms = ["darwin", "linux", "win32"]
tested_python = ["3.11", "3.12", "3.13"]
maturity = "stable"                 # experimental | beta | stable | deprecated
```

### 3.2 Field reference

#### `[plugin]`
- `name` (string, required) — Unique identifier. Convention: `tinkr-<vendor>-<family>`. Used in `tinkr plugin add <name>`.
- `display_name` (string, required) — Human-readable name.
- `version` (string, required) — SemVer 2.0.0.
- `description` (string, required) — One-line description.
- `authors` (array, required) — Name + email.
- `license` (string, required) — SPDX identifier.
- `homepage`, `repository` (string, optional) — URLs.

#### `[provides]`
- `families` (array) — MCU family identifiers (`esp32`, `rp2040`, `nrf52`, etc.).
- `boards` (array) — Specific board names this plugin supports.
- `firmware_types` (array) — `micropython`, `circuitpython`, `arduino`, `esp-idf`, `zephyr`, etc.
- `transports` (array) — Communication channels: `serial`, `usb-native`, `webrepl`, `ble`, `wifi`, etc.

#### `[capabilities]`
- Standard capabilities (booleans): `flash`, `repl`, `filesystem`, `package_manager`, `gdb`, `wifi_sim`, `logic_analyzer`, `ota_update`, `serial_plotter`, `power_mgmt`.
- `custom_capabilities` (array) — Plugin-specific capabilities (used in MCP tool description).

#### `[dependencies]`
- `tinkr` (string) — Required Tinkr core version range (SemVer).
- `python` (string) — Required Python version range.
- `packages` (array) — Required pip packages with version specifiers.
- `optional_packages` (array) — Optional pip packages (gated by capability flags).
- `plugins` (array) — Other Tinkr plugins required (`name@version-range`).

#### `[[tools]]` (array of tables)
- `name` (string, required) — Must match the CLI tool's invocation name.
- `entry` (string, required) — Path relative to plugin root.
- `runtime` (string, required) — `python` or `rust`.
- `description` (string, required) — One-line description.
- `tier` (int) — 1 (critical), 2 (high), 3 (medium), 4 (low). Used in UI prioritization.
- `requires_device` (bool) — Whether a physical device must be connected.
- `requires_port` (bool) — Whether a serial port must be specified.
- `streaming` (bool) — Whether the tool emits NDJSON `progress` events.

#### `[mcp]` (optional)
- `entry` (string) — Path to explicit MCP server. If absent, Tinkr auto-derives.
- `tool_prefix` (string) — Prefix for MCP tool names. Default: plugin name without `tinkr-`.

#### `[knowledge]`
- `chips`, `pinouts`, `datasheets`, `references` (arrays) — Glob patterns for files in the knowledge bundle. Referenced by absolute path in `.tinkr/knowledge/<plugin>/`.

#### `[build]`
- `build_command` (string, optional) — Run before `tinkr plugin publish`.
- `test_command` (string, required) — Must pass before publish.
- `entry_test` (string, required) — Smoke test that runs on `tinkr plugin install`.

#### `[compatibility]`
- `tested_tinkr_versions`, `tested_platforms`, `tested_python` (arrays) — Proven compatible.
- `maturity` (string) — `experimental`, `beta`, `stable`, `deprecated`.

---

## 4. CLI Tool Contract

A plugin's CLI tools follow the same NDJSON contract as the existing `tinkr.cli/tools/*` tools. The contract is fully specified in `lib/ndjson_protocol.py`. Re-stated here for plugin authors:

### 4.1 Output (NDJSON on stdout)

```json
{"type":"progress","stage":"connecting","pct":0,"message":"..."}
{"type":"progress","stage":"connecting","pct":50,"message":"..."}
{"type":"result","status":"ok","data":{"port":"/dev/cu.usbserial-XXX","chip":"esp32s3"}}
```

### 4.2 Errors (NDJSON on stdout, then exit 1)

```json
{"type":"error","code":"PORT_NOT_FOUND","message":"...","recoverable":true,"suggestion":"..."}
```

### 4.3 User feedback (NDJSON on stderr)

```json
{"type":"user_feedback","id":"confirm_erase","prompt":"Erase flash?","options":["yes","no"],"default":"no"}
```

### 4.4 User response (single line on stdin)

```json
{"id":"confirm_erase","response":"yes"}
```

### 4.5 Naming convention

`tinkr-<domain>-<action>` — e.g., `tinkr-esp32-port-scan`, `tinkr-esp32-flash-firmware`. The domain should be scoped to the plugin's namespace (e.g., `esp32`, not just `port`).

### 4.6 Invocation

```bash
# From the host shell (no Tinkr required)
tinkr-esp32-port-scan

# From Tinkr (via the runtime)
tinkr runtime tool invoke tinkr-esp32-port-scan

# Via the MCP server (auto-derived)
mcp.call("esp32.port_scan", {})
```

---

## 5. Knowledge Bundle Contract

The knowledge bundle is a directory of read-only files (datasheets, chip DBs, pinouts, reference docs) that the plugin ships. When the plugin is installed, these files are **referenced by absolute path** in the project's `.tinkr/knowledge/<plugin>/` directory. They are not parsed by Tinkr itself; Tinkr only knows the paths and the schema.

### 5.1 Reference, not parse

Tinkr does not parse datasheets. It does not OCR pinout diagrams. It knows:
- The path to a chip DB JSON file
- The path to a pinout diagram (PNG / SVG)
- The path to a datasheet PDF
- The path to a reference doc

Any consumer (UI, agent, third-party tool) can open the file by path. The schema of the file (if it's structured) is defined by the plugin, not by Tinkr.

### 5.2 Example: chip DB JSON

```json
// knowledge/chips/esp32s3.json
{
  "family": "esp32s3",
  "vendor": "Espressif",
  "core": "Xtensa LX7",
  "clock_mhz_max": 240,
  "flash_kb": 8192,
  "psram_kb": 512,
  "wifi": true,
  "bluetooth": true,
  "usb_native": true,
  "gpio_count": 45,
  "adc_count": 20,
  "datasheet_pdf": "knowledge/datasheets/esp32-s3-datasheet.pdf",
  "reference_manual_pdf": "knowledge/datasheets/esp32-s3-reference-manual.pdf",
  "default_firmware": "micropython",
  "flash_address": "0x0",
  "url": "https://www.espressif.com/en/products/socs/esp32-s3"
}
```

### 5.3 Why "reference, not parse"

This is the key design decision. By *referring* to knowledge rather than *parsing* it:
- The knowledge is human-readable, human-editable, human-shareable.
- There is no Tinkr-version-coupled schema migration.
- The AI agent can use any tool it wants (a PDF reader, a JSON parser, an image viewer) to read the knowledge.
- The plugin is small (KBs of metadata, not MBs of structured data).
- The user can add their own datasheets and notes to `.tinkr/knowledge/` and the agent will find them.

---

## 6. The `tinkr plugin` CLI

A first-class CLI for managing plugins. Subcommands:

### 6.1 `tinkr plugin init`

Scaffold a new plugin in the current directory. Interactive or `--name` flag.

```bash
$ tinkr plugin init --name tinkr-esp32
✓ Created tinkr.plugin.toml
✓ Created cli/tinkr_esp32_port_scan.py (Hello World)
✓ Created tests/test_port_scan.py
✓ Created knowledge/chips/esp32.json (stub)
✓ Created examples/tinkr-led/main.py
✓ Created README.md
✓ Created CHANGELOG.md

Next: cd into the new plugin, edit tinkr.plugin.toml,
add your CLI tools, then `tinkr plugin validate`.
```

### 6.2 `tinkr plugin validate`

Check the manifest, the CLI tools (do they exist, are they executable, do they parse), the knowledge bundle (do the files exist, are the JSON files valid), the tests (do they pass).

```bash
$ tinkr plugin validate tinkr-esp32/
✓ Manifest valid (SemVer 0.4.2, MIT, all required fields)
✓ 4 CLI tools found, all executable
✓ Knowledge bundle: 12 files (3 chip DBs, 2 pinouts, 4 datasheets, 3 refs)
✓ All chip DBs parse as JSON
✓ All tests pass (5/5)
✓ Pinout diagram dimensions valid (1200x800)
✓ No Python 3.10-only syntax detected (compatible with 3.11+)
```

### 6.3 `tinkr plugin add <name>`

Install a plugin into the current project. Resolves the plugin from the registry (git-based), downloads it, and copies its files into the project's `.tinkr/plugins/<name>/`. Adds it to `tinkr.toml` (project file).

```bash
$ tinkr plugin add tinkr-esp32
Resolving tinkr-esp32 from registry... ✓
Found 1.2.3 (latest stable) — testing on Tinkr 0.3.x: ✓
Downloading to .tinkr/plugins/tinkr-esp32/... ✓
Linking CLI tools to .tinkr/bin/... ✓ (4 tools)
Linking knowledge to .tinkr/knowledge/tinkr-esp32/... ✓ (12 files)
Adding to tinkr.toml... ✓
Validating against project devices... ✓
Running plugin's test suite against project... ✓ (5/5)

Installed tinkr-esp32@1.2.3.
Run `tinkr device scan` to see your connected ESP32 devices.
```

### 6.4 `tinkr plugin remove <name>`

Uninstall a plugin from the current project. Removes its files from `.tinkr/`. Updates `tinkr.toml`. The plugin's *original source* is untouched.

```bash
$ tinkr plugin remove tinkr-esp32
Removing .tinkr/plugins/tinkr-esp32/... ✓
Removing .tinkr/bin/tinkr-esp32-*... ✓
Updating tinkr.toml... ✓
No project files changed. Plugin source is unchanged.
```

### 6.5 `tinkr plugin list`

List installed plugins in the current project.

```bash
$ tinkr plugin list
NAME              VERSION  MATURITY  DEVICES  CAPABILITIES
tinkr-esp32       1.2.3    stable    2/3      flash, repl, fs, plotter
tinkr-rp2040      0.8.0    beta      0/1      flash, repl, fs
tinkr-sniffer     0.1.2    exp.      -        serial-monitor
```

### 6.6 `tinkr plugin publish`

Publish the current plugin to the registry. Requires the user to be logged in to the registry (GitHub-based auth for the open-source registry; service-based auth for the future services registry). Runs `tinkr plugin validate` first.

```bash
$ tinkr plugin publish
Validating... ✓
Bumping version (currently 0.4.2)... 0.4.3 (patch, suggested)
Pushing to registry/tinkr-esp32.git... ✓
Opening PR for review... ✓
URL: https://github.com/tinkr-registry/tinkr-esp32/pull/42

Your plugin is now in the community review queue.
After approval, run `tinkr plugin update` in your projects to get 0.4.3.
```

### 6.7 `tinkr plugin search <query>`

Search the public registry for plugins.

```bash
$ tinkr plugin search "esp32"
NAME                  STARS  DOWNLOADS  LATEST  MATURITY
tinkr-esp32           342    12,450     1.2.3   stable
tinkr-esp32-ulp       18     892        0.2.0   beta
tinkr-esp32-matter    5      124        0.1.0   exp.
```

### 6.8 `tinkr plugin update [<name>]`

Update installed plugins to the latest compatible version.

```bash
$ tinkr plugin update tinkr-esp32
Checking for updates... tinkr-esp32 1.2.3 → 1.3.0 (compatible)
Downloading 1.3.0... ✓
Validating against project... ✓
Running tests... ✓ (5/5, 2 new)

Updated tinkr-esp32@1.3.0.
```

---

## 7. Plugin Discovery (Registry)

The open-source plugin registry is a **git repo of git submodules**. This is the simplest possible registry:

- The registry repo is `github.com/tinkr-registry/index` (or self-hosted).
- Each plugin is a git submodule pointing to its own repo.
- `index/plugins.toml` lists every plugin, its repo URL, its latest version.
- Discovery is `git clone --recursive` of the index, then read `plugins.toml`.
- Updates are `git submodule update --remote` plus re-reading `plugins.toml`.

### 7.1 Why git, not a database

- Decentralized — anyone can fork the registry and run their own.
- No service to operate.
- Git handles versioning, provenance, signatures.
- Works offline (`git clone` once, then everything is local).
- Mirroring is trivial (the same pattern as Homebrew formulae, Linux distros, etc.).

### 7.2 Why not the public npm/PyPI registry

- A plugin is a multi-file bundle (manifest + tools + knowledge + tests), not a single package.
- A plugin's "package" is the whole repo, not a wheel.
- The plugin's knowledge files (datasheets, etc.) are too large for PyPI (which has a hard 100 MB per release cap).
- The plugin's CLI tools need to be invoked by name (`tinkr-esp32-port-scan`), not imported.
- The plugin's MCP tools are auto-derived from the manifest, not from a Python decorator.

### 7.3 Future services registry

For commercial / paid plugins (e.g., a vendor's first-party plugin with guaranteed support), the same manifest format works, but the registry is a service with auth, billing, and SLAs. The plugin spec does not change. The CLI commands (`tinkr plugin add`, etc.) accept either a git URL or a registry name.

---

## 8. The Plugin Lifecycle

```
                  ┌─────────────────────────────────────────────┐
                  │  Author writes plugin locally                │
                  │  - tinkr plugin init                        │
                  │  - fills in CLI tools, knowledge, tests     │
                  │  - tinkr plugin validate (must pass)        │
                  └────────────────┬────────────────────────────┘
                                   │ tinkr plugin publish
                                   ▼
                  ┌─────────────────────────────────────────────┐
                  │  Public registry (git-based)                │
                  │  - PR-based review                          │
                  │  - CI runs tinkr plugin validate            │
                  │  - Approved → merged to index               │
                  └────────────────┬────────────────────────────┘
                                   │ tinkr plugin add <name>
                                   ▼
                  ┌─────────────────────────────────────────────┐
                  │  User's project                             │
                  │  - .tinkr/plugins/<name>/ copied            │
                  │  - .tinkr/bin/ linked                       │
                  │  - .tinkr/knowledge/<name>/ linked          │
                  │  - tinkr.toml updated                       │
                  │  - tinkr device scan picks up new devices   │
                  └────────────────┬────────────────────────────┘
                                   │ project git commit
                                   ▼
                  ┌─────────────────────────────────────────────┐
                  │  Project repo (user's memory)               │
                  │  - tinkr.toml                               │
                  │  - main.py, lib/, etc.                      │
                  │  - .tinkr/ knowledge + plugins              │
                  │  - all versioned, all shareable             │
                  └─────────────────────────────────────────────┘
```

---

## 9. Versioning and Compatibility

### 9.1 Plugin SemVer

A plugin follows SemVer 2.0.0 strictly:
- **MAJOR**: Breaking changes to the manifest, the CLI tool names/args, or the MCP tool surface.
- **MINOR**: New tools, new knowledge files, new capabilities. Backwards-compatible.
- **PATCH**: Bug fixes, doc updates, dependency bumps. Backwards-compatible.

### 9.2 Tinkr core compatibility

The `[dependencies].tinkr` field is a SemVer range. `tinkr plugin add` only installs if the current Tinkr core version satisfies the range. A plugin author can support multiple Tinkr versions by widening the range.

### 9.3 Project lockfile

Each project has a `.tinkr/lock.toml` (or similar) that pins the exact installed version of every plugin. `tinkr plugin update` updates the lockfile. The lockfile is committed to the project repo (just like `package-lock.json` or `poetry.lock`).

---

## 10. Reference Implementation: `tinkr-esp32`

The first plugin to ship. It is the one the existing `tinkr.cli/tools/*` Python tools evolve into. Spec:

- **Name**: `tinkr-esp32`
- **Version**: 0.4.2 → 1.0.0 by the v1.0 release
- **Maturity**: stable (after validation)
- **Provides**: esp32, esp32s2, esp32s3, esp32c3, esp32c6, esp32c2
- **Boards**: ESP32-DevKitC, ESP32-S3-DevKitC-1, M5Stack-CoreS3, NodeMCU-32S, ESP32-C3-DevKitM-1
- **Firmware**: micropython, circuitpython, esp-idf, arduino
- **CLI tools** (4): `tinkr-esp32-port-scan`, `tinkr-esp32-flash-firmware`, `tinkr-esp32-repl-execute`, `tinkr-esp32-fs-list`
- **Knowledge bundle**: 12 chip DBs, 8 pinout diagrams, 5 datasheets, 10 reference docs
- **MCP tools**: 4 (auto-derived from CLI tools)
- **Dependencies**: tinkr >= 0.2.0, python >= 3.11, esptool >= 5.2, minny >= 0.13, pyserial >= 3.4
- **Tests**: 8 (use `socat` virtual serial ports)

This plugin is the **first v1.0 deliverable**. Until the plugin is split out of `tinkr.cli/`, the existing tool directory is the reference implementation. The split is a packaging refactor, not a reimplementation.

---

## 11. Open Questions

1. **Where does the `tinkr` core binary live?** Is it a PyInstaller bundle, a `pip install tinkr` package, a `cargo install tinkr`, or a Tauri-app-bundled sidecar? The plugin spec is independent of this answer, but the install UX depends on it.
2. **Should the plugin's CLI tools be invokable by name globally, or only through `tinkr runtime tool invoke`?** Globally is friendlier (you can `tinkr-esp32-port-scan` from any shell), but it requires PATH manipulation. Through `tinkr runtime tool invoke` is more controlled but less shell-friendly. Recommendation: globally, with the tools symlinked to `~/.local/bin/` on install.
3. **Should the plugin's knowledge bundle be downloaded on demand, or always fully installed?** Always fully installed is simpler and supports offline; on-demand is smaller but requires network. Recommendation: always fully installed. Knowledge is small.
4. **Should the plugin manifest be TOML, JSON, or YAML?** TOML is the simplest for the project (`tinkr.toml`) and is consistent. JSON is most universal but ugly. YAML is most flexible but error-prone. Recommendation: TOML.
5. **Should plugins be allowed to ship Rust binaries?** `[[tools]].runtime = "rust"` is in the spec but no Rust toolchain is assumed. A Rust plugin would require the user to have a Rust toolchain installed. Recommendation: allow it, but mark as `maturity = "beta"` until at least 3 reference plugins ship in Rust.
6. **What is the policy on a plugin writing to `tinkr.toml` or the project source?** The plugin is read-only with respect to the project. It can write to its own `.tinkr/plugins/<name>/` subdirectory. It cannot write to `main.py`, `lib/`, etc. Enforced by filesystem permissions + a manifest declaration of write scope.
