---
name: systems-thinking
description: Apply systems thinking frameworks whenever the user asks to evaluate, assess, audit, review, or analyze anything — a product, process, architecture, feature, team structure, business model, workflow, or strategy. Triggers on words like "evaluate", "assess", "analyze", "review", "is this working?", "what's wrong with", "how can we improve", "should we change", or any request to understand why something isn't performing as expected. Use this skill even when the user doesn't explicitly say "systems thinking" — if they're asking Claude to understand how something works and where it might fail, this skill should be consulted. Don't wait to be asked twice.
---

# Systems Thinking Evaluation Skill

Apply a rigorous systems lens to evaluate **what's working, what isn't, and why** in any system — technical, organizational, product, or process.

---

## When to Use This Skill

Trigger this skill whenever the user asks you to:
- Evaluate or assess a system, product, process, strategy, or architecture
- Understand why something isn't working as expected
- Identify bottlenecks, failure points, or risks
- Suggest where to intervene for the most impact
- Review a design or plan before execution

---

## Core Mental Models to Apply

### 1. Identify the System Boundary
- What's **inside** the system (in scope)?
- What's **outside** (environment, dependencies, constraints)?
- Where does the system begin and end?

### 2. Stocks and Flows
- **Stocks**: What accumulates over time? (users, debt, trust, knowledge, bugs, revenue)
- **Flows**: What increases or decreases those stocks? (acquisition, churn, learning, entropy)
- Where are flows **blocked**, **broken**, or **leaking**?

### 3. Feedback Loops
- **Reinforcing loops (R)**: Self-amplifying dynamics — virtuous cycles or vicious spirals
  - Example: More users → more content → more users (growth flywheel)
  - Example: More bugs → less trust → fewer contributors → more bugs
- **Balancing loops (B)**: Self-correcting dynamics — goal-seeking behaviors
  - Example: High load → auto-scale → stable performance
  - Example: User complaints → support → resolution → satisfaction
- Ask: Which loops **dominate** the system's current behavior?

### 4. Delays
- Where are there **time lags** between cause and effect?
- Delays often cause **oscillation**, **overcorrection**, or **invisible failures**
- Example: Hiring takes 3 months → team overloads → burnout → more attrition

### 5. System Archetypes (common failure patterns)
Match observed behavior to known archetypes:

| Archetype | Pattern | Signal |
|-----------|---------|--------|
| **Limits to Growth** | Growth hits a constraint and stalls | Plateau despite investment |
| **Fixes that Fail** | Quick fix creates new problems | Recurring issues after "solutions" |
| **Shifting the Burden** | Symptomatic fixes erode fundamental ones | Team always firefighting |
| **Tragedy of the Commons** | Shared resources are depleted | Quality/performance degrades over time |
| **Escalation** | Competing actors amplify each other | Bidding wars, arms races |
| **Drifting Goals** | Performance gap closed by lowering standards | "Good enough" keeps declining |
| **Accidental Adversaries** | Well-meaning actors undermine each other | Misaligned incentives between teams |

### 6. Leverage Points
Rank interventions by impact (from lowest to highest leverage):

1. Numbers (parameters, budgets, quotas) — **low leverage**
2. Buffer sizes and stock capacities
3. Flow rates and delays
4. Feedback loop strength
5. Information flows (who has access to what, when)
6. Rules and incentives
7. Goals of the system
8. Power to change the system's structure
9. **Mindsets and paradigms** — **highest leverage**

---

## Evaluation Output Format

When evaluating a system, structure the response as follows:

### 🟢 Where the System Works
- Identify functioning feedback loops, healthy stocks, aligned incentives
- Call out genuine strengths (not to be polite — to understand what to protect)

### 🔴 Where the System Breaks Down
- Point to broken loops, leaking flows, missing feedback, or misaligned incentives
- For each issue, name the **archetype** if one applies
- Identify **delays** that hide the problem

### ⚠️ Key Risks and Failure Modes
- What could cause the system to tip into a bad equilibrium?
- What reinforcing loop could go negative?
- What constraint will be hit next?

### 🎯 High-Leverage Interventions
- Ranked list of where to intervene
- For each: what changes, what loop or flow it affects, expected result
- Flag **quick fixes that might backfire** (Fixes that Fail archetype)

### 📊 System Diagram (optional, when helpful)
Describe or sketch a causal loop diagram in text:
```
[Variable A] → (+) [Variable B] → (+) [Variable A]  ← Reinforcing loop R1
[Variable A] → (+) [Variable C] → (-) [Variable A]  ← Balancing loop B1
```

---

## Tone and Approach

- Be **direct** about what's broken — systems evaluation is not diplomacy
- Use **concrete examples** tied to the user's specific context
- Prioritize **systemic causes** over symptoms — don't just describe what's wrong, explain *why the system produces that outcome*
- When a problem "keeps coming back," suspect a **reinforcing loop** or **Shifting the Burden** archetype
- Always suggest **at least one high-leverage intervention** — not just diagnosis

---

## Example Application Triggers

- "Evaluate our onboarding funnel" → apply stocks/flows to conversion, identify where users leak out and why
- "Why does our team keep missing deadlines?" → look for delays, Shifting the Burden, workload dynamics
- "Is this architecture scalable?" → identify capacity limits, balancing loops under load, missing circuit breakers
- "Assess our growth strategy" → find reinforcing flywheels, limits to growth constraints, escalation risks
- "What's wrong with our deploy process?" → trace flow from commit to production, find delays, balancing loops
- "Should we change our pricing model?" → map revenue stocks, customer feedback loops, competitive dynamics
