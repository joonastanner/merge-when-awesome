#!/usr/bin/env python3
"""Exercise validation policy resolution without host configuration."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validation_policy.py"


class ValidationPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="merge-policy-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.env = {**os.environ, "XDG_CONFIG_HOME": str(self.root / "config-home")}
        self.env.pop("MERGE_WHEN_AWESOME_CONFIG", None)

    def run_policy(self, *args: str, script: Path = SCRIPT) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *args], env=self.env, text=True, capture_output=True, check=False)

    def test_absent_implicit_config_uses_public_defaults(self) -> None:
        result = self.run_policy()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ci": "standard", "physical_device": "when-relevant", "source": "defaults", "config_path": None})

    def test_implicit_and_explicit_opt_outs(self) -> None:
        implicit = Path(self.env["XDG_CONFIG_HOME"]) / "merge-when-awesome" / "config.json"
        implicit.parent.mkdir(parents=True)
        implicit.write_text(json.dumps({"ci": "local-only", "physical_device": "optional", "managed_by": "luckydreamer-harness"}), encoding="utf-8")
        result = self.run_policy()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ci": "local-only", "physical_device": "optional", "source": "config", "config_path": str(implicit)})

        explicit = self.root / "explicit.json"
        explicit.write_text(json.dumps({"ci": "standard"}), encoding="utf-8")
        self.env["MERGE_WHEN_AWESOME_CONFIG"] = str(implicit)
        result = self.run_policy("--config", str(explicit))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["physical_device"], "when-relevant")
        self.assertEqual(json.loads(result.stdout)["config_path"], str(explicit))

    def test_explicit_missing_and_malformed_fail(self) -> None:
        missing = self.root / "missing.json"
        result = self.run_policy("--config", str(missing))
        self.assertEqual(result.returncode, 2)
        self.assertIn("does not exist", result.stderr)
        self.env["MERGE_WHEN_AWESOME_CONFIG"] = str(missing)
        self.assertEqual(self.run_policy().returncode, 2)

        bad = self.root / "bad.json"
        for content in ('{', '[]', '{"ci":"skip"}', '{"physical_device":null}', '{"extra":true}', '{"ci":[]}'):
            bad.write_text(content, encoding="utf-8")
            result = self.run_policy("--config", str(bad))
            self.assertEqual(result.returncode, 2, content)
            self.assertFalse(result.stdout)

        self.env.pop("MERGE_WHEN_AWESOME_CONFIG", None)
        implicit = Path(self.env["XDG_CONFIG_HOME"]) / "merge-when-awesome" / "config.json"
        implicit.parent.mkdir(parents=True)
        implicit.write_text('{"ci":"disabled"}', encoding="utf-8")
        result = self.run_policy()
        self.assertEqual(result.returncode, 2)
        self.assertIn("ci must be one of", result.stderr)

    def test_portable_folder_uses_bundled_script(self) -> None:
        copied = self.root / "portable-skill"
        (copied / "scripts").mkdir(parents=True)
        shutil.copy2(SCRIPT, copied / "scripts" / "validation_policy.py")
        result = self.run_policy(script=copied / "scripts" / "validation_policy.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["source"], "defaults")


if __name__ == "__main__":
    unittest.main()
