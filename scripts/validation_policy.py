#!/usr/bin/env python3
"""Resolve portable merge-when-awesome validation settings."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULTS = {"ci": "standard", "physical_device": "when-relevant"}
ALLOWED = {
    "ci": {"standard", "local-only"},
    "physical_device": {"when-relevant", "optional"},
}


def resolve(config_arg: str | None, environ: dict[str, str]) -> dict[str, str | None]:
    explicit = config_arg is not None or "MERGE_WHEN_AWESOME_CONFIG" in environ
    selected = config_arg if config_arg is not None else environ.get("MERGE_WHEN_AWESOME_CONFIG")
    if selected is not None and not selected.strip():
        raise ValueError("explicit config path must not be empty")
    if selected is None:
        config_home = environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
        path = Path(config_home).expanduser() / "merge-when-awesome" / "config.json"
    else:
        path = Path(selected).expanduser()
    path = path.absolute()

    if not path.exists():
        if explicit:
            raise ValueError(f"explicit config file does not exist: {path}")
        return {**DEFAULTS, "source": "defaults", "config_path": None}
    if not path.is_file():
        raise ValueError(f"config path is not a regular file: {path}")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON config at {path}: {exc}") from exc
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    unknown = set(config) - {*ALLOWED, "managed_by"}
    if unknown:
        raise ValueError(f"unknown config field(s): {', '.join(sorted(unknown))}")
    if "managed_by" in config and (not isinstance(config["managed_by"], str) or not config["managed_by"].strip()):
        raise ValueError("managed_by must be a non-empty string")
    for field, choices in ALLOWED.items():
        if field in config and (not isinstance(config[field], str) or config[field] not in choices):
            raise ValueError(f"{field} must be one of: {', '.join(sorted(choices))}")
    return {**DEFAULTS, **{field: config[field] for field in ALLOWED if field in config}, "source": "config", "config_path": str(path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="use this config file instead of the environment or default path")
    args = parser.parse_args()
    try:
        policy = resolve(args.config, os.environ)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(policy, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
