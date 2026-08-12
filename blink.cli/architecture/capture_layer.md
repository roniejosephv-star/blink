# The "Just By Building In It" Capture Layer — Design v0.1

> The piece that turns the learning loop from "users *can* contribute" into "users contribute without realizing they're contributing." The agent watches what you do, notices when you've done something worth capturing, offers to capture it, fills in 90% of the form, asks for your one-click approval, and submits. The friction is so low that contributing becomes a side-effect of building. This is what makes Tinkr compound.

---

## 1. The Core Idea

The capture layer is a set of **triggers** in the Tinkr agent that fire on certain events during normal use. When a trigger fires, the agent:

1. Recognizes that what just happened is worth capturing (a successful project deploy, a debugging fix, a new chip connection, a useful wiring).
2. Pre-fills a knowledge entry with what it already knows (project context, device state, code that worked).
3. Surfaces a small, non-intrusive suggestion to the user: "Want to save this as a recipe / fix / chip DB for others?"
4. If the user clicks "Yes," opens a review pane with the pre-filled entry. The user edits if needed, then clicks "Submit."
5. The entry becomes a PR to the KB repo, queued for curation.

The user has to do two things: **notice the suggestion**, and **click submit**. Everything else is automatic.

This is the same UX pattern that made Stack Overflow, GitHub Stars, and Spotify's "add to library" button work. The user does the meaningful work (building), the system does the bookkeeping (capturing), and the user approves the result.

---

## 2. The Capture Triggers

Five triggers, in priority order. Each fires on a specific event during normal Tinkr use.

### 2.1 Trigger A: Successful project deploy → "Save as recipe"

**Fires on**: A `tinkr project deploy` command that exits 0 and the device responds as expected (REPL prompt, expected output, no errors in the first 30s of monitoring).

**What it captures**: A **recipe** entry. The sequence of commands that worked: the plugin used, the chip family, the firmware, the steps from the project memory.

**Pre-filled fields**:
- `name` (from `tinkr.toml`'s project name)
- `description` (from the project description in `tinkr.toml`)
- `tags` (from the chip family, firmware, project category)
- `setup.requires_plugin` (from the installed plugins)
- `setup.requires_device_family` (from the device)
- `setup.requires_firmware` (from the project target)
- `steps` (from the commands actually run during deploy, captured by the agent's instrumentation)

**The user edits**:
- Tags (most likely tweak)
- Description (the agent's first draft is usually generic)
- A "this is a beginner recipe" / "this is an advanced recipe" flag

**Effort**: 30-60 seconds of user review.

**Example prompt to the user** (in the IDE):

> ✅ Your project `kitchen-sensor` just deployed successfully on an ESP32-S3 with MicroPython.
>
> **Save as a recipe** so others can use this workflow?
>
> Pre-filled draft:
> ```
> name: kitchen-sensor-deploy
> description: "Deploy a sensor project to an ESP32-S3 with MicroPython"
> tags: [esp32s3, micropython, sensor]
> steps: 7 (auto-captured)
> ```
>
> [Edit & Submit] [Skip this time] [Don't ask for recipes]

### 2.2 Trigger B: Debugging session that ends in a fix → "Save the fix"

**Fires on**: A debugging interaction with the agent that ends with a code change that resolves an error. The agent notices the "before" (an error) and the "after" (a working state).

**What it captures**: An **error** entry. The error signature, the likely causes, the fix steps, the verify steps.

**Pre-filled fields**:
- `error_code` (parsed from the error message, e.g., "OSError_ETIMEDOUT")
- `summary` (auto-generated from the error message)
- `category` (auto-classified, e.g., "i2c")
- `likely_causes` (the agent's hypothesis before the fix, e.g., "wrong pull-ups")
- `fix_steps` (the steps the user actually took to fix it, captured from the agent's command history)
- `verify_steps` (the steps the user took to confirm the fix, e.g., "ran i2c.scan() and got [0x76]")

**The user edits**:
- `summary` (often generic from the agent's first draft)
- Reorders the `fix_steps` (the agent might not know which was the actual fix vs which was a red herring)
- Adds context the agent missed (e.g., "I had the I2C pull-up on the wrong pin")

**Effort**: 60-120 seconds of user review.

**Example prompt**:

> 🐛 You had an `OSError: [Errno 110] ETIMEDOUT` on `i2c.scan()`. The fix (adding 4.7kΩ pull-ups) worked.
>
> **Save this as a fix** so others with the same error can find it?
>
> Pre-filled draft:
> ```
> error_code: OSError_ETIMEDOUT
> category: i2c
> summary: "I2C scan returns empty due to missing pull-up resistors"
> fix_steps: 3 (auto-captured)
>   1. Added 4.7kΩ pull-up from SDA to 3.3V
>   2. Added 4.7kΩ pull-up from SCL to 3.3V
>   3. Verified with i2c.scan() -> [0x76]
> ```
>
> [Edit & Submit] [Skip this time] [Don't ask for fixes]

### 2.3 Trigger C: First-time chip identified → "Save the chip info"

**Fires on**: A `tinkr-*-identify` command that discovers a chip the user has not seen before (not in the user's `tinkr.toml` `[devices]` history, not in the KB).

**What it captures**: A **fact** entry for the chip. The chip's identifying info, the flash address, the firmware it came with, the user's notes.

**Pre-filled fields**:
- `category`: "hardware-quirk" or "firmware-quirk" (inferred from the chip)
- `summary`: "{chip} on {board}"
- `chips`: the chip family
- `detail`: auto-extracted from the identify output (chip ID, MAC, flash size, etc.)
- `sources`: the plugin's datasheet references (if the plugin is `tinkr-esp32`, the `knowledge/datasheets/esp32-s3-datasheet.pdf` path)

**The user edits**:
- Adds personal notes ("this board is on my desk, runs at 240 MHz, has a known issue with GPIO9")
- Adds the actual pinout if it's a custom board

**Effort**: 30-60 seconds.

**Example prompt**:

> 🆕 New chip detected: ESP32-S3-DevKitC-1 (N8R8) on `/dev/cu.usbserial-1410`.
>
> **Save this chip to your project's knowledge** so the agent remembers it next time?
>
> Pre-filled draft:
> ```
> fact/esp32s3-devkitc-1-n8r8
> chips: [esp32s3]
> summary: "ESP32-S3-DevKitC-1 (N8R8) — 8MB flash, 8MB PSRAM"
> sources: [ESP32-S3 datasheet (from tinkr-esp32 plugin)]
> ```
>
> [Edit & Submit] [Skip] [Don't ask for chips]

### 2.4 Trigger D: Plugin used successfully → "Save as a wiring pattern"

**Fires on**: A project that uses a specific chip + sensor + wiring that the agent recognizes as a common pattern. The agent has a small library of "known good patterns" internally (e.g., "ESP32 + BME280 on I2C", "ESP32 + NeoPixel on GPIO48") and offers to save the user's exact wiring as a reusable pattern.

**What it captures**: A **pattern** entry. The chip, the sensor, the pins used, the code skeleton, the user's notes on what worked.

**Pre-filled fields**:
- `category`: "wiring-pattern"
- `summary`: "{chip} + {sensor} on {bus}"
- `chips`: the chip family
- `detail`: the wiring (SDA on GPIO8, SCL on GPIO9, VCC to 3.3V, GND to GND)
- `sources`: the user's project repo

**The user edits**:
- Confirms the wiring is correct
- Adds a "tested with firmware X" note
- Adds the actual I2C address they used

**Effort**: 30-60 seconds.

**Example prompt**:

> 🔌 You wired an ESP32-S3 to a BME280 over I2C and it's working.
>
> **Save this as a wiring pattern** so others with the same setup can copy it?
>
> Pre-filled draft:
> ```
> pattern/esp32s3-bme280-i2c
> chips: [esp32s3]
> summary: "ESP32-S3 + BME280 on I2C (SDA=GPIO8, SCL=GPIO9)"
> detail: [auto-extracted wiring]
> ```
>
> [Edit & Submit] [Skip] [Don't ask for patterns]

### 2.5 Trigger E: Project done + tests passing → "Publish the project as an example"

**Fires on**: A project that has been worked on for at least 30 minutes AND has at least one passing test AND has been deployed at least once AND is not yet published.

**What it captures**: A **published example** in the plugin's `examples/` directory. The project, the tinkr.toml, the main.py, the README, the chip DB entries.

**Pre-filled fields**:
- Project name, description
- The `main.py` (or the equivalent user code)
- The `tinkr.toml` (auto-curated from the project's actual config)
- A README generated from the project's git history and comments

**The user edits**:
- The README
- Tags
- License (default: MIT, but the user can choose)

**Effort**: 2-5 minutes. This is the highest-effort trigger because the artifact is bigger.

**Example prompt**:

> 🎉 Your project `kitchen-sensor` is in good shape: 3 tests passing, deployed successfully, has a README.
>
> **Publish it as an example** in the `tinkr-esp32` plugin so other ESP32 users can learn from it?
>
> The plugin maintainers will review and merge if it fits.
>
> [Edit & Submit] [Skip] [Don't ask for examples]

---

## 3. The UX: Non-Intrusive Capture

The key challenge: the user is building. The capture layer is a *side-effect*, not the main event. The UX must be non-intrusive.

### 3.1 Where the prompt appears

The prompt is **not** a popup. It is a small **Capture badge** in the IDE's status bar (or the TUI's footer). It looks like this:

```
[Status bar]
main.py ✓ tests 3/3 ✓ device: esp32s3-left   |   [📥 1 capture suggestion]  |
```

The badge is clickable. Clicking opens the **Capture Review Pane** — a side panel that shows the pre-filled entry. The user reviews, edits, and clicks Submit.

The badge stays visible until the user either submits or dismisses. It does not block the user's work. The user can ignore it and keep building.

### 3.2 The Capture Review Pane

The review pane is a small form, not a separate page. It shows:

- The pre-filled entry (editable)
- A "Why this was triggered" note (so the user understands)
- Three buttons: "Submit", "Skip this time", "Don't ask again for this type"
- A "Preview as it will appear in the KB" view

The user can edit any field. Most users will tweak the description and tags, then submit.

### 3.3 Silence mechanisms

The user has full control. Four silence mechanisms:

1. **Skip this time**: dismisses the current suggestion. The next one of the same type will appear.
2. **Don't ask again for this type**: silences this trigger type forever (the user can re-enable in settings).
3. **Don't ask in this session**: silences all capture suggestions for the rest of the session.
4. **Don't ask in this project**: silences all capture suggestions for this project only.

Silence is reversible in the settings. The user is in control.

### 3.4 Frequency cap

The agent will not surface more than **3 capture suggestions per session**. The user can set a higher cap in settings. This is to prevent the agent from being annoying on a long session.

### 3.5 The "low-confidence" rule

If the agent is not confident that the captured event is worth capturing (e.g., the project deploy succeeded but the device disconnected 5 seconds later, suggesting flakiness), the agent does **not** surface the suggestion. The user does not see low-quality prompts.

---

## 4. The Pipeline: From Capture to KB

The pipeline from "user clicks Submit" to "entry ships in the next Tinkr release" is a four-step flow.

### 4.1 Step 1: Local validation

The agent validates the entry locally before submitting:
- Schema validation (against `fact.schema.json`, `error.schema.json`, etc.)
- Duplicate check (against the local bundled KB and the user's project)
- Required fields present
- Reasonable length (not too short, not too long)

If validation fails, the user sees a small warning and can edit before submitting. The agent does not submit invalid entries.

### 4.2 Step 2: Submission to the KB queue

The user clicks Submit. The entry is sent to the KB queue. There are three submission paths:

1. **Direct to the user's fork** (default): the entry becomes a PR on `github.com/{user}/tinkr-kb`, then a PR from there to `github.com/tinkr-knowledge/index`. This is the most common flow.
2. **Direct to the central repo** (for verified contributors): contributors with >10 accepted entries can submit directly to the central repo.
3. **As a draft for the user to edit** (if the user wants to refine later): the entry is saved locally and surfaced in the user's KB draft list.

The GitHub-based flow is the same as any open-source contribution. The user signs in with GitHub (already done at install time), and the agent creates a fork + PR for them.

### 4.3 Step 3: Curation

A Tinkr team reviewer (or a community maintainer) reviews the PR. The review is:
- **Automated checks** (CI): schema validation, source URL verification, duplicate detection, cross-reference validation.
- **Human review**: correctness, clarity, attribution, copyright.

The review target is **3 days from PR open to merge**. The user's contribution is acknowledged in the PR comments.

### 4.4 Step 4: Shipping

The merged entry is included in the next **knowledge drop** (weekly) or the next **Tinkr release** (monthly), whichever comes first. The user gets a notification: "Your contribution to the KB shipped in Tinkr 0.5.2. It's been used by 142 other users in the past week."

The cycle: capture → review → ship → notify → next capture. The user's name is in the entry forever.

---

## 5. The Agent's Internal Trigger Logic

The capture layer is a small module in the Tinkr agent. It hooks into the agent's event stream.

```python
# Pseudo-code for the trigger logic.
# (The full implementation would be in tinkr/core/capture.py)

class CaptureLayer:
    def __init__(self, kb: KnowledgeBase, settings: UserSettings, agent: Agent):
        self.kb = kb
        self.settings = settings
        self.agent = agent
        self.session_count = 0  # Cap per session

    def on_event(self, event: AgentEvent) -> None:
        """Called on every agent event. The capture layer decides whether to surface a suggestion."""
        if self.session_count >= self.settings.max_captures_per_session:
            return

        for trigger in self.triggers:
            if trigger.matches(event):
                entry = trigger.prefill(event, self.kb, self.agent.context)
                if entry and trigger.is_confident_enough(entry, event):
                    self.agent.suggest_capture(entry, trigger)
                    self.session_count += 1
                    return  # One trigger per event max

    @property
    def triggers(self) -> list[Trigger]:
        return [
            SuccessfulDeployTrigger(),
            DebuggingFixTrigger(),
            NewChipIdentifiedTrigger(),
            WiringPatternTrigger(),
            ProjectReadyToPublishTrigger(),
        ]
```

The trigger class is small and focused. Each trigger knows its event type, what to prefill, and how to score confidence.

### 5.1 Example: SuccessfulDeployTrigger

```python
class SuccessfulDeployTrigger(Trigger):
    """Fires when a project deploy succeeds and the device responds as expected."""

    def matches(self, event: AgentEvent) -> bool:
        return event.type == "project.deploy.completed" and event.success

    def prefill(self, event: AgentEvent, kb: KnowledgeBase, ctx: AgentContext) -> dict | None:
        # Verify the device is still responding.
        if not ctx.device_alive(timeout=30):
            return None  # Low confidence — device flaked
        # Build a recipe from the project's config + the deploy command history.
        project = ctx.project
        return {
            "type": "recipe",
            "name": f"{project.name}-deploy",
            "description": project.description or f"Deploy {project.name}",
            "tags": [ctx.device.family, project.firmware, "user-contributed"],
            "setup": {
                "requires_plugin": project.plugins[0],
                "requires_device_family": ctx.device.family,
                "requires_firmware": project.firmware,
            },
            "steps": self._extract_steps_from_history(ctx.command_history),
        }

    def is_confident_enough(self, entry: dict, event: AgentEvent) -> bool:
        # Only suggest if the project has been worked on for at least 5 minutes
        # (so we're not capturing trivial deploys).
        return event.project_duration_seconds > 300
```

The trigger is small, focused, and explicit about when to fire. No LLM call needed for the trigger logic — just rule-based matching.

### 5.2 When the LLM IS used

The LLM is used for:
- Auto-generating the `description` from the project's `main.py` (a 1-line summary)
- Auto-suggesting tags from the project's content
- Re-phrasing the user's "fix" into clean `fix_steps` language

The LLM is NOT used for:
- The trigger decision (rule-based)
- The schema validation (deterministic)
- The pre-fill of factual data (the data is already in the project)

This means the capture layer is **fast and cheap**. The LLM is a polish step, not a critical path.

---

## 6. The Capture Layer in the 8-Week Plan

The capture layer ships in **v1.0** (week 8 of the original plan), with a phased rollout:

| Phase | What ships |
|---|---|
| v0.5 (week 4-5) | **Local-only capture**. The agent can capture entries and save them to the user's `~/.tinkr/captures/`. The user can review and submit manually. No GitHub flow yet. |
| v0.7 (week 6-7) | **GitHub submission**. The user signs in with GitHub. The agent creates a fork and PR. The user reviews before submission. |
| v1.0 (week 8) | **Full capture layer**. All 5 triggers, the review pane, the silence mechanisms, the weekly drop notification. |
| v1.5 (post-launch) | **Auto-extraction of chip DBs**. When the user identifies a new chip, the agent auto-extracts the chip info from the plugin's knowledge bundle. |
| v2.0 (q3 2026) | **Capture analytics**. The Tinkr team sees (anonymized) which triggers fire most, which have the highest submit rate, and uses this to improve the layer. |

---

## 7. What Makes This Different From "AI Writes Tools"

A natural reaction to this design: "How is this different from the original Loop 2 (AI writes tools)?"

**The difference is who is in the loop.**

| Original Loop 2 | Capture Layer |
|---|---|
| LLM writes a tool from scratch | LLM summarizes what the user already did |
| LLM generates code that might be wrong | LLM captures code that the user already verified works |
| LLM is the author | LLM is the summarizer; the user is the author |
| Auto-execution (with risk) | User clicks Submit; the user is the gate |
| "Self-growing" (autonomous) | "Just by building" (assisted) |

The capture layer puts the **user in the loop** for every entry. The LLM never writes a knowledge entry that the user has not seen and approved. The user is the source of truth; the LLM is the typist.

This is the **"human in the loop"** pattern from the original learning_loop.md §2.6 (OWASP ASI01–ASI05). It is the same safety model, applied to the capture layer.

---

## 8. Open Questions

1. **What's the right frequency cap?** 3 per session? 5? 10? Recommendation: 3, with the user-configurable max in settings.
2. **Should the capture layer also capture *unsuccessful* events?** "I tried X, it didn't work, I tried Y, it worked." This is gold for the KB. But the user's edit effort is higher. Recommendation: v2, after we have a good UX for successful captures.
3. **Should the user be able to capture manually?** "I just figured something out, let me write a KB entry from scratch." Yes — a `tinkr knowledge add` command for manual capture. The capture layer is the *proactive* version.
4. **What about capturing *intents* vs *outcomes*?** "I want to do X" vs "I did X and it worked." The current triggers capture outcomes. Intents are useful too (they tell us what users want to do, even if they haven't figured it out yet). Recommendation: v2, with anonymized "what users search for" telemetry.
5. **Should the capture layer learn from the user's silence?** If the user always skips "Save as recipe" suggestions, should the agent stop asking? Yes — after 3 consecutive skips of the same trigger type, the agent auto-silences it. The user can re-enable in settings.
6. **What's the right amount of LLM polish?** Auto-description, auto-tags, auto-phrasing of fix steps. Too much and the user doesn't feel ownership. Too little and the entry is messy. Recommendation: LLM suggests, user confirms. Never LLM-only.
7. **Should the capture layer be opt-in?** Default: ON. The user can disable in settings. The first run shows a one-time prompt explaining the feature. The user is in control, but the default is "yes, please help Tinkr get smarter."
