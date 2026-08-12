# tinkr-esp32

The first Tinkr hardware plugin. Adds support for the Espressif ESP32 family (ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6, ESP32-C2) to any Tinkr project.

This is the **reference implementation** of the Tinkr plugin spec. If you are building a plugin for a different chip family, this is the template to follow.

## What this plugin provides

- **5 CLI tools** (Python): port scan, identify, flash firmware, REPL execute, filesystem list.
- **Knowledge bundle**: 6 chip DBs, 6 board pinouts, 3 reference docs, datasheets.
- **HAL adapter**: the typed Python surface the rest of Tinkr uses.
- **Examples**: a `tinkr-led` starter project.
- **Tests**: smoke + integration, using `socat` virtual serial ports for offline testing.

## Install

```bash
# From the project you want to add ESP32 support to
tinkr plugin add tinkr-esp32
```

This copies the plugin's tools into `.tinkr/bin/`, links the knowledge bundle into `.tinkr/knowledge/tinkr-esp32/`, and updates `tinkr.toml` and `.tinkr/lock.toml`.

## CLI tools (invokable from any shell)

```bash
tinkr-esp32-port-scan                    # List all connected ESP32 devices
tinkr-esp32-identify --port /dev/cu.usbserial-1410
tinkr-esp32-flash-firmware --port /dev/cu.usbserial-1410 --firmware ./firmware.bin
tinkr-esp32-repl-execute --port /dev/cu.usbserial-1410 --code "print('hello')"
tinkr-esp32-fs-list --port /dev/cu.usbserial-1410 --path /
```

The CLI tools follow the [Tinkr NDJSON protocol](../../architecture/plugin_spec.md#4-cli-tool-contract). They are invokable by hand — no Tinkr required.

## MCP tools (auto-derived from CLI tools)

When this plugin is installed, the Tinkr MCP server exposes:

- `esp32.port_scan`
- `esp32.identify`
- `esp32.flash_firmware`
- `esp32.repl_execute`
- `esp32.fs_list`

Any MCP-speaking agent (Gemini, Claude, local Ollama, etc.) can call these.

## HAL capabilities

The `ESP32Adapter` class implements these capabilities (per `hal_design.md`):

- `identify`
- `flash`
- `repl.open`, `repl.execute`, `repl.interrupt`, `repl.reboot`
- `filesystem.list`, `filesystem.read`, `filesystem.write`, `filesystem.delete`
- `package.install`, `package.remove`, `package.list`, `package.freeze`
- `serial.monitor`, `serial.plot`
- `power.read`
- `wifi.scan`, `wifi.status`
- Custom: `esp32.deep_sleep`, `esp32.ulp_coprogram`, `esp32.efuse_read`

## Supported devices

| Family | Boards |
|---|---|
| ESP32 | ESP32-DevKitC, NodeMCU-32S |
| ESP32-S2 | ESP32-S2-DevKitC-1 |
| ESP32-S3 | ESP32-S3-DevKitC-1, M5Stack-CoreS3 |
| ESP32-C3 | ESP32-C3-DevKitM-1 |
| ESP32-C6 | ESP32-C6-DevKitC-1 |
| ESP32-C2 | ESP32-C2-DevKitM-1 |

## Architecture

This plugin is a packaging refactor of the original `tinkr.cli/tools/*.py` directory. The 12 existing tools are split into per-chip-family plugins; `tinkr-esp32` is the first (and currently only) one. The NDJSON contract is unchanged.

The HAL adapter is a thin object-oriented wrapper over the CLI tools. Both are kept in sync by the `tinkr plugin validate` CI check.

## License

MIT — see `LICENSE`.
