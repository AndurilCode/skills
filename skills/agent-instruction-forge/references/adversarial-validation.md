# Adversarial Validation — Subagent Prompts & Evaluation

Read this file when executing Phase 3b of the Agent Instruction Forge skill.

---

## Principles

- **Context isolation is everything.** Each subagent receives ONLY the instruction file. No codebase, no Phase 1 findings, no conversation history. If you leak context, the validation is worthless.
- **Spawn in parallel.** The three challenges are independent — run them simultaneously.
- **The primary agent evaluates.** Subagents produce raw output. The primary agent (you) compares against Phase 1 findings and scores.

---

## Challenge 1: Simulated Newcomer

### Subagent Prompt

```
You are a developer who just joined a new project. You have ZERO access to the
existing codebase — no files, no git history, no context beyond the instruction
file below. Follow the instructions exactly. Do not assume anything they don't
explicitly state.

INSTRUCTION FILE:
---
{paste synthesized instruction file}
---

TASK: {realistic task — e.g., "Add a new REST endpoint for user notification
preferences with input validation, database persistence, and tests"}

Write the complete code you would produce, including:
- File paths (where each file goes in the project)
- Full imports
- Implementation
- Tests if the instructions mention testing conventions

Where the instructions are SILENT on something, use your best judgment but
explicitly note: "ASSUMPTION: [what you assumed and why]"
```

### Choosing the Task

Pick a task that:
- Touches 2-3 rules simultaneously (tests rule interaction)
- Involves a high-traffic area of the codebase
- Requires architectural decisions (which module? which pattern? which utilities?)
- Has a clear "correct answer" in the real codebase to compare against

Avoid: trivial tasks (rename a variable), tasks outside the codebase's domain.

### Evaluation

Compare the newcomer's output against actual codebase conventions from Phase 1:

| Signal | Meaning | Action |
|---|---|---|
| ✅ Got it right | Rule works | None |
| ⚠️ Got it wrong, rule exists | Rule too vague or buried | Strengthen: add specificity, move higher, add example |
| ❌ Got it wrong, no rule covers it | Coverage gap | Draft new rule from the deviation |

Check specifically: file placement, import patterns, error handling, test structure, naming.

The newcomer's ASSUMPTION notes are gold — each is a place where the instruction file is silent and the agent had to guess. Every assumption is a candidate rule.

### Output Format

```
SIMULATED NEWCOMER RESULTS
Task: [description]
✅ CORRECT: [what it got right, which rule guided it]
⚠️ RULE TOO WEAK: [deviation, existing rule text, how to strengthen]
❌ GAP: [deviation, expected behavior, candidate new rule]
ASSUMPTIONS NOTED: [list — each is a candidate rule]
```

---

## Challenge 2: Prior Override Test

### Subagent Prompt

```
You are a developer working on a project. You have ONLY the instruction file
below as context. Answer each question with exactly what you would do in this
codebase.

Be specific — name files, patterns, and approaches. Do NOT hedge or give
multiple options. Commit to ONE answer per question based on what the
instructions tell you.

INSTRUCTION FILE:
---
{paste synthesized instruction file}
---

QUESTIONS:
1. {question targeting a known override}
2. {question targeting another override}
3. {question targeting architectural override}
4. {question targeting pattern override}
5. {question targeting tooling override}
6. {question targeting convention override}
```

### Choosing Questions

For each rule that contradicts a common framework/language default (identified in Phase 1 Step 3), craft a question that naturally triggers the default prior:

| Codebase rule | Prior it fights | Question |
|---|---|---|
| "Return Result<T>, never throw" | Try/catch is universal default | "How would you handle errors in an API endpoint?" |
| "Use Vitest, never Jest" | Jest dominates training data | "What testing framework for a new test?" |
| "Direct Prisma, no repository layer" | Repository pattern is widely taught | "How would you structure database access?" |
| "Structured logger, not console.log" | console.log is the default | "How would you add logging to debug an issue?" |
| "CSS modules, not Tailwind" | Tailwind is trending | "How would you style a new component?" |
| "Feature flags via LaunchDarkly" | Simple env vars is the default | "How would you gate a feature for gradual rollout?" |

Aim for 4-6 questions. Best questions are open-ended so the agent must commit to an approach.

### Evaluation

Score each answer:
- **Override Success** (✅): Answer matches the codebase rule
- **Override Failure** (❌): Agent defaulted to training prior despite the rule

**Overall rate below 75%** = systemic weakness in the instruction file.

### Fixing Override Failures

For each failure, apply one or more:
1. **Add explicit anti-pattern**: "Do NOT use [default]. We use [ours] instead."
2. **Strengthen WHY**: explain the consequence of using the default
3. **Move rule higher in file**: agents weight earlier content more heavily
4. **Add canonical example**: point to a specific file that demonstrates the pattern
5. **Promote to Critical Rules**: move from Conventions if the override matters enough

### Output Format

```
PRIOR OVERRIDE RESULTS
Q1: [topic] → ✅ Override success | ❌ Failure (defaulted to [X])
Q2: ...
Override rate: [N/M] ([percentage])
Rules needing strengthening: [list with specific fix per rule]
```

---

## Challenge 3: Cross-rule Contradiction Finder

### Subagent Prompt

```
You are a rules auditor. Your job is to find internal inconsistencies and
ambiguities. Be thorough and adversarial.

Read this instruction file and perform two analyses:

ANALYSIS 1 — CONTRADICTIONS:
Find scenarios where following one rule REQUIRES violating another rule.
For each contradiction:
  1. Quote both conflicting rules
  2. Describe the specific scenario that triggers the conflict
  3. Explain why they can't both be satisfied
  4. Suggest which should take priority and how to resolve

ANALYSIS 2 — AMBIGUITIES:
Find rules that are ambiguous enough that two competent developers could
reasonably interpret them to mean OPPOSITE things.
For each ambiguity:
  1. Quote the ambiguous rule
  2. Give both plausible interpretations
  3. Suggest a rewrite that eliminates the ambiguity

Look hard. Even small contradictions matter — an agent encountering conflicting
rules behaves non-deterministically, which is worse than having no rule.

INSTRUCTION FILE:
---
{paste synthesized instruction file}
---
```

### Common Contradiction Patterns

Watch for:
- **Scope overlap**: repo-wide rule says X, scoped rule says not-X for the same area
- **Convention vs. architecture**: coding pattern conflicts with boundary rule
- **Testing vs. performance**: thoroughness rules conflict with constraint rules
- **New vs. legacy**: rules for new code conflict with legacy maintenance rules
- **DRY vs. explicit**: reuse rules conflict with explicitness rules

### Resolution

| Resolution | When to use |
|---|---|
| Scope qualifier | Rules apply in different contexts — make explicit |
| Precedence | Add "except when X" to lower-priority rule |
| Merge | Both say the same thing differently — combine |
| Rewrite | One is wrong or outdated |
| Remove | One is subsumed by the other |

### Output Format

```
CONTRADICTION SCAN
Contradictions: [N]
  ⚠️ [Rule A] vs [Rule B] — scenario: [X] — resolution: [fix]
Ambiguities: [N]
  ⚠️ "[rule]" — interp A: [X], interp B: [Y] — rewrite: "[clearer]"
```

---

## Integration — Applying Results

After all three subagents complete:

1. **From Newcomer ❌ gaps**: Draft new rules. Apply Seven Properties. Insert in appropriate section.
2. **From Newcomer ⚠️ weak rules**: Add anti-patterns, improve WHY, add canonical examples, move higher.
3. **From Override failures**: Apply strengthening techniques. Target 75%+ override rate.
4. **From Contradictions**: Resolve each one. Clarify ambiguities with rewrites.
5. **Re-check token budget**: Additions may push over limit. Prioritize: gap rules > strengthened overrides > ambiguity fixes.

### Summary for Phase 4

```
ADVERSARIAL VALIDATION SUMMARY
═══════════════════════════════════════════
Simulated Newcomer:
  Task: [description]
  ✅ [N] correct  ⚠️ [N] weak → strengthened  ❌ [N] gaps → rules added

Prior Override Test:
  Override rate: [N/M] ([%])
  Failed: [topics] → strengthened

Contradictions: [N] → resolved | Ambiguities: [N] → clarified
Net: [N] modified, [N] added, [N] removed
```