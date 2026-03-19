---
name: context-debugging
description: Use when an agent is failing, producing wrong output, ignoring instructions, hallucinating, or behaving unexpectedly — and the cause isn't an obvious code bug. Triggers on "my agent keeps failing", "the agent ignores my instructions", "it hallucinates even though I told it not to", "I fixed one thing but something else broke", "the agent used to work but now it doesn't", "why is the agent doing X instead of Y?". Do NOT use for infrastructure errors (API 500s, timeouts), code bugs in the harness (use systematic-debugging), or when the agent has never worked (use context-cartography to design first).
---

# Context Debugging

**Check context first. It's the highest-ROI debugging target for agent failures.**

The agent ignored your instructions? The instructions might be buried. The agent hallucinated? It might lack the context to know what's real. The agent used the wrong tool? The tool descriptions might be ambiguous.

Context problems are the most common *and most fixable* source of agent failures. Debug context first — not because it's always the cause, but because when it is, the fix is fast.

## The Boundary Rule

```
Agent is failing and it's not an obvious code bug?  →  Use this skill.
Agent has never worked (greenfield)?                →  Use context-cartography instead.
Infrastructure error (API 500, timeout)?            →  Not a context problem.
Code bug in the harness (template error, parsing)?  →  Use systematic-debugging.
```

---

## The Triage Flow

### Step 0 — VERIFY ACTUAL CONTEXT

Before diagnosing, confirm you can see what the model actually receives. The context the model sees may differ from what you think you're sending.

**Do this first:**
1. Log or dump the full assembled context (system prompt + tools + retrieved docs + conversation history)
2. Compare it to what you expect. Are all sections present? In the right order? At the expected size?
3. If actual ≠ intended → the bug is in context assembly (template, serialization, retrieval pipeline). Use systematic-debugging for the code fix.

If you skip this step, every diagnosis below could be wrong — you'd be debugging the context you *intended* to send, not the context the model *actually received*.

### Step 1 — OBSERVE

Describe the failure precisely:

- **What did you expect?** (the correct behavior)
- **What happened instead?** (the actual behavior)
- **How often?** (every time, sometimes, rarely)
- **When did it start?** (always, after a specific change, gradually)

"Sometimes" failures are the strongest signal that the problem is context — stochastic behavior means the model is on the boundary, and context tips the balance.

### Step 2 — CLASSIFY

Run through **all** diagnostic questions. Mark every "yes." Multiple categories often co-occur — a regression can introduce buried context, or a missing context fix can create a conflict.

Investigate matches in order (earliest first), but **don't stop at the first match**. If your fix doesn't resolve the failure, continue to the next matching category.

| # | Question | If yes → | Quick test |
|---|----------|----------|------------|
| 1 | Was context recently changed? | **REGRESSION** | Revert to previous version. Fixed? |
| 2 | Does the agent lack information it needs? | **MISSING CONTEXT** | Add the info manually. Fixed? |
| 3 | Are tool definitions ambiguous or overlapping? | **TOOL PROBLEM** | Read each tool def cold. Ambiguous? |
| 4 | Can the agent find the info in the context? | **BURIED CONTEXT** | Move the instruction to the top. Fixed? |
| 5 | Are any instructions contradictory (including emergent interactions)? | **CONFLICTING CONTEXT** | Remove one of the conflicting instructions. Fixed? |
| 6 | Does less context fix it? | **CONTEXT OVERFLOW** | Keep only essential items. Fixed? |
| 7 | None of the above? | **REASONING FAILURE** | Try with ideal minimal context. Still fails? |

### Step 3 — LOCATE & FIX

Once classified, use the category-specific section below. Each category includes a **quick fix** (under 10 minutes, no other skills required) and a **full fix** (thorough, may involve companion skills).

---

## Failure Categories

### REGRESSION — "It used to work"

The most common and most treatable failure. Something changed and broke existing behavior.

**Diagnostic:**
1. Diff the current context against the last known-good version
2. For each change, ask: "could this affect the failing behavior?"
3. Revert and confirm the failure disappears
4. Re-apply changes one at a time until the failure reappears

**Common causes:**
- New instructions that compete with existing ones for attention
- Restructured sections that moved critical instructions to lower-attention positions
- Removed text that was load-bearing without being obviously important
- Added examples that anchor the model on wrong patterns

**Quick fix:** Revert to the known-good version. Ship the revert. You've stopped the bleeding.

**Full fix:** Re-introduce the change incrementally, validating each step with EDD assertions. The regression often reveals that the change interacted with something else — check for BURIED CONTEXT or CONFLICTING CONTEXT as secondary causes.

---

### MISSING CONTEXT — "The agent doesn't know"

The agent lacks information it needs to do the task correctly.

**Diagnostic:**
1. Look at the agent's output. What information would it need to get this right?
2. Search for that information in the assembled context (Step 0 output). Is it there?
3. If using retrieval (RAG): was the right document retrieved? Check the retrieval results, not just the source data.

**Common causes:**
- Assumed the model "knows" something it doesn't (project conventions, internal terminology)
- Retrieval returned irrelevant documents (query mismatch, bad embeddings, wrong chunking)
- Conversation history truncated, losing earlier context
- Information exists in the system but wasn't included in the context

**Signals:**
- Agent produces generic/default behavior instead of project-specific behavior
- Agent asks questions the context should answer
- Agent hallucinates plausible-but-wrong details (filling gaps with training data)

**Quick fix:** Add the missing information directly to the system prompt. If this fixes the behavior, the diagnosis is confirmed.

**Full fix:** Use context-cartography to determine proper priority and sizing for the new context. If the problem was retrieval, fix the retrieval pipeline — adding context manually is a band-aid that won't generalize.

---

### TOOL DEFINITION PROBLEM — "The agent can't use its tools"

The agent selects wrong tools, passes wrong parameters, or doesn't use tools when it should.

**Diagnostic:**
1. Read each tool definition as if you'd never seen the tool before. Is it unambiguous?
2. Are there two tools with overlapping descriptions? (agent can't distinguish them)
3. Do parameter names and descriptions match what the tool actually expects?
4. Does the system prompt explain WHEN to use each tool?
5. Compare the tool schema the model receives (Step 0) with the tool schema in your code — serialization bugs can silently drop fields.

**Common causes:**
- Two tools with similar descriptions — agent picks randomly between them
- Tool description says what the tool IS but not WHEN to use it
- Parameter names are ambiguous (`data`, `input`, `value`)
- Tool schema changed but description wasn't updated
- Serialization bug silently drops a parameter description

**Signals:**
- Agent calls the wrong tool consistently
- Agent passes plausible but incorrect parameters
- Agent does something manually that a tool handles
- Agent invents a tool name (real tool's name isn't descriptive enough)

**Quick fix:** Add a "WHEN to use" line to each tool description. If two tools overlap, add "Use X for [scenario], use Y for [other scenario]" to the system prompt.

**Full fix:** Rewrite all tool descriptions following the pattern: one-line purpose, when to use, when NOT to use, parameter descriptions with types and constraints. Validate with EDD.

---

### BURIED CONTEXT — "It's there but the agent ignores it"

The information exists in the context but the agent doesn't use it. The most frustrating failure — you can SEE the instruction but the agent acts as if it's not there.

**Diagnostic — use concrete tests, not judgment:**
1. Move the ignored instruction to the first 200 tokens of the system prompt. Does behavior change? → Position problem.
2. Remove 50% of surrounding context (keep the instruction). Does behavior change? → Signal-to-noise problem.
3. Add an explicit section header labeling the instruction. Does behavior change? → Labeling problem.

**Common causes:**
- **Lost in the middle**: Information in the middle of long context gets less attention
- **Unlabeled**: Raw text without headers — agent skims past it
- **Drowned by volume**: 50 tokens of critical instruction in 5,000 tokens of reference material
- **Overshadowed**: A more prominent or recent instruction takes priority

**Signals:**
- Agent follows some instructions but not others
- Moving the instruction to the top fixes it
- Removing unrelated context fixes it
- The problem is intermittent (model sometimes attends, sometimes doesn't)

**Quick fix:** Move the ignored instruction to the last 500 tokens of the system prompt (closest to the user message). If that fixes it, you've confirmed the diagnosis.

**Full fix:** Restructure the full context using context-cartography's STRUCTURE step. Label sections with WHAT and WHY. Reduce surrounding noise. Validate with EDD.

---

### CONFLICTING CONTEXT — "The agent gets mixed signals"

The context contains contradictions — including subtle emergent interactions between instructions that are individually clear but incompatible in combination.

**Diagnostic:**
1. Read the full context looking for any two statements that could contradict
2. Check if examples contradict instructions (shows one thing, says another)
3. Check if tool descriptions conflict with system instructions
4. Check for **emergent interactions**: two instructions that are each reasonable alone but conflict when combined (e.g., "always respond formally" + "mirror the user's tone")
5. Check if different sections use the same term to mean different things

**Common causes:**
- Instructions evolved over time without removing old versions
- Examples from an earlier version that don't match current rules
- Implicit vs. explicit: an example demonstrates a pattern that contradicts an instruction
- Two reasonable rules that produce impossible-to-follow combinations

**Signals:**
- High variance — sometimes follows rule A, sometimes rule B
- Agent output is a blend/compromise of contradictory instructions
- Agent follows the instruction closest to the task, ignores the other

**Quick fix:** Identify the two conflicting instructions. Remove or comment out one. Does the behavior stabilize? If yes, decide which wins and update the other.

**Full fix:** Audit the full context for conflicts, including example-vs-instruction mismatches and emergent interactions. Resolve each conflict by choosing a winner and removing or updating the loser. Pay special attention to examples — they override instructions more than developers expect.

---

### CONTEXT OVERFLOW — "Too much context drowns the signal"

The context is so full that important information gets diluted. Adding more context made things worse, not better.

**Diagnostic:**
1. What's the total token count of the context?
2. What percentage is directly relevant to the failing task?
3. Remove all non-essential context (keep only critical items). Does the failure resolve?

**Common causes:**
- Kitchen-sink design — everything included "just in case"
- Retrieval returning too many results without re-ranking
- Conversation history growing without summarization
- Too many or too-long few-shot examples

**Signals:**
- Performance was better with less context
- Agent ignores recent instructions but follows old ones
- Adding relevant context paradoxically makes output worse

**Quick fix:** Strip to bare minimum — role, task, and only the most critical reference. If the agent improves, progressively re-add sections one at a time. Stop when quality plateaus or drops.

**Full fix:** Apply context-cartography (PRIORITIZE + CUT steps). Measure each addition's impact with EDD. Consider dynamic context (retrieve per-task instead of including everything).

---

### REASONING FAILURE — "The model just can't do this"

After ruling out all context causes, the model genuinely can't perform the task. This is the only category that ISN'T a context problem.

**Diagnostic:**
1. Construct minimal, ideal context — only exactly what the model needs, perfectly structured
2. Run the task with this ideal context (5+ times for confidence)
3. If it still fails → genuine reasoning/capability limitation
4. If it succeeds → one of the above categories was the real cause

**Before concluding reasoning failure:**
- Have you verified the actual context (Step 0)?
- Have you tried moving instructions to a more prominent position?
- Have you tried chain-of-thought instructions?
- Have you tried decomposing the task into smaller steps?
- Have you tried a more capable model?

**Quick fix:** Decompose the task into smaller steps the model can handle individually. Or add explicit chain-of-thought instructions ("Think step by step: first identify X, then check Y, then decide Z").

**Full fix:** Redesign the task decomposition, upgrade the model, or add tools that compensate for the capability gap (e.g., a calculator tool for math tasks).

---

## Compound Failures

Agent failures often involve multiple categories simultaneously. Common co-occurrence patterns:

| Primary | Often co-occurs with | Why |
|---------|---------------------|-----|
| REGRESSION | BURIED CONTEXT | New content pushes existing instructions to low-attention positions |
| MISSING CONTEXT | CONFLICTING CONTEXT | Adding missing info introduces contradictions with existing content |
| TOOL PROBLEM | CONTEXT OVERFLOW | Ambiguous tool descriptions are harder to parse in bloated context |
| BURIED CONTEXT | CONTEXT OVERFLOW | More content = more competition for attention |

**Rule:** If fixing the first category doesn't resolve the failure, continue to the next matching category. Don't assume a single root cause.

---

## Quick Triage Checklist

```
0. Can you see the full assembled context?     →  If not, log it first
1. Was context recently changed?               →  Revert and confirm
2. Is needed information present?              →  Add it manually
3. Are tool definitions clear and unambiguous?  →  Read them cold
4. Is information findable (well-positioned)?   →  Move it to the top
5. Are instructions contradictory?             →  Remove one conflict
6. Does less context fix it?                   →  Strip to essentials
7. None of the above?                          →  Minimal context test
```

Most failures resolve at steps 1-4. If you regularly reach step 7, revisit your context design with context-cartography.

---

## Integration with the Context Skill Suite

| Situation | Skill |
|-----------|-------|
| Agent is failing → diagnose why | **context-debugging** (this skill) |
| Diagnosis points to context design problem | → context-cartography to redesign |
| Need to validate the fix didn't break other things | → EDD to run assertions |
| Want to measure whether the fix actually helped | → context-eval to compare before/after |

These are the **full fix** path. Every category above also has a **quick fix** that requires no other skills and takes under 10 minutes.

---

## Anti-Patterns

| Anti-pattern | Symptom | Fix |
|-------------|---------|-----|
| **Blaming the model first** | "The model is stupid" before checking context | Check context before concluding reasoning failure |
| **Symptom chasing** | Adding instructions to fix symptoms instead of root cause | Classify first, then fix the category |
| **Context band-aids** | Adding "IMPORTANT: DO NOT..." instead of fixing structural issues | Restructure, don't shout |
| **Debug by adding** | Response to every failure is adding more context | Sometimes the fix is removing context |
| **Skipping Step 0** | Debugging intended context, not actual context | Always verify what the model actually receives |
| **Single-cause assumption** | Fixing one category and declaring victory | Check remaining categories if the fix doesn't fully resolve |
| **One-shot debugging** | Testing the fix once and shipping | Stochastic systems need multiple runs — use EDD |
