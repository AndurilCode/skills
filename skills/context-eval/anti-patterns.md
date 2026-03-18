# Context Engineering Anti-Patterns

Patterns to detect during evaluation that indicate a harness is underperforming or actively harmful. These map to the three-phase maturity model: Tool Tourism → Token Firehose → Context Precision.

---

## Token Firehose

**What it looks like**: The harness dumps large amounts of context — full repo docs, entire API references, lengthy architectural descriptions — without curation for the task at hand.

**Eval signals**:
- With-harness runs are slower but no more accurate
- Token counts are significantly higher for with-harness runs
- The agent references only a small fraction of the provided context
- benefit_per_kilotoken is very low (< 0.05)

**Root cause**: The harness author assumed more context = better results. In practice, irrelevant context competes for attention and can push out relevant information.

**Fix**: Identify which sections of the harness the agent actually used (check transcripts). Keep those, prune the rest. Consider scoped resolution (.ctx pattern) — deliver only the context relevant to the current task.

---

## Stale Context

**What it looks like**: The harness contains information that was once accurate but is now outdated — old API endpoints, deprecated patterns, former team members, previous architectural decisions.

**Eval signals**:
- The agent follows instructions that produce wrong outputs for the current state
- Inverse assertions: with-harness fails where without-harness succeeds (because the agent's training data is more current than the harness)
- Grader flags factual claims from the output that don't match reality

**Root cause**: Context files were written once and never updated. No freshness management.

**Fix**: Add timestamps to context sections. Implement a freshness check (e.g., `max_age` in .ctx files). Prioritize recently-updated context over old context.

---

## Vague Guidance

**What it looks like**: The harness explains architecture, history, or philosophy but doesn't tell the agent what to *do* with that knowledge.

**Eval signals**:
- Non-discriminating assertions (both pass): the harness didn't change behavior
- The agent reads the context (visible in transcript) but takes the same approach as baseline
- benefit ≈ 0 despite the harness containing relevant information

**Root cause**: The harness is informational rather than instructional. "Our service uses event sourcing" doesn't tell the agent how to handle event sourcing in the current task.

**Fix**: Make instructions imperative. Instead of "We use event sourcing," write "When modifying state, always append events to the event store rather than mutating the aggregate directly. Never bypass the event store for 'quick fixes.'"

---

## Contradictory Instructions

**What it looks like**: The harness says different things in different sections, or earlier instructions conflict with later ones.

**Eval signals**:
- High variance in with-harness runs (sometimes follows instruction A, sometimes instruction B)
- The agent explicitly notes the contradiction in its transcript
- With-harness pass rates are inconsistent across runs of the same eval

**Root cause**: The harness was written by multiple people or evolved over time without reconciliation.

**Fix**: Audit for contradictions. Establish explicit priority ordering (e.g., "If instructions conflict, the section closest to the task takes precedence"). Consider a single-author review pass.

---

## Redundant with Training

**What it looks like**: The harness restates common knowledge — standard patterns, well-known APIs, textbook architectures.

**Eval signals**:
- Near-zero benefit: the baseline agent already knows this
- Non-discriminating assertions across the board
- The harness's token cost is all overhead, no value

**Root cause**: The author didn't consider what the model already knows. They documented everything rather than focusing on what's proprietary, specific, or novel.

**Fix**: Focus context on information the model can't know from training: internal naming conventions, proprietary APIs, team-specific patterns, recent decisions, domain-specific edge cases.

---

## Over-Constraining

**What it looks like**: The harness is so prescriptive that the agent can't adapt to variations in the task. Rigid templates, mandatory sequences, strict output formats that don't fit all cases.

**Eval signals**:
- Inverse assertions on novel or edge-case tasks
- The agent produces formulaic output that doesn't address the actual question
- With-harness runs fail when the task deviates slightly from the expected pattern
- Without-harness runs are more creative and adaptive

**Root cause**: The harness was optimized for the common case and can't flex. "ALWAYS use this exact template" breaks when the template doesn't fit.

**Fix**: Explain the *why* instead of mandating the *how*. "Use this template for standard handoff docs because it ensures coverage of X, Y, Z. For unusual cases, adapt the structure but ensure X, Y, Z are still covered."

---

## Context Cannibalism

**What it looks like**: The harness is so large that it pushes useful conversation context (user messages, file contents, tool results) out of the context window.

**Eval signals**:
- With-harness runs fail on tasks that require information from the conversation or input files
- Token budget is dominated by the harness, leaving little room for the actual task
- The agent "forgets" earlier parts of the conversation

**Root cause**: The harness wasn't designed with a token budget. It assumes unlimited context.

**Fix**: Implement token budgeting. A harness should never consume more than 20-30% of available context. Use progressive disclosure — load detail only when needed.

---

## Cargo Cult Context

**What it looks like**: The harness follows the format of good context engineering (proper structure, sections, metadata) but the content doesn't actually help.

**Eval signals**:
- The harness looks professional but benefit ≈ 0
- Assertions pass or fail equally with or without the harness
- Content is generic enough to apply to any project

**Root cause**: The author followed a template without understanding why each section exists. They filled in the blanks without providing genuinely useful information.

**Fix**: Start from the question "What does the agent need to know to do this task better than it would on its own?" Write only that. Skip any section that doesn't have a clear, specific answer.

---

## Detection Checklist

When running context-eval, scan for these signals:

| Anti-Pattern | Primary Signal | Metric |
|---|---|---|
| Token Firehose | Slow + not accurate | benefit_per_kilotoken < 0.05 |
| Stale Context | Inverse assertions | inverse_assertions > 0 |
| Vague Guidance | Non-discriminating | benefit ≈ 0, many non_discriminating |
| Contradictions | High variance | stddev of pass_rate > 0.20 |
| Redundant | Zero benefit | benefit ≈ 0, baseline already passes |
| Over-Constraining | Fails on variants | inverse assertions on edge cases |
| Context Cannibalism | Forgets conversation | with-harness fails on conversation-dependent tasks |
| Cargo Cult | Looks good, no effect | Professional format, benefit ≈ 0 |
