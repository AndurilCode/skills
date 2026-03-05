# skills

Personal collection of Claude skills — structured reasoning frameworks that teach the agent *when* and *how* to apply specific thinking modes when evaluating, diagnosing, or deciding.

Each skill lives in its own folder and is self-contained: a `SKILL.md` with a trigger description (so Claude knows when to apply it) and a structured methodology (so it knows how).

---

## Reasoning Skills

Twelve frameworks organized by what kind of thinking is needed.

### Understand the System

- [`systems-thinking`](skills/systems-thinking/SKILL.md) — Maps stocks, flows, feedback loops, and archetypes to find where a system structurally works and where it breaks down.
- [`first-principles-thinking`](skills/first-principles-thinking/SKILL.md) — Strips away conventions down to fundamental truths and rebuilds from scratch. Use when the frame itself might be wrong.
- [`cynefin-framework`](skills/cynefin-framework/SKILL.md) — Classifies the problem domain (Clear / Complicated / Complex / Chaotic) before choosing an approach. Prevents applying the wrong solution type.

### Find What's Broken

- [`theory-of-constraints`](skills/theory-of-constraints/SKILL.md) — Identifies the single bottleneck limiting throughput. Optimizing anything else is waste.
- [`five-whys-root-cause`](skills/five-whys-root-cause/SKILL.md) — Drills through symptoms to structural root causes. Stops fixes that don't hold.
- [`cognitive-bias-detection`](skills/cognitive-bias-detection/SKILL.md) — Audits the reasoning itself for systematic distortions: confirmation bias, sunk cost, anchoring, groupthink, and more.

### Stress-Test and Attack

- [`inversion-premortem`](skills/inversion-premortem/SKILL.md) — Imagines the future failure and works backwards. Surfaces hidden assumptions before commitment.
- [`red-teaming`](skills/red-teaming/SKILL.md) — Attacks the system adversarially across technical, incentive, process, and systemic dimensions.
- [`second-order-thinking`](skills/second-order-thinking/SKILL.md) — Traces consequences of consequences. Catches unintended side effects and equilibrium shifts.

### Navigate Uncertainty and People

- [`probabilistic-thinking`](skills/probabilistic-thinking/SKILL.md) — Applies base rates, Bayesian updating, and expected value to reason under uncertainty.
- [`scenario-planning`](skills/scenario-planning/SKILL.md) — Maps plausible futures across key uncertainties and stress-tests strategy against each.
- [`stakeholder-power-mapping`](skills/stakeholder-power-mapping/SKILL.md) — Maps who has power and interest, surfaces informal influence networks, designs engagement strategies.

### Generate New Options

- [`lateral-thinking`](skills/lateral-thinking/SKILL.md) — Deliberately escapes dominant patterns to generate non-obvious alternatives. Use when analytical thinking has hit a ceiling and all solutions feel like variations of the same idea.

---

## Chaining Skills

Skills are designed to be composed. A few sequences that work well together:

**Evaluating something that exists** → Cynefin → Systems Thinking → Theory of Constraints → 5 Whys

**Validating a plan before committing** → First Principles → Inversion/Pre-mortem → Second-Order Thinking → Cognitive Bias Detection

**Making a high-stakes decision** → Scenario Planning → Probabilistic Thinking → Red Teaming → Stakeholder Mapping

**Diagnosing a recurring problem** → 5 Whys → Systems Thinking → Cognitive Bias Detection

---

## Structure

```
skills/
├── cognitive-bias-detection/
├── cynefin-framework/
├── first-principles-thinking/
├── five-whys-root-cause/
├── inversion-premortem/
├── probabilistic-thinking/
├── red-teaming/
├── scenario-planning/
├── second-order-thinking/
├── stakeholder-power-mapping/
├── systems-thinking/
├── theory-of-constraints/
└── lateral-thinking/
    └── SKILL.md
```

Each `SKILL.md` has a YAML frontmatter `description` field — this is what Claude reads to decide whether to consult the skill for a given query.
