# Platform Portability

## Contents

- Portable core
- Agent host installation and invocation
- Code-host capability mapping
- Capability degradation
- Standalone repository and embedding

## Portable core

`merge-when-awesome` uses the open Agent Skills directory shape:

```text
merge-when-awesome/
├── SKILL.md
├── README.md
├── LICENSE
├── install.sh
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
├── templates/
└── tests/
```

`SKILL.md`, `references/`, `scripts/`, and `templates/` are the portable core. `agents/openai.yaml` is optional OpenAI host metadata. Other coding agents may ignore it.

Keep the shared `SKILL.md` frontmatter limited to fields from the Agent Skills specification. Host-specific safety must supplement the core, not fork its workflow.

The core activation gate is authoritative on every host: loading the skill implicitly does not grant write, push, thread-resolution, auto-merge, or merge authority.

## Agent host installation and invocation

### Codex

User scope:

```text
~/.agents/skills/merge-when-awesome/
```

Repository scope:

```text
<repo>/.agents/skills/merge-when-awesome/
```

Invoke explicitly:

```text
$merge-when-awesome Improve the current pull request and merge it when every gate passes.
```

`agents/openai.yaml` sets `allow_implicit_invocation: false` for OpenAI hosts that support that metadata.

### Claude Code

User scope:

```text
~/.claude/skills/merge-when-awesome/
```

Repository scope:

```text
<repo>/.claude/skills/merge-when-awesome/
```

Invoke explicitly:

```text
/merge-when-awesome Improve the current pull request and merge it when every gate passes.
```

The shared skill intentionally does not add Claude-only frontmatter because strict Agent Skills packagers may reject non-standard fields. Claude Code may still discover the skill from its description, so the activation gate in `SKILL.md` must remain explicit and early.

### Other Agent Skills-compatible coding agents

Copy or symlink the whole skill directory into the host's documented skills location. Invoke it by name and provide authenticated repository and code-host access. Do not assume that optional OpenAI metadata or Claude-specific command syntax is portable.

## Code-host capability mapping

Use provider-native names internally, but map them to these common concepts:

| Common concept | GitHub | GitLab | Bitbucket | Azure DevOps |
|---|---|---|---|---|
| Change request | Pull request | Merge request | Pull request | Pull request |
| Source identity | Head SHA | Source commit SHA | Source commit | Last source commit |
| Target identity | Base branch and SHA | Target branch and SHA | Destination branch and commit | Target branch and commit |
| Validation | Checks and workflow runs | Pipelines and jobs | Build statuses and pipelines | Policies and build validations |
| Human gate | Reviews and code owners | Approvals and approval rules | Approvals and default reviewers | Reviewers and branch policies |
| Deferred merge | Auto-merge or merge queue | Merge when pipeline succeeds or merge train | Merge checks and automation | Auto-complete |

This table is conceptual, not a promise that every connected tool exposes every operation.

For any provider, the agent must be able to:

1. identify the exact change request and source commit;
2. read the full diff and discussion;
3. inspect unresolved feedback and mechanical gates;
4. modify and push the source branch safely;
5. refresh the source commit immediately before merge;
6. use a provider-supported merge action without bypassing policy;
7. confirm the target branch contains the reviewed change afterward.

## Capability degradation

Do not fabricate missing platform capabilities.

- **Read access only:** Perform no write action. Return `BLOCKED` and state the missing branch-write capability.
- **Branch write but no discussion API:** Improve and push. Preserve an evidence report in the change description when possible. Do not claim threads were answered or resolved.
- **Branch write but no merge API:** Complete every other gate and return `READY FOR OWNER MERGE`.
- **No expected-head guard:** Refresh the source commit immediately before merge and stop on any movement. State that atomic head protection was unavailable.
- **No auto-merge support:** Return `READY FOR OWNER MERGE` when only external gates remain.
- **No fresh review context:** A separated same-agent adversarial pass may support green-risk merge only. Yellow and red work stop for an owner unless the required independence becomes available.
- **No target-branch status visibility:** Confirm the provider's merged state and target reachability, then disclose post-merge CI as `NOT RUN`.
- **Provider terminology or semantics are unclear:** Consult official provider documentation or stop. Do not guess destructive or merge behavior.

## Standalone repository and embedding

This repository root is the complete skill directory. It must remain movable and installable without a containing monorepo, package manager, generated wrapper, or private configuration.

To embed the skill in another repository or distribution:

1. copy or symlink the complete repository root into the agent host's documented skill location;
2. retain `SKILL.md`, `LICENSE`, references, templates, and the standalone validator;
3. keep `agents/openai.yaml` as optional host metadata;
4. add provider-specific adapters only as separate optional material, not as assumptions in the core workflow;
5. run:

```bash
python3 scripts/validate.py
```

6. test at least one safe fixture in every claimed agent host;
7. test capability degradation with read-only access, a moving source commit, a draft hold, and unavailable merge tooling.

No portable skill file may depend on a containing-repository name, path, secret, validator, or release system. Public repository maintenance files may describe this project, but the installed workflow must remain self-contained.
