# Risk and Merge Policy

## Contents

- Green, yellow, and red risk
- Review independence by risk
- Automatic escalation and prohibitions
- Quality, repository, and safety gates
- Provider capability fallback
- Merge execution, holds, and post-merge failure

Risk determines how much evidence and human authority are required. Classify the highest-risk behavior changed, not the average file in the diff.

## Green risk

Typical examples:

- documentation and copy changes;
- tests that do not alter production behavior;
- narrow internal refactors with strong coverage;
- developer tooling with no production credentials or release impact;
- small bug fixes with local, reversible effects;
- visual polish that changes no sensitive data or business rule.

Green work may merge autonomously after all quality and repository gates pass. A disclosed level 3 same-agent adversarial pass is acceptable only when no fresh context is available.

## Yellow risk

Typical examples:

- user-visible behavior or navigation;
- business logic and state transitions;
- compatible public or cross-service API changes;
- concurrency, caching, retries, background work, or resource management;
- meaningful dependency upgrades;
- performance-sensitive paths;
- mobile lifecycle, offline behavior, or storage;
- infrastructure configuration with bounded, reversible impact;
- feature flags and staged rollout logic.

Yellow work may merge autonomously only after stronger targeted evidence, a fresh specialist review, all repository gates, and a level 1 or 2 independent review. Without that independence, finish at `READY FOR OWNER MERGE`.

## Red risk

Typical examples:

- authentication, authorization, account recovery, permissions, or secrets;
- payments, billing, entitlements, refunds, financial calculations, or purchases;
- destructive or difficult-to-reverse data migrations;
- production database writes, bulk backfills, or deletion;
- privacy, legal, compliance, age-gating, or regulated behavior;
- cryptography or credential handling;
- production infrastructure with broad blast radius;
- release signing, supply-chain trust, or security policy;
- changes that can lock users out, expose private data, or cause material financial harm;
- an unclear rollback path for a high-impact change.

Red work may be improved, tested, committed, pushed, and prepared for merge. It stops at `READY FOR OWNER MERGE` unless the user explicitly authorizes autonomous red-risk merge for this exact change request after the risk has been stated.

Red-risk merge also requires level 1 or 2 independent review and every repository-mandated human gate. Invoking `merge-when-awesome` alone is not red-risk authorization.

## Automatic escalation

Raise the risk lane when any of these appear, even if the description calls the change low risk:

- permission expansion;
- schema or data mutation;
- secret or token handling;
- CI credentials or workflow permission changes;
- new production dependency or executable download;
- reduced validation, coverage, logging, or rollback capability;
- behavior that crosses trust boundaries;
- large rollout or irreversible side effects;
- unclear ownership of an external system.

Never lower the lane merely because checks pass.

## Absolute prohibitions

The skill must never:

- push directly to the target branch;
- bypass branch protection, merge trains, merge queues, required checks, or required approvals;
- use an administrator override to merge;
- dismiss a human review;
- mark disputed feedback resolved without a substantive response;
- force-push or rewrite published history without explicit authorization;
- delete the source branch automatically;
- weaken or skip meaningful tests, lint, type checks, security checks, accessibility checks, or coverage gates to obtain green status;
- hide failures with `|| true`, `continue-on-error`, broad ignores, swallowed exceptions, or equivalent mechanisms;
- expose credentials in logs, prompts, comments, commits, or reports;
- change production secrets, live data, billing state, or account permissions;
- deploy, publish, or roll back production unless separately authorized;
- treat an agent review as required human approval;
- execute or trigger untrusted change-controlled code where it can access secrets, production credentials, or sensitive host paths;
- approve or rely on a privileged workflow that checks out untrusted source-branch code;
- claim a provider capability, review, test, UI inspection, accessibility check, or post-merge check occurred when it did not.

## Merge gate

Every applicable item must pass against the exact source commit being merged.

### Quality

- The Awesome Contract is current.
- `UI surface` is explicitly classified.
- When `UI surface: YES`, the final source commit has a current `UI GATE PASS` under [ui-experience-gate.md](ui-experience-gate.md).
- No verified P0, P1, or P2 finding remains.
- Adversarial review is clean at the independence level required by risk.
- Every acceptance criterion has current evidence.
- Every `NOT RUN` item is non-required and disclosed.
- The full diff is coherent, minimal, and free of accidental scope.
- Changed tests and CI have been inspected for weakening or false success.
- No unresolved actionable human feedback remains unanswered.

### Repository

- The change request is open and any draft hold has been explicitly cleared.
- The source branch is writable and final commits are pushed.
- Source and target are current as required by repository policy.
- The provider reports no conflict.
- Checks or pipelines actually required by the repository or host pass, or trusted pending gates are eligible for host-native auto-merge. This skill adds no CI requirement; absent or optional CI does not prevent merge and does not need to be triggered.
- Required reviews, code-owner approvals, and other human gates are satisfied.
- Merge queue, merge train, signed commit, linear history, and other repository rules are satisfied.
- The selected merge method is supported and follows repository convention.

### Safety

- The risk lane is accurate.
- Yellow and red independence requirements are satisfied.
- Red-risk merge has exact additional authorization or stops for the owner.
- No policy or review requirement is bypassed.
- The current source commit matches the reviewed and validated commit.
- No source, target, discussion, or policy movement invalidated the evidence.
- Change-controlled code was inspected before execution and any untrusted execution was isolated from secrets and sensitive host access.

## Provider capability fallback

Use [platform-portability.md](platform-portability.md) to map host features. Apply these rules when the provider or available tool lacks a capability:

- No atomic expected-head guard: refresh the source commit immediately before merge and stop if it moved.
- No discussion-write or thread-resolution API: do not claim feedback was answered or resolved. Return `READY FOR OWNER MERGE` when substantive feedback remains.
- No auto-merge: use `READY FOR OWNER MERGE` when only external gates remain.
- No merge API: complete and push all other work, then use `READY FOR OWNER MERGE`.
- No post-merge CI visibility: confirm merged state and target reachability, then disclose post-merge CI as `NOT RUN`.
- No compatible UI specialist: use the embedded UI lens and disclose the independence level. Do not waive the UI gate.
- No credible runtime or presentation inspection for a UI change: record required evidence as `NOT RUN` and stop as `BLOCKED`.
- Unknown semantics for a destructive or merge action: consult official provider documentation or stop.

Missing tooling never authorizes a lower standard.

## Merge execution

Immediately before merge:

1. refresh change-request metadata, unresolved feedback, policy, and checks;
2. compare the current source commit with the reviewed commit;
3. stop if it moved unexpectedly;
4. refresh the target branch or merge-group state required by policy;
5. use the configured or established merge method;
6. use an expected-head or compare-and-swap guard when available;
7. do not delete the source branch automatically.

## Auto-merge

Auto-merge is appropriate only when:

- the change has already converged and is awesome;
- every applicable UI experience requirement has passed;
- only trusted external checks, required approvals, or a queue or train remain;
- the provider and repository permit it;
- the risk lane and review independence permit autonomous merge;
- enabling it does not bypass a draft state, hold, release window, or human decision.

Report `AUTO-MERGE ARMED` and name the remaining gates. Do not report `MERGED` until the provider confirms it.

## Human hold signals

Treat any of these as an owner-merge requirement unless the user's current instruction or an authorized repository owner explicitly clears it:

- draft state;
- `do not merge`, `hold`, `WIP`, or equivalent label or text;
- requested changes that remain active;
- a linked release or migration plan requiring a scheduled decision;
- an unresolved product, design, accessibility, or architecture decision;
- a reviewer explicitly asking to inspect the final result.

A general request made before the hold appeared does not clear a later hold. Refresh hold state immediately before merge.

## Post-merge failure

A merge can succeed while the target branch fails afterward. Check immediate target-branch CI and deployment signals when available. If they fail:

- report the failure plainly;
- do not claim healthy completion;
- do not roll back or hotfix without authorization unless an explicitly delegated repository process owns it;
- preserve the failing run, target commit, and observed symptom for the next action.
