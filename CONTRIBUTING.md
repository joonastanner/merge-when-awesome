# Contributing

Thank you for helping make `merge-when-awesome` safer, sharper, and more portable.

## Before opening a change

Please search existing issues and pull requests first. For a material workflow change, open an issue describing:

- the failure mode or missing capability;
- a realistic example change request;
- the smallest behavior change that would address it;
- any effect on permissions, merge safety, portability, or convergence.

Security vulnerabilities belong in GitHub Private Vulnerability Reporting, not a public issue. See [SECURITY.md](SECURITY.md).

## Design principles

Contributions should preserve these invariants:

1. **Intent before implementation.** Quality is judged against accepted outcomes, not the current diff alone.
2. **Evidence before confidence.** A claim needs proof capable of exposing the relevant defect.
3. **Material issues before nits.** The workflow must converge instead of manufacturing endless work.
4. **Authority stays explicit.** Review, edit, push, feedback resolution, merge, and deployment are distinct permissions.
5. **The reviewed commit is the merged commit.** Source movement invalidates stale evidence.
6. **Missing capability lowers authority, not quality.** The skill stops or hands off honestly.
7. **Portable core first.** Host and provider integrations supplement the shared Agent Skill rather than forking it.

## Development

Fork the repository, create a focused branch, and make the smallest coherent change. The project has no runtime dependencies.

Run all checks:

```bash
python3 scripts/validate.py
bash -n install.sh tests/test_install.sh
bash tests/test_install.sh
python3 tests/test_portable_copy.py
```

If you change workflow semantics, add or update a realistic adversarial case in:

- [references/evals.md](references/evals.md) for general behavior, authority, portability, or convergence;
- [references/ui-experience-evals.md](references/ui-experience-evals.md) for UI routing, runtime proof, accessibility, or visual quality.

Avoid tests that only assert exact prose when a semantic invariant can be checked instead.

## Pull requests

Keep pull requests reviewable and explain:

- the concrete problem and intended behavior;
- safety or authority implications;
- portability implications for Codex, Claude Code, and code hosts;
- validation performed;
- any behavior deliberately left unchanged.

By contributing, you agree that your contributions are licensed under the repository's [MIT License](LICENSE).
