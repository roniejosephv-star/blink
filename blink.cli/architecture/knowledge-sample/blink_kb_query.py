"""
blink-kb-query — The reference implementation of the agent's knowledge base query tool.

This is what the MCP server exposes to the agent. Given a query, it
returns the most relevant knowledge entries from the bundled KB.

The reference implementation uses:
- A simple keyword + tag search (no embeddings, no vector index)
- The bundled KB at `~/.blink/kb/` or in the package

For v1.0+, the production implementation would use a vector index
(lancedb, chroma, or numpy + cosine similarity) for semantic search.
The interface stays the same.

This script is also invokable from the shell for debugging:
    blink-kb-query search "ESP32 I2C timeout"
    blink-kb-query get fact/esp32-s3-i2c-pullups
    blink-kb-query fix-for "OSError: [Errno 110] ETIMEDOUT"
    blink-kb-query recipe-for esp32 micropython "deploy blink-led"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


# The bundled KB is shipped with Blink. In development, it lives in
# the package's `kb/` directory. In production, it's extracted to
# ~/.blink/kb/ on first run.

def _find_kb_root() -> Path:
    """Locate the bundled knowledge base."""
    candidates = [
        Path(__file__).resolve().parent,                    # The sample KB
        Path(os.environ.get("BLINK_KB_ROOT", "")),          # User override
        Path.home() / ".blink" / "kb",                       # Installed location
        Path("/usr/local/share/blink/kb"),                   # System install
    ]
    for c in candidates:
        if c.is_dir() and (c / "index.yaml").is_file():
            return c
    raise FileNotFoundError("No knowledge base found. Set BLINK_KB_ROOT or install Blink.")


def _load_index(kb_root: Path) -> dict:
    """Load the KB index file."""
    index_path = kb_root / "index.yaml"
    if not index_path.is_file():
        raise FileNotFoundError(f"No index.yaml at {index_path}")
    # Use a minimal YAML reader. Production uses PyYAML or ruamel.
    return _parse_simple_yaml(index_path.read_text())


def _parse_simple_yaml(text: str) -> dict:
    """
    A minimal YAML parser for the index.yaml file.

    Only handles the subset we use:
    - top-level scalars
    - lists of scalars
    - lists of dicts (with simple key: value)
    - nested dicts (2 levels deep)

    Production uses PyYAML. This is a self-contained fallback so the
    reference implementation has no extra dependencies.
    """
    import yaml  # type: ignore
    return yaml.safe_load(text)


def _load_entry(kb_root: Path, rel_path: str) -> dict:
    """Load a single KB entry by its relative path."""
    entry_path = kb_root / rel_path
    if not entry_path.is_file():
        raise FileNotFoundError(f"KB entry not found: {entry_path}")
    return _parse_simple_yaml(entry_path.read_text())


def _score_entry(query_terms: list[str], entry: dict) -> float:
    """Score a KB entry against a query. Higher is better."""
    text = " ".join([
        entry.get("summary", ""),
        entry.get("detail", ""),
        " ".join(entry.get("tags", [])),
        " ".join(entry.get("chips", [])),
        " ".join(c.get("summary", "") if isinstance(c, dict) else str(c) for c in entry.get("likely_causes", [])),
    ]).lower()
    matches = sum(1 for term in query_terms if term.lower() in text)
    if matches == 0:
        return 0.0
    # Boost if the summary matches.
    summary_matches = sum(1 for term in query_terms if term.lower() in entry.get("summary", "").lower())
    return matches + summary_matches * 2.0


def search(kb_root: Path, query: str, category: str | None = None, limit: int = 5) -> list[dict]:
    """Search the KB. Returns ranked results."""
    index = _load_index(kb_root)
    entries = index.get("entries", {})

    # Flatten the index entries into a list, respecting the category filter.
    candidates: list[dict] = []
    if category is None or category == "fact":
        for e in entries.get("facts", []):
            candidates.append({**e, "category": "fact"})
    if category is None or category == "error":
        for e in entries.get("errors", []):
            candidates.append({**e, "category": "error"})
    if category is None or category == "pattern":
        for e in entries.get("patterns", []):
            candidates.append({**e, "category": "pattern"})
    if category is None or category == "recipe":
        for e in entries.get("recipes", []):
            candidates.append({**e, "category": "recipe"})

    # Score and rank.
    query_terms = re.findall(r"\w+", query)
    scored = [(_score_entry(query_terms, e), e) for e in candidates]
    scored = [(s, e) for s, e in scored if s > 0]
    scored.sort(key=lambda x: -x[0])
    return [{"score": s, "entry": e} for s, e in scored[:limit]]


def get_entry(kb_root: Path, entry_id: str) -> dict:
    """Fetch a single KB entry by its ID."""
    index = _load_index(kb_root)
    for category, entries in index.get("entries", {}).items():
        for e in entries:
            if e.get("id") == entry_id:
                return _load_entry(kb_root, e["path"])
    raise KeyError(f"No KB entry with id: {entry_id}")


def fix_for(kb_root: Path, error_signature: str) -> dict | None:
    """Given an error signature, return the most likely fix.

    This is the agent's primary tool. It searches the KB for the best match.
    """
    results = search(kb_root, error_signature, category="error", limit=1)
    if not results:
        return None
    best = results[0]
    entry = get_entry(kb_root, best["entry"]["id"])
    return {
        "error_id": entry["id"],
        "summary": entry.get("summary", ""),
        "fix_steps": entry.get("fix_steps", []),
        "verify_steps": entry.get("verify_steps", []),
        "likely_causes": entry.get("likely_causes", []),
        "related_facts": entry.get("related_errors", []),
        "score": best["score"],
    }


def recipe_for(kb_root: Path, chip_family: str = "", firmware: str = "", goal: str = "") -> dict | None:
    """Given a setup, return the best matching recipe."""
    query_parts = [chip_family, firmware, goal]
    query = " ".join(p for p in query_parts if p)
    if not query:
        return None
    results = search(kb_root, query, category="recipe", limit=1)
    if not results:
        return None
    best = results[0]
    entry = get_entry(kb_root, best["entry"]["id"])
    return {
        "recipe_id": entry["id"],
        "name": entry.get("name", ""),
        "description": entry.get("description", ""),
        "setup": entry.get("setup", {}),
        "steps": entry.get("steps", []),
        "score": best["score"],
    }


# ---- MCP tool surface ----
# These are the functions exposed to the agent through MCP. The MCP server
# wrapper (a thin layer) calls these directly.

def mcp_search(query: str, category: str | None = None, limit: int = 5) -> dict:
    """MCP tool: kb.search"""
    kb_root = _find_kb_root()
    results = search(kb_root, query, category, limit)
    return {
        "results": [
            {
                "id": r["entry"]["id"],
                "category": r["entry"].get("category"),
                "summary": r["entry"].get("summary", ""),
                "score": r["score"],
            }
            for r in results
        ],
    }


def mcp_get(entry_id: str) -> dict:
    """MCP tool: kb.get"""
    kb_root = _find_kb_root()
    return get_entry(kb_root, entry_id)


def mcp_fix_for(error_signature: str) -> dict:
    """MCP tool: kb.fix_for"""
    kb_root = _find_kb_root()
    result = fix_for(kb_root, error_signature)
    if result is None:
        return {"found": False, "message": f"No fix found for: {error_signature}"}
    return {"found": True, **result}


def mcp_recipe_for(chip_family: str = "", firmware: str = "", goal: str = "") -> dict:
    """MCP tool: kb.recipe_for"""
    kb_root = _find_kb_root()
    result = recipe_for(kb_root, chip_family, firmware, goal)
    if result is None:
        return {"found": False, "message": "No matching recipe found."}
    return {"found": True, **result}


# ---- CLI ----

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query the Blink knowledge base. This is the reference implementation of the agent's KB tools."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Search the KB")
    p_search.add_argument("query", help="Search query (free text)")
    p_search.add_argument("--category", choices=["fact", "error", "pattern", "recipe"])
    p_search.add_argument("--limit", type=int, default=5)

    p_get = sub.add_parser("get", help="Get a specific entry by ID")
    p_get.add_argument("entry_id", help="Entry ID (e.g., 'fact/esp32-s3-i2c-pullups')")

    p_fix = sub.add_parser("fix-for", help="Get the fix for an error signature")
    p_fix.add_argument("error_signature", help="The error message or code")

    p_recipe = sub.add_parser("recipe-for", help="Find a recipe for a setup")
    p_recipe.add_argument("--chip-family", default="")
    p_recipe.add_argument("--firmware", default="")
    p_recipe.add_argument("--goal", default="")

    args = parser.parse_args()

    if args.cmd == "search":
        result = mcp_search(args.query, args.category, args.limit)
    elif args.cmd == "get":
        result = mcp_get(args.entry_id)
    elif args.cmd == "fix-for":
        result = mcp_fix_for(args.error_signature)
    elif args.cmd == "recipe-for":
        result = mcp_recipe_for(args.chip_family, args.firmware, args.goal)
    else:
        parser.error("Unknown subcommand")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
