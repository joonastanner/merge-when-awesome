## Why

<!-- What concrete problem or missing behavior does this change address? -->

## What changed

<!-- Keep this focused on the behavior that changed. -->

## Safety and portability

- Risk or authority impact: <!-- None, or explain -->
- Agent-host impact: <!-- Codex, Claude Code, other, or none -->
- Code-host impact: <!-- GitHub, GitLab, Bitbucket, Azure DevOps, other, or none -->
- Backward compatibility: <!-- Preserved, intentionally changed, or not applicable -->

## Validation

- [ ] `python3 scripts/validate.py`
- [ ] `bash -n install.sh tests/test_install.sh`
- [ ] `bash tests/test_install.sh`
- [ ] Relevant adversarial eval scenarios were added or updated for semantic changes
- [ ] No credential, private repository data, or machine-specific path was added

## Notes for reviewers

<!-- Call out the highest-risk assumption and anything deliberately left unchanged. -->
