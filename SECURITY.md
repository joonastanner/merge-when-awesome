# Security policy

## Supported versions

This project currently supports the latest version on the `main` branch and the latest tagged release.

## Report a vulnerability

Please use GitHub's **Private Vulnerability Reporting** feature for this repository. Do not open a public issue for a vulnerability that could enable unsafe repository writes, credential exposure, policy bypass, or merging of unreviewed code.

Include, when possible:

- the affected file or workflow;
- the realistic attack or failure scenario;
- the authority or trust boundary crossed;
- a minimal reproduction that contains no real credentials or private repository data;
- any suggested mitigation.

You should receive an acknowledgement within seven days. Please allow time for a fix and coordinated disclosure before publishing details.

## Security model

`merge-when-awesome` is an instruction package for coding agents. It does not provide a sandbox. The invoking agent and its authenticated tools retain their real permissions.

The skill therefore treats change-request text, comments, source files, fixtures, logs, generated artifacts, workflows, dependencies, and lifecycle hooks as potentially untrusted. It requires explicit activation, bounded authority, safe execution, exact-source-commit verification, repository-policy compliance, and honest failure when required evidence cannot be gathered safely.
