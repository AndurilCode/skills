---
name: code-review-amplifier
description: "Apply this skill whenever the user asks to review code, a PR, a diff, or a merge request — or when they paste code and ask for feedback on it. Also trigger when someone asks to 'prepare a review', 'check this PR', 'review my changes', 'what do you think of this code', 'is this PR ready to merge', 'help me review', or any situation where code quality assessment is involved. This skill does NOT try to replace the human reviewer. It amplifies human reviewers by assembling context, pre-scanning surface issues, generating design coherence questions, and routing knowledge-transfer opportunities. Use this skill even for small snippets — the 7-dimension framework scales down gracefully. If the user says 'code review' in any form, trigger this skill."
---

# Code Review Amplifier

**Core principle**: A perfect code review serves seven concurrent functions on a shared artifact. AI can fully handle 2/7, partially handle 2/7, and barely touch 3/7. This skill maximizes total review quality by doing what AI does well (surface scanning, velocity) while *arming the human reviewer* with context and questions for the dimensions that require human judgment (design coherence, knowledge transfer, mentoring).

The goal is not to produce a review. The goal is to make the human reviewer's next 15 minutes dramatically more effective.

---

## The Seven Dimensions of Code Review

Every code review, consciously or not, operates across these dimensions. Most reviews only cover 2-3 of them. A "perfect" review touches all seven with appropriate depth.

| # | Dimension | Core Question | AI Role |
|---|-----------|---------------|---------|
| **D1** | Correctness | Does this code do what it claims? | **Pre-scan**: Flag logic issues, edge cases, type mismatches, missing error handling |
| **D2** | Design Coherence | Does this fit the system's architecture? | **Arm the human**: Surface relevant architectural context, generate design questions |
| **D3** | Readability | Can the next person understand this? | **Pre-scan**: Flag complexity, naming, structure, readability issues |
| **D4** | Security & Resilience | Does this introduce vulnerabilities? | **Pre-scan**: Check for common vulnerability patterns, data exposure, failure modes |
| **D5** | Knowledge Transfer | Do more people now understand this area? | **Route**: Suggest who else should see this code and why |
| **D6** | Mentoring | Did the author learn from this review? | **Inform the human**: Note the author's patterns — what they're improving on, where they keep stumbling |
| **D7** | Velocity | Was the review timely and actionable? | **Deliver**: Be fast, structured, and scannable |

---

## How to Execute This Skill

Follow these phases in order. Each phase builds on the previous one. The output is a single structured review brief that a human reviewer can consume in under 3 minutes.

---

### PHASE 1 — Context Assembly

Before looking at the code itself, assemble the context that makes a review meaningful. This is the highest-leverage step — it's what separates a rubber-stamp review from a thoughtful one.

**Gather whatever is available from these sources** (skip what doesn't exist — work with what you have):

1. **The change itself**: What files are touched? What's the stated purpose? (PR title, description, commit messages, linked issues)
2. **Architectural context**: Are there `.ctx` files, `ARCHITECTURE.md`, `AGENTS.md`, or `CLAUDE.md` files in the repo? ADRs (Architecture Decision Records)? Read them for the areas this change touches.
3. **Recent history**: What recent changes have been made to these files? Is there an active refactor? A pattern migration in progress?
4. **Testing context**: What test coverage exists for the affected areas? Are there integration tests? What's the testing philosophy here?
5. **Author context**: If provided — what's the author's experience level with this area of the codebase? Are they new to the team? A domain expert?

Write the context brief:

```
CONTEXT BRIEF
Purpose: [What this change is trying to accomplish, in one sentence]
Scope: [Files/modules touched, approximate size]
Risk surface: [Low / Medium / High — based on what this touches]
Architectural relevance: [Which system boundaries or patterns does this cross?]
Missing context: [What you couldn't find but a human reviewer should look for]
```

The "Missing context" line is critical. It tells the human reviewer exactly where their judgment is needed because the AI couldn't find the information.

---

### PHASE 2 — Surface Pre-Scan (D1, D3, D4)

Scan the code across three dimensions where AI pattern matching is strong. Be concise and precise — every finding should be actionable.

**D1 — Correctness scan**:
- Logic errors, off-by-one, null/undefined paths
- Missing error handling or edge cases
- Inconsistencies between the stated purpose and the actual implementation
- Race conditions, state management issues
- Test coverage gaps (untested branches, missing edge case tests)

**D3 — Readability scan**:
- Naming clarity (variables, functions, classes)
- Function/method length and cognitive complexity
- Dead code, commented-out code, TODOs without context
- Consistency with existing codebase patterns
- Documentation gaps for non-obvious logic

**D4 — Security & Resilience scan**:
- Input validation and sanitization
- Authentication/authorization gaps
- Data exposure (logging sensitive data, returning too much in API responses)
- Dependency risks (new dependencies, known vulnerabilities)
- Error messages that leak internal details
- Failure modes (what happens when this breaks?)

**Output format for each finding**:

```
[D1/D3/D4] [SEVERITY: Critical | Warning | Suggestion]
📍 Location: [file:line or function name]
Finding: [One sentence — what's wrong]
Why it matters: [One sentence — what could go wrong]
Suggested fix: [Concrete suggestion, not vague advice]
```

**Severity calibration**:
- **Critical**: Will cause bugs in production, security vulnerability, data loss risk. Must fix before merge.
- **Warning**: Could cause problems under certain conditions, or violates important patterns. Should discuss.
- **Suggestion**: Improvement opportunity. Nice to have, not blocking.

Keep the total pre-scan findings to **a maximum of 10**. If there are more than 10 issues, prioritize by severity and group the rest as a summary ("Additionally, 5 minor readability suggestions around naming consistency in `utils.ts`"). Flooding the review with noise is the fastest way to get ignored — the skill optimizes for signal-to-noise ratio.

---

### PHASE 3 — Design Coherence Questions (D2)

This is the phase that matters most — and where the skill explicitly *does not pretend to have answers*. Instead, it generates the questions that a human reviewer with system knowledge should consider.

**Generate 2-5 design coherence questions**, drawn from:

- **Pattern alignment**: "This introduces [pattern X]. The rest of the codebase uses [pattern Y] for similar operations. Is this intentional divergence or should it align?"
- **Boundary violations**: "This change crosses the boundary between [module A] and [module B]. Is the coupling acceptable here, or should this go through [existing interface]?"
- **Future impact**: "If this pattern is adopted elsewhere, what happens at scale? Does the approach hold up with 10× more [entities/traffic/data]?"
- **Alternative approaches**: "Have you considered [alternative] which would [benefit]? The trade-off is [cost]."
- **Consistency with direction**: "The last ADR for this area decided [X]. This change [aligns with / diverges from] that direction. Is the ADR still current?"

Frame every question as a genuine question, not a disguised criticism. The format:

```
🏗️ DESIGN QUESTION [1-5]
Context: [Why this question is worth asking — what you observed]
Question: [The actual question for the human reviewer to consider]
What to look for: [Guidance on how to evaluate the answer]
```

If you don't have enough architectural context to generate meaningful design questions, say so explicitly: "I lack architectural context for this area. The human reviewer should assess design coherence directly." This is more valuable than inventing shallow questions.

---

### PHASE 4 — Knowledge & Growth Signals (D5, D6)

**Knowledge Transfer (D5)**:
- Who else on the team would benefit from seeing this code? (Based on file ownership, related modules, or domain relevance)
- Does this change introduce a pattern or technique that others should learn about?
- Is there tribal knowledge embedded in this code that should be documented?

```
📚 KNOWLEDGE ROUTING
Suggested additional reviewers: [Who and why — "Alex works on the payment module that this hooks into"]
Documentation opportunity: [If this change introduces something others need to know]
```

**Mentoring signals (D6)**:
Only include this section if there's genuine signal — patterns in the code that suggest growth opportunities. Never be condescending. Frame as observations, not judgments.

```
🌱 AUTHOR PATTERNS (for the human reviewer's eyes)
Positive: [What the author is doing well — be specific]
Growth area: [A pattern that suggests a learning opportunity — frame constructively]
```

Skip this section entirely if you don't have enough context about the author or if the code doesn't show clear patterns. Forced mentoring observations are worse than none.

---

### PHASE 5 — Review Brief Assembly

Assemble the complete review brief. This is the deliverable — what the human reviewer reads before (or instead of) doing their own line-by-line pass.

```
═══════════════════════════════════════════════
CODE REVIEW AMPLIFIER — REVIEW BRIEF
═══════════════════════════════════════════════

[CONTEXT BRIEF from Phase 1]

───────────────────────────────────────────────
PRE-SCAN FINDINGS (D1 · D3 · D4)
───────────────────────────────────────────────

[Findings from Phase 2, grouped by severity]

───────────────────────────────────────────────
DESIGN COHERENCE QUESTIONS (D2)
───────────────────────────────────────────────

[Questions from Phase 3]

───────────────────────────────────────────────
KNOWLEDGE & GROWTH (D5 · D6)
───────────────────────────────────────────────

[Signals from Phase 4, if any]

───────────────────────────────────────────────
DIMENSION COVERAGE SUMMARY
───────────────────────────────────────────────
D1 Correctness:        [✅ Scanned | ⚠️ Findings | ❌ Couldn't assess]
D2 Design Coherence:   [🔍 Questions generated | ❌ Insufficient context]
D3 Readability:        [✅ Scanned | ⚠️ Findings | ❌ Couldn't assess]
D4 Security:           [✅ Scanned | ⚠️ Findings | ❌ Couldn't assess]
D5 Knowledge Transfer: [📚 Routing suggested | ➖ Not applicable]
D6 Mentoring:          [🌱 Signals noted | ➖ Insufficient context]
D7 Velocity:           [⚡ Delivered]
```

The Dimension Coverage Summary at the end serves two purposes: it shows the human reviewer which dimensions still need their attention, and over time it becomes the measurement layer — teams can track which dimensions are consistently covered vs. consistently missed.

---

## Calibration Rules

These rules prevent the most common failure modes of AI code review:

**1. Signal over volume**: 5 high-quality findings beat 30 nitpicks. If the code is generally clean, say "Surface scan: no significant findings across D1/D3/D4" and move on. Don't manufacture issues to look thorough.

**2. Confidence calibration**: If you're not sure about a finding, prefix it with "Possible:" and explain why you're uncertain. Never state a false positive with high confidence — it destroys trust faster than missing a real bug.

**3. Context humility**: When you lack context (no architecture docs, no test suite to reference, no PR description), say so. "I'm reviewing this without architectural context — the design questions below are surface-level" is honest and useful. Pretending to have context you don't have produces useless reviews.

**4. Respect the author**: Every finding is a suggestion to a human who made a deliberate choice. Use language like "Consider..." and "Have you evaluated..." rather than "This is wrong" or "You should...". The human reviewer will decide what's actionable.

**5. Don't replicate linting**: If the project has a linter, ESLint, Prettier, or similar — don't duplicate their job. Focus on things automated tools can't catch. If you spot a style issue that a linter should have caught, the finding is "Your linter may not be configured to catch [X]" — not the style issue itself.

**6. Adapt to scope**: A 10-line utility function doesn't need 5 design coherence questions. Scale the review depth to the change size and risk surface. Small changes get a light touch. Large changes touching core systems get the full treatment.

---

## Thinking Triggers

These questions help calibrate the review:

- *"If this code caused an incident next week, what would the post-mortem find?"*
- *"What does this code assume about the rest of the system that might not be true?"*
- *"If I were onboarding tomorrow and had to modify this, what would confuse me?"*
- *"What's the blast radius if this goes wrong?"*
- *"Is this change fighting the codebase or flowing with it?"*
