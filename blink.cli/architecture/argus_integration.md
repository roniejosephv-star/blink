# Argus → tinkr-rpi5 Integration Plan — Argus is the prototype, Tinkr is the product

> Argus at `/Users/mindflow/Projects/Hackathon/Arm Create/argus` is Ronie's prototype repo. It's not shipped, it's a working proof-of-concept. The production code lives in `tinkr.cli/plugins/tinkr-rpi5/`. The argus repo becomes a reference / template that the plugin development uses as the source of architectural truth.

---

## 0. Reorientation: from "wrap" to "develop"

The earlier draft of this plan (Aug 12 18:25) framed argus as a third-party dependency to wrap. **Ronie has clarified**: argus is not a separate product. It's a prototype. The argus architecture, CLI patterns, Pydantic models, and FastMCP server are the **starting point** for the tinkr-rpi5 plugin. The argus code gets developed, refactored, and absorbed into Tinkr. The argus repo stays as a reference.

This is a simpler, more direct integration. No version-pinning, no external package, no drift. The tinkr-rpi5 plugin owns its destiny.

---

## 1. The mapping (argus module → tinkr plugin module)

---

## 1. Why Argus is the perfect complement

| Layer | What Tinkr needs | What Argus provides |
|---|---|---|
| **Build + Deploy** | Source → flashable artifact → push to device | Out of scope (Tinkr's job) |
| **REPL + File ops** | Talk to MicroPython on the device | Out of scope (Tinkr's job, via `minny`) |
| **Diagnostic + Optimization** | Profile the device, recommend configs, generate optimal CycloneDDS/FastDDS/sysctl files | **Argus's job** — already built |
| **Hardware-aware AI agent** | The agent needs to know the device's SoC, cache, ISA features, thermal envelope | **Argus's job** — already exposed via MCP |

Argus handles "what is this hardware and how do I optimize it." Tinkr handles "build my project and put it on the device." Together = complete RPi story. Argus is *already* shipped, MIT-licensed, working. The right move is to integrate, not reimplement.

---

## 2. What this plan delivers

Three v1.5 plugins that wrap Argus:

1. **`tinkr-rpi5`** — Raspberry Pi 4 / 5 support. Primary target.
2. **`tinkr-jetson`** — NVIDIA Jetson Orin Nano Super (and other Orin variants) support.
3. **`tinkr-arm-mac`** — Apple Silicon development hosts (M1–M4). Useful for users developing on a Mac, deploying to a Pi.

All three are deferred to **v1.5** (per the locked decision). v1.0 ships real hardware for microcontrollers only (ESP32, RP2040, nRF52).

---

## 3. The integration model

The plugin doesn't duplicate Argus. It **wraps it as a capability provider** in the HAL.

```
+---------------------------------------------------+
|  tinkr project deploy --target rpi5                |
+---------------------------------------------------+
                       |
                       v
+---------------------------------------------------+
|  tinkr-rpi5 plugin                                  |
|  +---------------------------------------------+   |
|  |  adapters/rpi5_adapter.py (HAL adapter)     |   |
|  |  - profile() -> calls argus via SSH        |   |
|  |  - assess() -> calls argus via SSH        |   |
|  |  - generate_config() -> calls argus       |   |
|  |  - deploy() -> scp + ssh + run             |   |
|  |  - repl() -> ssh + python3 -i              |   |
|  |  - read_file() -> ssh + cat                |   |
|  |  - write_file() -> ssh + tee               |   |
|  +---------------------------------------------+   |
|                       |                             |
|  cli/tinkr_rpi5_*.py (NDJSON-emitting wrappers)     |
|  - tinkr-rpi5-profile                                |
|  - tinkr-rpi5-assess                                |
|  - tinkr-rpi5-generate-config                       |
|  - tinkr-rpi5-deploy                                |
|  - tinkr-rpi5-repl                                  |
+---------------------------------------------------+
                       |
                       v  (over SSH)
+---------------------------------------------------+
|  Argus on the Pi (pip install argus)               |
|  - argus diagnose --json                            |
|  - argus assess --output-dir ./configs              |
|  - argus mcp serve --transport stdio                |
+---------------------------------------------------+
```

**The data flow**:
1. User runs `tinkr project deploy --target rpi5`
2. Tinkr's HAL dispatches to `RPi5Adapter`
3. Adapter calls `tinkr-rpi5-profile` (CLI) which SSHes to the Pi and runs `argus diagnose --json`
4. Adapter calls `tinkr-rpi5-assess` which runs `argus assess --output-dir ./configs`
5. Adapter calls `tinkr-rpi5-generate-config` which returns the generated DDS / sysctl / build-flag files
6. Adapter calls `tinkr-rpi5-deploy` which `scp`s the project + the configs to the Pi and runs it
7. Output streams back via NDJSON, surfaced in the IDE as progress

**The "MCP over SSH" pattern** is the key. Argus already supports `argus mcp serve --transport stdio`. We can chain that with SSH:

```bash
ssh pi@device argus mcp serve --transport stdio
```

This is exactly the same pattern as `argus-pi4` in Argus's own README. Tinkr just consumes it.

---

## 4. The plugin manifest (sketch)

This is what the `tinkr-rpi5` plugin's `tinkr.plugin.toml` will look like:

```toml
[plugin]
name = "tinkr-rpi5"
display_name = "Raspberry Pi 4/5 Support (via Argus)"
version = "0.1.0"
description = "Build, deploy, profile, and optimize projects on Raspberry Pi 4 and 5. Wraps Argus for hardware-aware diagnostics and config generation."
license = "MIT"

[provides]
families = ["rpi4", "rpi5"]  # These are *host* families (the Pi is a target, not an MCU)
boards = ["Raspberry Pi 4 Model B", "Raspberry Pi 5"]
firmware_types = ["raspbian", "ubuntu-server"]  # Pi runs Debian / Ubuntu, not bare-metal RTOS
transports = ["ssh", "serial"]  # SSH for the Pi; serial for the attached MCU

[capabilities]
flash = false         # No firmware flash on a Pi (it boots from SD)
repl = true            # Python3 -i over SSH
filesystem = true      # POSIX filesystem over SSH
package_manager = true # apt + pip
gdb = true             # gdbserver for attached MCU debugging
wifi_sim = false
logic_analyzer = false
ota_update = true      # apt upgrade + reboot
serial_plotter = true  # USB-attached MCU serial
power = true           # PoE HAT voltage monitoring
custom_capabilities = [
    "rpi.hardware-profile",     # Calls argus diagnose
    "rpi.ros2-tier-assessment", # Calls argus assess
    "rpi.dds-config-generate",  # Calls argus optimizer
    "rpi.sysctl-tune",          # Calls argus sysctl generator
]

[dependencies]
tinkr = ">=1.5.0"
python = ">=3.11"
packages = [
    "argus>=0.1.0",        # The key dependency
    "asyncssh>=2.13",      # Async SSH client
    "scp>=0.14",           # SCP for file transfer
    "pydantic>=2.0",
]

[[tools]]
name = "tinkr-rpi5-profile"
entry = "cli/tinkr_rpi5_profile.py"
runtime = "python"
description = "Profile the connected RPi's hardware (CPU, RAM, ISA, thermal)"
tier = 1
requires_device = true
streaming = false

[[tools]]
name = "tinkr-rpi5-assess"
entry = "cli/tinkr_rpi5_assess.py"
runtime = "python"
description = "Run Argus's 5-tier ROS 2 assessment on the connected RPi"
tier = 1
requires_device = true
streaming = false

[[tools]]
name = "tinkr-rpi5-generate-config"
entry = "cli/tinkr_rpi5_generate_config.py"
runtime = "python"
description = "Generate optimized CycloneDDS / FastDDS / sysctl / build-flag files via Argus"
tier = 1
requires_device = true
streaming = false

[[tools]]
name = "tinkr-rpi5-deploy"
entry = "cli/tinkr_rpi5_deploy.py"
runtime = "python"
description = "scp a project to the Pi + ssh to run it"
tier = 1
requires_device = true
requires_port = true
streaming = true

[[tools]]
name = "tinkr-rpi5-repl"
entry = "cli/tinkr_rpi5_repl.py"
runtime = "python"
description = "Open a python3 -i REPL over SSH"
tier = 1
requires_device = true
requires_port = true
streaming = true

[knowledge]
chips = ["knowledge/chips/bcm2711.json", "knowledge/chips/bcm2712.json"]
pinouts = ["knowledge/pinouts/rpi4-pinout.json", "knowledge/pinouts/rpi5-pinout.json"]
references = ["knowledge/references/raspbian-on-rpi.md", "knowledge/references/argus-on-rpi.md"]

[compatibility]
tested_tinkr_versions = ["1.5.0"]
tested_platforms = ["darwin", "linux", "win32"]  # Host platforms
tested_python = ["3.11", "3.12", "3.13"]
maturity = "beta"
```

The plugin depends on **argus** being installed on the Pi (via `pip install argus`), not on the host. The host just needs Python + asyncssh + scp.

---

## 5. The MCP tool surface (auto-derived from manifest)

The HAL auto-generates these MCP tools from the manifest:

- `rpi5.profile`
- `rpi5.assess`
- `rpi5.generate_config`
- `rpi5.deploy`
- `rpi5.repl`
- `rpi5.custom.rpi.hardware-profile`
- `rpi5.custom.rpi.ros2-tier-assessment`
- `rpi5.custom.rpi.dds-config-generate`
- `rpi5.custom.rpi.sysctl-tune`

For the Jetson plugin, similar. For the Mac dev-host plugin, similar but lighter (just for dev tooling, not deployment).

The agent can chain these: "Profile this Pi, then generate the optimal DDS config, then deploy my project." All through one MCP surface.

---

## 6. The user flow (hobbyist with a Pi 5)

```bash
# 1. Install Tinkr
brew install tinkr  # or pip install tinkr

# 2. Set up the project
mkdir my-robot && cd my-robot
tinkr init
tinkr plugin add tinkr-rpi5  # installs the plugin, which depends on argus

# 3. The plugin prompts: "Install argus on the Pi? [Y/n]"
#    If yes: ssh pi@device 'pip install argus'
#    The plugin needs SSH access (key-based, no password prompt)

# 4. Profile the Pi
tinkr device add --nickname my-pi5 --host pi@raspberrypi.local
tinkr device profile my-pi5
# → runs argus diagnose on the Pi
# → output: "BCM2712 (Pi 5), 4× Cortex-A76, 8GB RAM, NEON yes, SVE no, fingerprint a1b2c3..."

# 5. Assess the Pi for ROS 2
tinkr device assess my-pi5
# → runs argus assess
# → output: "Score 60/100, tier=ros-base, recommended RMW=CycloneDDS, profile=balanced"

# 6. Generate the optimal config
tinkr device generate-config my-pi5
# → pulls cyclonedds.xml, fastdds.xml, sysctl.conf, build_flags.json, install_ros2.sh
# → saves to .tinkr/state/rpi5-configs/

# 7. Build your project
vim main.py  # write your ROS 2 node
tinkr project build
# → runs pytest, mpy-cross, etc.

# 8. Deploy
tinkr project deploy --target my-pi5
# → scp . to the Pi
# → ssh to the Pi: cd /home/pi/my-robot && ./run.sh
# → streams output back

# 9. Monitor
tinkr monitor --target my-pi5
# → SSH-tailing the Pi's stdout

# 10. Iterate
# Edit, rebuild, redeploy, repeat.
```

This is the **"hardware plugin module not available so we build connecting the hardware to tinkr/ download plugin for the hardware"** workflow, applied to the RPi. The plugin isn't *building* hardware — it's the *software support* for the hardware, and it integrates with the existing argus (which IS the hardware-aware diagnostic).

---

## 7. The Argus integration risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | Argus goes out of sync with Tinkr (e.g., argus renames a CLI flag) | The plugin pins `argus>=0.1.0,<0.3.0`. The CI for the plugin runs the latest argus and catches breaks. |
| 2 | SSH key management is a UX nightmare for hobbyists | The plugin's first-run flow SSHes with a known key (`~/.ssh/id_ed25519`), or prompts once to set up key auth. Falls back to password (with user consent). |
| 3 | Argus needs Python 3.11+ on the Pi, but older Pi OS has Python 3.9 | The plugin checks Python version on first connect. If too old, recommends `sudo apt install python3.11` or upgrades to Pi OS Bookworm (which has 3.11). |
| 4 | The Pi's hostname is not `raspberrypi.local` (mDNS may not work) | The plugin accepts `--host user@192.168.1.50` as an override. Documented in the README. |
| 5 | SSH over WiFi is unreliable on a maker bench | Recommend ethernet. The plugin's deploy flow is idempotent (rsync-like) so partial transfers recover. |
| 6 | The Pi has a different OS (Ubuntu, DietPi, RetroPie) | Argus supports Linux. The plugin's first-run flow detects the OS and reports. ROS 2 install is OS-aware (per argus's `install_ros2.sh`). |

---

## 8. The roadmap

| When | What ships |
|---|---|
| **v1.0 (8 weeks)** | CLI only. Microcontroller plugins (ESP32, RP2040, nRF52). RPi / Jetson NOT supported. The user runs `ssh pi@device` manually if they need to talk to a Pi. |
| **v1.5 (4-6 months later)** | `tinkr-rpi5` plugin ships. Pi 4 and Pi 5 supported via argus. The plugin wraps argus, exposes the MCP surface, integrates with `tinkr project deploy`. |
| **v1.7 (post-launch)** | `tinkr-jetson` plugin ships. Jetson Orin Nano Super supported. Argus's planned Jetson support is the foundation. |
| **v2.0** | `tinkr-arm-mac` plugin ships. Apple Silicon development hosts. Useful for users who want to test on their Mac before deploying to a Pi. |
| **v2.5** | `tinkr-cluster` plugin. Multi-Pi deployments. Argus profiles each Pi, generates per-node configs, deploys in coordination. |

---

## 9. What changes in Tinkr core

Almost nothing. The plugin spec already supports:
- `firmware_types` other than microcontroller RTOSes (we add "raspbian" / "ubuntu-server")
- `transports` other than serial (we add "ssh")
- `requires_device = false` for tools that operate on a host

The HAL needs one new piece: a **host-target adapter pattern**. Currently the HAL assumes the target is a microcontroller with REPL + filesystem. The RPi plugin introduces the pattern where the target is a full Linux host. This is a small HAL extension (maybe 100 LoC).

The MCP server, the agent, the capture layer, the knowledge base — all unchanged. They consume the plugin's tools uniformly.

---

## 10. Migration plan (argus → tinkr-rpi5)

**Week 1**: scaffolding + profiler
- Create `tinkr.cli/plugins/tinkr-rpi5/`
- Port argus's `core/profiler.py` → `tinkr-rpi5/cli/tinkr_rpi5_profile.py` (CLI emits NDJSON per the Tinkr contract)
- Port argus's `core/models.py` (HardwareProfile) → `tinkr-rpi5/schemas/device_state.py` (Pydantic)
- Port argus's `core/assess.py` → `tinkr-rpi5/cli/tinkr_rpi5_assess.py`
- Tests: pass the argus `tests/test_core.py` against the ported code

**Week 2**: config generation + MCP
- Port argus's `core/optimizer.py` → `tinkr-rpi5/cli/tinkr_rpi5_generate_config.py` (the 7 artifacts)
- Port argus's `mcp/server.py` → `tinkr-rpi5/mcp/server.py` (FastMCP, 14 tools)
- Wire up as a sub-MCP of the Tinkr MCP server (`tool_prefix = "rpi5"`)
- Test the MCP surface end-to-end

**Week 3**: deploy + REPL + filesystem (NEW in Tinkr, not in argus)
- Write `tinkr-rpi5-deploy`: scp + ssh + run, with NDJSON progress
- Write `tinkr-rpi5-repl`: ssh + python3 -i, streaming
- Write `tinkr-rpi5-fs-{read,write,list,delete}`: ssh + standard POSIX ops
- The HAL adapter class
- Tests with `socat` + `pytest-mock` for the SSH layer

**Week 4**: knowledge bundle + ship
- Port the argus knowledge (configs/{soc}/) into the plugin's `knowledge/`
- Write KB entries (the agent's brain for Pi + ROS 2)
- CI: lint + test + manifest validation
- Publish as `tinkr-rpi5@0.1.0` to the registry

**After v1.5 ships**:
- The argus repo is preserved as a reference / proof-of-concept
- Future contributors study argus to understand the diagnostic + optimization architecture
- The tinkr-rpi5 plugin owns the production code path

---

## 11. What this looks like for Ronie

- **The argus repo is now your reference**, not your shipping product. Its README becomes a design doc that the plugin implementation follows.
- **The shipping code** lives in `tinkr.cli/plugins/tinkr-rpi5/`. It has the same architecture, the same Pydantic models, the same FastMCP server, but it's a Tinkr plugin (NDJSON CLI tools, HAL adapter, KB entries, manifest).
- **The migration is straightforward** because argus is well-architected. The Pydantic models transfer 1:1. The FastMCP server transfers 1:1. The CLI framework is the only change (Click → Tinkr's CLI contract).
- **You don't have to maintain two repos**. Argus can be archived or kept as a reference. The shipping product is tinkr-rpi5.

---

## 11. What the user sees

- **No "build the hardware" complexity in the plugin** — the user is using argus, which is already there.
- **One command** for the full profile + assess + generate + deploy flow: `tinkr project deploy --target rpi5`
- **The agent knows about the Pi's capabilities** — when the user asks "what's the best DDS profile for my setup?", the agent calls `kb.search("Pi 5 DDS profile")`, finds the argus recommendation, and surfaces it.
- **The KB accumulates knowledge about Pi + ROS 2 setups** — every project adds to the brain.

This is the **"hardware plugins will be knowledge base"** vision from your message, applied to RPi. The plugin's knowledge bundle + every project that uses it = the Pi brain. Over time, Tinkr gets smarter about Pi + ROS 2 just like it gets smarter about ESP32 + MicroPython.

---

## 12. Summary

- **Argus is the diagnostic half. Tinkr is the build + deploy half. Wrap argus as a Tinkr plugin.**
- **v1.5 ships `tinkr-rpi5`. v1.7 ships `tinkr-jetson`. v2.0 ships `tinkr-arm-mac`.**
- **The plugin is thin: 5-6 CLI tools that wrap `ssh ... argus ...`, plus the HAL adapter.**
- **The integration is clean: argus stays independent, Tinkr depends on it as a Python package.**
- **The user flow is "profile, assess, generate-config, deploy, monitor" — all through one CLI command.**

This is the right architecture. It uses what you've already built. It doesn't duplicate. It extends.
