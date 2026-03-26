# skills

Personal collection of Claude skills — structured reasoning frameworks and development methodologies that teach the agent *when* and *how* to apply specific thinking modes when evaluating, diagnosing, deciding, or engineering context.

Each skill lives in its own folder and is self-contained: a `SKILL.md` with a trigger description (so Claude knows when to apply it) and a structured methodology (so it knows how).

---

## Reasoning Skills

Forty-nine frameworks across ten thinking categories, plus development methodologies for context engineering.

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
- [`game-theoretic-analysis`](skills/game-theoretic-analysis/SKILL.md) — Analyzes strategic interaction between agents, actors, or systems where each party's best move depends on what others do. Catches incentive misalignments that systems-thinking alone misses.
### Generate New Options

- [`lateral-thinking`](skills/lateral-thinking/SKILL.md) — Deliberately escapes dominant patterns to generate non-obvious alternatives. Use when analytical thinking has hit a ceiling.
- [`analogical-thinking`](skills/analogical-thinking/SKILL.md) — Finds structural analogues in other domains and transfers solution patterns. Don't reinvent what's been solved elsewhere under a different name.
- [`bisociative-creativity`](skills/bisociative-creativity/SKILL.md) — Generates genuinely novel ideas by colliding distant frames of reference. Use when the deliverable is a creative concept, name, angle, or metaphor rather than an analysis.

### Decide, Communicate, and Execute

- [`decision-synthesis`](skills/decision-synthesis/SKILL.md) — Bridges analysis to action using weighted criteria and structured trade-off evaluation. The convergence layer after running other frameworks.
- [`decision-intelligence`](skills/decision-intelligence/SKILL.md) — Applies six probabilistic models (Expected Value, Base Rate, Sunk Cost, Bayesian Thinking, Survivorship Bias, Kelly Criterion) mandatorily and in sequence to any decision with quantifiable stakes.
- [`retrospective-counterfactual`](skills/retrospective-counterfactual/SKILL.md) — Reconstructs what actually caused a past outcome and what would have happened differently. Post-mortems, incident reviews, and decision quality assessment.
- [`argument-craft`](skills/argument-craft/SKILL.md) — Takes an analysis or recommendation and structures it into a persuasive argument tailored to a specific audience. Pyramid principle, objection pre-emption, framing selection.
- [`execution-planning`](skills/execution-planning/SKILL.md) — Decomposes a decision into an executable plan with WBS, dependency mapping, critical path, PERT estimation, RACI ownership, and risk buffers.
- [`narrative-construction`](skills/narrative-construction/SKILL.md) — Constructs narrative structure for content using story mechanics — arcs, hooks, tension management, and concrete detail anchoring.

### Negotiate and Navigate People

- [`negotiation-strategy`](skills/negotiation-strategy/SKILL.md) — Prepares for negotiations by mapping interests, BATNAs, ZOPA, value creation opportunities, and concession plans. Extends game-theoretic analysis into practical tactics.
- [`difficult-conversations`](skills/difficult-conversations/SKILL.md) — Prepares for conversations involving conflict, power dynamics, or emotional stakes using the Three Conversations model and Nonviolent Communication.
- [`facilitation-design`](skills/facilitation-design/SKILL.md) — Designs meeting and workshop structure with diverge-cluster-converge activities, decision protocols, and psychological safety engineering.

### Reason About Ethics and Fairness

- [`ethical-reasoning`](skills/ethical-reasoning/SKILL.md) — Applies consequentialist, deontological, and virtue ethics frameworks to surface obligations, harms, rights, and value trade-offs that analytical reasoning misses.
- [`fairness-auditing`](skills/fairness-auditing/SKILL.md) — Audits systems, algorithms, or policies for equitable outcomes across groups using five fairness definitions, data audits, and intersectionality checks.

### Validate, Synthesize, and Learn

- [`experimental-design`](skills/experimental-design/SKILL.md) — Designs rigorous experiments with hypothesis formulation, variable identification, sample sizing, pre-registration, and confound mitigation.
- [`evidence-synthesis`](skills/evidence-synthesis/SKILL.md) — Synthesizes evidence from multiple sources with quality grading (GRADE framework), pattern identification, conflict resolution, and confidence-weighted conclusions.
- [`learning-strategy`](skills/learning-strategy/SKILL.md) — Takes a knowledge gap and produces an efficient learning plan with prerequisite mapping, mode selection, deliberate practice, and transfer testing.
- [`financial-modeling`](skills/financial-modeling/SKILL.md) — Constructs structured financial reasoning with unit economics, cost-benefit analysis, NPV/IRR, scenario modeling, and sensitivity analysis.
- [`architecture-evaluation`](skills/architecture-evaluation/SKILL.md) — Evaluates system architecture decisions by mapping quality attributes, trade-offs, and producing Architecture Decision Records (ADRs).
- [`debugging-methodology`](skills/debugging-methodology/SKILL.md) — Applies systematic debugging: reproduce, observe, hypothesize, isolate (binary search), confirm root cause. Prevents fixing symptoms.
- [`process-design`](skills/process-design/SKILL.md) — Designs or redesigns workflows using current state mapping, Lean waste identification, value stream analysis, and automation assessment.

### Engineer and Evaluate Context

- [`context-cartography`](skills/context-cartography/SKILL.md) — Design what goes into an agent's context window. Prioritize, size, structure, and cut context sources using concrete patterns for common agent task types. Produces a versionable context manifest.
- [`context-debugging`](skills/context-debugging/SKILL.md) — Diagnose agent failures that originate in the context layer. Systematic triage across 7 failure categories with quick fixes. Most failures that look like reasoning problems are actually context problems.
- [`context-gap-analyzer`](skills/context-gap-analyzer/SKILL.md) — Identify the implicit context missing from a codebase that would most improve agent performance. The delta between what code explicitly says and what a competent team member knows.
- [`context-eval`](skills/context-eval/SKILL.md) — Measures whether a context engineering harness actually improves agent outcomes by comparing baseline vs. harnessed runs against explicit assertions. The measurement engine that EDD uses under the hood.
- [`edd`](skills/edd/SKILL.md) — Eval-Driven Development. TDD for context, not code. Write behavioral assertions about agent behavior, engineer harness/prompts until assertions pass, catch regressions before shipping.
- [`deep-document-processor`](skills/deep-document-processor/SKILL.md) — Multi-pass reading protocol to extract token-efficient, decision-relevant context from large documents. Optimized for agent consumption, not human summaries.
- [`llms-txt-generator`](skills/llms-txt-generator/SKILL.md) — Generate token-budgeted, section-per-concept Markdown optimized for LLM and RAG consumption. Turns sprawling docs into precise, structured context.
- [`business-logic-extractor`](skills/business-logic-extractor/SKILL.md) — Extract and document business logic, domain models, and product rules from a codebase into a structured llms.txt-style reference.
- [`deep-document-processor`](skills/deep-document-processor/SKILL.md) — Apply disciplined multi-pass reading to extract token-efficient, decision-relevant context from large documents. Four-pass protocol (survey, extract, cross-ref, assemble) optimized for agent consumption.
- [`test-challenger`](skills/test-challenger/SKILL.md) — Challenge AI-generated (or any) unit tests to find false positives — tests that pass against wrong behavior.
- [`code-review-amplifier`](skills/code-review-amplifier/SKILL.md) — Amplifies code reviews by assembling context, pre-scanning surface issues, and routing knowledge-transfer opportunities to human reviewers.
- [`agent-instruction-forge`](skills/agent-instruction-forge/SKILL.md) — Guides humans through creating effective instruction rules for coding agents (Copilot, Claude Code, Cursor, Windsurf). Reads the codebase first, then runs structured knowledge extraction to surface implicit conventions, past failures, and architectural decisions that code alone can't tell an agent.

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

**Communicating a decision** → Decision Synthesis → Argument Craft → Execution Planning

**Building a business case** → Fermi Estimation → Financial Modeling → Scenario Planning → Argument Craft

**Negotiating an agreement** → Game-Theoretic Analysis → Negotiation Strategy → Difficult Conversations (if needed)

**Validating a hypothesis** → Epistemic Mapping → Experimental Design → [run experiment] → Causal Inference → Evidence Synthesis

**Learning a new domain** → Epistemic Mapping → Learning Strategy → [learning] → Evidence Synthesis → Decision Synthesis

**Evaluating architecture** → Systems Thinking → Architecture Evaluation → Inversion/Pre-mortem → Decision Synthesis → Execution Planning

**Fixing a broken process** → Systems Thinking + Theory of Constraints → Process Design → Execution Planning

**Assessing fairness** → Ethical Reasoning → Fairness Auditing → Decision Synthesis

**Debugging software** → Debugging Methodology → 5 Whys / Causal Inference → fix

**Checking whether a context harness is worth the tokens** → Context Eval

**Iterating on a context harness** → EDD (uses Context Eval as measurement engine)

**Agent is failing, need to diagnose** → Context Debugging → fix → EDD to validate fix

**Full context engineering lifecycle** → Context Cartography (design) → EDD (validate) → Context Debugging (when it breaks) → Context Eval (measure)

**Creating agent instructions from scratch** → Context Gap Analyzer (audit gaps) → Agent Instruction Forge (create rules) → EDD (validate rules improve agent behavior)

---

## Structure

```
skills/
├── agent-instruction-forge/
├── analogical-thinking/
├── architecture-evaluation/
├── argument-craft/
├── bisociative-creativity/
├── business-logic-extractor/
├── causal-inference/
├── code-review-amplifier/
├── cognitive-bias-detection/
├── context-cartography/
├── context-debugging/
├── context-eval/
├── context-gap-analyzer/
├── cynefin-framework/
├── debugging-methodology/          ← NEW
├── decision-intelligence/
├── decision-synthesis/
├── deep-document-processor/
├── difficult-conversations/
├── edd/
├── epistemic-mapping/
├── ethical-reasoning/
├── evidence-synthesis/
├── execution-planning/
├── experimental-design/
├── facilitation-design/
├── fairness-auditing/
├── fermi-estimation/
├── financial-modeling/
├── first-principles-thinking/
├── five-whys-root-cause/
├── game-theoretic-analysis/
├── inversion-premortem/
├── lateral-thinking/
├── learning-strategy/
├── llms-txt-generator/
├── narrative-construction/
├── negotiation-strategy/
├── probabilistic-thinking/
├── process-design/
├── reasoning-orchestrator/
├── red-teaming/
├── retrospective-counterfactual/
├── scenario-planning/
├── second-order-thinking/
├── stakeholder-power-mapping/
├── system-thinking/
├── test-challenger/
└── theory-of-constraints/
    └── SKILL.md
```

Each `SKILL.md` has a YAML frontmatter `description` field — this is what Claude reads to decide whether to consult the skill for a given query.

---

## Orchestration

- [`reasoning-orchestrator`](skills/reasoning-orchestrator/SKILL.md) — The entry point for the collection. Triages the situation, selects the right skill(s), sequences them, and routes between them based on what each run surfaces. Start here when unsure which framework to apply.
