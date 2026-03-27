---
name: agent-instruction-forge
description: "Guide humans through creating effective instruction rules for coding agents (Copilot, Claude Code, Cursor, Windsurf, Aider, AGENTS.md, CLAUDE.md, .cursorrules, copilot-instructions.md). Trigger when someone asks to create, improve, or write agent instructions, copilot rules, AI coding guidelines, context files, or anything shaping agent behavior. Also trigger on 'agent keeps making mistakes', 'make Copilot follow our conventions', 'write rules for repo', 'set up agent context'. Runs an interactive extraction process — reads codebase first, then guides the human through targeted questions to surface implicit knowledge (past failures, non-obvious conventions, architectural decisions) that code alone can't tell an agent. For analyzing gaps in existing context, use context-gap-analyzer. This skill *creates* the rules."
---

# Agent Instruction Forge

**Core thesis**: The difference between mediocre and exceptional agent instructions is not verbosity or coverage — it's *signal density of implicit knowledge*. Generic rules ("write clean code", "follow best practices") actively hurt agent performance (ETH Zurich, 2024: LLM-generated context files reduce success rates ~3%). What works is encoding the specific, non-obvious knowledge that every team member carries but no file in the repo says.

This skill runs a structured interactive process that works in two modes, detected automatically:

- **Greenfield mode**: No instruction files exist yet. Read the codebase, extract human knowledge, synthesize rules from scratch.
- **Augment mode**: Instruction files already exist. Audit them for quality and coverage, validate against actual code, identify gaps and stale/weak rules, then guide the human to fill what's missing and strengthen what's there.

The mode is determined by Phase 1 discovery. If any instruction files are found, the skill enters Augment mode.

**If no codebase is accessible** (no filesystem, no files attached, chat-only context): enter **Interview-Only mode**. Skip Phase 1 Steps 2-4 entirely. The Discovery Brief becomes a short statement of what you DON'T know, and Phase 2 relies entirely on the human — lean harder on the Failure Round and Resource Ingestion. Flag to the human: "I can't validate rules against your code, so file paths and patterns will need manual verification before committing."

---

## Fast Path

If you need the shortest reliable execution path, do this:

1. **Detect mode**
   - Existing instruction files present → **Augment**
   - No instruction files → **Greenfield**
   - No codebase access → **Interview-Only**
2. **Always finish Phase 1 before asking the human anything**
   - Scan instruction surfaces
   - Sample real code patterns
   - Mine git/PR history if available
3. **In Augment mode, do not rewrite first**
   - Audit rules
   - Produce a Discovery Brief
   - Ask only the verification / gap-filling questions the audit makes necessary
4. **Start interactive extraction with the Failure Round**
   - Ask 2-4 questions
   - Probe for file path, correct pattern, and why
5. **Synthesize as a scoped diff, not a monolith**
   - remove / rewrite / add / re-scope
6. **Before finalizing, adversarially validate if possible**
   - newcomer / prior-override / contradiction checks

If a response skips mode detection, skips the audit in augment mode, or jumps straight to rewriting, it is probably missing the highest-value part of this skill.

---

## What Makes an Agent Instruction Rule Exceptional

Before executing, internalize these principles — they govern every phase.

### The Seven Properties of a Great Rule

**1. Specific and falsifiable** — an agent can verify compliance. If a rule can't be violated, it's not a rule.
BAD: "Write clean, maintainable code" → GOOD: "Every function calling an external API must return Result<T, AppError>, never throw."

**2. Encodes the WHY** — without rationale, agents optimize around rules when inconvenient. The WHY anchors *when* the rule matters.
BAD: "Don't use console.log" → GOOD: "Don't use console.log — use src/lib/logger.ts. All logs feed Datadog. console.log bypasses correlation IDs and breaks trace stitching."

**3. Born from a real failure** — past failures produce the most specific rules because the human remembers the pain.
GOOD: "Never add indexes to the reservations table without DBA approval. In Q2 2024 a compound index locked the table for 47 minutes."

**4. Scoped to the right level of the tree** — put a rule at the highest directory where it is universally true. Pull global rules up. Push package-specific rules down. Avoid broad wildcards like `**/*.ts` for package-specific logic.
Scope test: "Does this rule apply to ALL code the agent will see in this directory?" If not, move it deeper.

**5. Points to the canonical example** — agents learn patterns better from a concrete reference than from abstract description.
GOOD: "New API endpoints follow src/api/reservations/create.ts — handler → validation → service → response mapping."

**6. Includes the anti-pattern** — telling agents what NOT to do overrides training priors when the codebase does something unusual.
GOOD: "We do NOT use the repository pattern. Each service calls Prisma directly. Previous attempts added indirection without value."

**7. Token-efficient** — every wasted token is context window not available for code reasoning.
BAD: "When writing tests, please make sure to use Vitest and not Jest." → GOOD: "Tests: Vitest, never Jest. Config in vitest.config.ts."

### What Rules Should NOT Contain

- **Things fixable in code** — if you can solve it with a better type signature, a clearer function name, a well-placed comment at the call site, or a linter rule, do that instead. Code-level fixes are always more reliable than prose instructions.
- **Things the linter already enforces** — if ESLint/Prettier/Ruff catches it, don't repeat it. The agent will see the lint error.
- **Language documentation** — don't teach TypeScript. The agent knows TypeScript.
- **Obvious patterns derivable from code** — if every file in `/src/api/` follows the same structure, the agent will pick up the pattern. Only document it if there are *exceptions* or *non-obvious constraints*.
- **Aspirational rules nobody follows** — if the rule says "always write integration tests" but the codebase has zero, the rule will confuse the agent. Document reality, not ambition (unless explicitly marked as aspirational-by-design).

---

## Execution Process

### PHASE 1 — Codebase Context Discovery (Automated)

Read the codebase to understand what exists before asking the human anything. This prevents asking questions the code already answers.

#### Step 1: Discover existing instruction infrastructure

Scan broadly for files that may already steer agents or contributors:
- Root and scoped instruction files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/prompts/*.prompt.md`
- Supporting context: `.context/`, `.ctx`, `README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CONVENTIONS.md`, ADR dirs
- Workflow signals: `.editorconfig`, formatter/linter configs, `tsconfig`, `pyproject.toml`, `Makefile`/`justfile`/`Taskfile`, CI files, Docker configs

For each discovered file, read it and inventory:
- What topics it covers
- How current it feels (stale vs. maintained)
- What format/tone it uses (terse rules vs. prose vs. structured YAML)

#### Step 2: Codebase topology snapshot

Map the high-level structure:
- Languages, frameworks, package managers
- Directory structure (2-3 levels deep)
- Entry points (API routes, CLI commands, main files)
- Test structure and patterns
- External service integrations (API clients, SDKs, DB configs)

#### Step 3: Pattern extraction

Sample 3-5 representative files from the most-modified directories (via `git log --stat` if available; otherwise infer high-traffic areas from directory size, complexity, and proximity to entry points) to detect:
- Naming conventions actually in use
- Error handling patterns
- Import organization
- Logging patterns
- Test structure and assertion style

#### Step 3b: History mining (if git/PR access available)

PR review comments and commit messages are the richest untapped source of implicit rules — they capture the exact moment someone said "we don't do it this way" or explained *why* a change was made, but that knowledge rarely migrates to documentation.

**Commit messages** — scan recent history (`git log --oneline --no-merges -200`) for:
- **Reverts/fix-ups**: "revert X because Y" directly encodes a rule ("don't do X because Y")
- **Migration commits**: "migrate from X to Y" signals historical decisions (C9) and anti-patterns
- **Convention enforcement**: commits that rename, restructure, or standardize carry implicit rules
- **"Fix:" / "Hotfix:" commits**: encode past failures (Property 3), especially when descriptions explain what went wrong

Use targeted grep to surface high-signal commits: `git log --all --grep="convention\|instead\|revert\|breaking\|deprecated\|don't\|do not" -i --oneline`

**PR/MR review comments** — if the platform is accessible (GitHub CLI `gh pr list --state merged --limit 30 --json title,body,comments,reviews`, GitLab API, or MCP tools), scan recent merged PRs for:
- **Review corrections**: "nit:", "please use X instead of Y", "we prefer Z here" — these are rules enforced manually but never documented
- **PR descriptions with architectural rationale**: "this PR moves X to Y because Z" — encodes WHY (Property 2)
- **Repeated feedback**: the same correction across multiple PRs is a strong undocumented rule
- **Rejected/revised PRs**: the revision reason often encodes a constraint

For each signal found, capture: the source (commit/PR), the candidate rule, the category (C1-C9), and confidence (High = explicit correction or repeated pattern, Medium = implied from single PR, Low = ambiguous). Prioritize multi-occurrence signals — repetition indicates enforced-but-undocumented rules.

**When git/PR access is unavailable**: Skip this step. In Phase 2, ask the human directly: "Are there patterns you find yourself correcting repeatedly in code reviews that aren't written down anywhere?"

#### Step 4: Rule Audit (Augment Mode Only)

If existing instruction files were found in Step 1, perform a deep audit before asking the human anything. This is the most valuable step in augment mode — it turns a vague "improve our rules" into a concrete, prioritized action plan.

For each existing rule, evaluate:

**A. Seven Properties Score** — rate 0-7 by how many of the Seven Properties it satisfies. Flag `<=2` for rewrite or removal. If it fails Property 1 (specific and falsifiable), treat it as noise.

**B. Code Alignment Check** — mark each rule as:
- **Confirmed**: matches real code patterns
- **Stale**: describes a pattern that no longer exists
- **Aspirational**: desired future state, not current reality
- **Contradicted**: code does the opposite
- **Unverifiable**: not checkable from code

**C. Coverage Mapping** — map rules to C1-C9:
- C1 Architecture & Boundaries
- C2 Domain Model & Business Rules
- C3 Conventions & Patterns
- C4 Integrations & External Dependencies
- C5 Operations & Deployment
- C6 Testing Philosophy & Strategy
- C7 Security Model
- C8 Performance Constraints
- C9 Historical Decisions & Tech Debt

**D. Redundancy / Contradiction Detection** — flag rules duplicated by lint, type system, CI, or other instruction files. Redundant rules waste tokens; contradictory rules actively mislead agents.

**E. Scoping Assessment** — apply the scope test and flag:
- **Over-scoped**: should move deeper
- **Under-scoped**: duplicated rules that should move up
- **Wildcard abuse**: broad `applyTo` globs for package-specific logic
- **Missing intermediate levels**: nothing between repo root and leaf packages

Write the audit output as a concise table (note the Scope column):

```
RULE AUDIT — [file path]
═══════════════════════════════════════════
Rule                          | Score | Alignment    | Scope          | Verdict
"Use Result<T> for API calls" |  6/7  | Confirmed    | ✅ root (global)| ✅ Keep
"Write clean code"            |  1/7  | Unverifiable | — irrelevant   | 🗑️ Remove
"Billing API returns envelope"|  5/7  | Confirmed    | ❌ root→billing | 📦 Re-scope
"Don't modify user schema"    |  4/7  | Confirmed    | ✅ root (global)| 🔧 Rewrite
...

Summary: [N] total → ✅ [n] keep, 🔧 [n] rewrite, ⚠️ [n] verify, 🗑️ [n] remove, 📦 [n] re-scope
Redundant with linter/CI: [n] | Stale: [n] | Aspirational: [n] | Contradicted: [n]

Coverage: C1[●] C2[○] C3[●] C4[○] C5[◐] C6[●] C7[○] C8[○] C9[○]
          ● covered  ◐ partial  ○ missing

Token budget: ~[current] / [limit] — headroom: [remaining]
Scope health: [N] rules correctly scoped, [N] over-scoped, [N] under-scoped
```

#### Step 5: Produce a Discovery Brief

Synthesize findings into a brief for the human. This serves two purposes: (a) showing the human what you already know so they don't repeat it, and (b) identifying the exact gaps where human input is needed.

**Greenfield brief**:
- Target agent system and file format
- No existing instruction files found
- What the code already reveals
- Top candidate rules from git/PR history
- Highest-value undocumented gaps

**Augment brief**:
- Existing instruction files
- Rule health summary: keep / rewrite / verify / remove / re-scope
- Top issues
- Rules surfaced from git/PR history but not documented
- Coverage gaps, undocumented patterns, token budget

Present the brief, then verify your findings before proceeding. In augment mode, ask:
- Are any rules flagged for removal actually important?
- Are any "confirmed" rules outdated or aspirational?
- Which hidden rules from history are real conventions worth documenting?
- Which coverage gaps matter most right now?

---

### PHASE 2 — Guided Knowledge Extraction (Interactive)

This is the core of the skill. The human carries implicit knowledge that no amount of code reading can surface. The goal is to extract it efficiently through the *right* questions.

#### Mode-Aware Extraction Strategy

Do NOT dump 20 questions at once. Run this as a conversation with 2-4 questions per round, grouped thematically.

**In Greenfield mode**: Start with the highest-impact category based on the codebase topology. Follow the round sequence below.

**In Augment mode**: The extraction is shaped by the audit results. Three workstreams run in parallel, woven into the conversation rounds:

1. **Verify flagged rules**: Present the ⚠️ rules that need human confirmation. For each, ask: "This rule says [X]. Is this still accurate? Has anything changed?" This is low-effort for the human and immediately improves rule quality.

2. **Fill coverage gaps**: Skip categories that already have strong coverage. Focus extraction questions on the gap categories identified in the audit. If C3 (Conventions) and C6 (Testing) are well-covered but C9 (Historical Decisions) and C4 (Integration) are empty, start there.

3. **Strengthen weak rules**: For rules flagged as 🔧 rewrite, ask targeted questions to supply the missing properties. E.g., if a rule lacks WHY, ask: "This rule says [do X]. Can you tell me *why*? What goes wrong when someone does it differently?" If a rule lacks a canonical example, ask: "Is there a file that best exemplifies this pattern?"

Weave these three workstreams into the round structure below. Skip rounds whose topics are already well-covered by existing rules.

**Question prioritization formula**: Ask first about areas where (a) the agent will write code most often, AND (b) the code alone is most ambiguous or the conventions are most non-obvious. In augment mode, also prioritize (c) areas where existing rules are weakest or most contradicted by code.

#### Round 1 — The Failure Round (Always Start Here)

Past failures are the highest-signal source of implicit knowledge. The human remembers them vividly, describes them concretely, and the resulting rules carry the specificity that makes instructions exceptional.

Ask:

```
1. "Think about the last time a developer (human or AI) made a mistake that was
   frustrating to review. What did they do wrong, and what should they have done
   instead?"

2. "Are there any 'landmines' in this codebase — areas where doing the obvious
   thing leads to a subtle bug, a production incident, or a painful review cycle?"

3. "What's the most common mistake in PRs from new team members?"

4. "Are there any small, recurring annoyances in agent-generated code? Things you
   fix every time but that aren't dramatic 'mistakes' — just persistent friction?"
```

For each answer, immediately probe for specificity:
- "Can you point me to a file where this pattern applies?"
- "What does the correct version look like?"
- "Why does the codebase do it this way instead of the more common approach?"

#### Round 2 — The Conventions Round

Focus on conventions that *differ* from framework/language defaults — these are where agents fail most, because their training priors pull them toward the default.

```
1. "Where does your codebase intentionally deviate from the framework's recommended
   approach? (e.g., you use X instead of Y, or you structure things differently
   than the docs suggest)"

2. "Are there any patterns you enforce in code review that aren't caught by linting
   or CI? Things where you'd comment 'we don't do it this way here'?"

3. "If you could write one rule that would eliminate 50% of the nit-picks in code
   reviews, what would it be?"
```

#### Round 3 — The Architecture Round

Focus on boundaries, data flow, and module ownership — the spatial knowledge agents lack.

```
1. "When an agent needs to add a new feature, how should it decide which module/
   directory the code goes in? What's the mental model?"

2. "Are there any modules or files that should NOT be modified without extra caution
   or approval? (Shared libraries, core utilities, database schemas, etc.)"

3. "How does data flow through the system for the most common operation?
   (e.g., a user request: what gets called in what order?)"
```

#### Round 4 — The Integration Round (if external services detected)

```
1. "Are there any external APIs or services with quirks the agent should know about?
   (Rate limits, idempotency requirements, known bugs, retry strategies)"

2. "What's the correct way to add a new external dependency? Is there an approval
   process, a preferred client pattern, or a wrapper convention?"
```

#### Round 5 — The Testing Round

```
1. "What's your testing philosophy? (e.g., 'unit test business logic, integration
   test API endpoints, don't mock the database')"

2. "Are there any test patterns an agent should follow — or explicitly avoid?"
```

#### Round 6 — Resource Ingestion (Optional)

After the question rounds, ask:

```
"Is there any existing resource I should read to extract more context?
 This could be:
  - A Notion page, Google Doc, or wiki
  - A Slack thread or discussion where a convention was decided
  - An ADR or RFC document
  - A particularly well-written PR description that explains a pattern
  - A postmortem or incident report

 Share the link or paste the content, and I'll extract the relevant rules."
```

If the user provides resources, read them and extract rules using the same seven-property framework. Cross-reference against what's already been captured to avoid duplication.

#### Adaptive Questioning

Throughout the extraction, adapt based on:

- **Codebase type**: For a frontend app, emphasize component patterns, state management, styling conventions. For a backend API, emphasize endpoint patterns, database conventions, auth. For a CLI tool, emphasize argument parsing, output formatting, error messages.
- **Team size signals**: Solo developer → focus on future-self context. Large team → focus on consistency and boundary rules.
- **Agent system**: Copilot → focus on completion-level rules (what pattern should autocompletion follow). Claude Code / Cursor → focus on task-level rules (how to approach multi-file changes). General → cover both.
- **Human energy**: If the human gives short answers, consolidate remaining questions. If they're engaged and detailed, go deeper. Never exhaust the human — 15-20 minutes of input should produce excellent rules.

---

### PHASE 3 — Rule Synthesis & Integration

Transform extracted knowledge into agent-consumable rules. This is where most instruction files fail — the knowledge exists but it's poorly formatted for agent consumption.

#### Mode-Aware Synthesis

**In Greenfield mode**: Generate instruction files from scratch following the Synthesis Protocol and Output Structure Template below.

**In Augment mode**: Do NOT rewrite from scratch unless the existing rules are fundamentally broken. Instead, produce a changeset that preserves what works and surgically improves the rest:

1. **Remove** low-signal rules flagged 🗑️.
2. **Rewrite in place** for rules flagged 🔧, preserving grouping and tone.
3. **Add** new rules from extraction where coverage is missing.
4. **Re-scope** rules flagged 📦 to package- or directory-level files.
5. **Update coverage** and show the delta from Phase 1.

Present the changeset as a reviewable diff, not a monolithic rewrite. For each edit, say what changed and why.

Keep at least one compact before/after example when rewriting:
- BEFORE: `Don't use console.log`
- AFTER: `Don't use console.log — use src/lib/logger.ts. Structured logs feed Datadog; console.log breaks correlation IDs.`

#### Synthesis Protocol

1. **Scope correctly**: root for universal rules, package-level for package rules, deeper files for subdirectory rules, `applyTo` globs only when truly file-type-specific.
2. **Apply the Seven Properties**: every rule must at least be specific and falsifiable.
3. **Match local format**: preserve existing tone and structure unless the human asks for reorganization.
4. **Order by impact**: critical rules first because long files may be truncated.
5. **Add a short philosophy section**: help agents make judgment calls in cases no explicit rule covers.

#### Output Structure Template (Greenfield mode only)

Use this template when creating instruction files from scratch. In Augment mode, preserve the existing file's structure and tone — do not reorganize to match this template unless the human explicitly asks.

```markdown
# [Project Name] — Agent Instructions
## Philosophy — [2-3 sentences anchoring judgment for cases no rule covers]
## Critical Rules — [violations break things: what + why + anti-pattern]
## Conventions — [violations cause review friction: pattern + example file]
## Architecture — [module boundaries, data flow, where new code goes]
## Testing — [philosophy + patterns + what to mock/not mock]
```

Note: this template is for the ROOT file. Package-level files should be narrower — only rules that apply within that package, with a brief header stating the scope.

#### Token Budget Awareness

Different systems use different units — respect the native unit:
- **Copilot**: limits in **characters**. Root file: < 1,000 lines. Code review reads first **4,000 chars** per file. Scoped `.instructions.md`: same limit.
- **Claude Code**: limits in **tokens**. Root: < 4,000 tokens. Subdirectory: < 1,000 tokens.
- **Cursor / Windsurf / AGENTS.md**: similar to Claude Code.

When WHY and brevity conflict, keep the WHY. The main token-budget lever is scoping: keep repo-wide files short, push local rules down, and move low-frequency detail into references or prompts.

---

### PHASE 3b — Adversarial Validation

Before showing rules to the human, stress-test them with three isolated subagents that receive ONLY the synthesized instruction file. Read `references/adversarial-validation.md` for prompts and protocol.

Run in parallel:
1. **Simulated Newcomer** — finds gaps
2. **Prior Override Test** — checks whether rules beat common training priors
3. **Cross-rule Contradiction Finder** — finds conflicts and ambiguities

Do not include codebase files, Phase 1 findings, or conversation history in those prompts. After validation, update the rules and include a short summary of gaps, weak spots, and resolved contradictions.

---

### PHASE 4 — Review, Refinement & Delivery

Present the synthesized rules to the human and review them for:
1. **Accuracy** — wrong or outdated?
2. **Priority** — anything critical missing or low-value?
3. **Tone** — does it sound like the team?

Iterate based on feedback: clarify vague rules, correct inaccuracies, fill narrow gaps with targeted questions, and trim low-priority content.

#### Delivery

Write the final instruction file(s) to the appropriate location(s) based on the target agent system:

**GitHub Copilot** (three layers — most expressive system):
- **Repo-wide**: `.github/copilot-instructions.md` — always attached to all chat/agent requests
- **Path-specific**: `.github/instructions/NAME.instructions.md` — requires `applyTo` glob in YAML frontmatter (e.g., `applyTo: "src/api/**/*.ts"`). Supports coding agent + code review.
- **Prompt files**: `.github/prompts/NAME.prompt.md` — on-demand, user-invoked. Can reference files via `[name](../../path)` or `#file:path`.

Copilot also reads `AGENTS.md` (primary at root, additional in subdirectories), `CLAUDE.md` and `GEMINI.md` at root.

**Other agent systems**:

| Agent System | Primary File | Scoped Files |
|---|---|---|
| Claude Code | `CLAUDE.md` at root | `CLAUDE.md` in subdirectories |
| Cursor | `.cursorrules` at root | `.cursorrules` in subdirectories |
| Windsurf | `.windsurfrules` at root | `.windsurfrules` in subdirectories |
| Generic / Multi-agent | `AGENTS.md` at root | `AGENTS.md` in subdirectories, `.context/` or `.ctx` files |

If the target system isn't clear, ask the human which agent(s) they use. If multiple, generate for the primary and note any format differences for others. If the team uses Copilot, always produce the three-layer structure — it's the most expressive instruction system currently available.

After delivery, suggest: run your agent on a real task and see if rules improve output. If it still makes a specific mistake, that's the next rule. Revisit monthly — remove rules the agent has internalized, add rules from new incidents.

---

## Calibration Rules for This Skill

**1. Code-reading comes first.** Don't ask the human what the code already answers.

**2. The human is the oracle, not the bottleneck.** Ask sharp questions, in small batches, and accept concise answers.

**3. Specificity is non-negotiable.** If a rule can't be violated, it can't be followed.

**4. Failures beat aspirations.** Start from painful review cycles, incidents, and recurring corrections.

**5. Respect the token budget.** Document only the delta between code and tacit team knowledge. Keep the WHY when it matters; cut everything else.

---

## Composes With

- `context-gap-analyzer` → agent-instruction-forge: Use context-gap-analyzer first to audit what implicit context is missing from a codebase, then use this skill to create the rules that fill those gaps.
- agent-instruction-forge → `edd`: After creating instruction rules, use EDD to validate that the rules actually improve agent behavior via eval-driven iteration.
- agent-instruction-forge → `context-eval`: Measure whether the new instruction file produces better agent outcomes than the baseline.