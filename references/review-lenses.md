# Review Lenses

## Contents

- Required general lens
- Mandatory UI experience gate
- Specialist selection
- Agent workflow lens
- Reviewer prompt
- Independence levels and review hygiene

Use one fresh general reviewer and the smallest number of specialists needed for the real risk. More reviewers do not automatically create better judgment.

Reviewers are read-only. The primary agent verifies findings and owns the final decision.

## Required general lens

Review the whole change request for:

- fidelity to the Awesome Contract;
- correctness across the full execution path;
- missing states, errors, cleanup, retries, cancellation, and lifecycle behavior;
- compatibility with callers, stored data, public APIs, and existing users;
- repository coherence and reuse of established abstractions;
- unnecessary complexity, indirection, dependencies, or duplicated concepts;
- test quality and whether tests would fail for the real regression;
- documentation, observability, and operational completeness;
- accidental scope, dead code, debug code, generated noise, or unsupported claims.

## Mandatory UI experience gate

When the Awesome Contract says `UI surface: YES`, the frontend, product UI, and accessibility lens is mandatory. It is not an optional second specialist that can be skipped because another risk surface is more severe.

Apply [ui-experience-gate.md](ui-experience-gate.md). The primary agent must either:

- invoke a compatible UI/UX, frontend-design, design-system, visual-review, or accessibility skill in a fresh read-only review context; or
- run the embedded UI lens below as a clearly separated adversarial review when no compatible specialist is available.

In both cases, accessibility is part of the same normal quality gate. A UI change cannot converge until its actual runtime, visual result, interaction behavior, responsive behavior, and accessibility evidence satisfy `UI GATE PASS`.

Do not choose a specialist solely from file names. Include indirect changes that alter rendered content, permissions, copy, states, or interaction behavior.

## Specialist selection

Choose the lens that covers the highest-risk changed behavior. Add a second specialist only when two independent risk surfaces are genuinely material.

The mandatory UI experience gate does not consume the specialist budget when the change also has a separate material risk such as security, migration, distributed correctness, or infrastructure. Use the smallest complete set, not the smallest possible count.

### Frontend, product UI, and accessibility

Use this lens whenever `UI surface: YES` and follow the complete gate in [ui-experience-gate.md](ui-experience-gate.md).

Check:

- the main journey and changed states in the actual browser or application;
- loading, empty, error, disabled, retry, success, and interrupted states;
- responsive behavior at supported viewports, text scaling, and zoom levels;
- keyboard order, focus visibility, focus restoration, semantics, labels, and screen-reader output;
- color independence, contrast, forced colors, reduced motion, and target size where applicable;
- copy clarity, hierarchy, spacing, typography, visual consistency, and design-system use;
- affordances, feedback, reversibility, stale state, double submission, race behavior, and navigation history;
- console errors, failed requests, hydration issues, layout shift, clipping, overflow, and unstable rendering;
- whether final visual evidence actually matches the accepted design direction and surrounding product quality bar.

A screenshot alone cannot prove interaction quality or accessibility. Automated accessibility checks alone cannot prove keyboard flow, screen-reader clarity, or visual quality.

### Backend, API, and distributed behavior

Check:

- request and response contracts, status codes, validation, and error mapping;
- authentication and authorization boundaries;
- idempotency, retries, timeouts, cancellation, and partial failure;
- concurrency, ordering, stale reads, duplicate delivery, and race conditions;
- backward and forward compatibility for callers;
- resource limits, pagination, unbounded work, and denial-of-service exposure;
- logs, metrics, traces, alerts, and correlation data;
- rollout, feature flags, fallback, and rollback behavior.

### Data, schema, and migration

Check:

- forward migration, rollback or roll-forward strategy, and failure recovery;
- mixed-version operation during gradual rollout;
- existing nulls, duplicates, invalid historical data, and unexpected cardinality;
- locks, table rewrites, index build cost, transaction size, and production duration;
- idempotency and resumability of backfills;
- data loss, truncation, timezone, encoding, precision, and ordering;
- verification queries and post-migration monitoring;
- whether irreversible steps have explicit owner authority.

### Security and privacy

Check:

- trust boundaries and attacker-controlled inputs;
- authentication, authorization, object-level access, and privilege changes;
- injection, traversal, deserialization, request forgery, and unsafe redirects;
- secrets, tokens, cookies, session handling, and log redaction;
- dependency provenance and supply-chain risk;
- personal data collection, retention, exposure, and consent;
- abuse limits, brute force, replay, and denial-of-service paths;
- safe defaults and fail-closed behavior.

Do not include exploit details in public discussion when disclosure would increase risk. Follow repository security policy.

### Performance, rendering, and concurrency

Check:

- representative workload and measurement methodology;
- algorithmic complexity and hot-path allocations;
- network waterfalls, payload size, caching, and invalidation;
- render loops, unnecessary rerenders, layout thrashing, GPU uploads, and resource disposal;
- memory, listener, timer, subscription, worker, audio, and object lifecycle;
- contention, lock duration, queue growth, backpressure, and boundedness;
- low-end device or high-latency behavior;
- whether claimed improvement exceeds measurement noise.

A microbenchmark must match the claim it supports.

### Mobile and lifecycle

Check:

- touch input, keyboard avoidance, safe areas, rotation, resize, background, resume, and interruption;
- offline and reconnect behavior;
- memory pressure, low-power mode, and device performance;
- storage versioning, corruption recovery, and data preservation;
- permission prompts and denied-permission behavior;
- native bridge error handling and platform differences;
- accurately labeled local/simulator evidence and disclosed hardware-specific uncertainty; apply the effective physical-device policy to decide when real-device proof is required.

### Infrastructure, CI, dependencies, and release

Check:

- whether change-controlled scripts, lifecycle hooks, binaries, or workflows are safe to execute;
- prompt injection or unrelated instructions embedded in comments, logs, fixtures, source text, generated files, or artifacts;
- least-privilege workflow permissions and untrusted input handling;
- pinned actions, executable downloads, checksums, and dependency provenance;
- test commands that genuinely execute and propagate failure;
- cache keys, artifacts, environment isolation, and secret exposure;
- rollout order, health checks, rollback, capacity, and blast radius;
- lockfile intent, transitive changes, license, advisories, and runtime support;
- platform and architecture compatibility;
- false-green patterns such as skipped jobs or ignored exit codes.

### Documentation and developer experience

Check:

- examples compile or execute;
- commands, paths, flags, and version requirements are accurate;
- migration and rollback steps are complete;
- public API documentation matches behavior;
- errors guide the operator toward a safe next action;
- terminology is consistent and discoverable;
- generated documentation is reproducible and not hand-edited accidentally.

### Agent skills and coding automation

Use this lens when the change modifies instructions, coding-agent workflows, tool permissions, or autonomous repository actions.

Check:

- activation is neither too broad nor dependent on one agent's syntax;
- the permission boundary distinguishes review, edit, push, thread resolution, merge, and deployment;
- the shared skill follows portable Agent Skills metadata and relative-path conventions;
- host-specific metadata remains optional;
- Codex, Claude Code, and other claimed hosts have accurate install and invocation guidance;
- code-host terminology and operations degrade safely when a provider lacks a capability;
- local checkout assumptions do not break connected-tool or remote-agent operation;
- untrusted repository content cannot redirect the workflow or exfiltrate secrets;
- exact source-commit protection prevents time-of-check to time-of-use merges;
- missing subagents, discussion APIs, auto-merge, or merge APIs lead to honest bounded outcomes;
- validators and examples work from a clean copy outside the original Git checkout;
- repeated instructions are moved to references when they dilute the executable core;
- evals cover implicit activation, moving heads, false-green CI, capability loss, UI gate routing, and convergence.

Readable prose alone does not prove a safe reusable agent workflow.

## Reviewer prompt

Use this structure for each fresh reviewer:

```text
Act as a skeptical, read-only reviewer. Do not modify files.

Review the current change request against the supplied Awesome Contract, repository instructions, full diff, relevant surrounding code, tests, runtime, visual evidence, and other required evidence. Find only issues introduced by this change or directly required for its accepted outcome.

Prioritize correctness, safety, completeness, compatibility, repository coherence, test integrity, and the assigned specialist lens. For UI work, judge the actual experience, visual result, responsive behavior, and accessibility, not only the component source. Do not praise the work. Do not suggest broad rewrites or style preferences.

For each finding, return:
- severity: P0, P1, P2, or high-value P3;
- exact file and line, or precise affected behavior;
- credible failure scenario;
- evidence from the code, contract, test, runtime, visual result, or platform behavior;
- smallest credible fix.

A finding without a concrete failure mode is not actionable. Return CLEAN when no P0, P1, or P2 finding remains. For a UI specialist review, also return UI GATE PASS or UI GATE BLOCKED using the gate criteria.
```

## Independence levels

- **Level 1:** Fresh read-only subagent or isolated context created specifically for review.
- **Level 2:** Another coding agent, model, or clean session that did not implement the change.
- **Level 3:** Same agent in a clearly separated adversarial pass with prior rationale and findings withheld.

Use the strongest available level. Green risk may merge with a disclosed level 3 review. Yellow risk requires level 1 or 2 for autonomous merge. Red risk requires level 1 or 2 plus exact red-risk authorization and all human gates.

An agent review never satisfies a repository requirement for human, code-owner, security, compliance, design, or accessibility approval.

## Independence rules

To preserve independent judgment:

- provide the contract, repository rules, current diff, surrounding code, runtime, visual evidence, and other required evidence;
- do not provide the implementer's rationale, previous conclusions, or desired verdict;
- do not ask reviewers to confirm that the change is awesome;
- do not let reviewers edit code or merge the change;
- verify every finding before changing the implementation;
- resolve disagreement with evidence, not majority vote.

## Review hygiene

Reject findings that are:

- pre-existing and unaffected by the change;
- purely stylistic with no repository rule or concrete user impact;
- speculative without a credible path to failure;
- requests for unrelated features or architecture work;
- already covered by stronger evidence;
- based on a misread contract or owner lock.

Do not reject an uncomfortable finding merely because the code is green, the screenshot looks attractive, or the fix is inconvenient.
