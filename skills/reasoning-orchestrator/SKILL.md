---
name: reasoning-orchestrator
description: "Apply this skill first whenever the user presents a problem, question, or situation that requires structured thinking — before reaching for any specific reasoning framework. Triggers on any substantive request to evaluate, analyze, diagnose, decide, design, improve, understand, or learn from something. This is the entry point for the reasoning skill collection: it reads the situation, selects the right skill(s) to apply, sequences them, routes between them based on what each run surfaces, and determines whether skills should run sequentially or in parallel via subagents. If you're unsure which reasoning skill to use, always start here."
---

# Reasoning Orchestrator

**Role**: Triage the situation. Select the right reasoning framework(s). Sequence them. Route between them based on what each step reveals. Spawn subagents to run independent skills in parallel when the analysis allows it.

Skills stay pure — they do one thing well. This orchestrator holds the chaining logic and the execution model.

---

## Execution Model

Before planning the skill sequence, decide the execution mode for each step:

### Sequential Execution
Use when the output of one skill is the **input** of the next. The chain is data-dependent — you can't run step N until step N-1 has completed.

```
[Skill A] → (output feeds) → [Skill B] → (output feeds) → [Skill C]
```

### Parallel Execution via Subagents
Use when multiple skills apply **independent lenses to the same input**. They don't depend on each other — they run simultaneously and their outputs are synthesized afterward.

```
                    ┌─ [Skill B: subagent] ─┐
[Shared context] →  ├─ [Skill C: subagent] ─┼→ [Synthesize] → [Next step]
                    └─ [Skill D: subagent] ─┘
```

**Spawn a subagent when:**
- The skill applies an independent perspective on the same problem
- Its output doesn't depend on outputs from sibling skills in the same parallel block
- Running it in parallel saves meaningful time
- The synthesis step is clearly defined before spawning

**Keep sequential when:**
- The skill needs the output of a previous skill as its primary input
- Only 2 skills remain (parallelization overhead not worth it)
- Outputs would be too difficult to synthesize meaningfully

---

## Parallelization Patterns

Five canonical parallel clusters — groups of skills that apply independent lenses to the same input and should always be spawned as subagents:

### Pattern P1: Adversarial Panel
*Use when validating a plan, design, or decision before commitment.*

```
                    ┌─ [inversion-premortem]  ─┐
[Plan / design] →   ├─ [red-teaming]           ─┼→ synthesize risk register → [decision-synthesis]
                    └─ [second-order-thinking] ─┘
```

Each subagent receives the full plan. Outputs merged into a unified risk register: failure modes + attack surfaces + unintended consequences.

### Pattern P2: Generative Panel
*Use when stuck — all solutions feel like variations of the same idea.*

```
                    ┌─ [lateral-thinking]         ─┐
[Problem frame] →   ├─ [analogical-thinking]      ─┼→ pool options → [inversion-premortem] on best candidates
                    └─ [first-principles-thinking] ─┘
```

Each subagent generates alternatives independently — more diverse than running them sequentially. All options pooled before evaluation.

### Pattern P3: Diagnostic Panel
*Use when a system is failing and you need to understand why from multiple angles.*

```
                    ┌─ [systems-thinking]      ─┐
[Failing system] →  ├─ [theory-of-constraints] ─┼→ synthesize → [five-whys-root-cause] on convergent findings
                    └─ [causal-inference]       ─┘
```

Systems thinking maps structure, ToC finds the throughput limit, causal inference validates which changes actually caused failure. All three run on the same system description.

### Pattern P4: Uncertainty Panel
*Use when a decision needs quantification before committing.*

```
                        ┌─ [scenario-planning]      ─┐
[Strategic decision] →  ├─ [probabilistic-thinking] ─┼→ synthesize → [decision-synthesis]
                        └─ [fermi-estimation]        ─┘
```

Scenario planning maps futures, probabilistic thinking calibrates confidence, Fermi estimation grounds the numbers. All independent of each other.

### Pattern P5: Meta-Cognitive Panel
*Use at the start of any high-stakes analysis to clean the reasoning environment.*

```
                    ┌─ [epistemic-mapping]        ─┐
[Problem + context] ├─ [cognitive-bias-detection] ─┼→ synthesize → proceed with clean frame
                    └─ [cynefin-framework]         ─┘
```

Maps what's known/unknown, audits the reasoning for distortion, classifies the domain — three fully independent assessments of the same input.

---

## Subagent Spawn Instructions

When spawning parallel subagents, each receives:
1. **Shared context**: Full problem description, relevant constraints, prior findings
2. **Assigned skill**: Which reasoning framework to apply
3. **Output contract**: What format/structure the synthesis step expects

### Subagent prompt template
```
You are a reasoning specialist applying the [SKILL_NAME] framework.

Context:
[Full problem description]

Prior findings (if any):
[Outputs from sequential steps that preceded this parallel block]

Your task:
Apply [SKILL_NAME] to the above. Follow the skill's full methodology and output format.
Focus on: [specific angle this skill covers in the parallel cluster]

Do not wait for or reference other specialists running in parallel.
```

### Synthesis step after parallel execution
```
Synthesis from [Pattern PX]:

Convergent findings (2+ skills agree) → higher confidence, prioritize:
- [Finding]

Divergent findings (one skill only) → worth noting, lower confidence:
- [Finding from skill X]

Contradictions (skills disagree) → flag for explicit resolution:
- [Skill A says X, Skill B says Y]

Inputs for next step: [what the next sequential skill needs]
```

---

## Step 1: Situation Triage

Classify the request across four dimensions:

### 1a. Temporal Direction
- **Forward-looking**: Planning, designing, deciding what to do next
- **Present-state**: Understanding how something works right now
- **Backward-looking**: Learning from something that already happened

### 1b. Problem Maturity
- **Unframed**: The problem itself may not be correctly defined yet
- **Framed, unsolved**: Problem is understood, solution is not
- **Solved, needs validation**: Solution exists, needs stress-testing
- **Decided, needs learning**: Something happened, extract signal

### 1c. Primary Obstacle
- **Don't understand the system** → diagnostic track
- **Understand it, stuck on solutions** → generative track
- **Have solutions, need to choose** → convergence track
- **Something went wrong** → retrospective track
- **About to commit to something** → adversarial track
- **Don't know what we don't know** → epistemic track

### 1d. Domain Complexity
- **Clear**: Known solution exists → apply directly, no skill needed
- **Complicated**: Expertise + analysis required → structured skill application
- **Complex**: Emergent, unpredictable → probe-first approaches
- **Chaotic**: Crisis → act first, analyze after

*If domain is unclear, run `cynefin-framework` before anything else.*

---

## Step 2: Skill Selection and Execution Plan

### Entry Points by Situation

**"We don't know what we're dealing with yet"**
```
PARALLEL (P5): [epistemic-mapping] ∥ [cynefin-framework] ∥ [cognitive-bias-detection]
→ synthesize → re-triage with clean frame
```

**"We need to understand how this system works / why it's failing"**
```
PARALLEL (P3): [systems-thinking] ∥ [theory-of-constraints] ∥ [causal-inference]
→ synthesize → SEQUENTIAL: [five-whys-root-cause] on convergent findings
→ [decision-synthesis]
```

**"We have a plan / design / decision and want to validate it"**
```
PARALLEL (P1): [inversion-premortem] ∥ [red-teaming] ∥ [second-order-thinking]
→ synthesize risk register → SEQUENTIAL: [cognitive-bias-detection] on analysis
→ [decision-synthesis]
```

**"We're stuck, all solutions feel like variations of the same idea"**
```
SEQUENTIAL: [epistemic-mapping]  ← clean the frame first
→ PARALLEL (P2): [lateral-thinking] ∥ [analogical-thinking] ∥ [first-principles-thinking]
→ pool options → SEQUENTIAL: [inversion-premortem] on best candidates
→ [decision-synthesis]
```

**"We need to decide between options but can't land"**
```
PARALLEL (P4): [scenario-planning] ∥ [probabilistic-thinking] ∥ [fermi-estimation]
→ synthesize → [decision-synthesis]
```

**"Something already went wrong / post-mortem"**
```
SEQUENTIAL: [retrospective-counterfactual]  ← establish what happened first
→ PARALLEL: [five-whys-root-cause] ∥ [causal-inference]
→ synthesize → SEQUENTIAL: [cognitive-bias-detection] on findings
→ [epistemic-mapping] to update beliefs
```

**"We're about to make a long-term strategic commitment"**
```
PARALLEL (P5): [epistemic-mapping] ∥ [cognitive-bias-detection] ∥ [cynefin-framework]
→ PARALLEL (P4): [scenario-planning] ∥ [probabilistic-thinking] ∥ [fermi-estimation]
→ PARALLEL (P1): [inversion-premortem] ∥ [red-teaming] ∥ [second-order-thinking]
→ SEQUENTIAL: [stakeholder-power-mapping]
→ [decision-synthesis]
```

**"Something keeps getting blocked / people won't adopt this"**
```
PARALLEL: [stakeholder-power-mapping] ∥ [second-order-thinking] ∥ [causal-inference]
→ synthesize → [decision-synthesis]
```

---

## Step 3: Routing Logic

After each skill or parallel cluster, route based on findings:

### From `epistemic-mapping`
| Finding | Route to | Mode |
|---------|---------|------|
| Dangerous unknown assumptions | `first-principles-thinking` | Sequential |
| Multiple knowledge gaps | `cynefin-framework` ∥ `cognitive-bias-detection` | Parallel |
| Problem framing looks wrong | `first-principles-thinking` | Sequential |
| Ready to analyze | appropriate diagnostic track | — |

### From `cynefin-framework`
| Classification | Route to | Mode |
|----------------|---------|------|
| Clear | No skill needed | — |
| Complicated | `systems-thinking` ∥ `theory-of-constraints` | Parallel |
| Complex | `lateral-thinking` ∥ `scenario-planning` | Parallel |
| Chaotic | Act first; `retrospective-counterfactual` after | Sequential |
| Disorder | `epistemic-mapping` | Sequential |

### From Diagnostic Panel (P3)
| Finding | Route to | Mode |
|---------|---------|------|
| Convergent root cause | `five-whys-root-cause` | Sequential |
| Structural loop identified | `second-order-thinking` | Sequential |
| Multiple issues to prioritize | `decision-synthesis` | Sequential |

### From Adversarial Panel (P1)
| Finding | Route to | Mode |
|---------|---------|------|
| High-severity unguarded risks | `cognitive-bias-detection` on analysis | Sequential |
| Attack surface too large | `first-principles-thinking` on the design | Sequential |
| Risks acceptable | `decision-synthesis` | Sequential |

### From Generative Panel (P2)
| Finding | Route to | Mode |
|---------|---------|------|
| Strong candidates generated | `inversion-premortem` ∥ `second-order-thinking` | Parallel |
| All options weak | `epistemic-mapping` (frame may be wrong) | Sequential |
| One clear winner | `decision-synthesis` | Sequential |

### From Uncertainty Panel (P4)
| Finding | Route to | Mode |
|---------|---------|------|
| Clear EV winner | `decision-synthesis` | Sequential |
| High uncertainty persists | `inversion-premortem` on worst case | Sequential |
| Stakeholder alignment needed | `stakeholder-power-mapping` | Sequential |

### From `five-whys-root-cause`
| Finding | Route to | Mode |
|---------|---------|------|
| Structural root cause | `systems-thinking` | Sequential |
| Causal claim needs validation | `causal-inference` | Sequential |
| Multiple root causes | `decision-synthesis` | Sequential |

### From `decision-synthesis`
| Finding | Route to | Mode |
|---------|---------|------|
| Decision made with confidence | Done | — |
| Key assumption too uncertain | `epistemic-mapping` | Sequential |
| Stakeholder alignment needed | `stakeholder-power-mapping` | Sequential |
| Post-execution | `retrospective-counterfactual` | Sequential (later) |

### From `retrospective-counterfactual`
| Finding | Route to | Mode |
|---------|---------|------|
| Systemic cause | `systems-thinking` ∥ `five-whys-root-cause` | Parallel |
| Causal claim unclear | `causal-inference` | Sequential |
| Bias in analysis | `cognitive-bias-detection` | Sequential |
| Learnings extracted | Re-triage from Step 1 | — |

---

## Step 4: Termination Conditions

Stop the chain when:
- A decision has been made via `decision-synthesis` with acceptable confidence
- The problem is understood well enough to act
- Marginal return from another skill is lower than cost of running it
- **4+ skills have run without converging** → restart from `epistemic-mapping` (problem is likely unframed)

---

## Orchestrator Output Format

**At chain start**, declare the execution plan:
```
Situation: [1-sentence classification]
Track: [diagnostic / generative / adversarial / convergence / retrospective / epistemic]
Execution plan:
  Step 1 — PARALLEL (P5): [epistemic-mapping] ∥ [cynefin-framework] ∥ [cognitive-bias-detection]
  Step 2 — SEQUENTIAL: [five-whys-root-cause] on synthesis output
  Step 3 — PARALLEL (P1): [inversion-premortem] ∥ [red-teaming] ∥ [second-order-thinking]
  Step 4 — SEQUENTIAL: [decision-synthesis]
```

**After each step**:
```
Step [N] complete — [PARALLEL/SEQUENTIAL]
Finding: [1–2 sentences]
Convergent: [what multiple subagents agreed on]
Routing to: Step [N+1] — [reason]
```

**At termination**:
```
Chain complete.
Steps: [list with parallel/sequential labels]
Key finding: [1–2 sentences]
Recommended action: [what to do now]
```

---

## Quick Reference: Skill Registry

| Skill | Primary use | Parallelizes well with |
|-------|------------|----------------------|
| `epistemic-mapping` | Map knowledge/belief/unknown territory | `cynefin-framework`, `cognitive-bias-detection` |
| `cynefin-framework` | Classify problem domain | `epistemic-mapping`, `cognitive-bias-detection` |
| `systems-thinking` | Map structural causes | `theory-of-constraints`, `causal-inference` |
| `theory-of-constraints` | Find the single bottleneck | `systems-thinking`, `causal-inference` |
| `five-whys-root-cause` | Drill to structural root cause | `causal-inference` |
| `causal-inference` | Distinguish causation from correlation | `systems-thinking`, `five-whys-root-cause` |
| `cognitive-bias-detection` | Audit reasoning for distortion | `epistemic-mapping`, `cynefin-framework` |
| `inversion-premortem` | Surface failure modes | `red-teaming`, `second-order-thinking` |
| `red-teaming` | Adversarial stress-test | `inversion-premortem`, `second-order-thinking` |
| `second-order-thinking` | Trace unintended consequences | `inversion-premortem`, `red-teaming` |
| `probabilistic-thinking` | Reason under uncertainty | `scenario-planning`, `fermi-estimation` |
| `fermi-estimation` | Quantitative estimates from decomposition | `probabilistic-thinking`, `scenario-planning` |
| `scenario-planning` | Stress-test across multiple futures | `probabilistic-thinking`, `fermi-estimation` |
| `stakeholder-power-mapping` | Map human dynamics | `second-order-thinking`, `causal-inference` |
| `lateral-thinking` | Generate non-obvious alternatives | `analogical-thinking`, `first-principles-thinking` |
| `analogical-thinking` | Transfer solutions from other domains | `lateral-thinking`, `first-principles-thinking` |
| `first-principles-thinking` | Rebuild from fundamentals | `lateral-thinking`, `analogical-thinking` |
| `decision-synthesis` | Land a decision — convergence layer | runs after all others |
| `retrospective-counterfactual` | Learn from what already happened | `five-whys-root-cause`, `causal-inference` |
