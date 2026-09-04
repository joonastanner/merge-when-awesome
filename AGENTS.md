# Repository guidance

This repository root is the portable `merge-when-awesome` Agent Skill. It must remain installable as one self-contained directory.

## Change discipline

- Preserve the explicit activation gate. Loading or reviewing the skill must never imply permission to edit, push, resolve feedback, arm auto-merge, or merge.
- Preserve exact-source-commit protection, risk lanes, review-independence requirements, the bounded convergence loop, and honest capability degradation.
- Keep shared behavior provider-neutral and agent-neutral. Put optional host metadata under `agents/` and provider-specific guidance in references.
- Keep `SKILL.md` focused on executable decisions. Put detailed policy, evals, and examples in linked references.
- Never add credentials, cookies, tokens, private repository data, or machine-specific paths.
- Scripts must use standard tools, validate targets before writing, and refuse destructive overwrites.

## Validation

Before committing, run:

```bash
python3 scripts/validate.py
bash -n install.sh tests/test_install.sh
bash tests/test_install.sh
python3 tests/test_portable_copy.py
```

Update the relevant scenarios under `references/` whenever workflow behavior or safety policy changes.
