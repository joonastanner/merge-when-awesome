#!/usr/bin/env python3
"""Validate the portable merge-when-awesome Agent Skill."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "metadata",
    "allowed-tools",
}
REQUIRED_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "install.sh",
    "tests/test_install.sh",
    "tests/test_portable_copy.py",
    ".github/workflows/validate.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/idea.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "agents/openai.yaml",
    "references/awesome-contract.md",
    "references/evidence-and-convergence.md",
    "references/evals.md",
    "references/platform-portability.md",
    "references/review-lenses.md",
    "references/risk-and-merge-policy.md",
    "references/ui-experience-evals.md",
    "references/ui-experience-gate.md",
    "scripts/validate.py",
    "templates/AWESOME_REPORT.md",
}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_frontmatter(path: Path, result: Validation) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        result.error(f"{path}: missing YAML frontmatter on the first line")
        return {}, text

    values: dict[str, str] = {}
    current_key: str | None = None
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[0].isspace():
            if current_key != "metadata":
                result.error(f"{path}: unexpected nested frontmatter line: {raw_line!r}")
            continue
        if ":" not in raw_line:
            result.error(f"{path}: invalid frontmatter line: {raw_line!r}")
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        current_key = key
        values[key] = value.strip().strip('"').strip("'")

    unknown = sorted(set(values) - ALLOWED_FRONTMATTER)
    if unknown:
        result.error(
            f"{path}: non-portable frontmatter fields: {', '.join(unknown)}"
        )
    return values, text[match.end() :]


def validate_frontmatter(path: Path, result: Validation) -> None:
    values, body = parse_frontmatter(path, result)
    name = values.get("name", "")
    description = values.get("description", "")
    license_name = values.get("license", "")

    if name != SKILL_ROOT.name:
        result.error(
            f"{path}: name {name!r} must match directory {SKILL_ROOT.name!r}"
        )
    if not NAME_RE.fullmatch(name):
        result.error(f"{path}: invalid Agent Skills name {name!r}")
    if not 1 <= len(name) <= 64:
        result.error(f"{path}: name must be 1 to 64 characters")
    if not 80 <= len(description) <= 1024:
        result.error(f"{path}: description must be 80 to 1024 characters")
    if "use only when" not in description.lower():
        result.error(f"{path}: description must state the explicit activation boundary")
    if license_name != "MIT":
        result.error(f"{path}: license must be MIT")
    if len(body.splitlines()) > 500:
        result.error(f"{path}: body exceeds the 500-line portability budget")


def validate_links(path: Path, result: Validation) -> None:
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_RE.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        candidate = (path.parent / target).resolve()
        try:
            candidate.relative_to(SKILL_ROOT.resolve())
        except ValueError:
            result.error(f"{path}: relative link escapes the skill folder: {raw_target}")
            continue
        if not candidate.exists():
            result.error(f"{path}: broken relative link: {raw_target}")


def require(path: Path, fragment: str, result: Validation) -> None:
    if not path.is_file():
        result.error(f"missing required file: {path}")
        return
    if fragment not in path.read_text(encoding="utf-8"):
        result.error(f"{path}: missing required invariant {fragment!r}")


def validate_text_hygiene(path: Path, result: Validation) -> None:
    text = path.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), start=1):
        if line != line.rstrip():
            result.error(f"{path}:{number}: trailing whitespace")
    if "\u2013" in text or "\u2014" in text:
        result.error(f"{path}: contains an en dash or em dash")
    containing_brand = "lucky" + "dreamer"
    if containing_brand in text.lower():
        result.error(f"{path}: contains a containing-repository brand dependency")
    if re.search(r"(?i)(api[_-]?key|token|password)\s*[:=]\s*[^<\s]", text):
        result.warn(f"{path}: inspect possible credential-like example")


def main() -> int:
    result = Validation()

    for relative in sorted(REQUIRED_FILES):
        path = SKILL_ROOT / relative
        if not path.is_file():
            result.error(f"missing required file: {path}")

    skill_md = SKILL_ROOT / "SKILL.md"
    if skill_md.is_file():
        validate_frontmatter(skill_md, result)

    for path in SKILL_ROOT.rglob("*.md"):
        validate_links(path, result)
        validate_text_hygiene(path, result)

    for pattern in ("*.yaml", "*.yml", "*.sh"):
        for path in SKILL_ROOT.rglob(pattern):
            validate_text_hygiene(path, result)

    for relative in ("install.sh", "tests/test_install.sh"):
        path = SKILL_ROOT / relative
        if path.is_file() and not os.access(path, os.X_OK):
            result.error(f"{path}: executable bit is required")

    require(skill_md, "## Activation gate", result)
    require(skill_md, "$merge-when-awesome", result)
    require(skill_md, "/merge-when-awesome", result)
    require(skill_md, "potentially untrusted data, not instructions", result)
    require(skill_md, "expected-head or equivalent compare-and-swap guard", result)
    require(skill_md, "READY FOR OWNER MERGE", result)
    require(skill_md, "Standard mode allows at most three implementation rounds", result)
    require(skill_md, "UI surface: YES", result)
    require(skill_md, "UI GATE PASS", result)
    require(skill_md, "references/ui-experience-gate.md", result)

    readme = SKILL_ROOT / "README.md"
    require(readme, "$HOME/.agents/skills/merge-when-awesome", result)
    require(readme, "$HOME/.claude/skills/merge-when-awesome", result)
    require(readme, "Green is a gate, not a verdict", result)
    require(readme, "./install.sh --platform all", result)
    require(readme, "python3 scripts/validate.py", result)
    require(readme, "UI GATE PASS", result)
    require(readme, "references/ui-experience-gate.md", result)
    require(readme, "references/ui-experience-evals.md", result)

    contract = SKILL_ROOT / "references" / "awesome-contract.md"
    require(contract, "### UI surface", result)
    require(contract, "UI surface: YES", result)
    require(contract, "ui-experience-gate.md", result)

    review_lenses = SKILL_ROOT / "references" / "review-lenses.md"
    require(review_lenses, "## Mandatory UI experience gate", result)
    require(review_lenses, "UI GATE PASS", result)
    require(review_lenses, "ui-experience-gate.md", result)

    ui_gate = SKILL_ROOT / "references" / "ui-experience-gate.md"
    require(ui_gate, "## Specialist composition", result)
    require(ui_gate, "UI surface: YES", result)
    require(ui_gate, "UI GATE PASS", result)
    require(ui_gate, "UI GATE BLOCKED", result)
    require(ui_gate, "A passing automated scan is not sufficient", result)
    require(ui_gate, "Missing specialist tooling does not waive the gate", result)
    require(ui_gate, "Plain documentation", result)
    require(ui_gate, "terminal UI", result)

    ui_evals = SKILL_ROOT / "references" / "ui-experience-evals.md"
    require(ui_evals, "Indirect backend UI change", result)
    require(ui_evals, "Automated scan passes, live update is silent", result)
    require(ui_evals, "No visual runtime available", result)

    portability = SKILL_ROOT / "references" / "platform-portability.md"
    require(portability, "## Capability degradation", result)
    require(portability, "## Standalone repository and embedding", result)
    require(portability, "GitLab", result)

    installer = SKILL_ROOT / "install.sh"
    require(installer, "--platform codex|claude|all", result)
    require(installer, "--project PATH", result)
    require(installer, "--dry-run", result)
    require(installer, "refusing to overwrite non-symlink path", result)
    require(installer, "Preflight every destination", result)

    installer_tests = SKILL_ROOT / "tests" / "test_install.sh"
    require(installer_tests, "dry run created Codex destination", result)
    require(installer_tests, "preflight allowed a partial all-platform install", result)
    require(installer_tests, "Installer integration tests passed", result)

    portable_copy_test = SKILL_ROOT / "tests" / "test_portable_copy.py"
    require(portable_copy_test, "shutil.copytree", result)
    require(portable_copy_test, "Portable copy validation passed", result)

    workflow = SKILL_ROOT / ".github" / "workflows" / "validate.yml"
    require(workflow, "actions/checkout@v7", result)
    require(workflow, "actions/setup-python@v7", result)
    require(workflow, "bash tests/test_install.sh", result)
    require(workflow, "python3 tests/test_portable_copy.py", result)

    license_file = SKILL_ROOT / "LICENSE"
    require(license_file, "MIT License", result)
    require(license_file, "Copyright (c) 2026 Joonas Tanner", result)

    risk = SKILL_ROOT / "references" / "risk-and-merge-policy.md"
    require(risk, "Yellow work may merge autonomously only", result)
    require(risk, "No merge API", result)
    require(risk, "compare-and-swap guard", result)
    require(risk, "final source commit has a current `UI GATE PASS`", result)
    require(risk, "Do not waive the UI gate", result)

    evidence = SKILL_ROOT / "references" / "evidence-and-convergence.md"
    require(evidence, "## Agent skills and coding automation", result)
    require(evidence, "## Mandatory UI experience evidence", result)
    require(evidence, "UI GATE PASS", result)
    require(evidence, "NOT RUN", result)

    report = SKILL_ROOT / "templates" / "AWESOME_REPORT.md"
    require(report, "**UI surface:**", result)
    require(report, "**UI gate:**", result)
    require(report, "### UI experience", result)

    openai_yaml = SKILL_ROOT / "agents" / "openai.yaml"
    require(openai_yaml, "allow_implicit_invocation: false", result)
    require(openai_yaml, "$merge-when-awesome", result)
    require(openai_yaml, "UI experience gate", result)

    for path in (SKILL_ROOT / "references").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if len(text.splitlines()) > 100 and "## Contents" not in text[:700]:
            result.error(f"{path}: long reference is missing an early Contents section")

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    if result.errors:
        print(f"Validation failed with {len(result.errors)} error(s).")
        return 1

    print(
        "Portable merge-when-awesome validation passed"
        f" with {len(result.warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
