"""Smoke test for the tinkr-esp32 plugin.

Runs without hardware. Verifies:
- The manifest is well-formed.
- All CLI tools exist and are executable.
- The chip DBs parse as JSON.
- The pinout JSON is valid.

This is the test that runs on `tinkr plugin install` to ensure the plugin
is at least bootable.
"""
import json
import os
import stat
import sys
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def test_manifest_exists():
    """The manifest must exist at the plugin root."""
    manifest = PLUGIN_ROOT / "tinkr.plugin.toml"
    assert manifest.is_file(), f"Missing manifest: {manifest}"


def test_manifest_has_required_sections():
    """The manifest must declare plugin identity, capabilities, and tools."""
    import tomllib
    with open(PLUGIN_ROOT / "tinkr.plugin.toml", "rb") as f:
        manifest = tomllib.load(f)
    assert manifest["plugin"]["name"] == "tinkr-esp32"
    assert manifest["plugin"]["version"]
    assert "esp32s3" in manifest["provides"]["families"]
    assert manifest["capabilities"]["flash"] is True
    assert len(manifest["tools"]) >= 1


def test_cli_tools_exist_and_executable():
    """Each declared CLI tool must exist on disk and be executable."""
    import tomllib
    with open(PLUGIN_ROOT / "tinkr.plugin.toml", "rb") as f:
        manifest = tomllib.load(f)
    for tool in manifest["tools"]:
        entry = PLUGIN_ROOT / tool["entry"]
        assert entry.is_file(), f"Missing CLI tool: {entry}"
        assert entry.suffix == ".py", f"Only Python tools supported in v1: {entry}"
        mode = entry.stat().st_mode
        assert mode & stat.S_IXUSR, f"CLI tool not executable: {entry}"


def test_chip_dbs_parse():
    """Every chip DB JSON file must be valid JSON with the required fields."""
    chips_dir = PLUGIN_ROOT / "knowledge" / "chips"
    assert chips_dir.is_dir(), f"Missing chips directory: {chips_dir}"
    json_files = list(chips_dir.glob("*.json"))
    assert len(json_files) >= 1, "No chip DBs found"
    for jf in json_files:
        with open(jf) as f:
            data = json.load(f)
        assert "family" in data, f"Missing 'family' in {jf.name}"
        assert "vendor" in data, f"Missing 'vendor' in {jf.name}"
        assert "flash_address" in data, f"Missing 'flash_address' in {jf.name}"


def test_pinouts_parse():
    """Every pinout JSON file must be valid JSON."""
    pinouts_dir = PLUGIN_ROOT / "knowledge" / "pinouts"
    if not pinouts_dir.is_dir():
        pytest.skip("No pinouts directory — pinouts are optional.")
    for jf in pinouts_dir.glob("*.json"):
        with open(jf) as f:
            data = json.load(f)
        assert "board" in data, f"Missing 'board' in {jf.name}"
        assert "pins" in data, f"Missing 'pins' in {jf.name}"


def test_references_exist():
    """Reference docs declared in the manifest should exist."""
    refs_dir = PLUGIN_ROOT / "knowledge" / "references"
    if not refs_dir.is_dir():
        pytest.skip("No references directory — references are optional.")
    md_files = list(refs_dir.glob("*.md"))
    assert len(md_files) >= 1, "No reference docs found"


def test_examples_exist():
    """The example project should exist and have main.py + tinkr.toml."""
    example = PLUGIN_ROOT / "examples" / "tinkr-led"
    assert example.is_dir(), f"Missing example: {example}"
    assert (example / "main.py").is_file()
    assert (example / "tinkr.toml").is_file()


def test_license_exists():
    """A LICENSE file must be present."""
    license_files = list(PLUGIN_ROOT.glob("LICENSE*"))
    assert len(license_files) >= 1, "Missing LICENSE file"


def test_readme_exists():
    """A README.md must be present."""
    assert (PLUGIN_ROOT / "README.md").is_file()


def test_changelog_exists():
    """A CHANGELOG.md must be present."""
    assert (PLUGIN_ROOT / "CHANGELOG.md").is_file()
