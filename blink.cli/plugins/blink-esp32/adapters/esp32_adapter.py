"""HAL adapter for ESP32-family devices.

This is the typed Python surface the rest of Tinkr uses to talk to an ESP32.
The adapter wraps the plugin's CLI tools (which emit NDJSON) and exposes
typed, async, capability-decorated methods.

The adapter is auto-discovered by `tinkr.core.hal.HAL.discover()` and is
instantiated per-device by `HAL.find_adapter()`.

Usage (from Tinkr core or the MCP server):

    from tinkr.core.hal import HAL
    hal = HAL(plugin_dir=Path(".tinkr/plugins"))
    adapter = hal.find_adapter(device)
    result = await adapter.flash(device, firmware=Path("firmware.bin"))
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncIterator, Callable

# These would be in `tinkr.core.hal` once Tinkr core is factored out.
# For now, we provide minimal local types so this adapter is self-contained.
try:
    from tinkr.core.hal import (
        Device,
        DeviceAdapter,
        Capability,
        Result,
        ProgressEvent,
    )
except ImportError:
    # Local fallback: a minimal typing shim so the plugin is self-contained.
    from dataclasses import dataclass as _dc, field as _field
    from typing import Any as _A

    @_dc
    class Device:
        id: str
        port: str | None
        family: str
        plugin: str
        capabilities: frozenset[str] = _field(default_factory=frozenset)

    class DeviceAdapter:  # type: ignore[no-redef]
        plugin_name: str = ""
        def __init__(self, device: Device) -> None:
            self.device = device

        @classmethod
        def matches(cls, device_info: dict) -> bool:
            return False

    def Capability(name: str):  # type: ignore[no-redef]
        def deco(fn):
            fn.__capability__ = name
            return fn
        return deco

    @_dc
    class Result:
        data: _A = None
        ok: bool = True
        error: str | None = None

    @_dc
    class ProgressEvent:
        stage: str
        pct: int
        message: str


# The plugin's own CLI tool paths.
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
CLI_DIR = PLUGIN_ROOT / "cli"


class _CliRunner:
    """A small async wrapper around the plugin's CLI tools.

    Invokes a CLI tool as a subprocess, parses NDJSON from stdout,
    and yields typed events.
    """

    def __init__(self, cli_dir: Path = CLI_DIR) -> None:
        self.cli_dir = cli_dir

    def _path(self, tool: str) -> Path:
        return self.cli_dir / f"{tool}.py"

    async def run(self, tool: str, args: list[str]) -> dict:
        """Run a tool to completion. Returns the final result data."""
        path = self._path(tool)
        if not path.is_file():
            raise FileNotFoundError(f"CLI tool not found: {path}")
        proc = await asyncio.create_subprocess_exec(
            sys.executable, str(path), *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            # Try to extract an error code from the last NDJSON line.
            for line in stdout.decode().splitlines():
                try:
                    msg = json.loads(line)
                    if msg.get("type") == "error":
                        raise RuntimeError(
                            f"{msg.get('code', 'error')}: {msg.get('message', '')}"
                        )
                except json.JSONDecodeError:
                    continue
            raise RuntimeError(f"{tool} failed (exit {proc.returncode}): {stderr.decode().strip()}")
        # Find the last result event.
        for line in reversed(stdout.decode().splitlines()):
            try:
                msg = json.loads(line)
                if msg.get("type") == "result":
                    return msg.get("data", {})
            except json.JSONDecodeError:
                continue
        return {}

    async def stream(self, tool: str, args: list[str]) -> AsyncIterator[dict]:
        """Stream NDJSON events from a tool."""
        path = self._path(tool)
        if not path.is_file():
            raise FileNotFoundError(f"CLI tool not found: {path}")
        proc = await asyncio.create_subprocess_exec(
            sys.executable, str(path), *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        while True:
            line = await proc.stdout.readline()
            if not line:
                break
            try:
                yield json.loads(line.decode())
            except json.JSONDecodeError:
                continue
        await proc.wait()


class ESP32Adapter(DeviceAdapter):
    """The HAL adapter for ESP32-family devices."""

    plugin_name = "tinkr-esp32"

    # Chip family → identify tool arg (none, since the port is the arg).
    @classmethod
    def matches(cls, device_info: dict) -> bool:
        family = (device_info.get("family") or "").lower().replace("-", "")
        return family in {"esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32c2"}

    def __init__(self, device: Device) -> None:
        super().__init__(device)
        self.cli = _CliRunner()

    # -- Identification --

    @Capability("identify")
    async def identify(self) -> dict:
        """Identify the chip on the device's port."""
        if not self.device.port:
            raise ValueError("Device has no port; cannot identify.")
        info = await self.cli.run("tinkr-esp32-identify", ["--port", self.device.port])
        # Update the device with the discovered info (in-place mutation; the
        # caller should refresh its reference).
        self.device.family = info.get("family", self.device.family)
        return info

    # -- Flash --

    @Capability("flash")
    async def flash(self, *, firmware: Path, erase: bool = False,
                    address: str | None = None, baud: int = 460800) -> AsyncIterator[ProgressEvent]:
        """Stream flash progress events. Yields ProgressEvent; final yield is a Result.

        Usage:
            async for event in adapter.flash(firmware=Path("fw.bin")):
                print(event)
        """
        if not self.device.port:
            raise ValueError("Device has no port; cannot flash.")
        args = ["--port", self.device.port, "--firmware", str(firmware), "--baud", str(baud)]
        if erase:
            args.append("--erase")
        if address:
            args.extend(["--address", address])
        async for event in self.cli.stream("tinkr-esp32-flash-firmware", args):
            if event.get("type") == "progress":
                yield ProgressEvent(
                    stage=event.get("stage", ""),
                    pct=event.get("pct", 0),
                    message=event.get("message", ""),
                )
            elif event.get("type") == "result":
                yield Result(data=event.get("data", {}), ok=True)
            elif event.get("type") == "error":
                yield Result(ok=False, error=event.get("message", ""))

    # -- REPL --

    @Capability("repl.execute")
    async def repl_execute(self, code: str) -> dict:
        """Execute a Python snippet on the device."""
        if not self.device.port:
            raise ValueError("Device has no port; cannot execute code.")
        return await self.cli.run(
            "tinkr-esp32-repl-execute",
            ["--port", self.device.port, "--code", code],
        )

    # -- Filesystem --

    @Capability("filesystem.list")
    async def fs_list(self, path: str = "/") -> list[dict]:
        """List a path on the device's filesystem."""
        if not self.device.port:
            raise ValueError("Device has no port; cannot list filesystem.")
        result = await self.cli.run(
            "tinkr-esp32-fs-list",
            ["--port", self.device.port, "--path", path],
        )
        return result.get("entries", [])

    # -- Port scan (for HAL's auto-discovery) --

    @classmethod
    async def scan_ports(cls) -> list[dict]:
        """Run the port-scan tool and return detected devices."""
        runner = _CliRunner()
        result = await runner.run("tinkr-esp32-port-scan", [])
        return result.get("devices", [])
