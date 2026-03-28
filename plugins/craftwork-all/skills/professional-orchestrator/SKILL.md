---
name: professional-orchestrator
description: Entry point for professional skills — architecture, communication, process design, ethics, and leadership. Routes to the right skill based on what the user needs. Use this when the user's goal involves a professional discipline but they haven't named a specific skill.
---

# Professional Orchestrator

**This skill routes — it does not reason.** Read the user's intent, match it to an entry point below, then execute that skill's SKILL.md.

---

## Step 1 — Match the User's Intent

Read what the user wants to do and match it to the closest entry below. If ambiguous, ask one clarifying question.

| User wants to... | Start with | Then |
|---|---|---|
| **Architecture & Engineering** | | |
| Evaluate or choose between architectures | `architecture-evaluation` | → `execution-planning` |
| Debug a software failure systematically | `debugging-methodology` | → `casual-inference` if root cause is causal |
| Design or run an experiment | `experimental-design` | → `casual-inference` after results |
| Review code or a PR | `code-review-amplifier` | done |
| **Planning & Execution** | | |
| Break a decision into an action plan | `execution-planning` | done |
| Design or improve a workflow/process | `process-design` | → `execution-planning` |
| Build a financial model or business case | `financial-modeling` | → `argument-craft` |
| **Writing & Communication** | | |
| Write an RFC, design doc, ADR, runbook, postmortem, one-pager, or announcement | `technical-writing` | → `narrative-construction` if storytelling needed |
| Structure a recommendation or argument | `argument-craft` | → `technical-writing` to write it up |
| Tell a compelling story from analysis | `narrative-construction` | done |
| Prepare for a negotiation | `negotiation-strategy` | → `difficult-conversations` if high stakes |
| Navigate a difficult conversation | `difficult-conversations` | done |
| Design a meeting or workshop | `facilitation-design` | done |
| **People & Organizations** | | |
| Map stakeholder influence and blockers | `stakeholder-power-mapping` | → `negotiation-strategy` or `difficult-conversations` |
| Ramp up on a new domain | `learning-strategy` | → `topic-explainer` for specific concepts |
| Understand or learn a concept, technology, or idea | `topic-explainer` | → `technical-writing` to document it |
| **Ethics & Fairness** | | |
| Surface moral implications of a decision | `ethical-reasoning` | → `fairness-auditing` if systemic concerns |
| Audit a system for equitable outcomes | `fairness-auditing` | → `argument-craft` to present findings |
| Determine causation vs correlation | `casual-inference` | done |

---

## Step 2 — Execute

1. Read `skills/[skill-name]/SKILL.md`
2. Apply that skill's full methodology
3. When the skill completes, check the "Then" column above — if a follow-up is indicated and the findings match, read and execute the next skill

---

## Canonical Chains

**Architecture decision:**
```
architecture-evaluation → argument-craft → execution-planning
```
Use when making and implementing a system design choice.

**Building a business case:**
```
financial-modeling → argument-craft → execution-planning
```
Use when you need numbers, then narrative, then action.

**Navigating organizational resistance:**
```
stakeholder-power-mapping → negotiation-strategy → difficult-conversations
```
Use when people are blocking progress and you need to understand why and how to move them.

**Process improvement:**
```
process-design → execution-planning
```
Use when a workflow is slow or broken.

**Documenting a technical decision:**
```
architecture-evaluation → technical-writing (ADR or RFC)
```
Use when an architecture decision needs to be written up for review or posterity.

**Ethics review:**
```
ethical-reasoning → fairness-auditing → argument-craft
```
Use when a system needs moral and equity analysis, then communication of findings.

---

## Skill Registry

| Skill | Purpose |
|-------|---------|
| `architecture-evaluation` | Evaluate system design decisions, produce ADRs |
| `code-review-amplifier` | Structured pre-scanning for human code reviewers |
| `debugging-methodology` | Systematic debugging: reproduce, observe, hypothesize, isolate |
| `execution-planning` | Decompose decisions into executable plans |
| `experimental-design` | Design rigorous experiments to validate assumptions |
| `process-design` | Design workflows using Lean and value stream analysis |
| `financial-modeling` | Unit economics, cost-benefit, NPV/IRR, scenario modeling |
| `argument-craft` | Structure recommendations into persuasive arguments |
| `narrative-construction` | Turn analysis into compelling stories |
| `negotiation-strategy` | Prepare for negotiations with BATNA, ZOPA, concession planning |
| `difficult-conversations` | Navigate conflict, feedback, emotionally charged discussions |
| `facilitation-design` | Design meetings and workshops that produce decisions |
| `stakeholder-power-mapping` | Map influence networks and design engagement strategies |
| `ethical-reasoning` | Surface moral implications using multiple ethical frameworks |
| `fairness-auditing` | Audit systems for equitable outcomes across groups |
| `learning-strategy` | Build structured plans for closing knowledge gaps |
| `casual-inference` | Distinguish causation from correlation |
| `technical-writing` | Write RFCs, design docs, ADRs, runbooks, postmortems, announcements |
| `topic-explainer` | Explain concepts, technologies, or ideas using the best style for the topic |
