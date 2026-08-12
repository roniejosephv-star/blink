"""
capture.py — The reference implementation of the "just by building in it" capture layer.

This is a working example of the trigger-based capture system. In a real
Tinkr build, this would live in `tinkr/core/capture.py` and hook into
the agent's event stream.

The reference implementation shows:
- The 5 trigger classes
- The capture session (silence, frequency cap)
- The pre-fill logic (rule-based + LLM-polish hook)
- The submission pipeline (local validation + GitHub PR creation)

Run it directly to see the triggers in action (no real GitHub calls):

    /path/to/.kb-test-venv/bin/python capture.py demo
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


# ---- The data model ----

@dataclass
class AgentEvent:
    """An event the agent emits. The capture layer hooks into the agent's event stream."""
    type: str
    payload: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class UserSettings:
    """The user's capture-layer settings. Persistent in ~/.tinkr/settings.toml."""
    enabled: bool = True
    max_per_session: int = 3
    silence_recipe: bool = False
    silence_fix: bool = False
    silence_chip: bool = False
    silence_pattern: bool = False
    silence_publish: bool = False

    def is_trigger_silenced(self, trigger_name: str) -> bool:
        return getattr(self, f"silence_{trigger_name}", False)


@dataclass
class PrefilledEntry:
    """A pre-filled knowledge entry, ready for the user to review and submit."""
    trigger: str
    type: str  # "fact", "error", "pattern", "recipe", "example"
    entry: dict
    confidence: float  # 0.0 to 1.0
    reason: str  # Why this was triggered (shown to the user)
    prefill_source: str  # What data sources were used to prefill


# ---- The trigger base class ----

class Trigger:
    """Base class for capture triggers. Subclass and override matches() + prefill()."""
    name: str = "base"
    type: str = "fact"  # The KB entry type this trigger produces

    def matches(self, event: AgentEvent) -> bool:
        """Return True if this trigger should fire on this event."""
        raise NotImplementedError

    def prefill(self, event: AgentEvent, context: dict) -> dict | None:
        """Build a pre-filled KB entry from the event + context. Return None to skip."""
        raise NotImplementedError

    def confidence(self, event: AgentEvent, context: dict) -> float:
        """Return 0.0–1.0 confidence. Triggers below 0.5 are not surfaced."""
        return 0.7

    def reason(self, event: AgentEvent) -> str:
        """Human-readable explanation of why this fired. Shown to the user."""
        return f"Trigger '{self.name}' fired on event '{event.type}'."


# ---- The 5 concrete triggers ----

class SuccessfulDeployTrigger(Trigger):
    """Fires when a project deploy succeeds AND the device responds as expected."""
    name = "recipe"
    type = "recipe"

    def matches(self, event: AgentEvent) -> bool:
        return event.type == "project.deploy.completed" and event.payload.get("success")

    def prefill(self, event: AgentEvent, context: dict) -> dict | None:
        project = context.get("project", {})
        device = context.get("device", {})
        history = context.get("command_history", [])
        if not project or not device:
            return None
        return {
            "name": f"{project.get('name', 'project')}-deploy",
            "description": project.get("description") or f"Deploy {project.get('name')} to {device.get('family')}",
            "tags": [device.get("family", ""), project.get("firmware", ""), "user-contributed"],
            "setup": {
                "requires_plugin": project.get("plugins", ["tinkr-esp32"])[0],
                "requires_device_family": device.get("family"),
                "requires_firmware": project.get("firmware"),
            },
            "steps": [
                {"name": h.get("name", "step"), "run": h.get("command", "")}
                for h in history
            ],
        }

    def confidence(self, event: AgentEvent, context: dict) -> float:
        # Only suggest if the project has been worked on for at least 5 minutes.
        duration = event.payload.get("project_duration_seconds", 0)
        if duration < 300:
            return 0.2
        return 0.85

    def reason(self, event: AgentEvent) -> str:
        return f"✅ Your project just deployed successfully. Save as a recipe?"


class DebuggingFixTrigger(Trigger):
    """Fires when a debugging session ends in a fix."""
    name = "fix"
    type = "error"

    def matches(self, event: AgentEvent) -> bool:
        return event.type == "debug.session.resolved"

    def prefill(self, event: AgentEvent, context: dict) -> dict | None:
        before = event.payload.get("before", {})
        after = event.payload.get("after", {})
        fix_steps = event.payload.get("fix_steps", [])
        if not before or not fix_steps:
            return None
        return {
            "error_code": before.get("error_code", "UNKNOWN"),
            "category": before.get("category", "general"),
            "summary": before.get("summary") or f"Fix for {before.get('error_code', 'error')}",
            "likely_causes": [
                {"summary": cause} for cause in before.get("likely_causes", [])
            ],
            "fix_steps": fix_steps,
            "verify_steps": event.payload.get("verify_steps", []),
        }

    def confidence(self, event: AgentEvent, context: dict) -> float:
        # Higher confidence if the fix worked and the user confirmed.
        return 0.8 if event.payload.get("user_confirmed") else 0.5

    def reason(self, event: AgentEvent) -> str:
        err = event.payload.get("before", {}).get("error_code", "error")
        return f"🐛 You resolved a {err}. Save this fix so others can find it?"


class NewChipIdentifiedTrigger(Trigger):
    """Fires when a new (previously unseen) chip is identified."""
    name = "chip"
    type = "fact"

    def matches(self, event: AgentEvent) -> bool:
        return event.type == "device.identified" and event.payload.get("is_new")

    def prefill(self, event: AgentEvent, context: dict) -> dict | None:
        chip = event.payload.get("chip", {})
        board = event.payload.get("board")
        if not chip:
            return None
        return {
            "category": "hardware-quirk",
            "summary": f"{chip.get('chip', 'Unknown chip')} on {board or 'unknown board'}",
            "chips": [chip.get("family")],
            "detail": (
                f"Chip: {chip.get('chip')}\n"
                f"Family: {chip.get('family')}\n"
                f"Board: {board or 'unknown'}\n"
                f"Chip ID: {chip.get('chip_id', 'unknown')}\n"
                f"MAC: {chip.get('mac', 'unknown')}\n"
                f"Flash size: {chip.get('flash_size', 'unknown')}\n"
                f"Flash start address: {chip.get('flash_address', 'unknown')}"
            ),
            "sources": event.payload.get("datasheet_sources", []),
        }

    def confidence(self, event: AgentEvent, context: dict) -> float:
        return 0.9

    def reason(self, event: AgentEvent) -> str:
        chip = event.payload.get("chip", {}).get("chip", "new chip")
        return f"🆕 New chip detected: {chip}. Save to your project knowledge?"


class WiringPatternTrigger(Trigger):
    """Fires when the user has a working setup that matches a known-good pattern."""
    name = "pattern"
    type = "pattern"

    def matches(self, event: AgentEvent) -> bool:
        return event.type == "wiring.validated" and event.payload.get("matches_known_pattern")

    def prefill(self, event: AgentEvent, context: dict) -> dict | None:
        chip = event.payload.get("chip_family")
        sensor = event.payload.get("sensor")
        bus = event.payload.get("bus")
        pins = event.payload.get("pins", {})
        if not chip or not sensor or not bus:
            return None
        return {
            "category": "wiring-pattern",
            "summary": f"{chip} + {sensor} on {bus.upper()} (SDA={pins.get('sda')}, SCL={pins.get('scl')})",
            "chips": [chip],
            "detail": (
                f"Working wiring: {chip} connected to {sensor} over {bus.upper()}.\n"
                f"SDA: GPIO{pins.get('sda')}\n"
                f"SCL: GPIO{pins.get('scl')}\n"
                f"VCC: 3.3V\n"
                f"GND: GND\n"
                f"\n"
                f"Verified by: user working session on {time.strftime('%Y-%m-%d')}"
            ),
        }

    def confidence(self, event: AgentEvent, context: dict) -> float:
        return 0.75

    def reason(self, event: AgentEvent) -> str:
        chip = event.payload.get("chip_family")
        sensor = event.payload.get("sensor")
        return f"🔌 Working wiring: {chip} + {sensor}. Save as a pattern?"


class ProjectReadyToPublishTrigger(Trigger):
    """Fires when a project is in good shape and not yet published."""
    name = "publish"
    type = "example"

    def matches(self, event: AgentEvent) -> bool:
        return (
            event.type == "project.health.check"
            and event.payload.get("tests_passing", 0) >= 1
            and event.payload.get("deployed_successfully", False)
            and not event.payload.get("already_published", True)
        )

    def prefill(self, event: AgentEvent, context: dict) -> dict | None:
        project = context.get("project", {})
        if not project:
            return None
        return {
            "name": project.get("name"),
            "description": project.get("description", ""),
            "main_py": project.get("main_py", ""),
            "tinkr_toml": project.get("tinkr_toml", ""),
            "tags": project.get("tags", []),
            "license": "MIT",
        }

    def confidence(self, event: AgentEvent, context: dict) -> bool:
        # Only suggest if the project has been worked on for at least 30 minutes.
        return 0.7 if event.payload.get("session_minutes", 0) >= 30 else 0.3

    def reason(self, event: AgentEvent) -> str:
        return f"🎉 Your project is in good shape (tests passing, deployed). Publish as an example?"


# ---- The capture session ----

class CaptureSession:
    """The capture layer's per-session state. Manages silence, frequency cap, etc."""

    def __init__(self, settings: UserSettings, kb: Any = None, context: dict | None = None):
        self.settings = settings
        self.kb = kb
        self.context = context or {}
        self.suggested_this_session = 0
        self.skipped_streak: dict[str, int] = {}  # trigger_name -> consecutive skips
        self.triggers: list[Trigger] = [
            SuccessfulDeployTrigger(),
            DebuggingFixTrigger(),
            NewChipIdentifiedTrigger(),
            WiringPatternTrigger(),
            ProjectReadyToPublishTrigger(),
        ]

    def on_event(self, event: AgentEvent) -> PrefilledEntry | None:
        """Called on every agent event. Returns a prefilled entry if the layer wants to surface a suggestion."""
        if not self.settings.enabled:
            return None
        if self.suggested_this_session >= self.settings.max_per_session:
            return None

        for trigger in self.triggers:
            if not trigger.matches(event):
                continue
            if self.settings.is_trigger_silenced(trigger.name):
                continue
            if self.skipped_streak.get(trigger.name, 0) >= 3:
                # Auto-silence after 3 consecutive skips.
                self._auto_silence(trigger.name)
                continue

            entry = trigger.prefill(event, self.context)
            if entry is None:
                continue

            conf = trigger.confidence(event, self.context)
            if conf < 0.5:
                continue

            self.suggested_this_session += 1
            return PrefilledEntry(
                trigger=trigger.name,
                type=trigger.type,
                entry=entry,
                confidence=conf,
                reason=trigger.reason(event),
                prefill_source=f"trigger:{trigger.name}, event:{event.type}",
            )

        return None

    def user_skipped(self, trigger_name: str) -> None:
        """Called when the user clicks 'Skip this time'."""
        self.skipped_streak[trigger_name] = self.skipped_streak.get(trigger_name, 0) + 1

    def user_submitted(self, trigger_name: str) -> None:
        """Called when the user clicks 'Submit'."""
        self.skipped_streak[trigger_name] = 0  # Reset the streak on success.

    def _auto_silence(self, trigger_name: str) -> None:
        """After 3 skips, auto-silence the trigger type."""
        attr = f"silence_{trigger_name}"
        if hasattr(self.settings, attr):
            setattr(self.settings, attr, True)


# ---- The submission pipeline ----

def submit_entry(prefilled: PrefilledEntry, github_user: str | None = None) -> dict:
    """
    Submit a pre-filled entry to the KB queue.

    In production, this would:
    1. Validate the entry against the schema (fact.schema.json, etc.)
    2. Check for duplicates in the local KB
    3. Create a PR on the user's fork of tinkr-kb
    4. Open a PR from the fork to the central tinkr-kb

    The reference implementation just prints what it would do.
    """
    print(f"\n[Capture] Submitting {prefilled.type} entry:")
    print(f"  trigger: {prefilled.trigger}")
    print(f"  confidence: {prefilled.confidence:.2f}")
    print(f"  reason: {prefilled.reason}")
    print(f"  entry: {json.dumps(prefilled.entry, indent=2)[:300]}...")
    if github_user:
        print(f"  → Would create PR on github.com/{github_user}/tinkr-kb")
        print(f"  → Then open PR to github.com/tinkr-knowledge/index")
    else:
        print(f"  → Would save to ~/.tinkr/captures/drafts/ (no GitHub login)")
    return {"status": "queued", "trigger": prefilled.trigger, "type": prefilled.type}


# ---- The demo ----

def demo() -> None:
    """Demonstrate the capture layer in action with a few synthetic events."""
    print("=" * 60)
    print("Capture Layer Demo")
    print("=" * 60)

    settings = UserSettings()
    context = {
        "project": {
            "name": "kitchen-sensor",
            "description": "ESP32-S3 temperature + humidity sensor for the kitchen.",
            "firmware": "micropython",
            "plugins": ["tinkr-esp32@^1.2"],
            "main_py": "import machine, time\n...",
            "tinkr_toml": "[project]\nname = \"kitchen-sensor\"\n...",
        },
        "device": {
            "family": "esp32s3",
            "board": "ESP32-S3-DevKitC-1",
        },
        "command_history": [
            {"name": "scan-ports", "command": "tinkr esp32 port-scan"},
            {"name": "identify", "command": "tinkr esp32 identify --port /dev/cu.usbserial-1410"},
            {"name": "flash", "command": "tinkr esp32 flash-firmware --port /dev/cu.usbserial-1410 --firmware fw.bin"},
            {"name": "deploy", "command": "tinkr project deploy"},
        ],
    }
    session = CaptureSession(settings, context=context)

    events = [
        AgentEvent(type="device.identified", payload={
            "is_new": True,
            "chip": {"chip": "ESP32-S3", "family": "esp32s3", "chip_id": "0x12345678", "mac": "aa:bb:cc:dd:ee:ff", "flash_size": "8MB", "flash_address": "0x0"},
            "board": "ESP32-S3-DevKitC-1",
            "datasheet_sources": ["https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet.pdf"],
        }),
        AgentEvent(type="project.deploy.completed", payload={
            "success": True,
            "project_duration_seconds": 1500,
        }),
        AgentEvent(type="wiring.validated", payload={
            "matches_known_pattern": True,
            "chip_family": "esp32s3",
            "sensor": "BME280",
            "bus": "i2c",
            "pins": {"sda": 8, "scl": 9},
        }),
        AgentEvent(type="debug.session.resolved", payload={
            "before": {"error_code": "OSError_ETIMEDOUT", "category": "i2c", "summary": "I2C scan times out"},
            "after": {"state": "ok"},
            "fix_steps": ["Add 4.7kΩ pull-ups", "Verify with i2c.scan()"],
            "verify_steps": ["i2c.scan() returns [0x76]"],
            "user_confirmed": True,
        }),
        AgentEvent(type="project.health.check", payload={
            "tests_passing": 3,
            "deployed_successfully": True,
            "already_published": False,
            "session_minutes": 45,
        }),
    ]

    for i, event in enumerate(events, 1):
        print(f"\n--- Event {i}: {event.type} ---")
        suggestion = session.on_event(event)
        if suggestion:
            print(f"  💡 SUGGESTION: {suggestion.reason}")
            print(f"     confidence: {suggestion.confidence:.2f}")
            print(f"     would prefill: {list(suggestion.entry.keys())}")
            # In a real system, the user would see the review pane here.
            # For demo, just submit.
            submit_entry(suggestion, github_user="ronie")
        else:
            print(f"  (no suggestion — cap reached or trigger silenced)")

    # Test the silence mechanism: 3 skips auto-silence.
    print("\n" + "=" * 60)
    print("Silence mechanism test (3 skips auto-silence):")
    print("=" * 60)
    new_session = CaptureSession(UserSettings(max_per_session=100), context=context)
    for i in range(5):
        event = AgentEvent(type="device.identified", payload={"is_new": True, "chip": {"chip": "ESP32"}, "board": "X"})
        suggestion = new_session.on_event(event)
        if suggestion:
            print(f"  Skip {i+1}: would surface suggestion")
            new_session.user_skipped("chip")
        else:
            print(f"  Skip {i+1}: auto-silenced.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        print("Usage: capture.py demo")
