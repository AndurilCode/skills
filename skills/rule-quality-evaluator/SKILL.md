---
name: rule-quality-evaluator
description: "Evaluate the quality of existing agent instruction rule sets — CLAUDE.md, AGENTS.md, .cursorrules, copilot-instructions.md, or any coding-agent context file. Use this skill whenever someone asks to audit, score, or improve their agent rules; wants to know if their instructions are effective; or describes rules that aren't changing agent behavior. Trigger on phrases like 'are my rules good?', 'why is the agent ignoring my instructions?', 'score my CLAUDE.md', 'audit my agent rules', 'are these instructions effective?', 'review my copilot-instructions.md', 'my rules aren't working', 'evaluate my context file', or any situation where a human has an existing instruction file and wants to know whether it will actually improve agent behavior. Also trigger when someone has just run agent-instruction-forge and wants to verify the output before committing."
---

# Rule Quality Evaluator

**Core principle**: A rule that cannot be violated cannot be followed. Most instruction files fail not because they're too short or too long, but because they're full of unfalsifiable guidance, redundant noise, and implicit knowledge that never made it to paper. This skill scores rules against seven measurable properties, identifies structural weaknesses, and optionally verifies behavior with live coding tasks.

## Two-Phase Overview

- **Phase 1 — Static Critic** (always run): Read the rules, score each against the Seven Properties, detect structural issues, produce a scorecard. No agent execution required.
- **Phase 2 — Behavioral Test** (opt-in): Generate coding tasks that touch the rules, derive testable assertions, hand off to context-eval, synthesize the combined report.

**Interview-only fallback**: If no instruction file is accessible (chat-only context, no filesystem), ask the user to paste the rules directly. Flag at the end: "I can't verify codebase alignment — code pattern checks will need manual verification."

---

## Phase 1 — Static Critic

### Step 1: Ingest

Read the instruction file(s). Detect the format (Markdown prose, structured rules list, YAML front matter, fenced sections). Parse into individual rules — one rule = one discrete behavioral instruction. When in doubt, split on bullet points, numbered items, or paragraph breaks that each start an imperative.

Optionally scan the codebase for linter configs (`.eslintrc`, `pyproject.toml`, `ruff.toml`), type system configs (`tsconfig.json`), and CI configs (`.github/workflows/`). This enables redundancy detection in Step 3.

### Step 2: Score Each Rule — The Seven Properties

Score each rule 0–7 by counting which of the Seven Properties it satisfies (each is binary: 0 = absent, 1 = present).

| Property | ID | Score 0 Example | Score 1 Example |
|---|---|---|---|
| Specific and falsifiable | P1 | "Write clean code" | "Every API handler must return `Result<T, AppError>`, never throw" |
| Encodes the WHY | P2 | "Don't use console.log" | "Don't use console.log — use `src/lib/logger.ts`. Bypasses correlation IDs, breaks Datadog traces" |
| Born from a real failure | P3 | "Handle errors carefully" | "Never add indexes to `reservations` without DBA approval — compound index locked table 47 min in Q2 2024" |
| Scoped to the right level | P4 | Rule about billing API in root file | Same rule in `src/billing/CLAUDE.md` |
| Points to canonical example | P5 | "Follow our API patterns" | "New endpoints follow `src/api/reservations/create.ts` — handler → validation → service → response" |
| Includes the anti-pattern | P6 | "Use the service layer" | "We do NOT use the repository pattern. Each service calls Prisma directly" |
| Token-efficient | P7 | "When writing tests, please make sure to always use Vitest and not Jest" | "Tests: Vitest, never Jest. Config: `vitest.config.ts`" |

**Flag rules with score ≤ 2 as weak** — candidates for rewrite or removal.
**Flag rules where P1 = 0 as noise** — if the agent can't verify compliance, the rule cannot steer behavior.

### Step 3: Structural Analysis

**Redundancy detection**: Flag rules that duplicate enforcement already handled by:
- Linter (ESLint, Ruff, Pylint, etc.)
- Type system (TypeScript strict mode, mypy, etc.)
- CI checks (test requirements, build gates, etc.)
Redundant rules waste the token budget and dilute the signal of the rules that matter.

**Scope assessment**: Apply the scope test to each rule: "Does this rule apply to ALL code the agent will see in this directory?" Flag:
- **Over-scoped**: rule is specific to a package/module but lives in the root file
- **Under-scoped**: identical rules duplicated across subdirectory files that should move up

**Coverage mapping**: Map rules to the nine context categories:
- C1 Architecture & Boundaries
- C2 Domain Model & Business Rules
- C3 Conventions & Patterns
- C4 Integrations & External Dependencies
- C5 Operations & Deployment
- C6 Testing Philosophy & Strategy
- C7 Security Model
- C8 Performance Constraints
- C9 Historical Decisions & Tech Debt

Mark each as `●` (covered), `◐` (partial), or `○` (missing).

**Token budget check**: Count tokens (or characters) and compare against limits:
- Claude Code: root file < 4,000 tokens, subdirectory < 1,000 tokens
- Copilot: root file < 1,000 lines, first 4,000 chars are read per code review
- Cursor / Windsurf / AGENTS.md: similar to Claude Code

### Step 4: Produce Scorecard

Output this structured scorecard, then ask the user whether they want Phase 2.

---

#### 📊 Rule Scorecard — `[file path]`

| Rule (truncated) | Score | Weakest Property | Flags |
|---|---|---|---|
| "…" | N/7 | P? | weak / noise / redundant / over-scoped |
| … | | | |

#### 📋 Summary Stats

- Total rules: N
- Mean score: X.X / 7
- Strong (5–7): N | Adequate (3–4): N | Weak (0–2): N
- Noise rules (P1 = 0): N
- Redundant with linter/CI/types: N
- Over-scoped: N | Under-scoped: N

#### 🗺️ Coverage Map

```
C1 Architecture      [coverage indicator]
C2 Domain Model      [coverage indicator]
C3 Conventions       [coverage indicator]
C4 Integration       [coverage indicator]
C5 Operations        [coverage indicator]
C6 Testing           [coverage indicator]
C7 Security          [coverage indicator]
C8 Performance       [coverage indicator]
C9 Historical        [coverage indicator]
● covered  ◐ partial  ○ missing
```

#### ⚖️ Token Budget

- Current: ~N tokens / N chars
- Limit: [system-appropriate limit]
- Headroom: [remaining / over by N]

#### 🔍 Top 3 Improvements

1. [Most impactful change — which rule, which property, what to add]
2. [Second most impactful change]
3. [Third most impactful change]

#### 🏆 Phase 1 Verdict

| Threshold | Verdict |
|---|---|
| Mean score ≥ 5 | **STRONG** — rules are specific, grounded, and efficient |
| Mean score 3–4 | **ADEQUATE** — rules are usable but have meaningful gaps |
| Mean score < 3 | **WEAK** — rules will not reliably steer agent behavior |

---

**Would you like Phase 2 — Behavioral Testing?** It generates real coding tasks from your rules and measures whether the rules actually change agent behavior. Required: context-eval skill available.

---

## Phase 2 — Behavioral Test

### Step 5: Generate Coding Tasks

Generate 3 coding tasks derived from the rule set. Each task must:
- Be approximately 50 lines of code to produce
- Touch 2 or more rules simultaneously (to make grading discriminating)
- Target the highest-scoring rules by priority: Critical rules first, then rules born from incidents (P3 = 1)

For each task, record which rules it exercises and what correct behavior looks like.

### Step 6: Generate Assertions

Derive one testable assertion per rule. The assertion must be:
- Observable in agent output (checkable without running the code)
- Phrased as a pass/fail check

Write assertions to `evals/evals.json` in context-eval compatible format:

```json
{
  "harness_name": "[instruction file name]",
  "harness_type": "coding agent instruction rules",
  "harness_path": "[path to instruction file]",
  "evals": [
    {
      "id": 1,
      "prompt": "[the coding task prompt]",
      "expected_output": "[description of correct output under the rules]",
      "files": [],
      "assertions": [
        "[rule → assertion, e.g., 'Uses src/lib/logger.ts, not console.log']",
        "[second rule → assertion]"
      ]
    }
  ]
}
```

### Step 7: Hand Off to context-eval

Invoke the `context-eval` skill with the generated `evals/evals.json`. The harness under test is the instruction file; the baseline is the same tasks without the instruction file loaded.

```
→ context-eval: evaluate harness at [instruction file path] using evals/evals.json
```

context-eval will run the tasks with and without the harness, grade assertions, and compute the benefit delta.

### Step 8: Synthesize Report

Combine Phase 1 scorecard with Phase 2 results into a unified report.

---

#### 📊 Combined Report

**Phase 1 Static Score**: [mean] / 7 → [STRONG / ADEQUATE / WEAK]

**Phase 2 Behavioral Delta**: +[delta] pass rate improvement over baseline

#### ☑️ Per-Rule Behavioral Confirmation

| Rule | P1 Verdict | P2 Delta | Confirmed? |
|---|---|---|---|
| "…" | score/7 | +X% | ✅ / ⚠️ / ❌ |

#### 🏆 Final Verdict

| Condition | Verdict |
|---|---|
| Static ≥ 5 AND behavioral delta ≥ 0.25 | **STRONG** — rules are well-formed and measurably improve behavior |
| Static ≥ 3 AND behavioral delta ≥ 0.10 | **ADEQUATE** — rules work but have room to improve |
| Static < 3 OR behavioral delta < 0.10 | **WEAK** — rules are not reliably changing agent behavior |
| Behavioral delta < 0 | **HARMFUL** — rules are degrading agent performance |

#### ⚠️ Discrepancies

Rules that score high in Phase 1 but show no behavioral delta (or vice versa) — these are the most actionable findings. A high-scoring rule with no behavioral delta is either not reachable in the eval tasks or not being read by the agent. A low-scoring rule with high delta suggests it encodes something valuable that the scoring missed.

---

## Calibration Rules

**1. Phase 1 always comes first.** Never jump to behavioral testing without completing the static scorecard. Phase 1 takes minutes; Phase 2 requires agent execution infrastructure. The scorecard catches the most common failures without any tooling.

**2. P1 is the gatekeeper.** A rule that fails Property 1 (specific and falsifiable) cannot be improved by any other property. Fix specificity before adding WHY, examples, or anti-patterns. Unfalsifiable rules waste every other token they contain.

**3. Redundancy is the easiest win.** Rules that duplicate linter, type, or CI enforcement can be deleted immediately — they don't improve agent behavior and they consume tokens that better rules could use. Always check redundancy before recommending rewrites.

**4. Behavioral testing is the gold standard, not the default.** Phase 2 gives you ground truth on whether rules change agent behavior. But it requires working context-eval infrastructure and takes significantly longer. Most rule sets benefit more from targeted Phase 1 rewrites than from Phase 2 measurement of the current (weak) rules.

**5. Score what you see, not what you wish.** If a rule could be interpreted charitably as specific, score it as written — not as intended. The agent reads the literal text. A rule that requires generous interpretation to seem falsifiable will fail in practice.

---

## Composes With

`context-gap-analyzer` → `agent-instruction-forge` → `rule-quality-evaluator` → `context-eval`

- **context-gap-analyzer first**: audit what implicit knowledge is missing from the codebase
- **agent-instruction-forge next**: create rules that fill the identified gaps
- **rule-quality-evaluator**: verify the created rules are well-formed and will steer agent behavior
- **context-eval downstream**: measure whether the rules produce better outcomes over time
