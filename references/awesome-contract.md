# Awesome Contract

## Contents

- Authority order
- Contract template
- Acceptance criteria and owner locks
- UI surface declaration
- Scope and ambiguity rules
- Contract drift check

The Awesome Contract is the temporary source of truth for one `merge-when-awesome` run. It prevents two common failures: judging the change only by its current implementation, and expanding "awesome" into unbounded product work.

Keep it in working notes during execution. Add only the concise final form to the managed evidence section. Do not commit a separate contract file unless the repository already requires one.

## Authority order

Resolve intent using this order:

1. the user's current request and explicit owner decisions;
2. linked acceptance criteria and recorded product decisions;
3. the change-request description and human review discussion;
4. repository guidance, architecture records, public contracts, and established behavior;
5. tests and implementation details.

A lower source cannot silently override a higher source. Existing code reveals constraints but does not define product intent by itself.

## Contract template

```markdown
## Awesome Contract

Change request: <provider and repository identifier>
Original source: <branch or ref>@<commit>
Target: <branch or ref>@<commit>

### Intended outcome
<One or two sentences describing the user, product, or engineering result.>

### Acceptance criteria
- <Observable result>
- <Observable result>

### Owner locks
- <Decision that must not be changed>
- <None, when no lock exists>

### In scope
- <Behavior, component, API, migration, documentation, or test surface>

### Non-goals
- <Nearby feature or refactor that this change must not absorb>

### UI surface
<YES | NO>
Affected journeys and states: <List or NOT APPLICABLE>
Authoritative design source: <Design file, product requirement, surrounding experience, or NOT APPLICABLE>
Supported modes: <Viewports or terminal sizes, zoom or text scaling, keyboard, touch, screen reader, reduced motion, or NOT APPLICABLE>
Specialist path: <Compatible UI skill, fresh UI reviewer, embedded UI lens, or NOT APPLICABLE>

### Risk lane
<GREEN | YELLOW | RED>
Rationale: <Why this is the correct lane.>

### Required evidence
- <Command, runtime journey, state, viewport, measurement, migration proof, or review>

Record the effective validation policy and its source. With `ci: standard`, include relevant CI when available; `local-only` skips optional CI trigger/wait. With `physical_device: when-relevant`, include real-device proof for device-dependent acceptance; `optional` records missing hardware as a caveat. Explicit user requirements take priority, and repository/host-required checks remain external gates in every mode.

### External gates
- <Required approval, check, merge train or queue, release window, or none>

### Review independence
<LEVEL 1 fresh subagent/context | LEVEL 2 other agent/model/session | LEVEL 3 separated same-agent pass>

### Merge authority
<AUTONOMOUS | AUTO-MERGE WHEN EXTERNAL GATES PASS | OWNER MERGE REQUIRED>
```

## Writing good acceptance criteria

Acceptance criteria must be observable. Prefer:

- "A signed-out user receives a 401 response and no account data" over "authentication is handled."
- "The dialog remains usable at 320 CSS pixels, 200 percent zoom, and with keyboard-only input" over "responsive and accessible."
- "The migration supports old and new application versions during rollout" over "migration is safe."
- "The p95 duration does not regress beyond the agreed threshold on the representative dataset" over "performance is good."

Do not convert every implementation detail into an acceptance criterion. Criteria describe the outcome and important constraints.

## Owner locks

Owner locks are decisions the agent may improve around but not reinterpret. Examples:

- control scheme;
- public API shape;
- target audience;
- selected design direction;
- business rule;
- compatibility promise;
- approved dependency or architecture decision;
- deliberate non-goal.

When a reviewer proposes violating a lock, classify it as out of contract and explain why. Do not count it as an unresolved material finding.

## UI surface declaration

Set `UI surface: YES` whenever the change can alter an interactive user-facing or operator-facing experience, or the visual, auditory, haptic, or spatial presentation of one. This includes indirect backend, flag, permission, localization, or data-shape changes that modify a rendered or interactive product experience.

Do not decide from file extensions alone. A server response can change an empty state; a component-test refactor may not change the product at all.

Plain documentation, source comments, raw logs, telemetry, noninteractive build output, and API payloads are not a UI surface by themselves. Review them through their applicable specialist lenses unless an actual interface consumes the changed output. A CLI or terminal UI counts when its prompts, interaction, navigation, formatting, errors, or task flow change.

When uncertain about a plausible interface effect, choose `YES` and apply [ui-experience-gate.md](ui-experience-gate.md).

For `YES`, the contract must identify:

- the affected user or operator journeys and materially different states;
- the authoritative design direction or surrounding-product baseline;
- supported viewport, terminal-size, zoom or text-scaling, input, and assistive modes;
- the compatible UI/UX or accessibility skill, fresh specialist, or embedded lens that will review it;
- the runtime and presentation evidence required for `UI GATE PASS`.

Accessibility is always included in the UI gate. Do not mark it not applicable merely because the change request did not mention accessibility.

Set `UI surface: NO` only when the change cannot alter an interactive interface or its user-perceivable presentation. State why when the answer is not obvious.

## Scope rules

A change is in scope when at least one is true:

- it is required to meet an acceptance criterion;
- it fixes a regression introduced by the change request;
- it is necessary for safe integration, testing, observability, migration, rollback, or operation of the accepted change;
- it is small polish directly on the touched experience and creates no new product commitment.

A change is normally out of scope when it:

- adds a new feature or mode;
- redesigns an adjacent experience;
- replaces architecture that the accepted change does not depend on;
- performs repository-wide cleanup;
- changes a public contract without accepted criteria;
- introduces an optional platform, provider, or dependency;
- exists only because a reviewer prefers a different style.

Necessary supporting work is not scope creep. Unrelated opportunity is.

## Handling ambiguity

Do not ask for clarification about every small choice. Use the safest reversible interpretation that preserves established behavior.

Stop for an owner decision when ambiguity affects:

- product meaning or user-visible behavior;
- visual hierarchy, interaction model, or brand direction;
- public API or data contracts;
- irreversible migration or deletion;
- security, privacy, permissions, billing, or compliance;
- substantial new scope;
- a direct conflict between owner locks and acceptance criteria.

Report the decision as a concrete choice with consequences, not as a vague request for more context.

## Contract drift check

Before every new improvement round and immediately before merge, compare the full diff with the contract:

- Does each material change support an acceptance criterion or necessary delivery work?
- Did any owner lock move?
- Did any non-goal enter the diff?
- Did `UI surface` change from `NO` to `YES` because of implementation or indirect behavior?
- Does final UI evidence still cover every changed journey, state, viewport or terminal size, and assistive mode?
- Did the risk lane increase?
- Did validation or independence requirements change?
- Did source or target movement invalidate evidence?

If risk increases, reclassify before continuing. If UI surface changes to `YES`, activate the full UI experience gate before convergence. If scope expands materially, stop unless the expansion is clearly required for correctness or safety.
