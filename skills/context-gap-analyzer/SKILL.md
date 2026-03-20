---
name: context-gap-analyzer
description: "Identify the implicit context missing from a codebase that would most improve agent performance — the knowledge that code can't explicitly tell. Use this skill whenever someone asks to audit, assess, or improve context for a codebase; wants to find what's undocumented but critical for agents; asks 'what context is my codebase missing?', 'why do agents keep making mistakes here?', 'how do I improve agent performance on my repo?', 'what should I put in my AGENTS.md / CLAUDE.md / .context files?', 'audit my codebase context', 'context coverage', 'context gaps', 'what does an agent need to know about this codebase?', or any variation. Also trigger when a user is setting up agent context infrastructure for the first time, or when agent-generated code keeps violating implicit conventions. This is the context engineer's primary diagnostic tool."
---

# Context Gap Analyzer

**Core principle**: Code is necessary but insufficient context. The delta between "what the code explicitly says" and "what a competent team member knows" is where agents fail most expensively. This skill systematically identifies that delta, prioritizes it by agent impact, surfaces it as focused questions a human can answer, and tracks the answers into whatever context harness the codebase already uses.

An agent reading only code can derive syntax, types, structure, and test behavior. What it *cannot* derive:
- **Why** decisions were made (rationale)
- **What** conventions exist that aren't enforced by tooling (tribal knowledge)
- **How** things interact with systems beyond the repo boundary (integration knowledge)
- **When** to break a pattern vs. follow it (judgment)
- **Who** owns what and why (organizational context)

This skill helps the context engineer close those gaps, one focused question at a time.

---

## How to Execute This Skill

Follow these phases in order. Each phase builds on the previous. The final deliverable is a prioritized gap report with actionable questions, a quantified coverage map, and a tracking mechanism integrated into the existing context harness.

---

### PHASE 1 — Context Harness Discovery

Before analyzing gaps, discover the *full* context infrastructure already in place. Context harnesses are not a finite set — they evolve constantly. New conventions, tools, and delivery mechanisms emerge all the time. Do not rely on a checklist. Instead, **actively explore** the environment and classify everything you find.

**Discovery procedure — work through all four layers**:

#### Layer 1: File-level context (scan the repo)

Explore the repository root and 2-3 levels deep. Look for any files or directories whose name, location, or content suggests they carry context intended for humans or agents. Common *examples* include `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.context/`, `ARCHITECTURE.md`, ADR directories, `CONTRIBUTING.md`, `CONVENTIONS.md` — but these are illustrations, not a checklist. Anything that reads like "instructions for someone working in this codebase" is a context file, regardless of its name or format.

For each file found:
- Read it. Inventory what topics it covers.
- Note its scope (repo-wide, directory-scoped, module-specific).
- Note its format (markdown prose, structured rules, YAML front matter, JSON, etc.).
- Note its audience (humans, specific agents, general).

#### Layer 2: Toolchain-level context (inspect the agent environment)

The agent's toolchain *is* part of the harness. Look for:
- **MCP servers**: What MCP servers are available in the current environment? Each connected server is a context delivery channel — it tells the agent what external capabilities exist (e.g., a connected Jira MCP server means the agent can look up ticket context on-demand, which changes what needs to be pre-documented vs. fetched live).
- **Skills / plugins**: Are there installed skills (like this one), custom plugins, or extensions that shape agent behavior? What context do they already provide?
- **Hooks / middleware**: Git hooks, CI hooks, pre-commit configs, Claude Code hooks, linting configs — anything that runs automatically and enforces or injects context. These are implicit context delivery mechanisms.
- **IDE / editor config**: `.vscode/`, `.idea/`, editor-specific agent configs — these shape how the development environment presents context to both human and agent.

#### Layer 3: Runtime context (what's available but not in the repo)

Some context isn't stored in files — it's accessible through tools at runtime:
- **Connected services**: Google Drive, Notion, Confluence, Slack — if the agent can search these, they're part of the context surface. Document what's reachable vs. what must be pre-baked into repo files.
- **Environment variables / secrets management**: How is configuration injected? This affects what the agent needs to know about deployment contexts.
- **Package manager metadata**: `package.json`, `pyproject.toml`, `Cargo.toml` — these carry implicit architectural context (dependency choices signal patterns).

#### Layer 4: Delivery mechanism classification

After discovery, classify each context source by how it reaches the agent:

| Delivery | Examples | Implication |
|----------|----------|-------------|
| **Static (always in context)** | `AGENTS.md`, `.cursorrules`, system prompts | Token budget cost; must be concise |
| **On-demand (fetched when needed)** | MCP servers, connected search, skill files | Can be richer; agent must know *when* to fetch |
| **Triggered (injected by hooks)** | Git hooks, CI checks, pre-commit rules | Enforcement, not guidance; agent may not see the *why* |
| **Implicit (embedded in code)** | Type signatures, test assertions, linter configs | Partial context; the rationale behind choices is missing |

Write the discovery output:

```
CONTEXT HARNESS DISCOVERY
━━━━━━━━━━━━━━━━━━━━━━━━━

Static context files:
  [path] — covers: [topics] — scope: [repo/dir/module] — format: [type]
  ...

Toolchain context:
  MCP servers: [list connected servers and what they provide]
  Skills/plugins: [list what's installed]
  Hooks/enforcement: [list what runs automatically]

Runtime context:
  Connected services: [what's searchable on-demand]
  Config injection: [how env/secrets reach the code]

Delivery map:
  Static:    [count] sources, ~[X] topics covered
  On-demand: [count] sources available
  Triggered: [count] enforcement mechanisms
  Implicit:  [assessment — "heavy reliance on code-as-docs" or "well-supplemented"]

Already documented topics: [inventory from reading all discovered files]
Primary delivery format: [inferred from what exists — this determines Phase 6 output format]
```

If no context infrastructure is detected at all, note this explicitly and recommend the simplest viable starting point for the codebase type. But be thorough before concluding "nothing exists" — a `.eslintrc` is context. A `Makefile` with well-named targets is context. A `docker-compose.yml` with service labels is context. The question is whether it's *sufficient* context, not whether *any* exists.

---

### PHASE 2 — Codebase Topology Scan

Map the codebase structure to understand what areas exist, their relative complexity, and where agent activity is likely to concentrate.

**Scan these dimensions**:

1. **Directory structure**: Map top-level modules and their depth. Identify: source roots, test directories, configuration layers, build/deploy scripts, documentation directories.

2. **Technology fingerprint**: Languages, frameworks, package managers, build tools. This tells you what kind of implicit knowledge agents need (e.g., a Next.js app has different implicit conventions than a Django app).

3. **Complexity indicators** (proxies, not exact science):
   - File count per top-level module
   - Presence of deeply nested directories (often signals complex business logic)
   - Configuration file count and variety (signals integration complexity)
   - Number of environment-specific files (signals deployment complexity)

4. **Integration surface**: External service configs, API client directories, database migration directories, message queue configs, third-party SDK usage.

5. **Entry points**: Main files, route definitions, API endpoint directories, CLI command files, event handlers.

Write the topology output:

```
CODEBASE TOPOLOGY
Type: [monorepo / single-app / library / CLI tool / etc.]
Languages: [primary, secondary]
Framework: [detected framework(s)]
Top-level modules: [list with approximate complexity ranking]
Integration surface: [external dependencies and services detected]
High-traffic areas: [directories agents will touch most often based on structure]
```

---

### PHASE 3 — Gap Analysis (The Core)

Cross-reference Phase 1 (what's documented) against Phase 2 (what exists in code). Evaluate nine categories of implicit context. For each, assess the gap between what the code implies and what's explicitly documented.

#### The Nine Context Categories

**C1 — Architecture & System Boundaries**
What an agent needs: Component topology, service boundaries, data flow direction, module dependency rules, what talks to what and how.
Code signals: Directory structure, import patterns, service client files, API routes.
Gap indicator: Agent creates cross-boundary imports, puts code in the wrong module, misunderstands data flow direction.

**C2 — Domain Model & Business Rules**
What an agent needs: Business logic rationale, domain vocabulary, invariants, validation rules that aren't just type checks.
Code signals: Model files, validation logic, business rule functions, enum/constant definitions.
Gap indicator: Agent writes technically correct but domain-wrong code, misnames domain concepts, violates business invariants.

**C3 — Conventions & Patterns**
What an agent needs: Naming conventions, file organization rules, error handling patterns, logging conventions, code style beyond linter rules.
Code signals: Repeated patterns across files, consistent naming schemes, shared utility usage.
Gap indicator: Agent writes code that works but "feels wrong" to the team — inconsistent style, unfamiliar patterns, reinvented utilities.

**C4 — Integration & External Dependencies**
What an agent needs: How external APIs are called, retry/fallback strategies, rate limits, auth patterns, environment-specific behaviors.
Code signals: API client code, SDK wrappers, configuration files, environment variables.
Gap indicator: Agent calls external services incorrectly, misses retry logic, hardcodes environment-specific values.

**C5 — Operations & Deployment**
What an agent needs: CI/CD pipeline structure, feature flag system, rollback procedures, monitoring/alerting conventions, environment promotion flow.
Code signals: CI config files, Dockerfiles, deploy scripts, feature flag configs, monitoring setup.
Gap indicator: Agent writes code that breaks CI, doesn't follow feature flag conventions, introduces unmonitored failure modes.

**C6 — Testing Philosophy & Strategy**
What an agent needs: What gets unit-tested vs. integration-tested, mocking conventions, fixture patterns, test naming, coverage expectations.
Code signals: Test directory structure, test file patterns, mock/fixture files, test configuration.
Gap indicator: Agent writes wrong kind of tests, mocks at wrong boundaries, misses critical test scenarios, duplicates test infrastructure.

**C7 — Security Model**
What an agent needs: Auth patterns, authorization boundaries, data classification, secret management, input validation conventions.
Code signals: Auth middleware, permission checks, secret references, security-related utilities.
Gap indicator: Agent introduces auth bypasses, logs sensitive data, exposes internal details in API responses.

**C8 — Performance Constraints**
What an agent needs: Known bottlenecks, caching strategy, query optimization patterns, pagination conventions, rate limiting.
Code signals: Cache layers, query builders, pagination utilities, performance-related comments.
Gap indicator: Agent introduces N+1 queries, skips caching, builds unbounded queries, ignores pagination.

**C9 — Historical Decisions & Tech Debt**
What an agent needs: Why things are the way they are, planned migrations, "don't touch this" zones, temporary workarounds, deprecated patterns.
Code signals: TODO/FIXME comments, legacy directories, version-suffixed files, deprecated annotations.
Gap indicator: Agent extends deprecated patterns, builds on code scheduled for removal, repeats historical mistakes.

#### Scoring Each Category

For each category, assess:

| Factor | Score | Meaning |
|--------|-------|---------|
| **Documentation coverage** | 0-3 | 0 = nothing, 1 = mentioned, 2 = partial, 3 = thorough |
| **Code complexity** | 1-3 | 1 = simple/obvious, 2 = moderate, 3 = complex/non-obvious |
| **Agent exposure** | 1-3 | 1 = rarely touched, 2 = sometimes, 3 = frequently modified |

**Gap severity** = Code complexity × Agent exposure − Documentation coverage

This produces a score from -2 (over-documented simple code) to 9 (undocumented complex code agents touch constantly). Anything ≥ 5 is a critical gap. 3-4 is significant. ≤ 2 is acceptable.

Write the gap analysis:

```
GAP ANALYSIS
                          Doc  Complex  Exposure  Gap Score  Priority
C1 Architecture           [0-3] [1-3]   [1-3]     [score]   [Critical/Significant/OK]
C2 Domain Model           ...
C3 Conventions            ...
C4 Integration            ...
C5 Operations             ...
C6 Testing                ...
C7 Security               ...
C8 Performance            ...
C9 Historical Decisions   ...

Overall coverage: [percentage — sum of Doc scores / (9 × 3) × 100]
Critical gaps: [list categories with score ≥ 5]
```

---

### PHASE 4 — Prioritized Question Generation

For each gap scoring ≥ 3 (significant or critical), generate focused questions that a human can answer in 2-5 minutes each. These questions are the primary deliverable — they're the fastest path from "undocumented tribal knowledge" to "agent-readable context."

**Question design principles**:
- Each question targets exactly one piece of implicit knowledge
- The answer should be directly usable as agent context (no "describe your architecture" vagueness)
- Questions are ordered by gap severity × actionability
- Group by category but present in priority order across categories

**Question format**:

```
Q[number] — [Category code] — Priority: [Critical / High / Medium]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[The question — specific, focused, answerable in 2-5 minutes]

Why this matters for agents:
[One sentence explaining what goes wrong without this context]

Example of a good answer:
[A brief template showing the level of detail needed]
```

Generate 10-20 questions total, with at least 2 for each critical gap and 1 for each significant gap. Front-load the highest-impact questions.

---

### PHASE 5 — Coverage Map

Generate a quantified coverage map that visualizes the current state. This serves as the baseline for tracking improvement over time.

**Coverage map format** (render as a visual artifact if the environment supports it, otherwise output as structured text):

```
CONTEXT COVERAGE MAP — [repo name] — [date]
═══════════════════════════════════════════════════════

C1 Architecture      [████████░░░░░░░░░░░░]  40%  ⚠️ Significant gap
C2 Domain Model      [██░░░░░░░░░░░░░░░░░░]  10%  🔴 Critical gap
C3 Conventions       [██████████████░░░░░░]  70%  ✅ Acceptable
C4 Integration       [████░░░░░░░░░░░░░░░░]  20%  🔴 Critical gap
C5 Operations        [████████████░░░░░░░░]  60%  ⚠️ Significant gap
C6 Testing           [██████████░░░░░░░░░░]  50%  ⚠️ Significant gap
C7 Security          [████████░░░░░░░░░░░░]  40%  ⚠️ Significant gap
C8 Performance       [██░░░░░░░░░░░░░░░░░░]  10%  🔴 Critical gap
C9 Historical        [░░░░░░░░░░░░░░░░░░░░]   0%  🔴 Critical gap

OVERALL COVERAGE: 33%
Questions generated: 18 | Critical: 8 | High: 6 | Medium: 4
Estimated time to close critical gaps: ~40 minutes of human input
```

When the environment supports it (Claude.ai artifacts, HTML output), generate an interactive radar chart or heatmap visualization. Otherwise, the ASCII format above is the fallback.

---

### PHASE 6 — Tracking & Integration

Create a tracking file that persists the gap analysis and records progress as the user provides answers. The file format adapts to the detected harness.

**Tracking file**: `.context-coverage.json` (placed at repo root)

```json
{
  "version": "1.0",
  "repo": "[repo name]",
  "created": "[ISO date]",
  "updated": "[ISO date]",
  "harness": {
    "primary_format": "[inferred from discovery — e.g., 'markdown prose in AGENTS.md', '.ctx scoped files', etc.]",
    "static_sources": ["[paths to discovered static context files]"],
    "toolchain": ["[MCP servers, skills, hooks discovered]"],
    "delivery_summary": "[brief description of how context reaches agents in this codebase]"
  },
  "categories": {
    "C1_architecture": { "coverage": 40, "gap_score": 5, "questions_total": 3, "questions_answered": 0 },
    ...
  },
  "questions": [
    {
      "id": "Q01",
      "category": "C2",
      "priority": "critical",
      "question": "...",
      "status": "open",
      "answer": null,
      "integrated_to": null
    }
  ],
  "overall_coverage": 33
}
```

**When the user provides an answer**:
1. Update the question status to `"answered"` and store the answer text
2. Determine the best integration target by consulting the Phase 1 discovery output — specifically the primary delivery format and the delivery map
3. Write the answer into the harness using the conventions already established in the codebase:
   - Match the existing file's tone, structure, heading hierarchy, and formatting
   - Place content at the right scope (repo-wide context goes to repo-level files; module-specific context goes to directory-scoped files)
   - If the harness uses structured formats (YAML, JSON, rules syntax), match that format exactly
4. Update `integrated_to` with the file path where the context was written
5. Recalculate category coverage and overall coverage
6. Show the updated coverage map

**Integration principle**: Do not prescribe *where* context goes — infer it from what Phase 1 discovered. Read existing context files to absorb their voice, format, and organization before appending. If the codebase has a `.cursorrules` with terse imperative rules, write terse imperative rules. If it has prose-heavy `AGENTS.md` with rationale paragraphs, write prose with rationale. If it uses `.ctx` files scoped per directory, create a new scoped file. The skill adapts to the harness — never the reverse.

If no writable harness was found in Phase 1, ask the user where they want context written before proceeding. Suggest the simplest option that fits their environment, but let them decide.

---

## Running Incrementally

The skill supports incremental use:

- **First run**: Full analysis (Phases 1-6), generates baseline coverage map and all questions
- **Answer session**: User provides answers to questions → skill integrates them and updates coverage
- **Re-audit**: Re-run Phases 2-5 after significant codebase changes to detect new gaps
- **Coverage check**: Quick Phase 5 only, using existing `.context-coverage.json` to show current state

Detect which mode to use based on whether `.context-coverage.json` already exists and what the user is asking for.

---

## Calibration Rules

**1. Agent-first, not docs-first**: Every question must be framed from the perspective of "what would an agent get wrong?" — not "what's undocumented?" Plenty of undocumented things are obvious from code. Focus on the non-obvious.

**2. Precision over completeness**: 10 high-impact questions beat 50 thorough ones. The human's time is the bottleneck. Each question should unlock a meaningful improvement in agent behavior.

**3. Respect existing context**: If context files already exist, read them carefully. Don't generate questions whose answers are already documented. Cross-reference before asking.

**4. Harness humility**: Don't prescribe a context management approach. Detect what exists and work within it. If nothing exists, suggest the simplest viable option for the codebase type.

**5. Actionable answers**: The "example of a good answer" in each question is critical. It sets the bar for the level of detail needed and prevents both one-word answers and novel-length responses. Keep examples to 3-5 sentences.

**6. Coverage honesty**: Don't inflate coverage scores. A README that says "this is a web app" doesn't count as architecture documentation. Score based on what an agent would actually find useful, not what technically exists.

---

## Thinking Triggers

- *"If I dropped a competent agent into this codebase right now, what's the first mistake it would make?"*
- *"What does every team member know that no file in this repo says?"*
- *"Where has an agent already made a mistake because it lacked context? That's the highest-priority gap."*
- *"What's the costliest mistake possible from missing context? Work backwards from there."*
- *"Is this gap something I can close with a 3-sentence rule, or does it need a full architectural document?"*
