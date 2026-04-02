---
name: skill-router
description: "Scan ALL available skills before any non-trivial request. Prevents skill blindness, tunnel vision, and wrong-skill selection. Entry point for all skill-assisted work."
---

# Skill Router

Attention-recovery and composition layer. Does NOT perform tasks — scans, matches, plans. All work done by routed skills.

## Protocol

### STEP 1 — Intent Decomposition

```
Request: [one-sentence restatement]
Deliverable: [artifact or answer]
Secondary needs: [implicit — analysis, validation, formatting, org dynamics]
Domain: [technical / creative / analytical / organizational / mixed]
Complexity: [simple (1 skill) / composed (2-3) / orchestrated (4+)]
```

Rules: analysis + production = two skill needs. Decision = reasoning + output. Organizational dynamics (adoption, buy-in) = separate need even if unstated.

### STEP 2 — Exhaustive Skill Scan

Read EVERY skill description. Do not stop after first match.

Score each: **PRIMARY** (core intent, output worse without it) ORTING** (secondary need, quality boost) · **IRRELEVANT**

Zero PRIMARY matches = you skimmed. Re-read.

```
Primary:   [skill]: [which intent component]
Supporting: [skill]: [what quality dimension]
Excluded:  [skill]: [why not, non-obvious only]
```

### STEP 3 — Composition Pattern

| Intent shape | Pattern |
|---|---|
| Pure analysis/diagnosis/decision | **SINGLE** or **ORCHESTRATED** |
| Pure production (write/create/build) | **SINGLE** — match output format |
| Analysis → production | **PIPELINE** — analytical skill → production skill |
| Multi-lens review/audit | **PARALLEL → CONVERGE** — different quality dimensions |
| Compression/summarization | **SINGLE** or **PIPELINE** (chain if large input) |
| Ideation/brainstorming | **SINGLE** or **PARALLEL** creative skills |
| File transformation | **SINGLE** — match target format |
| Complex multi-faceted | **ORCHESTRATED** — split analysis + production phases |

### STEP 4 — Emit Plan, Execute

```
SKILL ROUTER — PLAN
Intent: [onettern]
Skills: [ordered list with roles]
---
Executing Step 1: [skill-name]
```

Read first skill's SKILL.md, begin. Pipeline: carry output forward. Parallel: execute sequentially then synthesize.

## Calibration

**Skip for**: greetings, factual questions, follow-ups mid-execution, user naming a specific skill.

**Always invoke for**: new substantive requests, temptation to answer from raw capability when skills exist, multi-domain requests.

**Mid-execution**: if a skill was missed — pause, re-run Step 2, amend, resume.

## Attention Decay Countermeasures

1. Never stop after first match — second-best skill often makes the difference
2. Re-read last 5 skill entries deliberately (attention worst at list end)
3. For each IRRELEVANT score, articulate why in one sentence — can't? Re-score
4. Prefer composition over omission — reading one extra SKILL.md is cheap
5. List excluded skills — makes decision auditable
