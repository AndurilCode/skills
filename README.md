# skills

Personal collection of Claude skills — structured reasoning frameworks and development methodologies that teach the agent *when* and *how* to apply specific thinking modes when evaluating, diagnosing, deciding, or engineering context.

Each skill lives in its own folder and is self-contained: a `SKILL.md` with a trigger description (so Claude knows when to apply it) and a structured methodology (so it knows how).

---

## Reasoning Skills

Twenty-two frameworks across seven thinking categories, plus development methodologies for context engineering.

### Understand the System

- [`systems-thinking`](skills/system-thinking/SKILL.md) — Maps stocks, flows, feedback loops, and archetypes to find where a system structurally works and where it breaks down.
- [`first-principles-thinking`](skills/first-principles-thinking/SKILL.md) — Strips away conventions down to fundamental truths and rebuilds from scratch. Use when the frame itself might be wrong.
- [`cynefin-framework`](skills/cynefin-framework/SKILL.md) — Classifies the problem domain (Clear / Complicated / Complex / Chaotic) before choosing an approach. Prevents applying the wrong solution type.
- [`epistemic-mapping`](skills/epistemic-mapping/SKILL.md) — Maps what you know, believe, and don't know before reasoning. Surfaces unknown unknowns, dangerous assumptions, and what would change your mind.

### Find What's Broken

- [`theory-of-constraints`](skills/theory-of-constraints/SKILL.md) — Identifies the single bottleneck limiting throughput. Optimizing anything else is waste.
- [`five-whys-root-cause`](skills/five-whys-root-cause/SKILL.md) — Drills through symptoms to structural root causes. Stops fixes that don't hold.
- [`causal-inference`](skills/casual-inference/SKILL.md) — Distinguishes causation from correlation when interpreting metrics, A/B tests, and system behavior. Surfaces confounders and counterfactuals.
- [`cognitive-bias-detection`](skills/cognitive-bias-detection/SKILL.md) — Audits the reasoning itself for systematic distortions: confirmation bias, sunk cost, anchoring, groupthink, and more.

### Stress-Test and Attack

- [`inversion-premortem`](skills/inversion-premortem/SKILL.md) — Imagines the future failure and works backwards. Surfaces hidden assumptions before commitment.
- [`red-teaming`](skills/red-teaming/SKILL.md) — Attacks the system adversarially across technical, incentive, process, and systemic dimensions.
- [`second-order-thinking`](skills/second-order-thinking/SKILL.md) — Traces consequences of consequences. Catches unintended side effects and equilibrium shifts.

### Navigate Uncertainty and People

- [`probabilistic-thinking`](skills/probabilistic-thinking/SKILL.md) — Applies base rates, Bayesian updating, and expected value to reason under uncertainty.
- [`fermi-estimation`](skills/fermi-estimation/SKILL.md) — Estimates unknown quantities by decomposition from first principles. Useful when data is unavailable and a decision can't wait.
- [`scenario-planning`](skills/scenario-planning/SKILL.md) — Maps plausible futures across key uncertainties and stress-tests strategy against each.
- [`stakeholder-power-mapping`](skills/stakeholder-power-mapping/SKILL.md) — Maps who has power and interest, surfaces informal influence networks, designs engagement strategies.

### Generate New Options

- [`lateral-thinking`](skills/lateral-thinking/SKILL.md) — Deliberately escapes dominant patterns to generate non-obvious alternatives. Use when analytical thinking has hit a ceiling.
- [`analogical-thinking`](skills/analogical-thinking/SKILL.md) — Finds structural analogues in other domains and transfers solution patterns. Don't reinvent what's been solved elsewhere under a different name.
- [`bisociative-creativity`](skills/bisociative-creativity/SKILL.md) — Generates genuinely novel ideas by colliding distant frames of reference. Use when the deliverable is a creative concept, name, angle, or metaphor rather than an analysis.

### Decide and Learn

- [`decision-synthesis`](skills/decision-synthesis/SKILL.md) — Bridges analysis to action using weighted criteria and structured trade-off evaluation. The convergence layer after running other frameworks.
- [`decision-intelligence`](skills/decision-intelligence/SKILL.md) — Applies six probabilistic models (Expected Value, Base Rate, Sunk Cost, Bayesian Thinking, Survivorship Bias, Kelly Criterion) mandatorily and in sequence to any decision with quantifiable stakes. Produces explicit calculations and a synthesized recommendation with confidence level.
- [`retrospective-counterfactual`](skills/retrospective-counterfactual/SKILL.md) — Reconstructs what actually caused a past outcome and what would have happened differently. Post-mortems, incident reviews, and decision quality assessment.

### Engineer and Evaluate Context

- [`edd`](skills/edd/SKILL.md) — Eval-Driven Development. TDD for context, not code. Write behavioral assertions about agent behavior, engineer harness/prompts until assertions pass, catch regressions before shipping. Use when iterating on any context artifact that runs repeatedly.
- [`context-eval`](skills/context-eval/SKILL.md) — Measures whether a context engineering harness actually improves agent outcomes by comparing baseline vs. harnessed runs against explicit assertions. The measurement engine that EDD uses under the hood.

---

## Chaining Skills

Skills are designed to be composed. Common sequences:

**Evaluating something that exists** → Cynefin → Systems Thinking → Theory of Constraints → 5 Whys → Causal Inference

**Validating a plan before committing** → Epistemic Mapping → First Principles → Inversion/Pre-mortem → Second-Order → Cognitive Bias Detection → Decision Synthesis

**Making a high-stakes decision** → Scenario Planning → Probabilistic Thinking → Fermi Estimation → Red Teaming → Stakeholder Mapping → Decision Synthesis

**Stuck with no good options** → Epistemic Mapping → Lateral Thinking → Analogical Thinking → First Principles

**Generating creative options from scratch** → Bisociative Creativity → Inversion/Pre-mortem → Decision Synthesis

**Diagnosing a recurring problem** → 5 Whys → Causal Inference → Systems Thinking → Cognitive Bias Detection

**After something goes wrong** → Retrospective/Counterfactual → 5 Whys → Epistemic Mapping → Decision Synthesis

**Checking whether a context harness is worth the tokens** → Context Eval

**Iterating on a context harness** → EDD (uses Context Eval as measurement engine)

---

## Structure

```
skills/
├── analogical-thinking/
├── bisociative-creativity/
├── casual-inference/
├── cognitive-bias-detection/
├── context-eval/
├── edd/
├── cynefin-framework/
├── decision-intelligence/
├── decision-synthesis/
├── epistemic-mapping/
├── fermi-estimation/
├── first-principles-thinking/
├── five-whys-root-cause/
├── inversion-premortem/
├── lateral-thinking/
├── probabilistic-thinking/
├── reasoning-orchestrator/
├── red-teaming/
├── retrospective-counterfactual/
├── scenario-planning/
├── second-order-thinking/
├── stakeholder-power-mapping/
├── system-thinking/
└── theory-of-constraints/
    └── SKILL.md
```

Each `SKILL.md` has a YAML frontmatter `description` field — this is what Claude reads to decide whether to consult the skill for a given query.

---

## Orchestration

- [`reasoning-orchestrator`](skills/reasoning-orchestrator/SKILL.md) — The entry point for the collection. Triages the situation, selects the right skill(s), sequences them, and routes between them based on what each run surfaces. Start here when unsure which framework to apply.
