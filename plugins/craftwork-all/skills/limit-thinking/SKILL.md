---
name: limit-thinking
description: "Apply limit thinking whenever the user wants to understand what happens when a variable, parameter, or condition is pushed toward its extreme — zero, infinity, 100%, or any boundary. Triggers on phrases like 'what happens if we scale this?', 'what if everyone adopts this?', 'where does this break?', 'what's the ceiling?', 'how does this behave at the extreme?', 'what does this converge to?', 'what if we push this to the max?', 'what's the asymptote?', or any situation where the user is evaluating a system, strategy, rollout, or design by exploring its trajectory rather than its current state. Also trigger when someone is making a decision based on a snapshot ('should we do X?') but hasn't examined the trajectory ('what does X converge to at scale?'). This skill catches the blind spot of static evaluation — most planning failures come from reasoning about where things are, not where things are going. Use this before any scaling decision, rollout plan, or growth strategy."
---

# Limit Thinking

**Core principle**: Don't ask "what is the value at this point?" — ask "what does this converge to as we push the variable toward its extreme?" Most planning failures happen because people evaluate a snapshot instead of a trajectory. Limit thinking reveals the destination that incremental progress is silently heading toward.

The mathematical concept of a limit — studying what a function *approaches* rather than where it *is* — is a powerful reasoning tool far beyond calculus. It exposes asymptotes, phase transitions, and convergence traps hiding inside seemingly linear plans.

---

## How to Execute This Skill

### STEP 1 — Identify the Variables

For the system, decision, or strategy being evaluated, identify the key variables that could be pushed toward an extreme.

```
LIMIT ANALYSIS SETUP
System: [what's being evaluated]
Variables to push:
  - Variable 1: [what is it?] → Push toward: [0 / ∞ / 100% / some boundary]
  - Variable 2: [what is it?] → Push toward: [0 / ∞ / 100% / some boundary]
  - Variable 3: [what is it?] → Push toward: [0 / ∞ / 100% / some boundary]

For each: What does intuition say happens? (This is the naive expectation to test.)
```

Good variables to push include:
- **Adoption rate** → 100% ("what if everyone uses this?")
- **Automation level** → total ("what if no human is in the loop?")
- **Scale** → orders of magnitude ("what if we 10x or 100x this?")
- **Time** → long horizon ("what does this look like in 5 years?")
- **Cost** → zero ("what if this becomes free?")
- **Speed** → instant ("what if latency drops to zero?")
- **Volume** → extreme ("what if input grows without bound?")

#### Selecting Variables: The 2-3 Rule

A vague or ambitious prompt ("scale AI across the org", "go all-in on microservices") can generate 5+ candidate variables. Tracing all of them produces an exhaustive but overwhelming analysis. Instead, identify all candidates first, then select the **2-3 most critical** using these filters:

1. **Highest leverage**: If pushed to the extreme, produces the most consequential or irreversible outcome?
2. **Most hidden**: Which variable's limit behavior would most surprise the decision-makers? (Variables where naive expectation ≈ actual convergence aren't worth tracing — they teach nothing.)
3. **Most coupled**: Which variable's limit behavior affects the other variables? (Trace the upstream variable first — its limit may redefine the others.)

List all candidates, mark the 2-3 you'll trace, and briefly note why the others are deprioritized. This keeps the analysis focused and the output actionable.

---

### STEP 2 — Trace the Convergence

For each variable, don't jump to the extreme — *approach it incrementally* and watch what happens. This is where the insight lives.

```
CONVERGENCE TRACE: [Variable] → [Extreme]

Current state: [where things are now]
  ↓ Push slightly...
Incremental: [what improves or changes — usually positive]
  ↓ Push further...
Midpoint: [what secondary effects appear — often the first sign of non-linearity]
  ↓ Push toward extreme...
Near-limit: [what breaks, saturates, or reverses — the real finding]
  ↓ At the limit...
Convergence: [variable] → [extreme] means [outcome] → [what it converges to]

Does the outcome converge to what intuition predicted? YES / NO
If NO — what's the actual limit, and why is it counterintuitive?
```

**Key patterns to watch for:**

| Pattern | What it looks like | Example |
|---|---|---|
| **Asymptotic ceiling** | Returns diminish and flatten. You approach a maximum but never reach it. | Adding more engineers to a team: productivity asymptotes, then declines (Brooks's Law) |
| **Phase transition** | The system changes state entirely at some threshold. No amount of incremental change prepares you for the discontinuity. | Water at 100°C: more heat doesn't make it "hotter water" — it becomes steam. Org maturity hitting L4: more tools don't help, you need structural change |
| **Reversal / collapse** | The variable's effect flips sign. What was helping starts hurting. | Context in an agent: more context helps until it doesn't, then success rate drops (ETH Zurich finding). Automation of review: reduces burden until reviewers disengage entirely |
| **Convergence to zero** | A human quality (attention, responsibility, skill) atrophies as the system takes over. | Pilots and autopilot: the more autopilot flies, the less skilled pilots become at manual flight — the limit of pilot skill as automation → 100% is dangerously low |
| **Divergence** | No stable limit exists. The system oscillates or explodes. | Feedback loops without damping: over-correction → under-correction → chaos |

---

### STEP 3 — Extract the Insight

The value of limit thinking is the delta between naive expectation and actual convergence. State it explicitly:

```
LIMIT INSIGHT

Naive expectation: "If we push [variable] toward [extreme], [outcome] will [improve/increase/get better]."

Actual convergence: As [variable] → [extreme], [outcome] → [surprising result].

The delta: [Why the actual limit differs from expectation.
            What force, feedback loop, or phase transition causes the divergence?]

Implication for the decision: [What should change about the plan, strategy, or design
                               given that the trajectory leads somewhere unexpected?]
```

---

### STEP 4 — Find the Optimal Operating Point

Limit thinking doesn't just reveal where things break — it helps find where to *stop pushing*. If the convergence trace shows diminishing returns, reversal, or collapse past a certain point, that inflection point is the practical operating target.

```
OPERATING POINT ANALYSIS

Variable: [what we're tuning]
Benefit curve: [how benefit changes as variable increases]
Inflection point: [where marginal benefit starts declining significantly]
Recommended range: [where to operate, stated as a range not a precise number]
Signal to watch: [what early indicator tells you you've pushed past the optimal point]
```

---

## Output Format

### Variables and Extremes
List each variable being pushed and toward what extreme.

### Convergence Traces
For each variable, the incremental trace from current state to limit:
- What the naive trajectory predicts
- Where secondary effects appear
- What the system actually converges to

### Limit Insights
For each trace where actual ≠ expected:
- The delta between expectation and reality
- The mechanism causing the divergence
- Why this matters for the decision at hand

### Optimal Operating Points
Where to operate if the limit reveals diminishing returns or reversal:
- The recommended range
- The early warning signal

### Implications
What changes about the plan, strategy, or design given these convergence findings.

---

## Thinking Triggers

Use these to sharpen the analysis:
- *"If we push this variable all the way, what does the outcome actually converge to?"*
- *"Is this a linear improvement, or does it hit a ceiling / flip / collapse at some point?"*
- *"We're reasoning about a snapshot — what does the trajectory look like?"*
- *"What human quality atrophies as we automate this further?"*
- *"Is there a phase transition hiding between here and the extreme?"*
- *"Everyone is debating the current state — but where is this heading?"*
- *"What would a mathematician say the limit of this function is?"*

---

## Example Applications

- **"Let's roll out AI code review to 100% of PRs"** → Trace automation → 100%: reviewer attention converges to zero, critical thinking atrophies, the review becomes a checkbox
- **"Let's add more context to the AI agent"** → Trace context volume → ∞: performance improves then degrades, signal-to-noise ratio collapses past the optimum
- **"Let's hire more engineers to go faster"** → Trace team size → large: communication overhead grows quadratically, velocity per engineer converges toward zero (Brooks's Law)
- **"Let's reduce meeting time to maximize focus"** → Trace meetings → 0: alignment gaps emerge, decisions happen in silos, rework increases until net productivity is worse
- **"Let's make the product free for adoption"** → Trace price → 0: adoption explodes but perceived value converges to zero, support costs diverge, unit economics collapse
- **"Let's keep investing monthly regardless of market"** → Trace time → long: dollar-cost averaging smooths volatility, compounding dominates, the limit of a disciplined PAC is wealth accumulation despite short-term noise

---

## Relationship to Other Skills

- **Second-order thinking**: Limit thinking is complementary — second-order asks "and then what?" for a single step; limit thinking asks "where does this end up?" across the full trajectory. Use limit thinking to set the destination, second-order thinking to trace the path.
- **First principles**: If limit thinking reveals a ceiling or collapse, first-principles thinking can question whether the variable being pushed is the right one at all.
- **Scenario planning**: Limit thinking can feed scenario planning by identifying the extremes that define the scenario space.
- **Theory of constraints**: If a variable hits an asymptotic ceiling, TOC can identify the constraint that creates the ceiling.
