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

## What Makes an Agent Instruction Rule Exceptional

Before executing, internalize these principles — they govern every phase.

### The Seven Properties of a Great Rule

**1. Specific and falsifiable** — an agent can verify compliance. If a rule can't be violated, it's not a rule.
BAD: "Write clean, maintainable code" → GOOD: "Every function calling an external API must return Result<T, AppError>, never throw."

**2. Encodes the WHY** — without rationale, agents optimize around rules when inconvenient. The WHY anchors *when* the rule matters.
BAD: "Don't use console.log" → GOOD: "Don't use console.log — use src/lib/logger.ts. All logs feed Datadog. console.log bypasses correlation IDs and breaks trace stitching."

**3. Born from a real failure** — past failures produce the most specific rules because the human remembers the pain.
GOOD: "Never add indexes to the reservations table without DBA approval. In Q2 2024 a compound index locked the table for 47 minutes."

**4. Scoped to the right level of the tree** — a rule must live where the agent encounters the code it governs. Not higher (wasting tokens on every interaction), not lower (duplicated across siblings). This applies at arbitrary depth — a monorepo with `packages/billing/src/api/` deserves rules scoped there, not dumped in the repo root.

The principle: **what is common stays in common rules; what is package-specific stays in package-level rules.** A rule about error handling that applies everywhere belongs at the root. A rule about how the billing API formats responses belongs in `packages/billing/`. A rule about a specific adapter's retry logic belongs in that adapter's directory. Avoid broad wildcards (e.g., `applyTo: "**/*.ts"`) that spray package-specific rules across the entire codebase — this is the scoping equivalent of a global variable.

```
repo root:                Cross-cutting rules (auth, logging, error philosophy)
├── packages/billing/:    Billing domain rules, payment API conventions
│   └── src/adapters/:    Adapter-specific rules (retry, idempotency)
├── packages/web/:        Frontend rules (component patterns, state management)
│   └── src/components/:  Component-specific rules (naming, props, testing)
└── packages/shared/:     Shared library rules (versioning, API contracts)
```

Every rule should pass the **scope test**: "Does this rule apply to ALL code the agent will see when working in this directory's context?" If not, push it deeper. If it applies everywhere equally, pull it up.

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

Scan for all files that could be carrying agent context:

```
Scan targets (examples — discover broadly, don't limit to this list):
- .github/copilot-instructions.md
- .github/instructions/*.instructions.md (path-specific Copilot rules — check applyTo frontmatter)
- .github/prompts/*.prompt.md (reusable Copilot prompt files)
- AGENTS.md, CLAUDE.md, GEMINI.md, .cursorrules, .windsurfrules
- .context/, .ctx files
- ARCHITECTURE.md, CONTRIBUTING.md, CONVENTIONS.md
- ADR directories (adr/, doc/adr/, docs/decisions/)
- README.md (look for "development" or "conventions" sections)
- .editorconfig, .prettierrc, .eslintrc, tsconfig, pyproject.toml
- Makefile / justfile / Taskfile (targets reveal workflow conventions)
- CI configs (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)
- Docker configs, docker-compose.yml
```

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

**For each existing rule, evaluate:**

**A. Seven Properties Score**
Rate each rule 0-7 based on how many of the Seven Properties it satisfies. Flag rules scoring ≤ 2 as candidates for rewrite. A rule that is neither specific nor falsifiable (Property 1 = 0) should always be flagged — it's noise in the context window.

**B. Code Alignment Check**
Cross-reference each rule against the actual code found in Step 2-3:
- **Confirmed**: The rule matches patterns actually found in code. Keep it.
- **Stale**: The rule describes a pattern that no longer exists, or uses outdated file paths / APIs. Flag for removal or update.
- **Aspirational**: The rule prescribes something the codebase doesn't actually follow (e.g., "all services have integration tests" but only 2 of 15 do). Present to the human with two options: **(a)** the rule is stale — code moved on, remove or update it; **(b)** the rule is a target — code should eventually comply, keep it but mark it as "aspirational-by-design" so the agent treats it as directional, not descriptive of current state. Never auto-remove aspirational rules — only the human knows the intent.
- **Contradicted**: The code actively does the opposite of what the rule says. Critical flag — this is the most harmful type of rule because it pushes agents to fight the codebase.
- **Unverifiable**: The rule covers something not observable in code (e.g., deployment procedures, team communication). Can't validate — leave for human confirmation.

**C. Coverage Mapping**
Map each existing rule to one of the Nine Context Categories (from the context-gap-analyzer framework):
- C1: Architecture & System Boundaries
- C2: Domain Model & Business Rules
- C3: Conventions & Patterns
- C4: Integration & External Dependencies
- C5: Operations & Deployment
- C6: Testing Philosophy & Strategy
- C7: Security Model
- C8: Performance Constraints
- C9: Historical Decisions & Tech Debt

Identify which categories have strong coverage, which have partial coverage, and which are completely missing.

**D. Redundancy & Contradiction Detection**
Identify rules that duplicate or contradict:
- Linters/formatters (ESLint, Prettier, Ruff, etc.) — redundant, remove
- Type system (TypeScript strict mode, mypy) — redundant, remove
- CI checks (tests, build validation) — redundant, remove
- Other instruction files (cross-file duplication) — merge into one location
- Other instruction files (cross-file contradiction) — critical flag, these confuse agents unpredictably. A rule in `.github/copilot-instructions.md` that contradicts one in `AGENTS.md` is worse than having no rule at all

Redundant rules waste token budget. Contradictory rules actively harm agent behavior. Flag both for resolution.

**E. Scoping Assessment**
For each rule, determine the narrowest scope it actually applies to by mapping it against the codebase's module/package tree from Step 2. Apply the **scope test**: "Does this rule apply to ALL code an agent sees in this directory's context?"

Flag:
- **Over-scoped rules**: sitting in the repo root but only relevant to a specific package or module. These waste token budget on every agent interaction in unrelated areas. Recommend pushing to package-level instruction file.
- **Under-scoped rules**: duplicated across multiple package-level files when they apply universally. Recommend pulling up to root.
- **Wildcard abuse**: rules using broad `applyTo` globs (e.g., `**/*.ts`) that spray package-specific logic across unrelated modules. Recommend narrowing the glob to the actual target directory.
- **Missing intermediate levels**: all rules at root + leaf, nothing at package level. If the module tree has 3+ levels of depth, check whether an intermediate instruction file would prevent duplication.

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

**In Greenfield mode**, the brief focuses on what the code tells you and what gaps you've identified:

```
DISCOVERY BRIEF — Greenfield
═══════════════════════════════════════════
Target agent system: [detected or ask — Copilot / Claude Code / Cursor / etc.]
Instruction file format: [detected — .md / .cursorrules / etc.]
No existing instruction files found.

What the code already tells an agent:
  - [pattern/convention detected from code]
  ...

Rules surfaced from git history / PR reviews:
  - [N] candidate rules from commit messages (confidence: high/medium/low)
  - [N] candidate rules from PR review comments
  [list top 3-5 highest-confidence candidates with source]

What's NOT documented but likely matters:
  - [gap identified — e.g., "no error handling convention documented, but 3 different patterns found in code"]
  ...
```

**In Augment mode**, the brief leads with the audit results:

```
DISCOVERY BRIEF — Augment
═══════════════════════════════════════════
Target agent system: [detected]
Existing instruction files: [list with file paths]

RULE HEALTH: [N] rules → ✅ [n] strong, 🔧 [n] rewrite, ⚠️ [n] verify, 🗑️ [n] remove
TOP ISSUES:
  1. [e.g., "8 of 12 rules lack a WHY — agents will optimize around them"]
  2. [e.g., "All rules in repo-wide file, 5 should be scoped to /src/api/"]
  3. [e.g., "No coverage of testing (C6) or historical decisions (C9)"]

RULES HIDDEN IN GIT HISTORY (not in any instruction file):
  - [candidate rule] — source: [PR #N / commit abc123] — confidence: [H/M/L]
  ...

COVERAGE GAPS: [list C-codes with missing/weak coverage and why it matters]
UNDOCUMENTED PATTERNS FROM CODE: [list patterns found but not in any rule file]
Token budget: [current] / [limit]
```

Present this brief to the human. Ask them to confirm or correct before proceeding. In augment mode, specifically ask:

```
"Before we start improving, I want to verify my findings:
 1. Are any of the rules I flagged for removal actually important? (I may have missed context)
 2. Are any rules I marked as 'confirmed' actually outdated? (Code can lag behind intent)
 3. I found [N] candidate rules hidden in PR comments and commit history. Which of these
    are real conventions worth documenting? (I'll show you each one)
 4. Which coverage gaps feel most urgent to you?"
```

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

1. **Remove**: Delete rules flagged 🗑️ in the audit (after human confirmation). Each removal frees token budget for higher-value rules.

2. **Rewrite in-place**: For rules flagged 🔧, rewrite them to satisfy more of the Seven Properties while preserving their position and grouping in the file. Show the human before/after for each rewrite so they can catch meaning drift.

3. **Add new rules**: Insert rules from the extraction phase into the appropriate section of the existing file. Match the tone, format, and structure already established. Don't reorganize the entire file unless the human explicitly asks.

4. **Re-scope**: Move every rule flagged 📦 in the audit to its correct level in the module tree. Create new package/directory-level instruction files as needed — don't hesitate to split a bloated root file into a root + N package files. This is often the single highest-impact structural improvement: it reduces token waste on every agent interaction in unrelated areas while making rules more visible where they matter. When using Copilot, convert over-scoped root rules into `.instructions.md` files with precise `applyTo` globs targeting the actual package path, not wildcards.

5. **Update coverage**: After all changes, regenerate the coverage map and show improvement vs. the Phase 1 baseline.

Present the changeset as a structured diff — not a monolithic new file — so the human can review incrementally:

```
PROPOSED CHANGES
═══════════════════════════════════════════
REMOVALS (N rules — saves ~X tokens):
  ❌ "Write clean code" — unfalsifiable, zero signal
  ❌ "Use semicolons" — already enforced by Prettier

REWRITES (N rules — showing before/after):
  🔧 BEFORE: "Don't use console.log"
     AFTER:  "Don't use console.log — use src/lib/logger.ts. Our structured
              logger feeds Datadog with correlation IDs. console.log breaks tracing."
     [Added: WHY, canonical path, consequence]

NEW RULES (N rules):
  ✨ [C4] "Stripe API requires idempotency keys on all POSTs. Use
     src/lib/stripe/idempotency.ts. Missing keys → duplicate charges (March 2024 incident)."

RE-SCOPED (N rules):
  📦 "React CSS modules rule" → .github/instructions/frontend.instructions.md

COVERAGE: 4/9 categories → 6/9 | Tokens: ~2,800 → ~3,100 / 4,000
```

#### Synthesis Protocol

1. **Scope each rule to the right level of the module tree.** This is the most impactful structural decision — it determines whether a rule fires precisely or pollutes unrelated contexts.

   Walk the codebase's directory tree and assign each rule to the narrowest directory where it applies universally:
   - If it applies to ALL code in the repo → root instruction file
   - If it applies to one package/module → package-level instruction file
   - If it applies to a subdirectory within a package → subdirectory-level file
   - If it applies to a specific file type within a scope → use `applyTo` globs (Copilot) or directory-level files (Claude Code, Cursor)

   **Never scope wider than necessary.** A billing API response format rule in the root file means every agent interaction — even in the frontend package — burns tokens reading it. Push it to `packages/billing/` or deeper.

   **Create intermediate instruction files** when the tree is deep. If you have 15 rules and 10 apply only to `packages/billing/`, don't keep them all at root — create `packages/billing/CLAUDE.md` (or equivalent). The depth of the instruction tree should mirror the depth of the module tree.

   **Inheritance is your friend.** Root rules apply everywhere. Package rules add to (or override) root rules within that package. This means a rule should live at the highest level where it's universally true, and be overridden at lower levels only when a package genuinely needs different behavior.

2. **Apply the Seven Properties**: For each rule, verify it meets as many of the seven properties as possible. At minimum, every rule must be *specific and falsifiable* (Property 1).

3. **Match the existing format**: If the codebase already has instruction files with a specific tone and format, match them exactly. If starting fresh, use terse imperative prose (highest token efficiency, clearest for agents).

4. **Order by impact**: Put the most important rules first. Agents may see a truncated version of long instruction files. Front-load what matters most.

5. **Add the meta-rule**: Include a brief section explaining the codebase's philosophy or "spirit" — this helps agents make correct *judgment calls* in situations no rule covers explicitly.

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

When WHY and brevity conflict, keep the WHY. Proper scoping is the best token budget strategy — a well-scoped rule set is naturally smaller per file because each file only carries what's relevant to its scope.

If the rules are too long, prioritize ruthlessly. Move secondary rules into scoped files or reference documents. The highest-impact rules go in the repo-wide file; pattern-specific rules go in scoped files near the code they govern.

---

### PHASE 3b — Adversarial Validation

Before showing rules to the human, stress-test them with three adversarial subagents. Each subagent receives ONLY the synthesized instruction file — not the codebase, not the Phase 1 findings, not the conversation history. This context isolation is what makes the validation genuine: the challenger knows nothing except what the rules say.

**Read `references/adversarial-validation.md` for full subagent prompts, evaluation protocols, and integration guidance.**

#### Execution

Spawn three subagents in PARALLEL. Each receives the instruction file as its sole context:

1. **Simulated Newcomer** (catches **gaps**): Give it the instruction file + a realistic task (e.g., "add a new API endpoint for user preferences"). It writes code. Compare output against actual codebase conventions from Phase 1. Deviations reveal: ✅ rule works, ⚠️ rule exists but too weak, ❌ gap — no rule covers this. The newcomer's explicitly-noted assumptions are especially valuable — each is a candidate rule.

2. **Prior Override Test** (catches **weakness**): Give it the instruction file + 4-6 questions where common training priors conflict with rules (e.g., "how do you handle errors?" when the rule says `Result<T>` but agents default to try/catch). Score override rate — below 75% means rules are systemically too weak.

3. **Cross-rule Contradiction Finder** (catches **inconsistency**): Give it the instruction file and ask it to find scenarios where following Rule A requires violating Rule B, plus rules ambiguous enough for opposite interpretations.

**Critical**: Do NOT include codebase files, Phase 1 analysis, or any other context in the subagent prompts. The whole point is isolation — if the subagent can only succeed by reading the rules, then the rules are working.

#### After all challenges

Update the instruction file before presenting to the human:
- Add rules for Newcomer gaps. Strengthen rules with low override rates. Resolve contradictions.
- Include the validation summary in Phase 4 — it's evidence the rules were tested, not just written.

```
ADVERSARIAL VALIDATION SUMMARY
Simulated Newcomer: [N] correct, [N] weak, [N] gaps → [N] rules added
Prior Override: [N/M] override rate — [list failed topics]
Contradictions: [N] found → resolved | Ambiguities: [N] found → clarified
```

---

### PHASE 4 — Review, Refinement & Delivery

Present the synthesized rules to the human. Frame the review around quality:

```
"Here are the synthesized rules. Before we finalize, I want you to check three things:

1. ACCURACY — Is any rule wrong or outdated?
2. PRIORITY — Is anything critical missing? Is anything included that doesn't matter much?
3. TONE — Does this sound like your team? Would a teammate read this and nod?"
```

Iterate based on feedback. Common refinement patterns:
- Rule is too vague → ask for a concrete example, rewrite with specificity
- Rule is wrong → correct and verify with human
- Missing context → run a targeted mini-extraction (1-2 questions) for the specific gap
- Too long → help prioritize, move lower-priority rules to scoped files or a separate reference doc

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

**1. The human is the oracle, not the bottleneck.** Minimize their effort per unit of extracted knowledge. Ask sharp questions. Accept concise answers. Never make them feel like they're filling out a form.

**2. Code-reading comes first.** Every question you ask that the code already answers is a trust-eroding waste of the human's time. Do your homework.

**3. Specificity is non-negotiable.** If a rule can't be violated, it can't be followed. Every rule must be falsifiable. Push back on vague answers during extraction — "Can you give me a concrete example?" is always valid.

**4. Rules from failures > rules from aspirations.** A rule born from a real production incident carries more signal than ten rules from a style guide. Always start with failures.

**5. Don't generate rules the agent doesn't need.** If the linter catches it, don't write a rule. If the code makes it obvious, don't write a rule. Only document the delta between "what the code says" and "what a competent team member knows."

**6. Respect the token budget — but WHY beats brevity.** The instruction file competes with actual code for context window space. Every token must earn its place. But when forced to choose between a terse rule without rationale and a longer rule with WHY, keep the WHY. Agents circumvent rules they don't understand.

**7. Match the team's voice.** If the team writes terse commit messages and short PR descriptions, the instruction file should be terse. If they write detailed RFCs, the file can be more explanatory. Mirror the culture.

---

## Composes With

- `context-gap-analyzer` → agent-instruction-forge: Use context-gap-analyzer first to audit what implicit context is missing from a codebase, then use this skill to create the rules that fill those gaps.
- agent-instruction-forge → `edd`: After creating instruction rules, use EDD to validate that the rules actually improve agent behavior via eval-driven iteration.
- agent-instruction-forge → `context-eval`: Measure whether the new instruction file produces better agent outcomes than the baseline.