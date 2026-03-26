---
name: reasoning-orchestrator
description: "Apply this skill first whenever the user presents a problem, question, or situation that requires structured thinking — before reaching for any specific reasoning framework. Triggers on any substantive request to evaluate, analyze, diagnose, decide, design, improve, understand, or learn from something. This is the entry point for the reasoning skill collection. If you are unsure which reasoning skill to use, always start here."
---

# Reasoning Orchestrator

**CRITICAL: This skill does NOT perform any reasoning itself. It plans and delegates. All reasoning is done by reading and applying individual skill files, or by spawning subagents. Do not shortcut by reasoning inline.**

---

## How to Execute This Skill

Follow these steps exactly, in order. Do not skip steps. Do not collapse steps.

---

### STEP 1 — Triage (do this yourself, no skill file needed)

Classify the situation across these dimensions and write the classification out loud before proceeding:

**Temporal direction**: Forward-looking / Present-state / Backward-looking

**Problem maturity**:
- Unframed — the problem itself may not be correctly defined
- Framed, unsolved — problem understood, solution not found
- Solved, needs validation — solution exists, needs stress-testing
- Decided, needs learning — something happened, extract signal

**Primary obstacle**:
- Don't understand the system → diagnostic track
- Understand it, stuck on solutions → generative track
- Have solutions, need to choose → convergence track
- Something went wrong → retrospective track
- About to commit to something → adversarial track
- Don't know what we don't know → epistemic track
- Incentives are misaligned / need to design rules → strategic track

**Domain complexity** (if unclear, assign `unknown` and include `cynefin-framework` in Step 2):
- Clear / Complicated / Complex / Chaotic / Unknown

Write the triage output in this format before moving to Step 2:
```
TRIAGE
Temporal: [forward / present / backward]
Maturity: [label]
Obstacle: [label] → [track]
Domain: [label]
```

---

### STEP 2 — Build the Execution Plan (do this yourself, no skill file needed)

Using the triage output and the routing table below, produce a numbered execution plan. Label each step as `SEQUENTIAL` or `PARALLEL`. Do not execute anything yet.

**Routing table — entry points by obstacle:**

| Obstacle | Execution plan |
|----------|---------------|
| Don't know what we're dealing with | PARALLEL: epistemic-mapping ∥ cynefin-framework ∥ cognitive-bias-detection → re-triage |
| Don't understand the system / why it's failing | PARALLEL: systems-thinking ∥ theory-of-constraints ∥ causal-inference → SEQUENTIAL: five-whys-root-cause → decision-synthesis |
| Don't understand the system / strategic agents involved | PARALLEL: systems-thinking ∥ game-theoretic-analysis ∥ causal-inference → SEQUENTIAL: five-whys-root-cause → decision-synthesis |
| Plan / design needs validation | PARALLEL: inversion-premortem ∥ red-teaming ∥ second-order-thinking → SEQUENTIAL: cognitive-bias-detection → decision-synthesis |
| Plan / design needs validation + ethical review | PARALLEL: inversion-premortem ∥ red-teaming ∥ ethical-reasoning → SEQUENTIAL: cognitive-bias-detection → decision-synthesis |
| Stuck, all solutions feel the same | SEQUENTIAL: epistemic-mapping → PARALLEL: lateral-thinking ∥ analogical-thinking ∥ first-principles-thinking → SEQUENTIAL: inversion-premortem → decision-synthesis |
| Need to decide between options | PARALLEL: scenario-planning ∥ probabilistic-thinking ∥ fermi-estimation → decision-synthesis |
| Need to decide between options + financial | PARALLEL: scenario-planning ∥ probabilistic-thinking ∥ fermi-estimation → SEQUENTIAL: financial-modeling → decision-synthesis |
| Something went wrong / post-mortem | SEQUENTIAL: retrospective-counterfactual → PARALLEL: five-whys-root-cause ∥ causal-inference → SEQUENTIAL: cognitive-bias-detection |
| Software bug / unexpected behavior | SEQUENTIAL: debugging-methodology → PARALLEL: five-whys-root-cause ∥ causal-inference → decision-synthesis |
| Long-term strategic commitment | PARALLEL: epistemic-mapping ∥ cognitive-bias-detection ∥ cynefin-framework → PARALLEL: scenario-planning ∥ probabilistic-thinking ∥ fermi-estimation → PARALLEL: inversion-premortem ∥ red-teaming ∥ second-order-thinking → PARALLEL: stakeholder-power-mapping ∥ game-theoretic-analysis → decision-synthesis |
| Blocked / people won't adopt | PARALLEL: stakeholder-power-mapping ∥ game-theoretic-analysis ∥ second-order-thinking ∥ causal-inference → decision-synthesis |
| Incentives misaligned / need to design rules | SEQUENTIAL: game-theoretic-analysis → PARALLEL: second-order-thinking ∥ red-teaming → SEQUENTIAL: stakeholder-power-mapping → decision-synthesis |
| Need to negotiate or reach agreement | SEQUENTIAL: game-theoretic-analysis → SEQUENTIAL: negotiation-strategy → difficult-conversations (if escalation needed) |
| Need to communicate or persuade | SEQUENTIAL: argument-craft → execution-planning (if action follows) |
| Need to build a business case | SEQUENTIAL: fermi-estimation → SEQUENTIAL: financial-modeling → SEQUENTIAL: scenario-planning → SEQUENTIAL: argument-craft |
| Need to validate a hypothesis | SEQUENTIAL: epistemic-mapping → SEQUENTIAL: experimental-design → [run experiment] → SEQUENTIAL: causal-inference → SEQUENTIAL: evidence-synthesis → decision-synthesis |
| Need to learn a new domain | SEQUENTIAL: epistemic-mapping → SEQUENTIAL: learning-strategy → [learning] → SEQUENTIAL: evidence-synthesis → decision-synthesis |
| Decision needs to be executed | SEQUENTIAL: decision-synthesis → SEQUENTIAL: argument-craft → SEQUENTIAL: execution-planning |
| Architecture decision needed | SEQUENTIAL: systems-thinking → SEQUENTIAL: architecture-evaluation → PARALLEL: inversion-premortem ∥ red-teaming → decision-synthesis → execution-planning |
| Process is slow / broken / needs redesign | PARALLEL: systems-thinking ∥ theory-of-constraints → SEQUENTIAL: process-design → execution-planning |
| Need to run a meeting or workshop | SEQUENTIAL: facilitation-design |
| Need to tell a compelling story | SEQUENTIAL: argument-craft → SEQUENTIAL: narrative-construction |
| Need to assess fairness or equity | SEQUENTIAL: ethical-reasoning → SEQUENTIAL: fairness-auditing → decision-synthesis |
| Synthesize evidence from multiple sources | SEQUENTIAL: evidence-synthesis → decision-synthesis |
| Need to create or improve agent instructions | SEQUENTIAL: context-gap-analyzer → SEQUENTIAL: agent-instruction-forge → SEQUENTIAL: edd (to validate) |

Write the plan in this format:
```
EXECUTION PLAN
Step 1 — PARALLEL: [skill-a] ∥ [skill-b] ∥ [skill-c]
Step 2 — SEQUENTIAL: [skill-d]
Step 3 — PARALLEL: [skill-e] ∥ [skill-f]
Step 4 — SEQUENTIAL: [skill-g]
```

---

### STEP 3 — Execute the Plan (step by step, never all at once)

Work through the execution plan one step at a time. For each step:

#### For a SEQUENTIAL step:

1. **Read the skill file**:
   ```
   view: skills/[skill-name]/SKILL.md
   ```
2. **Apply the skill** to the current problem context, following the methodology in that file exactly
3. **Write the output** in the skill's output format
4. **Write the routing decision**:
   ```
   STEP [N] COMPLETE — SEQUENTIAL: [skill-name]
   Key finding: [1–2 sentences]
   Routing to Step [N+1]: [reason based on finding]
   ```
5. Proceed to the next step

#### For a PARALLEL step:

1. **Spawn one subagent per skill** using the Task tool. Each subagent receives:
   - The full problem description
   - Any findings from prior sequential steps
   - This instruction: *"Read skills/[skill-name]/SKILL.md then apply that skill's full methodology to the problem. Output your findings in that skill's output format. Do not perform other reasoning."*

2. **Wait for all subagents to complete**

3. **Synthesize their outputs**:
   ```
   SYNTHESIS — Step [N] PARALLEL: [skill-a] ∥ [skill-b] ∥ [skill-c]

   Convergent findings (2+ skills agree — higher confidence):
   - [finding]

   Divergent findings (1 skill only — worth noting):
   - [finding] (from [skill])

   Contradictions (skills disagree — resolve before proceeding):
   - [skill-a] says [X], [skill-b] says [Y] → resolution: [...]

   Key inputs for Step [N+1]: [what the next step needs]
   ```

4. Proceed to the next step

---

### STEP 4 — Terminate

Stop when any of these conditions are met:
- `decision-synthesis` has completed and produced a decision with acceptable confidence
- The problem is understood well enough to act without further analysis
- **If 4+ steps have run without converging**: stop, flag the problem as likely unframed, restart from Step 1 with `epistemic-mapping` as the only entry point

Write the termination output:
```
CHAIN COMPLETE
Steps executed: [list with SEQUENTIAL/PARALLEL labels]
Key finding: [1–2 sentences]
Recommended action: [what to do now]
```

---

## Parallelization Reference

These five clusters are the canonical parallel groups. Skills within a cluster apply independent lenses and never depend on each other's output.

| Pattern | Skills | Use when |
|---------|--------|---------|
| P1 — Adversarial | inversion-premortem ∥ red-teaming ∥ second-order-thinking | Validating a plan before commitment |
| P2 — Generative | lateral-thinking ∥ analogical-thinking ∥ first-principles-thinking | Stuck, need new options |
| P3 — Diagnostic | systems-thinking ∥ theory-of-constraints ∥ causal-inference | System is failing, need to understand why |
| P4 — Uncertainty | scenario-planning ∥ probabilistic-thinking ∥ fermi-estimation | Decision needs quantification |
| P5 — Meta-cognitive | epistemic-mapping ∥ cognitive-bias-detection ∥ cynefin-framework | Clean the reasoning environment first |
| P6 — Strategic | game-theoretic-analysis ∥ stakeholder-power-mapping ∥ second-order-thinking | Multiple agents with competing incentives |

---

## Post-Step Routing Reference

After completing any step, use this table to adjust the plan if findings warrant it:

| Completed skill | Finding | Adjust plan to include |
|----------------|---------|----------------------|
| epistemic-mapping | Dangerous assumptions found | first-principles-thinking (sequential, next) |
| cynefin-framework | Domain = Complex | lateral-thinking ∥ scenario-planning (parallel) instead of structured analysis |
| cynefin-framework | Domain = Chaotic | Act immediately; retrospective-counterfactual after stabilization |
| stakeholder-power-mapping | Strategic agents with conflicting incentives | game-theoretic-analysis (sequential) |
| game-theoretic-analysis | Nash Equilibrium ≠ Pareto Optimum | Mechanism design needed — decision-synthesis with design constraints |
| game-theoretic-analysis | Information asymmetry identified | red-teaming on exploitability (sequential) |
| game-theoretic-analysis | Repeated game dynamics | second-order-thinking on reputation effects (sequential) |
| systems-thinking | Bottleneck identified | theory-of-constraints (sequential) |
| five-whys-root-cause | Root cause is causal claim | causal-inference (sequential) |
| five-whys-root-cause | Multiple root causes | decision-synthesis (sequential, to prioritize) |
| adversarial panel (P1) | High-severity risks | cognitive-bias-detection on the risk analysis (sequential) |
| generative panel (P2) | All options weak | epistemic-mapping — frame may be wrong (sequential, restart) |
| uncertainty panel (P4) | High uncertainty persists | inversion-premortem on worst-case scenario (sequential) |
| decision-synthesis | Key assumption too uncertain | epistemic-mapping → validate before committing |
| decision-synthesis | Decision made, needs communication | argument-craft (sequential) |
| decision-synthesis | Decision made, needs execution | execution-planning (sequential) |
| decision-synthesis | Ethical criteria needed | ethical-reasoning (sequential, before re-running decision-synthesis) |
| decision-synthesis | Financial criteria needed | financial-modeling (sequential, before re-running decision-synthesis) |
| argument-craft | Audience won't be convinced by logic alone | narrative-construction (sequential) |
| argument-craft | Decision committed, ready to execute | execution-planning (sequential) |
| execution-planning | Resources/timeline need approval | argument-craft (sequential, resource ask) |
| negotiation-strategy | Emotional stakes or power asymmetry too high | difficult-conversations (sequential) |
| ethical-reasoning | Systemic/algorithmic fairness concerns | fairness-auditing (sequential) |
| architecture-evaluation | Architecture decided | execution-planning (sequential) |
| debugging-methodology | Root cause identified as causal claim | causal-inference (sequential) |
| debugging-methodology | Root cause is structural | five-whys-root-cause ∥ systems-thinking (parallel) |
| experimental-design | Experiment complete, results ready | causal-inference (sequential) |
| evidence-synthesis | Evidence synthesized, decision needed | decision-synthesis (sequential) |
| learning-strategy | Learning complete, sources to integrate | evidence-synthesis (sequential) |
| financial-modeling | Scenarios need stress-testing | scenario-planning (sequential) |
| process-design | Process designed, needs implementation | execution-planning (sequential) |
| retrospective-counterfactual | Systemic cause found | systems-thinking ∥ five-whys-root-cause (parallel) |

---

## Skill Registry

| Skill | File path | Parallelizes with |
|-------|-----------|------------------|
| epistemic-mapping | skills/epistemic-mapping/SKILL.md | cynefin-framework, cognitive-bias-detection |
| cynefin-framework | skills/cynefin-framework/SKILL.md | epistemic-mapping, cognitive-bias-detection |
| systems-thinking | skills/systems-thinking/SKILL.md | theory-of-constraints, causal-inference |
| theory-of-constraints | skills/theory-of-constraints/SKILL.md | systems-thinking, causal-inference |
| five-whys-root-cause | skills/five-whys-root-cause/SKILL.md | causal-inference |
| causal-inference | skills/causal-inference/SKILL.md | systems-thinking, five-whys-root-cause |
| cognitive-bias-detection | skills/cognitive-bias-detection/SKILL.md | epistemic-mapping, cynefin-framework |
| inversion-premortem | skills/inversion-premortem/SKILL.md | red-teaming, second-order-thinking |
| red-teaming | skills/red-teaming/SKILL.md | inversion-premortem, second-order-thinking |
| second-order-thinking | skills/second-order-thinking/SKILL.md | inversion-premortem, red-teaming |
| probabilistic-thinking | skills/probabilistic-thinking/SKILL.md | scenario-planning, fermi-estimation |
| fermi-estimation | skills/fermi-estimation/SKILL.md | probabilistic-thinking, scenario-planning |
| scenario-planning | skills/scenario-planning/SKILL.md | probabilistic-thinking, fermi-estimation |
| stakeholder-power-mapping | skills/stakeholder-power-mapping/SKILL.md | second-order-thinking, causal-inference, game-theoretic-analysis |
| game-theoretic-analysis | skills/game-theoretic-analysis/SKILL.md | stakeholder-power-mapping, second-order-thinking, causal-inference |
| lateral-thinking | skills/lateral-thinking/SKILL.md | analogical-thinking, first-principles-thinking |
| analogical-thinking | skills/analogical-thinking/SKILL.md | lateral-thinking, first-principles-thinking |
| first-principles-thinking | skills/first-principles-thinking/SKILL.md | lateral-thinking, analogical-thinking |
| decision-synthesis | skills/decision-synthesis/SKILL.md | runs after all others |
| decision-intelligence | skills/decision-intelligence/SKILL.md | standalone (single-option evaluation) |
| retrospective-counterfactual | skills/retrospective-counterfactual/SKILL.md | five-whys-root-cause, causal-inference |
| execution-planning | skills/execution-planning/SKILL.md | runs after decision-synthesis or architecture-evaluation |
| argument-craft | skills/argument-craft/SKILL.md | runs after decision-synthesis or scenario-planning |
| ethical-reasoning | skills/ethical-reasoning/SKILL.md | inversion-premortem, red-teaming (parallel validation) |
| experimental-design | skills/experimental-design/SKILL.md | runs after epistemic-mapping |
| negotiation-strategy | skills/negotiation-strategy/SKILL.md | runs after game-theoretic-analysis |
| difficult-conversations | skills/difficult-conversations/SKILL.md | runs after negotiation-strategy or stakeholder-power-mapping |
| financial-modeling | skills/financial-modeling/SKILL.md | runs after fermi-estimation |
| architecture-evaluation | skills/architecture-evaluation/SKILL.md | runs after systems-thinking |
| evidence-synthesis | skills/evidence-synthesis/SKILL.md | runs after causal-inference or learning-strategy |
| learning-strategy | skills/learning-strategy/SKILL.md | runs after epistemic-mapping |
| process-design | skills/process-design/SKILL.md | runs after systems-thinking, theory-of-constraints |
| debugging-methodology | skills/debugging-methodology/SKILL.md | standalone entry point for software bugs |
| facilitation-design | skills/facilitation-design/SKILL.md | standalone (produces session plan) |
| narrative-construction | skills/narrative-construction/SKILL.md | runs after argument-craft |
| fairness-auditing | skills/fairness-auditing/SKILL.md | runs after ethical-reasoning |
| agent-instruction-forge | skills/agent-instruction-forge/SKILL.md | runs after context-gap-analyzer |
