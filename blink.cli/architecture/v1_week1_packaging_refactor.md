# v1.0 Week 1 — Packaging Refactor Plan

> Concrete, code-level plan for splitting the 12 existing flat Python tools into a `tinkr.core` host + the `tinkr-esp32` reference plugin. Pre-staged while the UI mockup agents finish.

---

## 1. Current state (what we have)

`tinkr.cli/`:
- `tools/` — 12 flat Python scripts, each a standalone Click-style CLI:
  - chip-specific (10): `tinkr_flash_firmware`, `tinkr_flash_detect_chip`, `tinkr_flash_address`, `tinkr_port_scan`, `tinkr_port_identify`, `tinkr_repl_connect`, `tinkr_repl_execute`, `tinkr_fs_list`, `tinkr_fs_upload`, `tinkr_fs_download`, `tinkr_firmware_fetch`
  - core (1): `tinkr_pkg_install` (the plugin installer)
- `lib/ndjson_protocol.py` — shared NDJSON emit/read for the orchestrator
- `plugins/tinkr-esp32/` — already exists (19 files, ~3000 LoC, the reference plugin per `plugin_spec.md`)

The 12 tools are *duplicated* by the `plugins/tinkr-esp32/cli/` directory today. The refactor is the **deletion of the duplication**: the flat tools go away, the plugin becomes the single source of truth for chip-specific commands, and `tinkr.core` owns the installer + plugin loader.

---

## 2. Target structure (what we want)

```
tinkr.cli/
├── pyproject.toml                  # NEW — the `tinkr` Python package
├── tinkr/
│   ├── __init__.py
│   ├── __main__.py                 # NEW — `python -m tinkr` → CLI root
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── root.py                 # NEW — Click group, plugin discovery, version
│   │   ├── plugin_install.py       # MOVED from tools/tinkr_pkg_install.py
│   │   └── plugin_list.py          # NEW — `tinkr plugin list`
│   ├── core/
│   │   ├── plugin_loader.py        # NEW — discover plugins from ~/.tinkr/plugins + venv
│   │   ├── manifest.py             # NEW — parse tinkr.plugin.toml
│   │   ├── device_state.py         # NEW — Pydantic models (moved from plugins/tinkr-esp32/schemas/)
│   │   └── project.py              # NEW — tinkr.toml project model
│   ├── lib/
│   │   └── ndjson_protocol.py      # MOVED from lib/ndjson_protocol.py
│   └── plugins/                    # bundled plugins, shipped with the CLI
│       └── tinkr-esp32/            # KEEP — but reorganize per plugin_spec.md
│           ├── tinkr.plugin.toml
│           ├── adapters/esp32_adapter.py
│           ├── cli/
│           │   ├── __init__.py     # NEW — Click command group "esp32"
│           │   ├── flash_firmware.py       # MOVED from tools/
│           │   ├── flash_detect_chip.py    # MOVED
│           │   ├── flash_address.py        # MOVED
│           │   ├── port_scan.py            # MOVED
│           │   ├── port_identify.py        # MOVED
│           │   ├── repl_connect.py         # MOVED
│           │   ├── repl_execute.py         # MOVED
│           │   ├── fs_list.py              # MOVED
│           │   ├── fs_upload.py            # MOVED
│           │   ├── fs_download.py          # MOVED
│           │   └── firmware_fetch.py       # MOVED
│           ├── knowledge/
│           ├── examples/
│           ├── schemas/
│           └── tests/
└── tests/                          # NEW — tests for tinkr.core
    ├── test_plugin_loader.py
    ├── test_manifest.py
    └── test_plugin_install.py
```

After the refactor:
- `tinkr` is the user-facing command (was: 12 different `tinkr_*` scripts)
- `tinkr plugin install <path>` (was: `tinkr_pkg_install.py`)
- `tinkr plugin list` (NEW)
- `tinkr esp32 flash --port /dev/cu.usbserial-1410 --firmware firmware.bin` (was: `tinkr_flash_firmware.py --port ...`)
- All other chip-prefixed commands follow the same pattern

---

## 3. The 5 sub-tasks (each is a commit-sized unit of work)

### Sub-task 1.1: Create the `tinkr` Python package

- Add `pyproject.toml` at `tinkr.cli/` root with:
  - Package name: `tinkr`
  - Entry point: `console_scripts.tinkr = "tinkr.cli.root:main"`
  - Deps: `click >= 8.1`, `pydantic >= 2.5`, `rich >= 13.0`, `esptool >= 4.7`, `minny >= 0.5`
- Add `tinkr/__init__.py` with `__version__ = "0.1.0"`
- Add `tinkr/__main__.py` for `python -m tinkr` invocation
- Add `tinkr/cli/__init__.py` and `tinkr/cli/root.py` with the Click group

**Done when:** `pip install -e .` succeeds, `tinkr --version` prints `0.1.0`, `tinkr --help` shows the empty root.

### Sub-task 1.2: Move `ndjson_protocol.py` and add core utilities

- Move `lib/ndjson_protocol.py` → `tinkr/lib/ndjson_protocol.py` (no code changes, just path)
- Add `tinkr/core/manifest.py` — parse `tinkr.plugin.toml` with Pydantic
- Add `tinkr/core/plugin_loader.py` — find plugins from:
  1. `tinkr.plugins` Python entry points (bundled)
  2. `~/.tinkr/plugins/*/tinkr.plugin.toml` (user-installed)
  3. `./tinkr.toml`'s `[plugins]` section (project-local)
- Add `tinkr/core/device_state.py` — Pydantic models for device state (currently in `plugins/tinkr-esp32/schemas/device_state.py`); keep the schema but make it core so all plugins share it

**Done when:** `python -c "from tinkr.core import plugin_loader; plugin_loader.discover()"` returns the bundled `tinkr-esp32` plugin.

### Sub-task 1.3: Move `tinkr_pkg_install.py` into Click form

- Convert `tools/tinkr_pkg_install.py` to `tinkr/cli/plugin_install.py` as a Click command
- Behavior unchanged: takes a path (or git URL), copies/symlinks into `~/.tinkr/plugins/<name>`, validates `tinkr.plugin.toml`
- Add `tinkr/cli/plugin_list.py` — `tinkr plugin list` shows installed plugins, version, source path, status

**Done when:** `tinkr plugin install plugins/tinkr-esp32` succeeds, `tinkr plugin list` shows `tinkr-esp32` as installed.

### Sub-task 1.4: Reorganize `tinkr-esp32` plugin per `plugin_spec.md`

- Move 10 chip-specific tools from `tools/tinkr_*` → `tinkr/plugins/tinkr-esp32/cli/tinkr_esp32_*` (the file names already match!)
- Add `cli/__init__.py` to the plugin — Click command group named `esp32`
- Each file gets a Click decorator: `@esp32.command("flash")`, `@esp32.command("repl")`, etc.
- Update the parent to register the sub-command group via the plugin manifest

**Done when:** `tinkr esp32 --help` shows the 10 sub-commands. `tinkr esp32 flash --port X --firmware Y` works the same as the old `tinkr_flash_firmware.py --port X --firmware Y`.

### Sub-task 1.5: Delete the old `tools/` directory and add core tests

- Delete `tinkr.cli/tools/` (the 12 flat scripts)
- Delete `tinkr.cli/lib/` (now `tinkr/lib/`)
- Add `tests/test_plugin_loader.py`, `tests/test_manifest.py`, `tests/test_plugin_install.py`
- Update `plugins/tinkr-esp32/tests/` to use the new `tinkr esp32 ...` invocation
- Run the full test suite; ensure all pass

**Done when:** `pytest tests/` is green. `git status` shows the 12 old scripts deleted, the 10 plugin CLIs reorganized, no orphan references.

---

## 4. The one thing the refactor must NOT do

**It must not change the on-the-wire NDJSON contract.** The Rust orchestrator (Tauri shell) reads NDJSON events from stdout. Every `emit_progress`, `emit_result`, `emit_error` call must produce the same shape as before. The refactor is a packaging change, not a protocol change.

Verified by: running `tinkr esp32 flash --port fake --firmware fake.bin` and confirming the NDJSON stream is byte-identical to the old `tinkr_flash_firmware.py --port fake --firmware fake.bin`.

---

## 5. Risk + mitigation

- **Risk:** Subprocess invocations between the old tools (e.g. `tinkr_flash_firmware.py` calls `tinkr_flash_detect_chip.py` as a subprocess) become Python function calls in the new structure. The two-step pattern was an artifact of the flat layout, not a design choice. **Mitigation:** rewrite as direct function calls; add unit tests that previously couldn't be written (the subprocess layer made them hard).
- **Risk:** Plugin discovery path differs between dev (`pip install -e .`) and installed (`pip install tinkr`). **Mitigation:** use Python entry points for bundled plugins, `~/.tinkr/plugins/` for user plugins. Test both paths.
- **Risk:** The Rust orchestrator's expected CLI surface changes. **Mitigation:** ship an alias shim for one release (`tinkr_flash_firmware.py` → `tinkr esp32 flash`). Or: update the orchestrator in the same PR.

---

## 6. Effort estimate

- Sub-tasks 1.1, 1.2: 4 hours (mostly typing)
- Sub-task 1.3: 1 hour
- Sub-task 1.4: 4 hours (10 file moves + Click conversion)
- Sub-task 1.5: 2 hours (cleanup + tests)
- Total: ~11 hours = ~1.5 working days

A solo dev with the existing test coverage lands this in 2 days with margin. A fresh dev lands it in 3-4 days.

---

## 7. When this lands

The refactor is the prerequisite for **everything else in the 8-week v1.0 plan**: HAL adapter calls go through `tinkr.core`, project memory is in `tinkr.core.project`, the agent reads from `tinkr.core.device_state`, the Tauri shell calls `tinkr <plugin> <command>`.

Without this refactor, every subsequent week's work piles technical debt. With it, weeks 2-8 land in their planned positions.

**Awaiting Ronie's go-ahead.**
