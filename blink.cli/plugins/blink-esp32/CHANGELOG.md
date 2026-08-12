# Changelog

All notable changes to `tinkr-esp32` are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] — 2026-08-12

### Changed
- Repackaged as the first Tinkr plugin (per `architecture/plugin_spec.md`).
- Original 12 tools in `tinkr.cli/tools/*` evolved into the 5 core tools of this plugin.
- HAL adapter class added (`adapters/esp32_adapter.py`).
- Knowledge bundle split into `chips/`, `pinouts/`, `datasheets/`, `references/`.

### Added
- `tinkr-esp32-port-scan` — port scan (replaces `tinkr_port_scan.py`).
- `tinkr-esp32-identify` — chip identify (replaces `tinkr_flash_detect_chip.py`).
- `tinkr-esp32-flash-firmware` — flash firmware (replaces `tinkr_flash_firmware.py`).
- `tinkr-esp32-repl-execute` — REPL execution (replaces `tinkr_repl_execute.py`).
- `tinkr-esp32-fs-list` — filesystem list (replaces `tinkr_fs_list.py`).
- Reference `tinkr-led` example project.

## [0.3.x] — pre-plugin era

The 12 tools lived in `tinkr.cli/tools/*` and were invokable as `tinkr-*-*.py` scripts. They emitted NDJSON on stdout, used `minny` for device communication, and `esptool` for flashing. The plugin repackaging preserves all of this behavior.
