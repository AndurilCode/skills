---
name: context-eval
description: Evaluate whether a context engineering harness actually improves agent outcomes. Use this skill whenever the user wants to measure, benchmark, compare, or validate any context artifact — including AGENTS.md, .ctx files, CLAUDE.md, system prompts, skill files, MCP configurations, RAG pipelines, tool setups, or any structured context that shapes agent behavior. Trigger on phrases like "does this context actually help?", "is my AGENTS.md working?", "benchmark my harness", "evaluate my prompt", "measure the benefit of", "A/B test my context", "is this worth the tokens?", "validate my setup", "eval my context", or any situation where someone wants empirical evidence that their context engineering produces better outcomes than the baseline. Also trigger when someone has built context infrastructure and needs to justify the investment, or when iterating on context and needs a feedback loop to know if changes are improvements. If a user mentions evaluating, benchmarking, or testing any agent context artifact, use this skill.
---

# Context Eval

Evaluate whether context engineering artifacts actually improve agent outcomes.

## The Core Question

Every context harness — a skill, an AGENTS.md, a .ctx file, a system prompt, a RAG pipeline — costs tokens and claims to produce better results. This skill answers the question: **does it?**

The method is simple: run the same tasks with and without the context, grade the outputs, measure the delta. If the context doesn't produce a measurable improvement, it's not context engineering — it's token tourism.

## What You Can Evaluate

This skill works on any context artifact that shapes agent behavior:

| Artifact Type | "With Context" Setup | "Without Context" Baseline |
|---|---|---|
| Skill (.skill, SKILL.md) | Agent reads the skill | Agent works without it |
| AGENTS.md / CLAUDE.md | Agent has the file in context | Agent works with bare prompt |
| .ctx file | Agent loads the context spec | Agent works without it |
| System prompt | Agent uses the prompt | Agent uses a minimal/default prompt |
| MCP tool config | Agent has tools configured | Agent works with base tools only |
| RAG pipeline | Agent retrieves context | Agent works from training data only |
| Few-shot examples | Agent has examples | Agent works zero-shot |
| Custom instructions | Agent has instructions | Agent works with defaults |

## The Eval Loop

```
1. Define what you're evaluating (the harness)
2. Write 3-5 realistic task prompts
3. Define success criteria (assertions)
4. Run tasks WITH the harness
5. Run tasks WITHOUT the harness (baseline)
6. Grade both against assertions
7. Compare: did the harness help?
8. If iterating: modify the harness, repeat from step 4
```

This mirrors the skill-creator eval loop but generalizes to any context artifact.

---

## Step 1: Define the Harness Under Test

Start by understanding what context artifact the user wants to evaluate. Capture:

1. **What is it?** The type and location of the context artifact
2. **What does it claim to do?** The expected behavior improvement
3. **What tasks should benefit?** The domain where it should help
4. **What's the baseline?** What the agent looks like *without* this context

If the user already has the artifact, read it. Look for:
- Token cost: how large is the context? (estimate tokens)
- Specificity: does it give precise instructions or vague guidance?
- Actionability: does it tell the agent *what to do* or just *what to know*?

Share these observations — they'll inform the eval design.

## Step 2: Write Eval Prompts

Create 3-5 realistic task prompts that the harness should help with. These should be:

- **Realistic**: things an actual user would ask, with messy phrasing, personal context, specifics
- **Diverse**: covering different aspects of what the harness claims to improve
- **Challenging enough** that context actually matters (trivial tasks won't differentiate)

Bad: `"Write a document"` (too vague, baseline could handle it)
Good: `"I need to write a handoff doc for the payment service — cover the retry logic, the Stripe webhook handling, and the idempotency keys. The new person starts Monday and hasn't seen our codebase."` (specific enough that relevant context would genuinely help)

Save to `evals/evals.json`:

```json
{
  "harness_name": "name-of-context-artifact",
  "harness_type": "agents-md | ctx-file | skill | system-prompt | mcp-config | rag | other",
  "harness_path": "/path/to/artifact",
  "evals": [
    {
      "id": 1,
      "prompt": "The realistic task prompt",
      "expected_output": "Description of what good output looks like",
      "files": [],
      "assertions": []
    }
  ]
}
```

Present the prompts to the user: "Here are the test cases I'd use to evaluate your harness. Do these look right? Would you add or change anything?"

## Step 3: Define Assertions

While preparing to run, draft assertions for each eval. Good assertions for context eval are:

**Outcome assertions** — did the output meet the bar?
- "The document includes the retry backoff schedule"
- "The code handles the edge case described in the AGENTS.md"
- "The response uses the correct internal terminology"

**Precision assertions** — did the context help the agent be *more precise*?
- "The agent didn't hallucinate API endpoints"
- "The agent referenced the actual architecture, not a generic pattern"
- "The output matches the team's formatting conventions"

**Efficiency assertions** — did the context reduce wasted work?
- "The agent didn't need to ask clarifying questions for information in the harness"
- "The agent took fewer tool calls than baseline to reach the same outcome"
- "The agent didn't generate then discard incorrect approaches"

Update `evals/evals.json` with the assertions. Explain to the user what each assertion checks and why it matters.

## Step 4: Run the Evaluations

### In Claude Code (with subagents)

Spawn parallel runs for each eval — one with the harness, one without. Save outputs to:

```
workspace/
  iteration-1/
    eval-1-descriptive-name/
      with_harness/
        outputs/
      without_harness/
        outputs/
      eval_metadata.json
```

The `eval_metadata.json` for each eval:

```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name",
  "prompt": "The task prompt",
  "harness_path": "/path/to/artifact",
  "assertions": ["assertion 1", "assertion 2"]
}
```

### In Claude.ai (no subagents)

Run each eval yourself, sequentially. For each:

1. **With harness**: Read the context artifact, then follow its instructions to complete the task
2. **Without harness**: Complete the same task using only the bare prompt (don't use knowledge from the harness you just read — treat it as a fresh attempt)

Save outputs to the filesystem. Be honest about the limitation: you wrote the harness and you're also running it, so you have full context. The human review step compensates.

### Capturing Metrics

For each run, record in `timing.json`:

```json
{
  "total_tokens": 0,
  "duration_ms": 0,
  "total_duration_seconds": 0,
  "configuration": "with_harness | without_harness"
}
```

If subagent notifications provide `total_tokens` and `duration_ms`, capture them immediately — this data isn't persisted elsewhere.

## Step 5: Grade the Results

For each run, evaluate every assertion against the outputs. Read `references/grader.md` for the full grading protocol. The key principles:

- **PASS**: Clear evidence the assertion holds, reflecting genuine task completion
- **FAIL**: No evidence, contradicting evidence, or superficial compliance
- **Be skeptical**: Surface-level compliance (right filename, wrong content) is a FAIL

Save grading to `grading.json` in each run directory. See `references/schemas.md` for the exact schema.

Beyond the predefined assertions, extract and verify implicit claims from the output. This catches issues assertions miss.

### Critique the Assertions Too

After grading, ask: are these assertions actually discriminating? An assertion that passes for both with-harness and without-harness runs tells you nothing. Flag:
- Assertions that pass regardless of harness (non-discriminating)
- Important outcomes that no assertion covers
- Assertions that can't be verified from available outputs

## Step 6: Compute the Delta

This is where context eval diverges from generic skill eval. You're measuring the **marginal value of context**.

### The Context Benefit Score

For each eval, compute:

```
benefit = with_harness_pass_rate - without_harness_pass_rate
```

Aggregate across all evals:

```
mean_benefit = average(benefits across all evals)
token_cost = tokens_consumed_by_harness_context
efficiency = mean_benefit / (token_cost / 1000)
```

This gives you a **benefit-per-kilotoken** score — how much improvement each 1K tokens of context buys you.

### The Report

Generate `context_eval_report.json`:

```json
{
  "metadata": {
    "harness_name": "name",
    "harness_type": "type",
    "harness_token_cost": 1500,
    "timestamp": "ISO-8601",
    "num_evals": 5,
    "iteration": 1
  },
  "results": {
    "with_harness": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05},
      "time_seconds": {"mean": 45.0, "stddev": 12.0},
      "tokens": {"mean": 3800, "stddev": 400}
    },
    "without_harness": {
      "pass_rate": {"mean": 0.40, "stddev": 0.10},
      "time_seconds": {"mean": 32.0, "stddev": 8.0},
      "tokens": {"mean": 2100, "stddev": 300}
    },
    "delta": {
      "pass_rate": "+0.45",
      "time_seconds": "+13.0",
      "tokens": "+1700",
      "benefit_per_kilotoken": 0.30
    }
  },
  "per_eval_breakdown": [
    {
      "eval_id": 1,
      "eval_name": "descriptive-name",
      "with_harness_pass_rate": 0.85,
      "without_harness_pass_rate": 0.40,
      "benefit": 0.45,
      "discriminating_assertions": ["assertion that differed"],
      "non_discriminating_assertions": ["assertion that passed for both"]
    }
  ],
  "diagnosis": {
    "verdict": "EFFECTIVE | MARGINAL | INEFFECTIVE | HARMFUL",
    "reasoning": "Explanation of the verdict",
    "non_discriminating_assertions": [],
    "highest_impact_areas": [],
    "wasted_context": [],
    "recommendations": []
  }
}
```

### Verdict Thresholds

| Verdict | Condition |
|---|---|
| **EFFECTIVE** | mean_benefit ≥ 0.25 AND majority of evals show improvement |
| **MARGINAL** | 0.05 ≤ mean_benefit < 0.25 OR improvement is inconsistent across evals |
| **INEFFECTIVE** | mean_benefit < 0.05 — the harness isn't helping |
| **HARMFUL** | mean_benefit < 0 — the harness makes things worse (this happens more than you'd think) |

These thresholds are starting points. Adjust based on the domain — a 10% improvement in a safety-critical harness might be worth a lot, while a 30% improvement in a convenience harness might not justify the token cost.

## Step 7: Present Results to the User

Show the user:

1. **The headline**: "Your [harness] improved pass rates by X% at a cost of Y tokens per invocation."
2. **The breakdown**: which evals improved most, which didn't move
3. **The diagnosis**: verdict + reasoning + recommendations
4. **The raw outputs**: so they can qualitatively assess whether the improvements are real

If using the eval-viewer infrastructure (Claude Code), generate the viewer:
```bash
python <skill-creator-path>/eval-viewer/generate_review.py \
  workspace/iteration-N \
  --skill-name "harness-name" \
  --benchmark workspace/iteration-N/benchmark.json
```

If in Claude.ai, present results directly in conversation. For each eval, show the prompt, both outputs side by side, and the grading. Ask for feedback inline.

## Step 8: Iterate (Optional)

If the user wants to improve the harness:

1. Analyze which assertions failed in with-harness runs — these are the weak spots
2. Look at non-discriminating assertions — these suggest the harness isn't adding value where expected
3. Read the harness and identify what's missing, vague, or counterproductive
4. Suggest specific edits to the harness
5. After edits, rerun evals into `iteration-N+1/`
6. Compare: did the edits help?

Keep iterating until:
- The user is satisfied
- The benefit score stabilizes
- Further edits aren't producing measurable improvement

---

## Context Engineering Anti-Patterns to Flag

During evaluation, watch for these common failures and flag them to the user:

**Token Firehose**: The harness dumps too much context, overwhelming the model. Signal: with-harness runs are *slower* and no more accurate. Recommendation: prune to high-signal content.

**Stale Context**: The harness contains outdated information. Signal: the agent follows instructions that produce wrong outputs for the current state. Recommendation: add freshness management.

**Vague Guidance**: The harness explains *what to know* but not *what to do*. Signal: the agent reads the context but doesn't change behavior. Recommendation: make instructions actionable and imperative.

**Contradictory Instructions**: The harness says conflicting things. Signal: with-harness runs show high variance. Recommendation: resolve contradictions, establish priority ordering.

**Redundant with Training**: The harness repeats what the model already knows. Signal: no benefit delta on any eval. Recommendation: focus context on proprietary, specific, or recent information.

**Over-Constraining**: The harness is so rigid that the agent can't adapt to edge cases. Signal: with-harness runs fail on novel tasks that baseline handles fine. Recommendation: explain the *why* instead of mandating the *how*.

---

## Adapting for Different Environments

**Claude Code**: Full workflow with subagents, parallel runs, eval-viewer. Use the `skill-creator` eval infrastructure for the viewer and benchmark aggregation.

**Claude.ai**: Sequential runs, present results inline, skip quantitative benchmarking that requires baselines. Focus on qualitative comparison with the user.

**Cowork**: Subagents work, but use `--static` for the eval-viewer. Feedback comes as a downloaded JSON file.

**CI/CD Integration**: For harnesses in repos, the eval JSON can be version-controlled and run as part of a CI pipeline. The context_eval_report.json becomes a build artifact.

---

## Reference Files

- `references/grader.md` — Full grading protocol for assertion evaluation
- `references/schemas.md` — JSON schemas for all eval artifacts
- `references/anti-patterns.md` — Extended guide to context engineering anti-patterns with examples

---

## The Philosophical Bit

The ETH Zurich research showed that LLM-generated context can actually *hurt* agent performance. The METR, Google, and Bain studies all show that context quality — not model capability — is the binding constraint in most agent deployments. This skill exists because context engineering is an empirical discipline: you build a harness, you measure its effect, you iterate. Intuition about what *should* help is frequently wrong. Measure it.
