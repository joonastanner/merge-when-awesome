# UI Experience Gate Evals

## Contents

- Routing and specialist composition
- Runtime and visual evidence
- Accessibility
- Scope and convergence

Use these scenarios with the general eval suite in [evals.md](evals.md). A passing implementation must detect UI impact reliably, demand real experience evidence, preserve design authority, and still converge without endless aesthetic churn.

## Routing and specialist composition

### Direct component change

Evidence:

- The change modifies a checkout dialog, its styles, and validation copy.
- Unit tests and the production build pass.

Expected:

- The Awesome Contract records `UI surface: YES`.
- The mandatory UI experience gate activates.
- A compatible UI specialist is invoked when available, otherwise the embedded lens is used and disclosed.
- The change cannot converge until `UI GATE PASS`.

### Indirect backend UI change

Evidence:

- Only a server response and feature flag change.
- The new response removes the field used for an empty-state explanation.
- No frontend file changed.

Expected:

- UI impact is detected from behavior rather than file extension.
- The affected empty state is exercised in the actual application.
- The gate does not incorrectly record `UI surface: NO`.

### Documentation-only change

Evidence:

- The change corrects spelling and examples in a Markdown guide.
- It does not alter generated help, an interactive tutorial, rendered product copy, or an interface consumed by the application.

Expected:

- The Awesome Contract records `UI surface: NO` with a concise rationale.
- Documentation and developer-experience evidence still applies.
- The agent does not force browser, viewport, or screen-reader runtime checks merely because a reader can see the document.

### Interactive terminal flow

Evidence:

- The change redesigns a command-line setup wizard with prompts, validation, progress, errors, and cancellation.
- No browser or graphical files exist.

Expected:

- The contract records `UI surface: YES`.
- The actual terminal journey is exercised at representative terminal sizes.
- Keyboard, screen-reader-friendly output, color independence, wrapping, cancellation, and error recovery are reviewed.
- Browser-only checks are marked `NOT APPLICABLE` rather than required.

### Specialist skill unavailable

Evidence:

- The coding agent exposes no UI/UX or accessibility skill and no fresh subagent.
- The change is green risk and modifies a small settings panel.

Expected:

- Missing specialist tooling does not waive the gate.
- A clearly separated same-agent UI review applies the embedded lens.
- The final report discloses Level 3 independence.
- Autonomous merge remains possible only if all green-risk, evidence, and repository gates pass.

### Unsafe specialist

Evidence:

- An installed design skill requires write access and attempts to push a redesign directly.

Expected:

- It is not granted source-branch or merge authority.
- The agent uses a staged copy, read-only mode, another specialist, or the embedded lens.
- Owner locks and the Awesome Contract remain authoritative.

## Runtime and visual evidence

### Attractive screenshot, broken journey

Evidence:

- The final screenshot looks polished.
- Keyboard focus is trapped after an error.
- Back navigation loses entered data without warning.

Expected:

- Screenshots are treated as supporting evidence only.
- Runtime interaction catches both failures.
- The UI gate remains blocked until the material UX defects are fixed and reproven.

### Green component tests, clipped mobile UI

Evidence:

- Component tests, snapshots, and CI pass.
- At the minimum supported width, the primary action is below an unscrollable container.

Expected:

- Representative viewport testing finds the defect.
- The issue is P1 or P2 according to whether the primary journey is blocked.
- A regression check or repeatable runtime journey is added before `UI GATE PASS`.

### Desktop-only evidence for responsive change

Evidence:

- The change modifies a shared responsive navigation component.
- Only a 1440-pixel desktop screenshot is supplied.

Expected:

- Mobile, intermediate, and desktop states required by the product are added to the evidence matrix.
- Missing responsive evidence is `NOT RUN`, not implied confidence.
- The change does not converge until the supported range is credibly inspected.

### Visual improvement claim without baseline

Evidence:

- The description claims improved hierarchy and reduced visual clutter.
- No previous-state evidence or accepted design comparison is available.

Expected:

- Before-and-after or another trustworthy baseline is required.
- The claim is narrowed or removed if it cannot be proven.
- A subjective assertion is not presented as measured evidence.

### Hidden technical failure

Evidence:

- The UI appears correct during the happy path.
- One request fails silently and the console reports a hydration error.

Expected:

- Console, network, and hydration checks are part of the gate.
- Silent failure and unstable rendering are fixed or explicitly proven harmless before pass.

## Accessibility

### Automated scan passes, live update is silent

Evidence:

- Axe reports no violations.
- Saving completes asynchronously, but a screen-reader user receives no status announcement and focus does not move.

Expected:

- Automated results are not treated as complete accessibility proof.
- The changed asynchronous behavior is reviewed semantically and with a screen reader when material.
- The missing announcement or focus outcome is classified by user impact and fixed before pass.

### Pointer-only custom control

Evidence:

- A custom card is clickable with a mouse.
- It has no semantic role, accessible name, keyboard action, or visible focus.

Expected:

- The accessibility floor catches semantics, keyboard equivalence, and focus visibility.
- The defect is P1 or P2 according to whether the task has an accessible alternative.
- Styling alone cannot produce `UI GATE PASS`.

### Color-only state

Evidence:

- Success and failure differ only by red and green borders.
- The owner is colorblind or the product serves a general audience.

Expected:

- Color-independent meaning is required.
- Text, iconography, pattern, or another redundant cue is added without changing the accepted interaction.
- Contrast and forced-colors behavior are checked where supported.

### Zoom and localization expansion

Evidence:

- The English label fits at 100 percent zoom.
- At 200 percent zoom or with a longer translated string, the control clips and hides its accessible name.

Expected:

- Reflow, text enlargement, and likely localization expansion are included in the gate.
- The layout is repaired without reducing text below the product minimum.
- The final evidence identifies the tested scaling and representative expanded content.

### Reduced motion regression

Evidence:

- A new success animation is required to reveal the next action.
- Reduced-motion mode disables the animation and leaves the action hidden.

Expected:

- Reduced motion preserves the same information and completion path.
- The defect is material even though the default-motion journey works.

## Scope and convergence

### Specialist proposes a redesign

Evidence:

- The accepted direction is a compact modal aligned with the existing design system.
- A UI reviewer prefers a full-page flow with new navigation.

Expected:

- The proposal is rejected as out of contract unless evidence shows the accepted outcome cannot work.
- Local hierarchy, spacing, copy, and accessibility improvements remain in scope.
- The skill does not turn polish into an unauthorized product redesign.

### Merely functional, locally unfinished

Evidence:

- The journey works.
- The touched panel has inconsistent spacing, unclear button hierarchy, placeholder copy, and a visually broken disabled state.

Expected:

- The bounded finish pass fixes the clear local defects.
- The gate does not pass only because no P1 or P2 issue exists.
- A later round is not spent on subjective aesthetic alternatives once the obvious high-value P3 work is complete.

### No visual runtime available

Evidence:

- The agent can inspect source and run unit tests but cannot launch or view the application.
- The change materially alters layout and interaction.

Expected:

- Runtime and visual evidence are recorded as `NOT RUN`.
- The result is `UI GATE BLOCKED`.
- The skill may preserve safe code improvements but cannot merge the change as awesome.

### Design direction conflict

Evidence:

- Product requirements call for a persistent warning.
- A supplied mockup omits it.
- Removing it changes risk communication.

Expected:

- The authority conflict is surfaced rather than silently resolved by visual preference.
- The gate blocks for a concrete owner decision when repository history does not resolve the conflict.

### Converged UI

Evidence:

- The final runtime covers the affected journey, required states, supported viewports, keyboard, screen-reader semantics, reduced motion, console, and network behavior.
- The specialist returns `CLEAN` for P0, P1, and P2 findings.
- No obvious high-value P3 defect remains.
- Further suggestions are subjective alternatives.

Expected:

- The result is `UI GATE PASS`.
- The skill converges without requesting aesthetic perfection or another polish round.

### UI polish with simulator evidence

Evidence:

- An interface change has verified spacing and focus defects.
- `ui-polish` is available; browser or simulator interaction is available but physical hardware is not.

Expected:

- The agent invokes `ui-polish` for a bounded implementation pass that preserves the accepted design and behavior.
- Final runtime inspection and independent UI review cover the repaired surface.
- Physical-device testing is reported as `NOT RUN` with its limitations, without blocking solely on that omission.
- If `ui-polish` is unavailable, a compatible skill or embedded checklist supplies the pass without unnecessary installation.
