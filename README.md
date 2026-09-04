<div align="center">

# Merge When Awesome

### A quality ratchet for AI coding agents

Take a pull request beyond “green” to the best defensible version of what it was meant to be.

[![Validate](https://github.com/joonastanner/merge-when-awesome/actions/workflows/validate.yml/badge.svg)](https://github.com/joonastanner/merge-when-awesome/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-4f46e5)](https://agentskills.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-f4c430.svg)](LICENSE)

</div>

**Green is a gate, not a verdict.**

Auto-merge tools wait for checks. Review bots leave comments. `merge-when-awesome` gives a coding agent a different job: understand the accepted intent, find and fix material weaknesses, prove the real behavior, challenge the result with fresh review, and merge only when the exact reviewed commit is genuinely worth shipping.

It is a portable [Agent Skill](https://agentskills.io/specification) for Codex, Claude Code, and other compatible coding agents. It is not a hosted service, GitHub App, or replacement for repository policy.

> [!IMPORTANT]
> This skill can edit code, push commits, resolve objectively addressed feedback, arm auto-merge, and merge. It is intentionally explicit-only. Review the [authority and risk model](#safety-and-authority) before using it.

## The idea

“Merge when ready” asks whether a change is mechanically allowed to merge.

“Merge when awesome” asks:

> Is this the version we should ship?

The answer is grounded in a temporary **Awesome Contract**: accepted intent, observable acceptance criteria, owner locks, scope, non-goals, UI impact, risk, required evidence, and merge authority. “Awesome” is therefore demanding without becoming subjective or endless.

The workflow is deliberately bounded:

1. **Define:** resolve intent and capture a truthful baseline.
2. **Challenge:** review adversarially and fix verified material issues.
3. **Prove:** test the behavior at the boundary that actually matters.
4. **Converge:** repeat only while material issues remain and the round limit allows it.
5. **Protect:** verify the exact source commit and every repository gate, then merge, arm auto-merge, or stop safely.

## What makes it different

- **Owns improvement, not just commentary.** It fixes verified blockers and material weaknesses instead of stopping at a review report.
- **Defines quality from intent.** The Awesome Contract prevents both shallow approval and unrelated gold-plating.
- **Treats UI quality as a real gate.** Interface-affecting work requires runtime UX, visual, responsive, and accessibility proof, not just screenshots or component tests.
- **Uses evidence that could fail.** Green CI is useful, but runtime behavior, migration safety, compatibility, performance, and test integrity are proven at the boundary that matters.
- **Requires adversarial review.** The strongest available fresh read-only context challenges the final implementation.
- **Converges deliberately.** Standard mode permits three implementation rounds; explicit `deep` mode permits five. Nits and subjective polish do not restart the loop.
- **Protects the reviewed commit.** Expected-head or equivalent compare-and-swap checks prevent an unreviewed source update from slipping into the merge.
- **Degrades honestly.** Missing merge access, runtime proof, specialist review, or provider capability produces a bounded owner handoff or blocker, never simulated success.

## Quick start

Clone the repository:

```bash
git clone https://github.com/joonastanner/merge-when-awesome.git
cd merge-when-awesome
```

Install for Codex:

```bash
./install.sh --platform codex
```

Install for Claude Code:

```bash
./install.sh --platform claude
```

Install for both:

```bash
./install.sh --platform all
```

The installer creates a symlink to this checkout, refuses to overwrite a real file or directory, preflights every destination before writing, and is safe to rerun. Preview any operation with `--dry-run`.

To install only for one repository:

```bash
./install.sh --platform all --project /absolute/path/to/project
```

Start a new agent session after first installation so the skill is discovered reliably.

### Manual installation

The repository root is the skill directory. Copy or symlink the whole repository, not only `SKILL.md`.

| Host | User scope | Project scope | Invocation |
|---|---|---|---|
| Codex | `$HOME/.agents/skills/merge-when-awesome` | `.agents/skills/merge-when-awesome` | `$merge-when-awesome` |
| Claude Code | `$HOME/.claude/skills/merge-when-awesome` | `.claude/skills/merge-when-awesome` | `/merge-when-awesome` |

Other Agent Skills-compatible hosts can use their documented skill directory. Host-specific metadata under `agents/` is optional; the workflow itself remains portable.

## Use it

Codex:

```text
$merge-when-awesome Take the current pull request through adversarial review,
fix every verified material weakness, prove the real behavior, and merge it
only when the exact reviewed head passes every gate.
```

Claude Code:

```text
/merge-when-awesome Take merge request 42 through final quality, apply the UI
experience gate if any interface is affected, and merge when every gate passes.
```

For unusually complex but still bounded work:

```text
$merge-when-awesome deep Take PR 123 through at most five justified improvement
rounds. Preserve accepted scope and stop rather than guessing when owner judgment
is required.
```

The skill begins by resolving the exact change request, repository policy, source and target commits, discussion, checks, risk, and available host capabilities. If those cannot be identified safely, it does not edit.

## Outcomes

Every run begins its final response with exactly one status:

| Status | Meaning |
|---|---|
| `MERGED` | The provider confirms the reviewed change is merged and the target contains it. |
| `AUTO-MERGE ARMED` | The change has converged; only trusted external gates or a queue remain. |
| `READY FOR OWNER MERGE` | The implementation is ready, but authority, independence, or provider capability requires an owner. |
| `BLOCKED` | A material issue, missing decision, unsafe proof path, or unavailable required gate prevents convergence. |

There is no numeric awesomeness score. The standard is current evidence, a clean material review, and every applicable repository and safety gate.

## UI Experience Gate

Any change that can alter an interactive user or operator experience records `UI surface: YES`. That includes indirect backend, flag, permission, localization, or data-shape changes that affect rendered behavior.

The gate covers:

- the real end-to-end journey and materially different states;
- mobile, tablet, desktop, native, game, or terminal dimensions as applicable;
- keyboard, touch, pointer, gesture, and assistive behavior;
- screen-reader semantics and dynamic feedback;
- text scaling, zoom, contrast, non-color communication, and reduced motion;
- hierarchy, copy, spacing, typography, affordances, feedback, and visual coherence;
- clipping, overflow, layout instability, console errors, failed requests, and stale state.

The skill composes the smallest compatible UI/UX or accessibility specialist available. When no specialist exists, it uses its embedded hostile UI lens. Missing tooling never waives the gate, and the final source commit must earn `UI GATE PASS` before an interface-affecting change can converge. See [the UI Experience Gate](references/ui-experience-gate.md).

## Safety and authority

Explicit invocation grants bounded authority to improve and merge the identified change request. It does **not** authorize force-pushes, history rewrites, branch-protection bypasses, administrator overrides, production deployment, secret changes, live-data mutation, source-branch deletion, or manufactured green checks.

Risk controls are intentionally asymmetric:

- **Green:** Local, reversible changes may merge after all gates pass. A disclosed same-agent adversarial pass is the last-resort independence floor.
- **Yellow:** User-visible behavior, public contracts, concurrency, meaningful dependencies, or infrastructure require stronger targeted evidence and a fresh independent review for autonomous merge.
- **Red:** Authentication, payments, destructive migrations, privacy, secrets, production data, signing, or broad infrastructure stop for exact additional merge authorization and required human gates.

An agent review never counts as a repository-required human, code-owner, security, compliance, design, or accessibility approval. Read the full [risk and merge policy](references/risk-and-merge-policy.md).

## Code-host portability

The core language maps to GitHub pull requests, GitLab merge requests, Bitbucket pull requests, Azure DevOps pull requests, and equivalent source-branch review proposals. Actual capabilities depend on the authenticated tools available to the agent.

When a provider feature is absent, the skill chooses a truthful fallback. For example, branch write access without a merge API can still produce `READY FOR OWNER MERGE`; it cannot produce `MERGED`. See [platform portability](references/platform-portability.md).

## Requirements

- `git`;
- Python 3.9 or newer for the dependency-free validator;
- authenticated access to the code host and writable source branch;
- read access to the full change request, discussion, approvals, and checks or pipelines;
- the build, test, and runtime tools required by the target repository;
- a coding agent capable of reading Agent Skills and operating the repository safely.

## Repository layout

```text
merge-when-awesome/
├── SKILL.md                         Executable skill contract
├── agents/openai.yaml               Optional Codex interface metadata
├── references/                      Deep guidance and adversarial evals
├── scripts/validate.py              Dependency-free package validator
├── templates/AWESOME_REPORT.md      Managed PR evidence section
├── install.sh                       Safe Codex and Claude Code installer
├── tests/test_install.sh            Installer integration tests
└── .github/                         CI and contribution templates
```

## Develop and validate

No package installation is required:

```bash
python3 scripts/validate.py
bash -n install.sh tests/test_install.sh
bash tests/test_install.sh
python3 tests/test_portable_copy.py
```

Changes to workflow semantics should update the relevant adversarial scenarios in [the general eval suite](references/evals.md) or [UI eval suite](references/ui-experience-evals.md). The validator checks structure and safety invariants; it cannot prove that an agent will exercise sound judgment in every repository.

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md), follow the [Code of Conduct](CODE_OF_CONDUCT.md), and report vulnerabilities through [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Joonas Tanner.
