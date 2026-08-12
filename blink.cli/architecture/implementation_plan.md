# Tinkr — Implementation Plan (Aug 13, 2026)

> **The build plan.** This is the canonical reference for what to ship, in what order, in what week, with what gates. It is a living document — update when decisions change, when weeks complete, when scope shifts.
>
> Source-of-truth precedence: `decisions.md` (A-numbers) > this plan > `blink_synthesis_report.md` > `v1_week1_packaging_refactor.md` (now folded into Week 1 here).

---

## 0. Mission

Build **Tinkr** — a hardware IDE for ESP32 / MicroPython / CircuitPython / RP2040 / nRF52 — that:

- **Open-source from day one.** MIT core, GitHub-hosted, no cloud lock-in.
- **Local-first.** Project = memory. The `.tinkr/` folder IS the state.
- **Community-driven.** KB grows with use, plugins from anyone, capture layer compounds.
- **Single product, three personas.** Hobbyist (Mira), educator (Devansh), embedded engineer (Sara).
- **Honest pushback.** No marketing fluff. Every claim is something a senior designer would ship.

**The locked ship signal (A9):** 100 installs + 5 plugins + 50 KB entries + <5 critical bugs + 2-min Loom demo.

**The locked 4-tier pricing (A10):** Tinkr Pro sub + per-plugin annual updates + creator annual fee + project cloud hosting. Free v1.0, monetization v1.5.

**The locked product timeline:**
- **v1.0** (8 weeks) — open-source CLI, 4 free plugins, GitHub discovery, GitHub+email auth, BYO AI key, capture layer local-only, 50 KB entries
- **v1.5** (4-6 mo) — marketplace, Stripe Connect, vendor first-party plugins, `tinkr-rpi5` (wraps Argus), managed AI tokens
- **v2.0** (12 mo) — creator program, simulator, `tinkr-jetson` + `tinkr-arm-mac`
- **v3.0** (18+ mo) — agentic self-extension, Tindie integration

---

## 1. Current state (snapshot, Aug 13 2026)

**Working artifacts (load-bearing, do not break):**
- 12 Python CLI tools in `tools/blink_*.py` — the foundation, fully functional, emit NDJSON
- 1 NDJSON protocol lib at `lib/ndjson_protocol.py` (65 LoC)
- 1 reference plugin at `plugins/blink-esp32/` — 19 files, ~3,000 LoC, polished
- 6 KB sample entries in `architecture/knowledge-sample/` (1 recipe, 1 pattern, 2 facts, 2 errors)
- 15 brand mockups in `brand/mockups/` (4 with v7 PCB mark, 11 with stale v1 LED)
- 17 architecture docs in `architecture/`
- 17 Tinkr-specific skills in `~/.minimax/skills/tinkr-*/`

**Gaps (the work):**
- No `tinkr/` Python package; no `pyproject.toml`; cannot be `pip install`'d
- Brand rename "Blink → Tinkr" is half-done (folder, plugin folder, tool files, KB tool, mockups 01–11, root README)
- `tools/` and `plugins/blink-esp32/cli/` have duplicated logic
- 4 free plugins for v1.0 not built (only ESP32 exists)
- 44 more KB entries to hit 50
- No working Tauri shell, no Stripe Connect, no MCP server
- Decisions.md has stale path references to `/Users/mindflow/Projects/Tinkr/tinkr.cli/` (real path is `/Users/mindflow/Projects/Blink/blink.cli/`)

---

## 2. The 12-week build plan (v1.0 → v1.5)

### **Week 1 — Pack & rename (Aug 13-19, 2026)**
**Goal:** A runnable `tinkr` Python package on PyPI preview. All "Blink" references gone.

| Day | Task | Skill | Output |
|---|---|---|---|
| 1 | Rename sweep: `blink.cli/` → `tinkr.cli/`, `plugins/blink-esp32/` → `plugins/tinkr-esp32/`, all `blink_*` filenames → `tinkr_*` | `tinkr-rename-sweep` (new) | New directory structure |
| 1-2 | Update mockups 01-11 from v1 LED mark to v7 PCB trace mark | `tinkr-mockup-v7-migrator` (new) | 11 updated mockups |
| 2 | Create `tinkr/` package: `pyproject.toml`, `tinkr/__init__.py`, `tinkr/__main__.py`, `tinkr/cli/root.py` | `tinkr-packaging-refactor` (new) | Installable package |
| 2-3 | Move `lib/ndjson_protocol.py` → `tinkr/lib/`. Add `tinkr/core/{manifest,plugin_loader,device_state,project}.py` | `tinkr-packaging-refactor` | `tinkr.core` module |
| 3-4 | Convert `tools/blink_*.py` → `tinkr/cli/*.py` Click commands. Delete `tools/` and `lib/`. | `tinkr-packaging-refactor` | Single source of truth |
| 4-5 | Reorganize `plugins/tinkr-esp32/cli/`: add `cli/__init__.py` Click group, convert tools to sub-commands. Move `device_state.py` to `tinkr/core/`. | `tinkr-packaging-refactor` | Plugin as proper subcommand |
| 5 | Write `tests/test_{plugin_loader,manifest,plugin_install}.py` | `tinkr-test-author` | Tests pass |
| 5 | Update root `README.md` + `decisions.md` paths + all mockup READMEs | `tinkr-rename-sweep` | Consistent naming |

**Gate (end of Week 1):** `pip install -e .` works, `tinkr --help` runs, `tinkr esp32 port-scan` runs end-to-end, all tests pass, no `blink` references in source.

### **Week 2 — The 4 free plugins (Aug 20-26)**
**Goal:** 4 plugins scaffolded and working, hitting the 5-plugin ship signal.

| Day | Task | Skill | Output |
|---|---|---|---|
| 6 | Scaffold `tinkr-rp2040` (clone ESP32 plugin, swap minny → picotool, add MicroPython + CircuitPython variants) | `tinkr-plugin-author` | Working RP2040 plugin |
| 7 | Scaffold `tinkr-nrf52` (clone, swap → nrfjprog + nrfutil) | `tinkr-plugin-author` | Working nRF52 plugin |
| 8 | Scaffold `tinkr-micropython-runtime` (cross-board firmware installer; wraps `mpypkg`) | `tinkr-plugin-author` | Working MicroPython runtime plugin |
| 8 | Add a "plugin" plugin: `tinkr plugin list/install/update/remove` | `tinkr-plugin-author` | CLI surface for plugin ecosystem |
| 9 | Test all 4 plugins end-to-end on real hardware (or `socat` PTY) | `tinkr-test-author` | 4 plugins ship-signal-ready |

**Gate (end of Week 2):** 5 plugins on disk (esp32, rp2040, nrf52, micropython-runtime, + the base `tinkr` plugin command). 5 = A9 plugin count.

### **Week 3 — The 50 KB entries (Aug 27-Sep 2)**
**Goal:** 44 more KB entries to hit 50, hitting the 50-entry ship signal.

| Day | Task | Skill | Output |
|---|---|---|---|
| 10 | Author 10 facts: `fact/esp32-flash-addresses`, `fact/esp32-s3-i2c-pullups`, + 8 more (chip-specific register maps, electrical limits, etc.) | `tinkr-kb-curator` (new) | 10 facts |
| 10 | Author 2 schemas: `pattern.schema.json`, `story.schema.json` (only fact/recipe/error exist) | `tinkr-kb-curator` | 5 schemas total |
| 11 | Author 5 patterns: `pattern/micropython-{i2c,spi,uart,i2s,async}-driver` | `tinkr-kb-curator` | 5 patterns |
| 11-12 | Author 15 errors: `error/{i2c-timeout,flash-failed-wrong-address,esp32-bootloop,repl-no-response,pyboard-raw-paste,...}` | `tinkr-kb-curator` | 17 errors total |
| 12-13 | Author 10 recipes: `recipe/{esp32-blink-led,esp32-i2c-scan,rp2040-pico-blink,nrf52-blinky,esp32-wifi-connect,esp32-mqtt-publish,...}` | `tinkr-kb-curator` | 11 recipes total |
| 13 | Author 4 stories: real-world Tinkr use cases with provenance | `tinkr-kb-curator` | 4 stories (the "story" type finally has entries) |
| 14 | Update `blink_kb_query.py` → `tinkr_kb_query.py`. Path sweep: `~/.blink/kb/` → `~/.tinkr/kb/`, `BLINK_KB_ROOT` → `TINKR_KB_ROOT`. | `tinkr-kb-curator` + `tinkr-rename-sweep` | Rebrand complete |

**Gate (end of Week 3):** 50 KB entries on disk, schemas cover all 5 types, `tinkr kb search "i2c timeout"` returns the right entry.

### **Week 4 — Project memory + capture layer (Sep 3-9)**
**Goal:** `.tinkr/` folder is a first-class state. Capture layer works.

| Day | Task | Skill | Output |
|---|---|---|---|
| 15 | Implement `tinkr.core.project.Project` — load/save `tinkr.toml`, `lock.toml`, `.tinkr/{plugins,bin,knowledge,state}` | `tinkr-cli-developer` (new) | Project loader |
| 16 | Implement the capture layer (port `architecture/knowledge-sample/capture.py` into `tinkr/core/capture.py`) | `tinkr-cli-developer` | Capture layer |
| 17 | Wire capture into the CLI: when an error occurs, suggest a KB entry; one-click submit to a local `prefill.json` | `tinkr-cli-developer` | User-facing capture |
| 18 | Add the `tinkr capture prefill --last-error` command + `tinkr capture submit --dry-run` for review | `tinkr-cli-developer` | CLI surface |
| 18-19 | Test the full error → capture → KB submission flow with mock errors | `tinkr-test-author` | End-to-end capture |

**Gate (end of Week 4):** Every CLI error event can be captured, pre-filled, and saved locally. No remote upload yet (that's v1.5).

### **Week 5 — MCP server + headless AI (Sep 10-16)**
**Goal:** The agent can drive Tinkr. BYO AI key works.

| Day | Task | Skill | Output |
|---|---|---|---|
| 20 | Implement `tinkr mcp serve` — FastMCP server exposing all plugin tools | `tinkr-cli-developer` | MCP server (200 LoC) |
| 21 | Add `tinkr ai config` — set BYO key (Anthropic, Gemini, OpenAI); store in `.tinkr/ai.toml` | `tinkr-cli-developer` | AI config |
| 22 | Add `tinkr ai ask "<question>"` — drives the agent against the project | `tinkr-cli-developer` | Headless AI |
| 22-23 | Add a `tinkr agent "..."` command — multi-step agent with the 5-step observability (READ/THINK/DECIDE/ACT/REPORT) | `tinkr-cli-developer` | Agent CLI |
| 24 | Add `tinkr thinking` toggle (deep vs fast) + `tinkr commands` toggle (show vs hide) | `tinkr-cli-developer` | UX controls |
| 24-25 | Test against a real Anthropic key + Gemini key + OpenAI key | `tinkr-test-author` | All 3 providers work |

**Gate (end of Week 5):** `tinkr agent "audit my project"` runs, uses tools, returns a report. The agent surface is fully usable headlessly.

### **Week 6 — Tauri shell (Sep 17-23)**
**Goal:** Desktop app exists, even at MVP. Mockup 12 (agentic orchestrator) becomes real.

| Day | Task | Skill | Output |
|---|---|---|---|
| 26 | `tauri init` + `pnpm create tauri-app` (React + TS + Vite) | `tinkr-tauri-builder` (new) | Tauri scaffold |
| 26-27 | Sidebar component (collapsible cards: Project, Progress, Deliverables, Agent team) per mockup 12 | `tinkr-tauri-builder` | Sidebar |
| 27-28 | Chat center column (user/agent turns, Thought expansion, working chip with v7 mark) per mockup 12 | `tinkr-tauri-builder` | Chat |
| 28-29 | Right panel (model selector, reasoning toggles, this-run stats) per mockup 12 | `tinkr-tauri-builder` | Right panel |
| 29-30 | Action Report (5 tabs: Changes / Brand & docs / KB / Decisions / Raw log) per mockup 15 | `tinkr-tauri-builder` | Report |
| 30 | Wire shell to `tinkr mcp serve` via stdio | `tinkr-tauri-builder` | Tauri ↔ MCP |

**Gate (end of Week 6):** `tinkr` opens a Tauri window, sidebar shows project state, chat drives the agent, action report shows changes. Mockup 12 is real.

### **Week 7 — Brand v7 sweep + polish (Sep 24-30)**
**Goal:** All 15 mockups on v7 PCB mark. Brand tokens applied across the shell. Polish.

| Day | Task | Skill | Output |
|---|---|---|---|
| 31-32 | Update mockups 01-11 to v7 mark (carried over from Week 1 if not done; full sweep) | `tinkr-mockup-v7-migrator` | 15 mockups on v7 |
| 32-33 | Wire `tinkr` colors + Inter + JetBrains Mono into the Tauri shell | `tinkr-tauri-builder` | Branded shell |
| 33-34 | Add the 4 plugin marketplace tile to the Tauri shell (even at v1.0, 4 free plugins are listed) | `tinkr-tauri-builder` | Plugin tile |
| 34-35 | Add the settings page (GitHub login, BYO AI key, install path) per mockup 11 | `tinkr-tauri-builder` | Settings |
| 35 | Add `tinkr --version` + `tinkr doctor` (sanity check) | `tinkr-cli-developer` | Diagnostics |

**Gate (end of Week 7):** The Tauri shell uses the v7 mark everywhere, the brand tokens are applied, the surface is "Linear, Notion, Figma, Stripe, Raycast, or Arc" quality per the design DNA.

### **Week 8 — The 2-min Loom + ship (Oct 1-7)**
**Goal:** A9 ship signal achieved. Loom recorded. Public release.

| Day | Task | Skill | Output |
|---|---|---|---|
| 36 | Write the `tinkr-esp32` first-touch walkthrough: install → login → first project → first flash | `tinkr-spec-writer` | Walkthrough doc |
| 36-37 | Record the 2-min Loom: "Tinkr in 2 minutes" — install, port scan, identify, flash, run, error → KB | `tinkr-launch-checklist` | Loom video |
| 37-38 | Cut the v1.0 release: tag `v1.0.0`, write CHANGELOG, update README with the Loom embed | `tinkr-changelog-writer` | v1.0.0 release |
| 38-39 | Run the launch checklist: A9 gates all green, no critical bugs, plugin manifest schema lint clean, KB queries return the right entries | `tinkr-launch-checklist` | Launch verdict |
| 39-40 | Announce: GitHub release, Hacker News, Reddit r/esp32, r/MicroPython, r/embedded, Maker news, Hackaday | `tinkr-launch-checklist` | Public launch |

**Gate (end of Week 8):** A9 ship signal achieved: 100 installs, 5 plugins, 50 KB entries, <5 critical bugs, 2-min Loom. v1.0.0 tagged. v1.5 begins the next day.

---

## 3. The v1.5 backlog (post-ship, 4-6 months)

> Do NOT start until Week 8 ships. Each item is sized for ~1 week of work.

1. **Stripe Connect integration.** Per the `tinkr-stripe-integration` skill. 70/30 default split. Webhook → plugin update license.
2. **Vendor first-party plugins.** Per A2 / A8. Approach Espressif + Wemos in parallel using `tinkr-partner-pitch`. M5Stack via Espressif channel.
3. **Managed AI tokens.** Per A13. Partnership with MiniMax for managed Anthropic tokens. `tinkr ai config --managed` enables.
4. **`tinkr-rpi5` plugin.** Per A11 + `architecture/argus_integration.md`. 4-week absorption plan from Argus. 14 MCP tools + 10 resources + 4 prompts.
5. **Hardware deploy as paid.** Per A14. `tinkr flash` is free in v1.0; v1.5 adds "flash with Tinkr cloud" (pay-per-flash or bundled in Pro).
6. **Per-plugin annual updates.** Per A10. Plugin author can charge annual fee for continued updates; plugin still works without paying; 1-year window, no penalty.
7. **Project cloud hosting.** Per A10. 4th tier. Optional sync of `.tinkr/` to Tinkr cloud; shareable project URLs.
8. **Plugin marketplace UI.** Tauri shell tab; vendors + creators + free 4 plugins; "verified" badge for community-vetted plugins.

---

## 4. The v2.0+ backlog (12-18 months out)

- **Creator program open launch.** Per A10 / A15. Anyone publishes. 70% creator / 30% Tinkr. `tinkr creator` CLI surface.
- **Simulator.** Per A3. v2.0+. `tinkr sim` runs MicroPython on the host for testing. Wokwi competitor on the open-source side.
- **`tinkr-jetson` + `tinkr-arm-mac`.** Extend the platform to NVIDIA Jetson (Orin, Nano) and Apple Silicon native. The "edge devices" axis.
- **Tindie integration.** Per v3.0. Optional Tindie store for physical hardware projects. "Stays true to contributions" 3-clause contract (A6).
- **Agentic self-extension.** Per v3.0. The AI agent writes plugin tools with human review. The "agentic IDE" axis.

---

## 5. The directory structure (post-Week-1)

```
tinkr.cli/                                          # was: blink.cli/
├── README.md                                       # Tinkr CLI (was: Blink CLI)
├── pyproject.toml                                  # NEW: installable
├── tinkr/                                          # NEW: the package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── root.py                                 # Click group, "tinkr"
│   │   ├── plugin_list.py
│   │   ├── plugin_install.py
│   │   ├── plugin_update.py
│   │   ├── plugin_remove.py
│   │   ├── ai_config.py
│   │   ├── ai_ask.py
│   │   ├── agent.py
│   │   ├── capture.py
│   │   ├── kb_query.py                             # was: blink_kb_query.py
│   │   └── ...
│   ├── core/
│   │   ├── __init__.py
│   │   ├── manifest.py
│   │   ├── plugin_loader.py
│   │   ├── device_state.py                         # was: plugins/blink-esp32/schemas/
│   │   ├── project.py
│   │   ├── capture.py
│   │   └── hal.py
│   ├── lib/
│   │   ├── __init__.py
│   │   └── ndjson_protocol.py                      # was: lib/ndjson_protocol.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── anthropic.py
│   │   ├── gemini.py
│   │   └── openai.py
│   └── mcp/
│       ├── __init__.py
│       └── server.py                               # FastMCP
├── plugins/                                        # was: blink-*
│   ├── tinkr-esp32/                                # was: blink-esp32/
│   ├── tinkr-rp2040/                               # NEW
│   ├── tinkr-nrf52/                                # NEW
│   └── tinkr-micropython-runtime/                  # NEW (cross-board firmware)
├── architecture/                                   # unchanged
│   ├── decisions.md                                # updated paths
│   ├── implementation_plan.md                      # NEW: this file
│   ├── ... (16 other docs)
│   └── knowledge/
│       ├── facts/                                  # 12 entries
│       ├── recipes/                                # 11 entries
│       ├── errors/                                 # 17 entries
│       ├── patterns/                               # 5 entries
│       ├── stories/                                # 4 entries
│       └── schema/                                 # 5 schemas
├── brand/                                          # unchanged
│   ├── 01-positioning.md                           # updated
│   ├── 02-visual-identity.md                       # updated to v7
│   ├── 03-design-tokens.json
│   ├── 04-component-library.md
│   ├── 05-applications.md
│   ├── README.md
│   ├── SUMMARY.md
│   └── mockups/                                    # 15 mockups, all on v7
└── tests/
    ├── test_plugin_loader.py                       # NEW
    ├── test_manifest.py                            # NEW
    ├── test_plugin_install.py                      # NEW
    ├── test_capture.py                             # NEW
    ├── test_ai_*.py                                # NEW
    └── test_*.py                                   # per-plugin
```

---

## 6. The skill ecosystem (post-Week-1)

**22 existing Tinkr skills** (in `~/.minimax/skills/tinkr-*/`) cover:
- KB authoring, plugin scaffolding, spec writing, test writing, decision recording, week planning, changelog, pricing, Stripe, launch, funnel, roadmap, mockup authoring, trademark, partner pitch, workflow router, spec check.

**7 NEW Tinkr skills** to add (this week):

1. **`tinkr-rename-sweep`** — One-shot script + checklist for "Blink → Tinkr" rename across the repo. Handles directory names, file names, package names, env vars, README references, decision paths.
2. **`tinkr-packaging-refactor`** — Step-by-step guide for the Week 1 packaging refactor (5 sub-tasks, 11 hours). Validates `pyproject.toml`, `tinkr/` layout, Click command structure, plugin import.
3. **`tinkr-cli-developer`** — Patterns for developing within the `tinkr/` core package: Click commands, NDJSON output, exit codes, error envelopes, the `tinkr.core.hal` adapter contract.
4. **`tinkr-kb-curator`** — Bulk-authoring 50 KB entries. Patterns for facts, recipes, errors, patterns, stories. Quality bar (must have fix_steps + verify_steps for errors, must have runnable code for recipes).
5. **`tinkr-tauri-builder`** — Building the Tauri shell. React + TS + Vite, the 3-column layout, v7 PCB mark SVG components, MCP stdio bridge, brand token application.
6. **`tinkr-mockup-v7-migrator`** — One-click update of mockups 01-11 from v1 LED to v7 PCB mark. Generates the inline SVG and the CSS state classes. Used in Week 1 (mockup sweep) and Week 7 (full sweep).
7. **`tinkr-v1-ship-runbook`** — The Week 8 checklist. The A9 ship signal, the Loom recording, the launch announcement templates. Verdict = go / no-go / fix-this-first.

**General skills** (3, all relevant):
- `ui-ux-pro-max` — for color palette + design system decisions
- `ui-ux-designer` — for the Tauri shell component library
- `code-review` — for PR review

---

## 7. The execution pattern

Every week follows the same 5-step loop:

1. **Plan** (Monday morning, 15 min) — `tinkr-week-planner` skill surfaces 3-5 things
2. **Build** (Tue-Thu) — `tinkr-workflow` routes each task to the right skill
3. **Test** (Thu afternoon) — `tinkr-test-author` + `tinkr-spec-check` validate
4. **Record** (Fri morning) — `tinkr-decision-recorder` captures any A-number changes
5. **Ship** (Friday afternoon) — `tinkr-launch-checklist` validates the gate

The `tinkr-workflow` skill is the conductor. Every other skill is an instrument. When in doubt, ask `tinkr-workflow` "what's the right skill for X?"

---

## 8. The risk register

| Risk | Severity | Mitigation |
|---|---|---|
| Week 1 refactor breaks the working tools | High | Run `tools/blink_*.py` against the same hardware AFTER `tinkr esp32 port-scan` works. Drop `tools/` only after green. |
| MCP server doesn't match FastMCP API | Medium | `tinkr-cli-developer` skill will pin the FastMCP version. Tests against Anthropic SDK + real agent. |
| v7 mark doesn't render in 11 mockups | Medium | `tinkr-mockup-v7-migrator` skill generates the SVG + CSS. Manual verify in browser. |
| KB schema drift between types | Low | All schemas in `architecture/knowledge/schema/*.schema.json` with `additionalProperties: false`. JSON Schema 2020-12. |
| Argus → tinkr-rpi5 absorption takes longer than 4 weeks | High (v1.5) | Argus is a prototype, not a shipped product (A11). v1.5 absorbs in 4-6 weeks. If longer, defer. |
| Stripe Connect for India-based founder | Medium | `incorporation_research.md` recommends Singapore Pte Ltd for Stripe access. Mercury rejects Indian passports. Use Airwallex. |
| Trademark conflict for "Tinkr" | Low (resolved) | Tinkercad (Autodesk) is class 9 but a kids' simulator. No collision in the IDE space. A18 brand mark v7 is independent of name. |

---

## 9. The success criteria

**v1.0 ships when ALL of the following are true:**

- [ ] `pip install tinkr-cli` works on macOS / Linux / Windows
- [ ] `tinkr --help` shows 20+ commands across 5 plugins
- [ ] `tinkr esp32 port-scan` returns results on real hardware
- [ ] `tinkr agent "audit my project"` returns a 5-step report
- [ ] 5 plugins on disk (esp32, rp2040, nrf52, micropython-runtime, base)
- [ ] 50 KB entries (12 facts + 11 recipes + 17 errors + 5 patterns + 4 stories)
- [ ] 5 schemas (fact, recipe, error, pattern, story)
- [ ] Tauri shell opens, chat drives the agent, sidebar shows project state
- [ ] All 15 mockups use v7 PCB mark
- [ ] 0 `blink` references in source
- [ ] 0 critical bugs in the 2 weeks before launch
- [ ] 2-min Loom recorded
- [ ] 100 installs in the first 30 days
- [ ] All A9 ship-signal gates green

**v1.0 ships NO EARLIER than the gate above. No v1.5 work begins until then.**

---

## 10. The next move

Right now (Aug 13, 2026, 02:00 IST), the highest-leverage action is:

> **Spawn a worker to do the Week 1 packaging refactor + rename sweep.**

That single week unblocks everything else in the 8-week plan. Without it, no `tinkr` package, no v1.0 install, no A9 ship signal.

The `tinkr-rename-sweep` and `tinkr-packaging-refactor` skills are the next two skills to add. The worker session will use them.

---

*Last updated: 2026-08-13 02:00 IST by Mavis. Plan is the canonical reference. Update this when decisions change.*
