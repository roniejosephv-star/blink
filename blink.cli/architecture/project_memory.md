# Tinkr Project Memory Design — v0.1

> The user's project repo is the memory. Tinkr itself stores nothing. Everything the user cares about — datasheets, chip DBs, pin maps, the current device, the plugin list, the project config — lives in the project, in `.tinkr/` and in the project's own files (`main.py`, `lib/`, etc.). Tinkr reads these by reference; it does not duplicate, normalize, or "own" them.

This is the design that makes "Tinkr is lightweight" and "doesn't store any device data" actually true.

---

## 1. The Core Idea

A Tinkr project is a normal Python (or other) project that has a `.tinkr/` directory in its root. That directory holds:

- **`tinkr.toml`** — the project-level config (plugins, devices, knowledge refs, user prefs)
- **`plugins/`** — symlinks (or shallow copies) of installed Tinkr plugins
- **`bin/`** — symlinks to the plugins' CLI tools (so the user can `tinkr-esp32-port-scan` from the project root)
- **`knowledge/`** — symlinks to the plugins' knowledge bundles, plus the user's own datasheets and notes
- **`state/`** — gitignored runtime state (last device, last flash, build cache)
- **`lock.toml`** — pinned versions of every installed plugin (committed)

That's it. The project repo is the source of truth. Tinkr reads from it; it does not write to it (except for `state/` and `lock.toml`, with explicit user consent for `lock.toml`).

### 1.1 The user owns the data

This is a deliberate design choice with real consequences:

- **The project is git-versioned.** Every change to plugins, knowledge, and config is a commit. The user has a full history.
- **The project is portable.** Move it to another machine, run `tinkr plugin install` (which reads `lock.toml`), and the project is fully set up.
- **The project is shareable.** Send the repo to a friend; they get the same setup.
- **The project is the documentation.** `tinkr.toml` lists the plugins; `lock.toml` pins the versions; the user's code is the code.
- **Tinkr can be uninstalled** and the project still works (because the CLI tools are invokable by name, not through Tinkr).

### 1.2 What is gitignored, what is committed

| Path | Committed? | Why |
|---|---|---|
| `tinkr.toml` | Yes | The project's Tinkr config. |
| `.tinkr/lock.toml` | Yes | The plugin lockfile. Reproducible builds. |
| `.tinkr/plugins/<name>/` | **No** (gitignored, or git submodule) | Plugin source lives in the plugin's own repo. We just symlink. |
| `.tinkr/bin/` | No | Symlinks to plugin CLI tools. |
| `.tinkr/knowledge/<name>/` | **Optional** | See section 5. |
| `.tinkr/state/` | **No** | Runtime state (cache, logs, build artifacts). |
| User's project files (`main.py`, `lib/`, etc.) | Yes (user's choice) | The user's code. |

---

## 2. `tinkr.toml` — The Project Config

The single, human-readable, version-controlled project file. TOML, because it's the same format as `pyproject.toml` and is easy to edit by hand.

```toml
# tinkr.toml — the Tinkr project config

[project]
name = "kitchen-sensor"
description = "ESP32 temperature + humidity sensor for the kitchen"
version = "0.1.0"
authors = ["Ronie Joseph <ronie@example.com>"]
license = "MIT"

# What devices this project targets
[targets]
default = "esp32s3-left"           # Set by `tinkr device use`
boards = ["ESP32-S3-DevKitC-1"]
families = ["esp32s3"]
firmware = "micropython"

# Plugins installed in this project
[plugins]
tinkr-esp32 = "^1.2"               # SemVer range
tinkr-micropython-runtime = "^0.3"
tinkr-sniffer = "^0.1"             # Optional / experimental

# Plugin-specific config
[plugins.tinkr-esp32]
# Override defaults per-project (rare; usually defaults are right)
default_baud = 460800
flash_mode = "dio"

# The project's own knowledge (user-added)
[knowledge]
# Datasheets and reference docs the user has added, by path
datasheets = [
    "docs/datasheets/sht31.pdf",
    "docs/datasheets/bme280.pdf",
]
# Chip-specific notes the user has written
notes = [
    "docs/notes/esp32-s3-pinout.md",
    "docs/notes/i2c-bus.md",
]

# The project's package manifest (MicroPython packages)
[dependencies]
# Direct format: just specify the package and a source
"umqtt.simple" = "latest"
"bme280" = "github:miketeachman/micropython-bme280@master"
"sht31" = "local:lib/sht31"

# Device-specific overrides
[devices."esp32s3-left"]
nickname = "kitchen sensor"
location = "kitchen counter"
notes = "Sometimes loses WiFi; check antenna if data stops at 03:00."
last_seen_port = "/dev/cu.usbserial-1410"

[devices."esp32s3-spare"]
nickname = "spare board"
location = "desk drawer"
notes = "Used for development; reset to defaults before deploying to prod."
```

### 2.1 Field reference

#### `[project]`
Standard project metadata. Mirrors `pyproject.toml`'s `[project]` for consistency.

#### `[targets]`
- `default` (string) — The default device for `tinkr` commands without `--device`.
- `boards` (array) — The boards this project is designed for.
- `families` (array) — The chip families the project supports.
- `firmware` (string) — The firmware type: `micropython`, `circuitpython`, `arduino`, etc.

#### `[plugins]`
Map of plugin name → SemVer range. `tinkr plugin add` updates this. `tinkr plugin install` reads it.

#### `[plugins.<name>]`
Plugin-specific config. Each plugin defines its own schema. The plugin's manifest lists the keys it accepts.

#### `[knowledge]`
- `datasheets` (array of paths) — User-added PDFs / docs.
- `notes` (array of paths) — User-added Markdown notes about the project.

#### `[dependencies]`
Mirrors the `[tool.belay.dependencies]` and `pyproject.toml` pattern. Direct map of `package-name = "source"`. Sources:
- `"latest"` — latest from the MicroPython package index
- `"name@version"` — pinned version
- `"github:user/repo@branch"` — from a GitHub repo
- `"gitlab:user/repo"` — from a GitLab repo
- `"local:path"` — a local file or directory in the project

#### `[devices.<id>]`
Per-device user metadata:
- `nickname` (string) — Human-readable name.
- `location` (string) — Where the device physically is.
- `notes` (string) — User's notes about this specific device.
- `last_seen_port` (string) — Last known serial port (transient, used for reconnection).

### 2.2 `tinkr.toml` is for the user

The format is intentionally simple and human-editable. No nested dynamic structures. Every field is documented. The user can `cat tinkr.toml` and understand their project.

---

## 3. `.tinkr/lock.toml` — The Plugin Lockfile

Pinned versions of every installed plugin. Generated by `tinkr plugin add` / `tinkr plugin update`. Committed to the project repo.

```toml
# .tinkr/lock.toml — generated, do not edit by hand
version = "1"

[plugins.tinkr-esp32]
version = "1.2.3"
source = "github:tinkr-registry/tinkr-esp32"
resolved_at = "2026-08-12T14:32:00Z"
checksum = "sha256:abc123..."

[plugins.tinkr-micropython-runtime]
version = "0.3.1"
source = "github:tinkr-registry/tinkr-micropython-runtime"
resolved_at = "2026-08-12T14:32:05Z"
checksum = "sha256:def456..."

[plugins.tinkr-sniffer]
version = "0.1.2"
source = "github:user-contrib/tinkr-sniffer"
resolved_at = "2026-08-12T14:32:10Z"
checksum = "sha256:789abc..."
```

When a teammate clones the project, they run `tinkr plugin install` (or `tinkr install`), which reads `lock.toml` and installs the exact same versions. The same pattern as `poetry.lock`, `package-lock.json`, `Cargo.lock`.

---

## 4. `.tinkr/state/` — Runtime State, Gitignored

Runtime state that is useful but not part of the project source. Gitignored.

```
.tinkr/state/
├── cache/
│   ├── firmware/              # Downloaded firmware files, keyed by URL+checksum
│   │   └── ESP32_GENERIC-v1.24.1.bin
│   └── plugin-index/          # Cached plugin index, refreshed on `tinkr plugin update`
│       └── index.toml
├── devices.toml               # Last-known device-to-port mappings (per-machine)
├── last-build.log             # Output of the last `tinkr project build`
├── last-flash.log             # Output of the last `tinkr project flash`
├── repl-history               # Per-device REPL command history
└── mcp-sessions/              # Active MCP server state
```

`state/devices.toml` is the *transient* device registry — different from `tinkr.toml`'s `[devices]` section, which is *persistent* user metadata. State is gitignored; the user's metadata in `tinkr.toml` is committed.

---

## 5. `.tinkr/knowledge/` — Knowledge Bundle References

Knowledge is referenced, not stored. Three layers:

### 5.1 Layer 1: Plugin-shipped knowledge (symlinks)

When a plugin is installed, its `knowledge/` directory is symlinked into the project:

```
.tinkr/knowledge/
└── tinkr-esp32/ → ../plugins/tinkr-esp32/knowledge/
    ├── chips/esp32s3.json
    ├── pinouts/esp32-s3-devkitc-1.png
    ├── datasheets/esp32-s3-datasheet.pdf
    └── references/micropython-stdlib.md
```

Plugins ship the knowledge that ships with them. The user can read it, but the user doesn't own it.

### 5.2 Layer 2: User-added knowledge (committed)

The user can add their own datasheets, notes, and pinouts:

```
docs/
├── datasheets/
│   ├── sht31.pdf
│   └── bme280.pdf
└── notes/
    ├── esp32-s3-pinout.md
    └── i2c-bus.md
```

These are referenced by relative path in `tinkr.toml` (`[knowledge].datasheets` and `[knowledge].notes`).

### 5.3 Layer 3: Project-cached knowledge (gitignored or git-LFS)

Large files (multi-MB datasheets, full KiCad symbol libraries) that the user does not want to commit to git can be gitignored or stored in git-LFS:

```
docs/datasheets/
└── esp32-s3-datasheet-full.pdf  # 12MB — gitignored or LFS
```

The path is referenced in `tinkr.toml` either way.

### 5.4 Why three layers

- **Plugin-shipped**: The plugin author curates the knowledge. High quality, versioned with the plugin.
- **User-added**: The user customizes. Their notes, their datasheets. Committed because they're part of the project.
- **Project-cached**: The user downloads large files. Either gitignored (re-downloaded on clone) or git-LFS (committed, but efficiently).

The agent (MCP) can read from all three layers. The user can choose.

### 5.5 Why "reference, not parse"

Tinkr does not parse datasheets. It does not OCR pinout diagrams. It knows:
- The path to a chip DB JSON file
- The path to a pinout diagram (PNG / SVG)
- The path to a datasheet PDF
- The path to a reference doc

Any consumer (UI, agent, third-party tool) can open the file by path. The schema of the file (if it's structured) is defined by the plugin, not by Tinkr.

This is the design that makes "everything is downloaded and referenced" actually true. Tinkr is lightweight because it does not try to know everything about every chip; it knows where to find the knowledge and lets the agent / user read it.

---

## 6. The Project Bootstrap Flow

A new project is created like this:

```bash
$ mkdir kitchen-sensor && cd kitchen-sensor
$ tinkr init
✓ Created tinkr.toml
✓ Created .tinkr/
✓ Created .gitignore (ignores .tinkr/state/, .tinkr/cache/)
✓ Created main.py (hello world)
✓ Created lib/ (empty)
✓ Created tests/

$ tinkr plugin add tinkr-esp32
Resolving tinkr-esp32@^1.2 ... ✓ (1.2.3)
Installing to .tinkr/plugins/tinkr-esp32/... ✓
Linking CLI tools to .tinkr/bin/... ✓ (4 tools)
Linking knowledge to .tinkr/knowledge/tinkr-esp32/... ✓ (12 files)
Adding to tinkr.toml [plugins]... ✓
Writing to .tinkr/lock.toml... ✓
Running plugin's entry test... ✓

Installed tinkr-esp32@1.2.3. Run `tinkr device scan` to see your ESP32.

$ tinkr device scan
Scanning ports for all installed plugins... ✓
  /dev/cu.usbserial-1410  ESP32-S3-DevKitC-1  [tinkr-esp32]  → esp32s3-left
  /dev/cu.usbmodem14101   Raspberry Pi Pico   [tinkr-rp2040] → rp2040-pico

$ tinkr device use esp32s3-left
✓ Default device set to esp32s3-left

$ tinkr repl
MicroPython v1.24.1 on ESP32-S3 (kitchen sensor)
Type Ctrl+D to soft-reboot, Ctrl+C to interrupt, Ctrl+] to exit.
>>>
```

The whole flow is: `mkdir`, `tinkr init`, `tinkr plugin add`, `tinkr device scan`, `tinkr repl`. Five commands, ~30 seconds.

---

## 7. The "AI-Native" Loop on Top of Project Memory

The project memory design makes the AI-native claim concrete:

1. **The agent reads `tinkr.toml`** to know which plugins and devices are in scope.
2. **The agent reads `.tinkr/knowledge/<plugin>/`** to access chip DBs, pinouts, datasheets, references.
3. **The agent reads `main.py` and `lib/`** to understand the user's project.
4. **The agent reads `docs/notes/`** to understand the user's intent and quirks.
5. **The agent calls HAL capabilities** to interact with the device.
6. **The agent reads the device's `/main.py` and REPL state** to understand the current run.
7. **The agent proposes changes** — to `main.py`, to `tinkr.toml`, to `docs/notes/`.
8. **The user reviews the diff** and commits.

The agent has access to the *entire project context*, not just the device state. It can reason about pin assignments (from pinout diagrams), package choices (from the datasheets), and the user's specific quirks (from notes).

The agent cannot *write* to the project without explicit user approval. The project's git history is the safety net.

### 7.1 Example: AI helping a hobbyist

The hobbyist says: "I want to add a BME280 sensor to my kitchen sensor project."

The agent:
1. Reads `tinkr.toml` → knows the project is on ESP32-S3 with MicroPython.
2. Reads `.tinkr/knowledge/tinkr-esp32/datasheets/esp32-s3-datasheet.pdf` (the relevant pages) → knows the I2C pins.
3. Reads `docs/datasheets/bme280.pdf` → knows the BME280's I2C address (0x76 or 0x77).
4. Reads `main.py` → sees the current sensor code.
5. Reads `docs/notes/esp32-s3-pinout.md` → confirms the user's I2C pin choice.
6. Suggests the wiring (which pins to connect) and the code (using `bme280` package).
7. Runs `tinkr pkg install bme280` to add the package.
8. Writes a new `lib/bme280_helper.py` and updates `main.py`.
9. Deploys to the device and verifies the readings.

The user reviews the diff (4 files changed), commits, and the new sensor is live.

### 7.2 Example: AI helping an educator

The educator has 10 students, each with an ESP32 and a "tinkr the LED" project.

The agent:
1. Reads `tinkr.toml` → knows the project.
2. Reads the student's `main.py` → sees the buggy code.
3. Reads the REPL output → sees the traceback.
4. Suggests a fix.
5. The fix is reviewed by the educator before being committed.

The agent is a teaching assistant, not an autonomous code-writer. The educator is in the loop.

### 7.3 Example: AI helping an embedded engineer

The engineer is bringing up a new sensor. The agent:
1. Reads the sensor's datasheet (referenced in `docs/datasheets/`).
2. Reads the chip's reference manual (referenced in `.tinkr/knowledge/tinkr-esp32/`).
3. Proposes a driver skeleton.
4. The engineer reviews, refines, and commits.
5. The agent runs the driver's test suite against the device.
6. The agent iterates with the engineer.

The agent is a pair-programming partner, not a replacement.

---

## 8. The Project Memory and the Three User Personas

| Persona | What they store in the project | What the project means to them |
|---|---|---|
| **Hobbyist** | `main.py`, `lib/`, maybe a `docs/notes/` file or two | "My project's stuff." |
| **Educator** | Per-student `main.py`, shared `tinkr.toml` template, example projects | "The student's current work, with reference to the course material." |
| **Embedded engineer** | Driver code, hardware tests, datasheet references, design notes | "Living documentation of the hardware bring-up." |

All three use the same project structure. The HAL is the same. The agent surface is the same. The user adds more knowledge to the project as their needs grow.

---

## 9. Migration from the Current `tinkr.cli/`

The current `tinkr.cli/` structure is a pre-project state. The migration is straightforward:

1. **Move `tinkr.cli/tools/*` to a new `tinkr-esp32` plugin** (a separate repo, or `plugins/tinkr-esp32/` in the same repo). The 12 existing tools become the first 12 CLI tools of the first plugin.
2. **Move `tinkr.cli/knowledge_base/*` to `tinkr-esp32/knowledge/`**. The Thonny spec, the engineering deep-dive, the CLI tools registry — these become the first plugin's knowledge bundle.
3. **Create `tinkr.core`** as a new module (or repo) that contains: the HAL, the MCP server, the `tinkr` CLI, the `tinkr plugin` subcommand, the `tinkr device` subcommand, the `tinkr init` flow.
4. **Create the registry** as a new git repo (`tinkr-registry/index`).
5. **Update the documentation** (`README.md`, `tinkr.cli/architecture/`, `tinkr.cli/knowledge_base/`) to point to the new structure.

This is a 1–2 week packaging refactor, not a reimplementation. The existing code is the reference implementation of the first plugin.

---

## 10. Open Questions

1. **Should the project be a single repo (`kitchen-sensor/`) or a monorepo (`kitchen-sensor/` with `firmware/`, `host/`, etc.)?** Recommendation: single repo, with `firmware/` and `host/` as subdirectories. The user's `main.py` and `lib/` live in `firmware/`. The Tinkr config (`tinkr.toml`, `.tinkr/`) is at the repo root.
2. **Should the `.tinkr/` directory be hidden (the leading dot) or visible?** Hidden is the convention for tool-managed state (`.git/`, `.venv/`, `.cargo/`). Recommendation: hidden.
3. **Should `tinkr.toml` be merged into `pyproject.toml` (under `[tool.tinkr]`)?** This is the Belay pattern. It keeps one config file for Python projects. Recommendation: optional — `tinkr.toml` is the default, but Tinkr reads `[tool.tinkr]` from `pyproject.toml` if `tinkr.toml` is absent.
4. **Should the user be able to add custom CLI tools to a project (not from a plugin)?** Yes, but only for project-specific build/test/deploy scripts. The plugin system is for hardware support; project scripts are for project workflows. Recommendation: `scripts/` directory, auto-discovered, auto-exposed as `tinkr <project>:script-name`.
5. **What is the relationship between the project's package manifest (`[dependencies]`) and a `requirements.txt` or `pyproject.toml` for the project itself?** The Tinkr `[dependencies]` is for *device* packages (MicroPython / CircuitPython). The project's own Python dependencies (for host-side scripts, tests, etc.) live in `pyproject.toml` as normal. Two separate concerns, two separate files.
6. **Should the project memory be backed by something other than git?** For most users, git is right. For students, maybe a simpler `tar` snapshot? Recommendation: git is the default; non-git project initialization is a v2 feature for the educator persona.
