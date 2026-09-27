# UI Experience Gate

## Contents

- Activation
- Product and design authority
- Specialist composition
- Required runtime evidence
- UX and visual polish
- Accessibility floor
- Verdict and convergence
- Capability degradation
- Reporting

This gate makes UI quality a required part of `merge-when-awesome`, not an optional polish suggestion.

## Activation

Set `UI surface: YES` whenever the change can alter an interactive user-facing or operator-facing experience, or the visual, auditory, haptic, or spatial presentation of one.

Common triggers include:

- pages, screens, routes, views, components, templates, forms, dialogs, menus, navigation, games, terminal interfaces, or interactive command flows;
- CSS, styling, layout, typography, themes, design tokens, icons, images, animation, transitions, sound cues, or haptics;
- visible copy, localization, formatting, validation messages, notifications, prompts, or error presentation inside an interface;
- focus, keyboard, pointer, touch, gesture, screen-reader, voice, audio, haptic, or reduced-motion behavior;
- loading, empty, disabled, success, failure, retry, offline, permission, or interrupted states;
- backend, flag, permission, or data-shape changes that alter a rendered or interactive experience.

Do not decide from file extensions alone. A server or configuration change can modify a product UI, while a component-test refactor may not.

Plain documentation, source comments, raw logs, telemetry, noninteractive build output, and API payloads are not a UI surface by themselves. Review them through the documentation, developer-experience, API, or observability lenses unless an actual interface consumes the changed output. A CLI or terminal UI is a UI surface when its prompts, interaction, navigation, formatting, errors, or task flow change; use terminal-appropriate evidence rather than forcing browser checks.

When uncertain about a plausible interface effect, set `UI surface: YES`. The extra review is cheaper than merging a visibly unfinished or inaccessible experience.

## Product and design authority

Before judging polish, identify the authoritative direction:

1. current user instructions and owner locks;
2. accepted product requirements and design decisions;
3. repository design-system guidance and existing product patterns;
4. supplied design files, screenshots, prototypes, or acceptance frames;
5. the surrounding shipped experience.

Do not use this gate to invent a redesign, change product meaning, or override an approved visual direction. Improve the touched experience within the Awesome Contract.

If the accepted direction is materially ambiguous and the choice would change product meaning, hierarchy, interaction, or brand expression, stop for an owner decision rather than selecting a new design by taste.

## Specialist composition

UI work requires a UI, UX, and accessibility specialist pass.

Before falling back to the embedded lens, inspect the skills and tools actually available in the current agent environment for a compatible UI/UX, frontend-design, design-system, visual-review, usability, or accessibility capability. Do not depend on a particular vendor or skill name.

Invoke the smallest relevant specialist capability when available. A compatible specialist must:

- accept the Awesome Contract, repository rules, current runtime, diff, and evidence;
- preserve owner locks and accepted scope;
- review the actual changed journey, not only source code or screenshots;
- include accessibility in its judgment;
- return concrete findings with severity, affected behavior, evidence, and smallest credible fix;
- operate read-only during review, or work on an isolated staged copy that cannot push or merge;
- leave implementation, thread disposition, merge authority, and final convergence with the primary agent.

Prefer a fresh specialist context that did not implement the UI. Run it after the baseline is understood and again after the final material UI changes. A single final specialist pass is sufficient for a very small UI change only when the baseline and required states are already proven.

If no compatible specialist skill or fresh context exists, apply the embedded frontend, product UI, and accessibility lens in [review-lenses.md](review-lenses.md) as a clearly separated hostile review. Missing specialist tooling does not waive the gate.

A specialist's design preference is not authority. Verify every finding against the contract, actual runtime, accepted design direction, repository patterns, and user impact before changing code.

## Bounded UI polish implementation

After verifying findings, perform one finish pass on the touched interface using `$ui-polish` when installed and compatible. Read its instructions and give it the accepted design direction, affected surfaces, owner locks, and verified findings. This is authorized implementation within the active merge workflow, separate from the read-only specialist review above. Use another compatible polish capability or the embedded UX and visual checklist when unavailable; do not install a tool just to satisfy the pass.

Preserve product behavior and visual direction. Improve local hierarchy, typography, spacing, copy, interaction feedback, loading/empty/error states, responsive behavior, focus, and accessibility where useful. If the interface already meets the bar, report the inspected areas without manufacturing edits. Reinspect the final runtime and refresh independent review after material changes. Backend-only changes do not require this pass unless they affect the rendered experience.

## Required runtime evidence

A UI change cannot pass from source inspection, unit tests, snapshots, or a build alone.

Exercise the actual changed experience in the strongest representative runtime available. The evidence contract must identify the affected journeys, states, input modes, viewports or terminal dimensions, and assistive behavior.

At minimum, verify as applicable:

- entry into the changed journey;
- the primary interaction and intended completion;
- validation, error, recovery, cancellation, and retry;
- loading, empty, disabled, success, and interrupted states;
- minimum and maximum supported viewport widths or terminal dimensions;
- representative mobile, tablet, desktop, game, native, or terminal layouts when supported;
- browser zoom or text scaling, including 200 percent for web interfaces when practical;
- keyboard-only operation and visible focus or terminal cursor state;
- touch, pointer, gesture, or command behavior at the intended target size and interaction cost;
- reduced motion and color-independent meaning;
- refresh, back navigation, resize, orientation, background, resume, and process interruption when relevant;
- console errors, failed requests, hydration problems, layout shifts, stale state, and broken terminal output.

Capture final visual evidence for the main changed state and every materially different state, viewport, terminal size, or platform needed to judge the result. Before-and-after evidence is required when the change request claims a visual, UX, accessibility, or performance improvement over existing behavior.

Screenshots, recordings, and terminal captures support judgment but do not replace interaction. Automated browser or terminal checks support interaction but do not replace visual review where visual presentation matters.

## UX and visual polish

The changed experience should feel deliberate, coherent, and complete at the surrounding product's quality bar.

Review:

- task clarity, information hierarchy, and whether the next action is obvious;
- interaction cost, feedback, reversibility, prevention of double action, and recovery from mistakes;
- copy clarity, labels, instructions, validation, and empty or error guidance;
- alignment, spacing, density, rhythm, typography, iconography, terminal formatting, and visual grouping;
- component and design-token reuse rather than one-off styling;
- consistent states, affordances, hover, pressed, selected, disabled, loading, focus, and cursor treatment;
- clipping, overflow, truncation, overlap, wrapping, awkward whitespace, and unstable layout;
- motion purpose, timing, interruption, reduced-motion behavior, and perceived responsiveness;
- visual and interaction continuity with the surrounding application and accepted design direction.

A locally obvious unfinished detail on the touched surface is not dismissed merely because the feature works. Fix high-value P3 polish in the bounded finish pass. Do not spend later rounds chasing subjective preference once no material issue or clear local defect remains.

## Accessibility floor

Accessibility is part of normal UI quality. It is not a separate optional specialist that applies only when requested.

Verify as applicable:

- semantic structure, headings, landmarks, lists, tables, form associations, names, roles, values, and states;
- logical reading and focus order;
- visible focus and correct focus placement, trapping, restoration, and escape behavior;
- keyboard or command equivalence for pointer, touch, gesture, and mouse actions;
- accessible names for icons and controls without duplicate or misleading announcements;
- useful live-region, status, or terminal feedback for asynchronous changes;
- contrast, non-color cues, forced-colors behavior where supported, and readable disabled states;
- reflow, text enlargement, localization expansion, terminal resizing, and content that is not lost at zoom;
- reduced motion, pause or stop controls, and avoidance of seizure or vestibular hazards;
- target size, spacing, gesture alternatives, timeout handling, and nonvisual alternatives where applicable;
- screen-reader behavior for the primary journey when semantics or dynamic announcements changed.

Use established repository tooling such as axe, accessibility linters, contrast checks, platform inspectors, or terminal accessibility checks when available. A passing automated scan is not sufficient proof of keyboard quality, screen-reader clarity, visual hierarchy, or usable error recovery.

A material accessibility regression is P1 or P2 according to user impact. A clear, local accessibility defect introduced or directly exposed by the change is not deferred as generic backlog.

## Verdict and convergence

Record one gate result:

- `UI GATE PASS`: The required runtime, UX, visual or presentation, responsive or resizing, and accessibility evidence is current for the final source commit; the specialist review is `CLEAN` of P0, P1, and P2 findings; and no obvious high-value P3 defect remains on the touched surface.
- `UI GATE BLOCKED`: Required evidence is missing or unsafe to run, a material finding remains, accepted design direction is unresolved, or the actual experience cannot be inspected credibly.

The whole change cannot converge while `UI surface: YES` and the result is not `UI GATE PASS`.

The gate does not demand aesthetic perfection. It demands a defensible shipped-quality result for the scope actually touched.

## Capability degradation

- No compatible specialist skill: use the embedded lens and disclose the review independence level.
- No browser, application, game, native, or terminal runtime: mark required presentation and interaction evidence `NOT RUN` and do not merge as awesome.
- No screenshot, recording, or terminal-capture capability: use another trustworthy inspection path. If presentation quality is part of the outcome and no direct inspection is possible, block.
- No screen reader: use semantic inspection, keyboard testing, and automated checks, but block when the change depends materially on live announcements or screen-reader interaction that cannot be proven.
- No physical device: use representative simulator, emulator, or browser evidence and label it accurately. Record unverified touch, platform accessibility, haptics, audio, and lifecycle behavior. Apply the effective physical-device policy: `when-relevant` blocks device-dependent UI acceptance without real-device proof; `optional` treats the gap as a caveat unless the user or repository requires it. Other runtime and accessibility evidence still applies.
- No authoritative design artifact: use accepted requirements and the surrounding product. Stop when the missing direction would require a material design choice.

Never replace missing evidence with confidence language.

## Reporting

The final evidence summary for a UI change must include:

- `UI surface: YES`;
- affected journeys and states;
- authoritative design source or surrounding-product baseline;
- specialist skill or embedded lens used, plus independence level;
- runtime and viewport, platform, or terminal-size matrix;
- keyboard, interaction, and accessibility checks;
- visual or presentation evidence locations;
- console, network, process, and output-integrity result as applicable;
- `UI GATE PASS` or `UI GATE BLOCKED`;
- every `NOT RUN`, limitation, or remaining caveat.
