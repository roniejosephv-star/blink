# Tinkr Smart Agentic Platform — The Learning Loop Design v0.1

> How Tinkr gets smarter as users build in it. The production-grade knowledge-accumulation loop that makes the platform compounding instead of static. Every new version of Tinkr ships new knowledge. Every user that builds in Tinkr contributes to that knowledge — by using the platform, by writing plugins, by saving recipes, by contributing reference data. The result: a hardware IDE that gets visibly better every release, and where new users get the benefit of every prior user's work for free.

---

## 1. The Vision in One Picture

```
                          ┌────────────────────────────────────────┐
                          │   New Tinkr release ships knowledge    │
                          │   - new curated facts                  │
                          │   - new error→fix mappings             │
                          │   - new patterns & recipes             │
                          │   - new default configs                │
                          │   - new agent prompts                  │
                          └────────────────┬───────────────────────┘
                                           │ users upgrade
                                           ▼
                          ┌────────────────────────────────────────┐
                          │   Users build with smarter Tinkr       │
                          │   - better suggestions                 │
                          │   - better error messages              │
                          │   - better defaults                    │
                          │   - more plugins to choose from        │
                          └────┬───────────────────┬───────────────┘
                               │                   │
              ┌────────────────▼──┐      ┌─────────▼──────────────┐
              │ opt-in telemetry  │      │  contributions         │
              │ - what plugins    │      │  - plugins             │
              │ - what patterns   │      │  - recipes             │
              │ - what errors     │      │  - chip DBs / datasheets│
              │   (anonymized)    │      │  - error→fix mappings  │
              └─────────┬─────────┘      └────────────┬──────────┘
                        │                            │
                        └─────────────┬──────────────┘
                                      ▼
                          ┌────────────────────────────────────────┐
                          │   Curated knowledge base               │
                          │   (the "brain" of Tinkr)               │
                          │   - automated curation pipeline        │
                          │   - human review for quality           │
                          │   - versioned + signed                 │
                          │   - ships with Tinkr                   │
                          └────────────────────────────────────────┘
                                      │
                                      │ queries via MCP
                                      ▼
                          ┌────────────────────────────────────────┐
                          │   The agent in Tinkr                   │
                          │   - reads project memory               │
                          │   - reads device state                 │
                          │   - queries the knowledge base         │
                          │   - suggests better than before        │
                          └────────────────────────────────────────┘
```

The **brain** is the curated knowledge base. The **loop** is: users build → contributions flow in → brain gets richer → new release ships brain → users build smarter. The **agent** is the surface that turns the brain into action.

This is not retraining a model. This is **knowledge accumulation** — the same compounding effect that makes Stack Overflow, npm, Homebrew, Wikipedia, and Linux powerful. The compounding comes from the structure, not from the size.

---

## 2. The Four Feedback Channels

Four distinct channels through which Tinkr gets smarter. Each has its own format, its own opt-in model, its own curation flow, and its own productization.

### 2.1 Channel 1: Opt-in Telemetry

**What it is**: Anonymous, aggregated usage data. Which plugins are installed, which operations are run, which errors are hit, which features are used.

**Format**: NDJSON event stream, one event per operation. Examples:

```json
{"type":"event","name":"plugin.install","plugin":"tinkr-esp32","version":"1.2.3","ts":"2026-08-12T14:32:00Z","session":"abc","device_family":"esp32s3","platform":"darwin","tinkr_version":"0.3.0"}
{"type":"event","name":"project.deploy","plugin":"tinkr-esp32","success":true,"duration_ms":12450,"ts":"...","session":"abc"}
{"type":"event","name":"error.encountered","plugin":"tinkr-esp32","error_code":"OSError_ETIMEDOUT","context":"i2c.scan","ts":"..."}
{"type":"event","name":"repl.execute","plugin":"tinkr-esp32","snippet_size":150,"success":true,"duration_ms":45,"ts":"..."}
```

**Opt-in model**: Default OFF. The user explicitly opts in. Once opted in, the user can see exactly what's being sent (a transparent local log at `~/.tinkr/telemetry.log` before it's sent).

**What is NOT collected**:
- Project source code
- File names in the project
- Datasheet content
- Any personally identifiable information
- Any user-typed text in the REPL
- Any device serial numbers or MACs

**Curation**: An ETL pipeline aggregates events. The Tinkr team looks at:
- Which plugins are most used → "ship them by default"
- Which plugins are installed but unused → "improve onboarding"
- Which errors are most common → "ship better error messages"
- Which operations are slowest → "optimize the slow path"
- Which features are never used → "consider removing"

**Productization**: Aggregated stats feed the new Tinkr release. The user sees a "What's new in this version" list that includes "we shipped 47 new error messages based on what users actually hit this quarter."

**Privacy infrastructure**: A dedicated telemetry endpoint (could be `telemetry.tinkr.build` or a self-hosted equivalent). The user can:
- Inspect every event before it's sent (`tinkr telemetry show`)
- Pause sending (`tinkr telemetry pause`)
- Delete their data (`tinkr telemetry delete`)
- Self-host the endpoint (`tinkr telemetry endpoint https://my-server.example`)

### 2.2 Channel 2: Plugin Publications

**What it is**: When a user writes a plugin and `tinkr plugin publish`s it, the plugin enters the registry and becomes available to other users.

**Format**: A complete plugin package (per `plugin_spec.md`) — manifest, CLI tools, knowledge bundle, tests, examples. Git-hosted in the registry.

**Opt-in model**: Implicit (you published, you want to share). The user controls the plugin's visibility (`public`, `unlisted`, `private`).

**Curation**: The registry is PR-based. A maintainer reviews each submission against quality criteria:
- Manifest is valid
- All tests pass
- Knowledge bundle is non-empty
- README + LICENSE + CHANGELOG present
- No security flags (the manifest is scanned for hard-deny patterns per `plugin_spec.md`)
- A working example exists

**Productization**: Approved plugins become discoverable via `tinkr plugin search`. Featured plugins (curated by the Tinkr team) are highlighted. Plugins with high usage / ratings are auto-featured after a threshold.

**Knowledge extracted from plugins**:
- The plugin's chip DB → added to the global chip DB
- The plugin's datasheet → added to the global datasheet index
- The plugin's pattern (e.g., "ESP32-C3 + WiFi + MQTT") → added to the recipe library
- The plugin's error mappings → added to the global error→fix database

This means **every published plugin contributes to the global knowledge base**, not just to the plugin itself. The user's work has multiplicative value.

### 2.3 Channel 3: Recipe Sharing

**What it is**: A **recipe** is a multi-step workflow that worked. "Connect to ESP32, identify, flash MicroPython, deploy tinkr-led, monitor serial output" is a recipe.

**Format**: A YAML or TOML file. Each step is a CLI command or an MCP tool call. Optionally a natural-language description and pre/post-conditions.

```yaml
# recipes/esp32-tinkr-led-deploy.yaml
name: esp32-tinkr-led-deploy
description: Flash MicroPython to a fresh ESP32 and deploy the tinkr-led example.
tags: [esp32, micropython, beginner, getting-started]

setup:
  requires_plugin: tinkr-esp32@^1.2
  requires_device_family: esp32

steps:
  - name: scan-ports
    run: tinkr-esp32-port-scan
    capture: ports

  - name: identify-device
    run: tinkr-esp32-identify
    args: { port: "$ports.0.port" }
    capture: device

  - name: download-firmware
    run: tinkr-firmware-fetch
    args:
      board: "$device.board"
      firmware_type: micropython
      output: /tmp/firmware.bin
    capture: firmware

  - name: flash-firmware
    run: tinkr-esp32-flash-firmware
    args:
      port: "$device.port"
      firmware: "$firmware.path"
      erase: true

  - name: deploy-tinkr-led
    run: tinkr project deploy
    args: { project: "./tinkr-led" }

  - name: monitor-serial
    run: tinkr monitor
    args: { port: "$device.port", duration: "10s" }
```

**Opt-in model**: Recipes are project-level by default. The user explicitly chooses to share: `tinkr recipe share ./recipes/esp32-tinkr-led-deploy.yaml`. The recipe becomes a PR to a community recipes repo (`github.com/tinkr-recipes/index`).

**Curation**: PR-based review. Recipes are checked for:
- They actually work (CI runs them against a virtual serial port)
- They have a clear description
- They have a reasonable setup (plugin versions, device families)
- They follow the schema

**Productization**: Approved recipes become discoverable via `tinkr recipe search "esp32"`. The agent can invoke a recipe: "I see you're trying to flash an ESP32. Want me to run the [esp32-tinkr-led-deploy] recipe?"

**Knowledge extracted from recipes**:
- The step sequence → added to the agent's "common workflow" library
- The preconditions (plugin version, device family) → added to the agent's setup detection
- The success rate (telemetry) → used to rank recipes

### 2.4 Channel 4: Knowledge Contributions

**What it is**: Direct contributions to the global knowledge base. Chip DBs, datasheets, error→fix mappings, reference docs.

**Format**: Structured YAML/TOML files. Examples:

```yaml
# knowledge/facts/esp32-s3-i2c-pullups.yaml
type: fact
category: hardware-quirk
chips: [esp32, esp32s2, esp32s3, esp32c3, esp32c6]
summary: "ESP32 I2C pins have no internal pull-up resistors"
detail: |
  Unlike some MCUs, the ESP32's I2C pins have NO internal pull-ups. You must
  add external 4.7kΩ pull-up resistors on both SDA and SCL for reliable
  communication. The internal pull-ups (when enabled via machine.Pin.PULL_UP)
  are ~45kΩ, which is too weak for most I2C devices at standard speeds.
  ...
sources:
  - "https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet.pdf#page=42"
related_errors:
  - OSError_ETIMEDOUT  # Symptom on I2C.scan()
contributed_by: "@ronie"
contributed_at: "2026-08-12T14:32:00Z"
```

```yaml
# knowledge/errors/i2c-timeout.yaml
type: error
category: i2c
error_code: OSError_ETIMEDOUT
summary: "I2C scan or read times out"
likely_causes:
  - fact: knowledge/facts/esp32-s3-i2c-pullups.yaml
  - fact: knowledge/facts/wrong-i2c-address.yaml
  - fact: knowledge/facts/wrong-i2c-pins.yaml
fix_steps:
  - "Check that SDA and SCL have external 4.7kΩ pull-up resistors to 3.3V."
  - "Verify the I2C address with `i2c.scan()`. Common addresses: 0x76, 0x77 (BME280), 0x44, 0x45 (SHT31), 0x68 (MPU6050)."
  - "Verify you're using the correct pins. ESP32-S3-DevKitC-1 defaults: SDA=GPIO8, SCL=GPIO9. But MicroPython's I2C defaults differ — set explicitly in code."
contributed_by: "@community"
contributed_at: "..."
```

**Opt-in model**: Contributions are explicit. The user runs `tinkr knowledge contribute` after writing the entry. The entry becomes a PR to a community knowledge repo (`github.com/tinkr-knowledge/index`).

**Curation**: PR-based review. Knowledge entries are checked for:
- They are factually correct (verified by a domain expert or referenced)
- They are clearly written
- They cite sources
- They don't include proprietary / licensed material without permission
- They follow the schema

**Productization**: Approved knowledge entries are merged into the global knowledge base. New Tinkr releases ship the new knowledge. The agent queries this knowledge base when the user asks a question.

---

## 3. The Curated Knowledge Base (the "Brain")

The brain is what makes Tinkr "smart." It is a structured, versioned, signed collection of knowledge that ships with Tinkr and grows with every release.

### 3.1 Structure

```
tinkr-kb/                              # Git repo, the canonical source
├── index.yaml                         # Top-level index, versioned
├── facts/                             # Atomic facts (chip quirks, electrical specs, etc.)
│   ├── esp32-s3-i2c-pullups.yaml
│   ├── esp32-flash-addresses.yaml
│   └── ...
├── errors/                            # Error → fix mappings
│   ├── i2c-timeout.yaml
│   ├── flash-failed-stub-loader.yaml
│   └── ...
├── patterns/                          # Code patterns, wiring patterns
│   ├── micropython-i2c-driver.yaml
│   ├── esp32-deep-sleep-wakeup.yaml
│   └── ...
├── recipes/                           # Multi-step workflows
│   ├── esp32-tinkr-led-deploy.yaml
│   ├── rp2040-circuitpython-install.yaml
│   └── ...
├── stories/                           # Anonymized case studies
│   ├── "esp32s3-bme280-mqtt-publish.yaml"
│   ├── "rp2040-pio-neopixel.yaml"
│   └── ...
├── CHANGELOG.md
└── schema/
    ├── fact.schema.json
    ├── error.schema.json
    ├── pattern.schema.json
    ├── recipe.schema.json
    └── story.schema.json
```

### 3.2 Schemas (high level)

#### `fact.schema.json`

```json
{
  "type": "object",
  "required": ["type", "category", "summary", "detail", "sources"],
  "properties": {
    "type": { "const": "fact" },
    "id": { "type": "string", "description": "Globally unique ID, e.g., 'fact/esp32-s3-i2c-pullups'" },
    "category": { "enum": ["hardware-quirk", "electrical-spec", "register-map", "voltage-level", "current-limit", "timing", "protocol-detail"] },
    "summary": { "type": "string", "maxLength": 200 },
    "detail": { "type": "string" },
    "chips": { "type": "array", "items": { "type": "string" }, "description": "Chip families this fact applies to" },
    "related_errors": { "type": "array", "items": { "type": "string" } },
    "related_patterns": { "type": "array", "items": { "type": "string" } },
    "sources": { "type": "array", "items": { "type": "string", "format": "uri" } },
    "contributed_by": { "type": "string" },
    "contributed_at": { "type": "string", "format": "date-time" }
  }
}
```

#### `error.schema.json`

```json
{
  "type": "object",
  "required": ["type", "error_code", "summary", "likely_causes", "fix_steps"],
  "properties": {
    "type": { "const": "error" },
    "id": { "type": "string" },
    "category": { "enum": ["i2c", "spi", "uart", "wifi", "ble", "flash", "repl", "filesystem", "import", "memory", "general"] },
    "error_code": { "type": "string", "description": "The actual error code or pattern (e.g., 'OSError_ETIMEDOUT' or 'ImportError_no_module_named_machine')" },
    "summary": { "type": "string", "maxLength": 200 },
    "likely_causes": { "type": "array", "items": { "type": "string", "description": "References to fact IDs" } },
    "fix_steps": { "type": "array", "items": { "type": "string" } },
    "verify_steps": { "type": "array", "items": { "type": "string" }, "description": "How to confirm the fix worked" },
    "contributed_by": { "type": "string" },
    "contributed_at": { "type": "string", "format": "date-time" }
  }
}
```

#### `recipe.schema.json`

```json
{
  "type": "object",
  "required": ["name", "description", "steps"],
  "properties": {
    "name": { "type": "string" },
    "description": { "type": "string" },
    "tags": { "type": "array", "items": { "type": "string" } },
    "setup": {
      "type": "object",
      "properties": {
        "requires_plugin": { "type": "string" },
        "requires_device_family": { "type": "string" },
        "requires_firmware": { "type": "string" }
      }
    },
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "run"],
        "properties": {
          "name": { "type": "string" },
          "run": { "type": "string", "description": "CLI command or MCP tool name" },
          "args": { "type": "object" },
          "capture": { "type": "string", "description": "Variable name to store the result" },
          "if": { "type": "string", "description": "Conditional expression" }
        }
      }
    },
    "contributed_by": { "type": "string" },
    "contributed_at": { "type": "string", "format": "date-time" }
  }
}
```

### 3.3 Versioning and signing

The knowledge base is versioned. Every release of Tinkr ships a specific version of the knowledge base, and the version is part of the release notes. The knowledge base is signed (the Tinkr team's GPG key) so users can verify integrity.

```yaml
# In a Tinkr release:
tinkr_version: 0.4.0
kb_version: 2026.08.12
kb_signed_by: "ronie@tinkr.build"
kb_signature: "..."
```

Old versions of the knowledge base are kept (git history). A user can pin their Tinkr to an older KB if needed for reproducibility.

### 3.4 Distribution

The knowledge base ships in two ways:

1. **Bundled with Tinkr**: A snapshot of the KB at the time of the Tinkr release is included in the binary. This is the default — works offline, no extra download.
2. **Pulled live** (optional): The user can configure Tinkr to pull the latest KB on startup. Useful for users who want the freshest knowledge, at the cost of a network call.

The bundled snapshot is the source of truth. The live pull is a delta.

### 3.5 Curation pipeline

The KB is curated through a CI/CD pipeline:

```
contribution (PR) → automated checks → human review → merge → automated build → bundled into next release
       │                  │                  │              │                │
       │                  │                  │              │                └── ships to users
       │                  │                  │              └── signs + versions + builds delta
       │                  │                  └── subject-matter expert approves
       │                  └── schema validation, fact consistency, source verification
       └── user submits via `tinkr knowledge contribute`
```

A "subject-matter expert" can be anyone with verified domain knowledge. The Tinkr team curates the list. Contributors earn reviewer status after N accepted contributions.

---

## 4. The Agent's MCP Tool Surface (How the Agent Queries the Brain)

The agent queries the knowledge base through MCP tools. These tools are always available, regardless of which plugins are installed.

### 4.1 `kb.search(query, category?, limit?)`

Semantic + keyword search across the knowledge base. Returns ranked results.

```python
# Agent calls:
mcp.call("kb.search", {
    "query": "ESP32 I2C timeout",
    "category": "error",
    "limit": 3,
})
# Returns:
# [
#   {"id": "error/i2c-timeout", "score": 0.92, "summary": "I2C scan or read times out", ...},
#   {"id": "fact/esp32-s3-i2c-pullups", "score": 0.87, "summary": "ESP32 I2C pins have no internal pull-up resistors", ...},
#   ...
# ]
```

### 4.2 `kb.get(id)`

Fetch a single knowledge entry by ID.

```python
mcp.call("kb.get", {"id": "error/i2c-timeout"})
# Returns the full YAML/JSON for that error entry.
```

### 4.3 `kb.fix_for(error_signature)`

The agent's primary tool. Given an error signature, return the most likely fix.

```python
mcp.call("kb.fix_for", {"error_signature": "OSError: [Errno 110] ETIMEDOUT"})
# Returns:
# {
#   "error_id": "error/i2c-timeout",
#   "summary": "I2C scan or read times out",
#   "fix_steps": [
#     "Check that SDA and SCL have external 4.7kΩ pull-up resistors to 3.3V.",
#     "Verify the I2C address with i2c.scan()...",
#     "Verify you're using the correct pins..."
#   ],
#   "verify_steps": ["Run i2c.scan() and confirm the expected address appears."],
#   "related_facts": ["fact/esp32-s3-i2c-pullups", "fact/wrong-i2c-address"]
# }
```

### 4.4 `kb.recipe_for(setup)`

Given a setup (chip family, firmware type, goal), return the best recipe.

```python
mcp.call("kb.recipe_for", {
    "chip_family": "esp32s3",
    "firmware": "micropython",
    "goal": "deploy tinkr-led example",
})
# Returns the recipe spec.
```

### 4.5 `kb.facts_for(chip_family, category?)`

Get all known facts for a given chip family, optionally filtered by category.

```python
mcp.call("kb.facts_for", {
    "chip_family": "esp32s3",
    "category": "hardware-quirk",
})
# Returns a list of fact IDs + summaries.
```

### 4.6 `kb.contribute(entry)` (opt-in)

Submit a new knowledge entry. Returns a PR URL.

```python
mcp.call("kb.contribute", {
    "type": "fact",
    "category": "hardware-quirk",
    "summary": "ESP32-C6 USB-CDC requires explicit driver load on Windows",
    "detail": "...",
    "chips": ["esp32c6"],
    "sources": ["https://..."],
})
# Returns:
# {"pr_url": "https://github.com/tinkr-knowledge/index/pull/42", "status": "pending"}
```

### 4.7 What the agent does with the KB

The agent's reasoning pattern with the KB:

```
1. User says: "I2C scan returns []"
2. Agent reads project memory → sees ESP32-S3, BME280 sensor, code that uses I2C(0, scl=Pin(9), sda=Pin(8))
3. Agent reads device state → sees the I2C.scan() returned []
4. Agent calls kb.fix_for("I2C scan returns empty")
5. KB returns: "Check pull-ups, check address, check pins"
6. Agent asks user: "Are you using external pull-up resistors on SDA (GPIO8) and SCL (GPIO9)?"
7. User: "No"
8. Agent: "ESP32 I2C pins have no internal pull-ups. Add 4.7kΩ resistors from SDA→3.3V and SCL→3.3V. Here's the wiring and a code snippet to verify: [details]"
9. User adds pull-ups, restarts, I2C.scan() now returns [0x76]
10. Agent: "BME280 detected at 0x76. Here's how to read it: [code]"
```

Without the KB, the agent would have to reason from first principles. With the KB, it has the same knowledge a senior embedded engineer has — the same 5 common causes, ranked.

---

## 5. The Versioned Release Process

The release cadence is the heartbeat of the platform. Three cadences, three types of releases.

### 5.1 Knowledge Drops (weekly)

A **knowledge drop** is a small, curated addition to the KB. It can include:
- New facts (chip quirks, datasheet references)
- New error→fix mappings
- New patterns
- New recipes
- Edits to existing entries (corrections, additions)

Knowledge drops ship as a delta. Users who opted into the live KB pull get the new knowledge within a week of curation. Users on the bundled KB get it on the next Tinkr release.

A knowledge drop is small (5–20 entries), curated by 1–3 reviewers, and ships in 2–3 days from PR to merge.

### 5.2 Tinkr Minor Releases (monthly)

A **Tinkr minor release** (e.g., 0.4.0 → 0.5.0) includes:
- All knowledge drops since the last release
- New features (typically user-requested, based on telemetry)
- Bug fixes
- Plugin ecosystem updates (new featured plugins, deprecations)
- The bundled KB at the latest version

A Tinkr minor release is medium-sized, takes 2–3 weeks from planning to release, and ships on a fixed schedule (e.g., first Tuesday of the month).

### 5.3 Tinkr Major Releases (quarterly)

A **Tinkr major release** (e.g., 0.x → 1.0, or 0.4 → 0.5) includes:
- All minor release content
- Breaking changes (rare, with migration guides)
- New core features
- Architectural shifts (e.g., the v1.0 release is the first stable)
- The bundled KB at the latest version

A Tinkr major release is large, takes 4–6 weeks, and ships on a fixed schedule (every 3 months).

### 5.4 The release pipeline

```
PR merged into tinkr-kb → CI runs validation
                           ↓
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
   live KB delta published       weekly summary report
   (for live-pull users)         (curators + community)
                                       │
                                       ▼
                          monthly Tinkr release bundles
                          the latest KB + new features
                                       │
                                       ▼
                          users get `tinkr update`
                          (or auto-update)
```

The release process is:
- **Transparent**: every change is in a git repo, signed, auditable.
- **Reproducible**: every release is built from a specific git commit.
- **Reversible**: if a release breaks, a patch release ships within 24 hours.
- **Scheduled**: weekly, monthly, quarterly — predictable for the community.

---

## 6. Privacy Model

Privacy is the foundation of the trust that makes the platform work. If users don't trust Tinkr with their data, they won't contribute, and the platform won't grow.

### 6.1 Principles

1. **Opt-in by default**. Telemetry is OFF unless the user explicitly opts in. Contributions are explicit (the user runs a command to share).
2. **Transparent**. The user sees exactly what's being sent. `tinkr telemetry show` prints the next event before it sends.
3. **Minimal**. We collect only what's needed. No project source. No file names. No user-typed text.
4. **Anonymized**. Telemetry events have no user identifier — only a randomly-generated session ID that rotates weekly.
5. **User-controlled**. The user can pause, delete, self-host, or fully opt out at any time.
6. **Auditable**. The telemetry endpoint is open source. The aggregation pipeline is documented. The KB is public.

### 6.2 The opt-in flow

On first run, Tinkr asks the user (one time, with a clear explanation):

```
┌──────────────────────────────────────────────────────────┐
│  Help make Tinkr smarter (optional)                       │
│                                                            │
│  Tinkr can learn from anonymous usage patterns to:         │
│  - Ship better error messages                             │
│  - Improve default configs                                │
│  - Recommend better plugins                               │
│                                                            │
│  What we DO collect:                                       │
│  ✓ Which plugins you install                              │
│  ✓ Which operations succeed/fail                          │
│  ✓ Which errors are most common                           │
│                                                            │
│  What we NEVER collect:                                    │
│  ✗ Your project source code                               │
│  ✗ Your file names                                        │
│  ✗ Anything you type in the REPL                          │
│  ✗ Device serial numbers                                  │
│                                                            │
│  You can change this any time: `tinkr telemetry settings`  │
│                                                            │
│  [Enable]  [Not now]                                      │
└──────────────────────────────────────────────────────────┘
```

The choice is sticky. The user can change it via `tinkr telemetry settings` at any time.

### 6.3 The self-hosted option

For users who don't trust a third-party endpoint, Tinkr supports a self-hosted telemetry endpoint:

```bash
tinkr telemetry endpoint https://my-telemetry.example.com
```

The endpoint is just an HTTP receiver that accepts NDJSON events. The Tinkr team publishes a reference implementation (`tinkr-telemetry-aggregator`) that the user can run on their own server. The aggregator produces the same curated output the official endpoint does.

### 6.4 The data lifecycle

| Data type | Retention | Deletion |
|---|---|---|
| Raw telemetry events | 30 days | Auto-deleted after 30 days |
| Aggregated stats | Indefinite | Tied to KB version |
| User's project (never sent) | N/A | N/A |
| User's contributions to KB | Indefinite (attributed) | User can request removal |
| User's session ID | 7 days | Auto-rotates weekly |

The user can request a full data export at any time (`tinkr telemetry export`) and full deletion (`tinkr telemetry delete --all`).

---

## 7. The User Incentive Model

Users contribute because they get something back. The contribution loop is designed to be a **fair exchange**.

### 7.1 What the user gives

- A small amount of telemetry (if opted in)
- Occasional contributions (a chip DB, a recipe, an error fix)
- Public credit (their handle in the KB)

### 7.2 What the user gets

| Contribution | Return |
|---|---|
| Opt-in telemetry | Better defaults, better error messages, more relevant plugin recommendations |
| Published plugin | Visibility in the registry, downloads, ratings, optional Patreon/GitHub Sponsors integration |
| Published recipe | Visibility in the recipe index, usage stats, community feedback |
| Knowledge entry | Attribution in the KB (their handle on every entry), a "Contributor" badge in the IDE, early access to new features |
| Sustained contribution (10+ accepted entries) | "Maintainer" status — direct push access to a specific KB subdirectory |

### 7.3 Attribution

Every KB entry has a `contributed_by` field. The user's handle (GitHub, or a Tinkr ID) shows up in:
- The KB entry itself
- `tinkr knowledge show <id>` (the local viewer)
- The agent's responses (when the agent uses that entry, it credits the contributor: "Based on @ronie's note on I2C pull-ups...")
- The KB search results (if a contributor is the source of multiple entries, their handle is featured)
- The annual "Top contributors" report (public, with the user's consent)

### 7.4 Discovery and gamification (light)

- A "Contributor" badge in the IDE (visible to the user, not the public)
- A weekly "Your contribution shipped" notification ("This week's Tinkr release includes 2 entries you contributed, used by 1,247 users this week")
- Optional public profile (off by default): `tinkr.build/u/@handle` shows your contributions
- Annual "Tinkr Contributor Awards" (a blog post + small SWAG)

The gamification is light, not aggressive. The point is fair attribution, not dopamine hits.

---

## 8. The Production Infrastructure

What it actually takes to run this. The infrastructure is real, not aspirational.

### 8.1 Components

| Component | Purpose | Hosted where | Cost (rough) |
|---|---|---|---|
| `tinkr-kb` git repo | Canonical source of the KB | GitHub (or self-hosted Gitea) | $0 (open source) |
| `tinkr-recipes` git repo | Community recipes | GitHub | $0 |
| `tinkr-registry` git repo | Plugin registry | GitHub | $0 |
| Telemetry endpoint | Receives NDJSON events | Cloudflare Workers + R2 (or self-hosted) | $5/mo for low traffic |
| Telemetry aggregator | ETL pipeline | GitHub Actions or a small VM | $20/mo for low traffic |
| KB build pipeline | Validates, signs, bundles the KB | GitHub Actions | $0 (within free tier) |
| Tinkr release pipeline | Builds, signs, publishes Tinkr binaries | GitHub Actions + macOS signing service | $100/mo for signing |
| Static KB viewer | Public, read-only viewer (tinkr.build/kb) | Cloudflare Pages | $0 |
| Public API for KB | Read-only, rate-limited | Cloudflare Workers | $5/mo |

Total: ~$130/mo for low traffic. Scales linearly with users.

### 8.2 The team

The platform can run with:
- 1 full-time maintainer (release management, security, infra)
- 2-3 part-time reviewers (knowledge curation)
- 1-2 community moderators (registry moderation)
- A wider community of contributors (free)

This is the "BDFL + community" model that Homebrew, Rust, and Kubernetes use. It scales.

### 8.3 The CI/CD pipeline

Every change to the KB goes through:

1. **PR opened** (user or maintainer)
2. **Automated checks** (CI):
   - Schema validation
   - Source URL verification (HEAD request to each cited URL)
   - Duplicate detection (new entry is not a near-duplicate of an existing one)
   - Cross-reference validation (cited `related_errors`, `related_facts` exist)
   - Sanity check (entry is not empty, has at least 2 fix_steps, etc.)
3. **Human review** (subject-matter expert):
   - Correctness
   - Clarity
   - Attribution
4. **Merge** (reviewer with write access)
5. **Automated build**:
   - Index regenerated
   - KB signed with team GPG key
   - Delta published to live endpoint
   - New KB version bundled for next Tinkr release
6. **Notification**:
   - Contributor gets a "shipped" notification
   - The next Tinkr release notes include the new entries

The whole PR-to-merge cycle is targeted at <3 days. The PR-to-shipped cycle is targeted at <7 days (typically the next knowledge drop or Tinkr release).

### 8.4 Scaling considerations

- **KB size**: Current estimate: ~1000 entries at v1.0, ~10,000 at v2.0. Each entry is small (1-5 KB). Total KB: 1-50 MB. Fits in memory.
- **Search**: At 10,000 entries, a vector index is ~50 MB, queryable in <10ms. Tools: LanceDB, Chroma, or even just numpy + cosine similarity.
- **Telemetry volume**: 10,000 active users × 50 events/day = 500K events/day = 100 MB/day. Trivial for any ingestion pipeline.
- **Plugin registry**: Git scales to 10,000s of plugins. We're nowhere near that.
- **KB build time**: <5 minutes for 10,000 entries. Acceptable.

The infrastructure scales well past the v1.0 needs. The team is the bottleneck, not the tech.

---

## 9. What "Smarter" Means in Practice

Concrete, user-visible examples of what gets better over time.

### 9.1 The first-time user experience

| Tinkr version | What a new user gets |
|---|---|
| v0.1 | Empty KB. Defaults are the ones the Tinkr team wrote by hand. Agent has only the project memory to work with. |
| v0.5 | 100 KB entries. Defaults are tuned from 10,000 user-hours. Agent has 20 common error→fix mappings. |
| v1.0 | 1000 KB entries. Defaults are tuned from 100,000 user-hours. Agent has 200 common error→fix mappings, 50 recipes, 500 chip facts. |
| v2.0 | 10,000 KB entries. Defaults are tuned from 1M user-hours. Agent has 2000 error→fix mappings, 500 recipes, 5000 facts. The "best practice" for every common task is encoded. |

### 9.2 The agent's increasing capability

| Stage | The agent can... |
|---|---|
| v0.1 (no KB) | Read project memory. Read device state. Reason from the model's training data. Limited to general programming + the project context. |
| v0.5 (small KB) | Read project memory. Read device state. Query the KB for known fixes. Recall 20 common error patterns. Suggest fixes with citations. |
| v1.0 (rich KB) | All of the above. Recall 200 error patterns. Suggest recipes for common workflows. Propose chip-specific best practices. Cross-reference datasheets. |
| v2.0 (large KB) | All of the above. Recall 2000 error patterns. Auto-detect the user's setup and propose the most likely fix path. Run multi-step recipes. Generate driver skeletons from KB patterns. |

### 9.3 The compounding effect

The compounding is real and measurable. Every accepted KB entry:
- Helps every user that hits that error
- Helps every user with that setup
- Helps every agent session that queries that entry
- Compounds: 1 entry × 10,000 users × 10 errors per user = 100,000 helpful interventions

The investment to add a KB entry is small (10-30 minutes for a subject-matter expert). The return is permanent and scales linearly with users.

This is the **flywheel** the user is asking about. It is real, it is production-proven (Stack Overflow, Wikipedia, npm, Linux), and it is the right model for Tinkr.

---

## 10. Risks and Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | Privacy incident: a user discovers Tinkr sent data they didn't consent to | Low | Very High | Default OFF. Transparent logs. Self-host option. Open-source aggregator. Aggressive deletion policy. |
| 2 | KB quality degrades: incorrect or misleading entries ship | Medium | High | Human review required. CI validation. Subject-matter expert approval. Easy user reporting (`tinkr kb report <id>`). |
| 3 | Contributor burnout: a few people do all the work and quit | Medium | High | Maintain a wide contributor base. Recognize contributors publicly. Pay top contributors (post-1.0). Automate what can be automated. |
| 4 | KB poisoning: a malicious actor contributes bad entries | Low | High | Required human review. Pattern detection (CI flags suspicious patterns). Reversible: a bad entry can be reverted in the next release. |
| 5 | Vendor capture: a single chip vendor dominates the KB with self-serving entries | Low | Medium | Subject-matter expert from outside the vendor required for review. Community flagging. Transparency on contributions. |
| 6 | Knowledge obsolescence: KB entries become outdated as chips evolve | Medium | Low | Each entry has a "verified_at" date. The agent flags old entries. Periodic re-review (the "Is this still true?" check). |
| 7 | Telemetry overcollection: a future version of Tinkr starts sending too much | Low | Very High | Telemetry code is open source. Privacy review on every release. The user can audit their own telemetry log. |
| 8 | Plugin registry spam: a vendor publishes 100 low-quality plugins | Medium | Medium | PR-based review. Spam detection. "Featured" status is curated. Rate limits on new publishes per user. |
| 9 | KB search performance: at 10,000 entries, search becomes slow | Low | Low | Vector index. Caching. Pre-computed embeddings. |
| 10 | Agent over-reliance: users stop debugging themselves and just ask the agent | Low | Low | The agent encourages learning ("This is why your I2C wasn't working..."). KB entries link to primary sources. The "Why?" is in the answer, not just the fix. |

---

## 11. The Roadmap

When to ship what.

| Release | Knowledge base | Agent | Other |
|---|---|---|---|
| **v0.1 (weeks 1-8)** | Empty (ship the schema + tooling only) | Reads project memory, calls HAL | CLI only |
| **v0.5 (weeks 9-16)** | 100 hand-curated entries (the Tinkr team's initial seed) | KB search + KB get | Tauri shell ships |
| **v1.0 (week 17-24)** | 1000 entries (community contribution flow is live) | KB fix_for + recipe_for | VS Code ext + ratatui TUI ship |
| **v1.5 (post-launch)** | 2000 entries. First A/B test of KB quality. | Agent prompts tuned from telemetry. First "best practice" auto-suggestions. | Self-host telemetry option |
| **v2.0** | 5000 entries. KB search is vector + keyword. | Agent uses KB proactively (suggests fixes before the user asks). | PyInstaller sidecar ships. Tauri updates. |
| **v2.5** | 10,000 entries. | Agent can run recipes automatically. | Logic analyzer, WiFi sim, GDB integration |
| **v3.0** | 20,000+ entries. | Constrained self-extension within plugins (the original Loop 2, in its proper form). | 3D is still cut. |

The KB growth is roughly: 100 → 1000 → 2000 → 5000 → 10,000 → 20,000 over 18 months. That's 50-100 new entries per week on average, which is achievable with 1-2 curators and a community.

---

## 12. Open Questions

1. **Should the KB ship inside Tinkr, or be pulled live by default?** Bundled is more private and offline-friendly. Live pull is fresher. Recommendation: bundled by default, live pull opt-in.
2. **Should contributions be anonymous, attributed, or both?** Attributed by default (incentive), anonymous opt-in. Users can choose.
3. **What's the right size for a knowledge drop?** 5-20 entries feels right. Too small and it's noise. Too large and the review burden is heavy.
4. **Should we have a "verified" badge for KB entries?** Yes — entries that have been used in production by 100+ users and have no bug reports get a "verified" badge.
5. **How do we handle entries that turn out to be wrong?** The user can flag them (`tinkr kb report <id>`). The curator reviews. A corrected entry ships in the next knowledge drop. The wrong entry is marked as "deprecated" but not deleted (so future users can see the correction history).
6. **What's the relationship to the chip vendor's documentation?** The KB cites official sources. The KB does not duplicate copyright material (datasheet excerpts are short quotes with citation). Long-form docs live in the plugin's knowledge bundle.
7. **How do we handle translations?** The KB is English-only at v1.0. Translations are a v2.0 feature. The schema is i18n-friendly.
8. **What about commercial / paid knowledge?** The same KB, but with a "commercial" tag and a license. The plugin ecosystem supports both free and commercial plugins; the KB can do the same.
9. **Should the agent be able to suggest a KB entry that doesn't exist yet?** Yes — if the user hits an error that's not in the KB, the agent says "this isn't in our knowledge base yet, but here's a draft entry based on my reasoning. Want to contribute it?" The user can review, edit, and submit.
10. **What's the relationship to other knowledge bases (Stack Overflow, GitHub Issues, vendor forums)?** The KB is the curated subset. Stack Overflow answers can be promoted to KB entries (with attribution). GitHub Issues can be linked. Vendor forums can be cited. The KB is the "what's true enough to ship to every user" layer on top of the chaotic long tail of community knowledge.

---

## 13. The One-Sentence Summary

> **Tinkr gets smarter by accumulating structured knowledge from its users — through opt-in telemetry, plugin publications, recipe sharing, and direct knowledge contributions — curated by humans, versioned, signed, and shipped with every Tinkr release, so the agent's answers get demonstrably better with every quarterly release and the compounding effect turns the user base into the platform's brain.**
