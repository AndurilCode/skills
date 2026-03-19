---
name: context-eval
description: Evaluate whether a context engineering harness actually improves agent outcomes. Use this skill whenever the user wants to measure, benchmark, compare, or validate any context artifact that shapes agent behavior — rules, instructions, guidelines, documentation, retrieval pipelines, tool setups, or any structured context injected into an agent's working memory. Trigger on phrases like "does this context actually help?", "is my harness working?", "benchmark my context", "evaluate my prompt", "measure the benefit of", "A/B test my context", "is this worth the tokens?", "validate my setup", "eval my context", or any situation where someone wants empirical evidence that their context engineering produces better outcomes than the baseline. Also trigger when someone has built context infrastructure and needs to justify the investment, or when iterating on context and needs a feedback loop to know if changes are improvements. If a user mentions evaluating, benchmarking, or testing any agent context artifact, use this skill.
---

# Context Eval

Evaluate whether context engineering artifacts actually improve agent outcomes.

## The Core Question

Every context harness — whatever its format or delivery mechanism — costs tokens and claims to produce better results. This skill answers the question: **does it?**

The method is simple: run the same tasks with and without the context, grade the outputs, measure the delta. If the context doesn't produce a measurable improvement, it's not context engineering — it's token tourism.

## What You Can Evaluate

This skill works on any context artifact that shapes agent behavior, regardless of format, delivery mechanism, or which LLM runs it. If it occupies tokens in the agent's working memory and claims to improve outcomes, it's a harness and you can evaluate it.

Common examples include project-level rules and instructions, coding guidelines, domain documentation, retrieval-augmented generation pipelines, tool and integration configurations, few-shot examples, and system-level prompts — but the skill doesn't prescribe what the harness looks like. Step 1 discovers that.

## The Eval Loop

```
1. Define what you're evaluating (the harness)
2. Write 3-5 realistic task prompts
3. Define success criteria (assertions)
4. Run tasks WITH and WITHOUT the harness (you MUST actually run them — see Step 4)
5. Grade both against assertions
6. Compare: did the harness help?
7. If iterating: modify the harness, repeat from step 4
```

**Use tasks to track progress.** Create a task for each step above and update status as you go (in_progress when starting, completed when done). This eval is a multi-step process — task tracking prevents skipping steps, losing track of which evals have been run, or forgetting to grade before computing the delta.

---

## Step 1: Define the Harness Under Test

Start by understanding what context artifact the user wants to evaluate. Read the artifact and characterize it:

1. **What is it?** Identify the format, structure, and delivery mechanism. Is it a single file? A directory of documents? A retrieval pipeline? A set of tool configurations? Don't assume — read it.
2. **What does it claim to do?** The expected behavior improvement.
3. **What tasks should benefit?** The domain where it should help.
4. **What's the baseline?** What the agent looks like *without* this context.
5. **What does it cost?** Estimate the token footprint. Use `estimate_tokens.py` for files and directories.

After reading the artifact, assess:
- **Specificity**: does it give precise instructions or vague guidance?
- **Actionability**: does it tell the agent *what to do* or just *what to know*?
- **Freshness**: does it look current or potentially stale?

Record the harness type as a descriptive string (e.g., "project coding guidelines", "service documentation", "retrieval pipeline", "tool configuration"). This is a free-form field — use whatever describes the artifact accurately.

Share these observations — they'll inform the eval design.

## Step 2: Write Eval Prompts

Create 3-5 realistic task prompts that the harness should help with. These should be:

- **Realistic**: things an actual user would ask, with messy phrasing, personal context, specifics
- **Diverse**: covering different aspects of what the harness claims to improve
- **Challenging enough** that context actually matters (trivial tasks won't differentiate)

Bad: `"Write a document"` (too vague, baseline could handle it)
Good: `"I need to write a handoff doc for the payment service — cover the retry logic, the webhook handling, and the idempotency keys. The new person starts Monday and hasn't seen our codebase."` (specific enough that relevant context would genuinely help)

Save to `evals/evals.json`:

```json
{
  "harness_name": "name-of-context-artifact",
  "harness_type": "descriptive string inferred from step 1",
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
- "The code handles the edge case described in the harness"
- "The response uses the correct internal terminology"

**Precision assertions** — did the context help the agent be *more precise*?
- "The agent didn't hallucinate API endpoints"
- "The agent referenced the actual architecture, not a generic pattern"
- "The output matches the team's conventions"

**Efficiency assertions** — did the context reduce wasted work?
- "The agent didn't need to ask clarifying questions for information in the harness"
- "The agent took fewer tool calls than baseline to reach the same outcome"
- "The agent didn't generate then discard incorrect approaches"

Update `evals/evals.json` with the assertions. Explain to the user what each assertion checks and why it matters.

## Step 4: Run the Evaluations

**You MUST actually run the evals, not just reason about them.** Post-hoc analysis of existing outputs is not evaluation — it's rationalization. Spawn subagents, get real outputs, then grade.

### Determine the eval mode

The harness type determines how you run:

**Repo-specific harness** (coding guidelines, project docs, retrieval pipelines): The eval tasks operate on the real codebase. Subagents work within the repo — one with the harness loaded, one without.

**Methodology harness** (skills, reasoning frameworks, diagnostic workflows): There is no repo to run against. You MUST synthesize realistic scenarios and dispatch subagents that role-play the scenario. Each subagent receives the scenario prompt; the with-harness agent also receives the skill/methodology content. The subagent's output IS the eval output.

**CRITICAL for methodology harnesses:** Do not grade outputs you already have from prior conversation. The eval must produce fresh, independent outputs from agents that don't share your context. Reusing prior outputs conflates "did the skill help?" with "did having a long conversation about the skill help?"

### Running with subagents (default)

For each eval, launch a pair of subagents:

**Without-harness agent:**
- Receives: the scenario prompt only
- Instruction: "Respond to this scenario as you naturally would. Describe your approach step by step."
- Does NOT receive the harness content

**With-harness agent:**
- Receives: the harness content + the scenario prompt
- Instruction: "You have access to the following skill/methodology. Follow it if applicable. Respond to this scenario step by step."

Launch pairs in parallel where possible. Save outputs to:

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

### Without subagent support (fallback only)

If the environment genuinely cannot spawn subagents, run each eval yourself sequentially. For each:

1. **Without harness**: Complete the task using only the bare prompt. Do this FIRST — before reading the harness. You cannot un-know the harness content.
2. **With harness**: Read the context artifact, then follow its instructions to complete the task.

Save outputs to the filesystem. Be honest about the limitation: you wrote the harness and you're also running it, so you have full context. The human review step compensates.

**This fallback is significantly weaker than subagent-based evaluation.** Flag the limitation in the report.

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

If the agent runtime provides token counts or duration metrics on task completion, capture them immediately — this data may not be persisted elsewhere.

## Step 5: Grade the Results

For each run, evaluate every assertion against the outputs. Read `grader.md` for the full grading protocol. The key principles:

- **PASS**: Clear evidence the assertion holds, reflecting genuine task completion
- **FAIL**: No evidence, contradicting evidence, or superficial compliance
- **Be skeptical**: Surface-level compliance (right filename, wrong content) is a FAIL

Save grading to `grading.json` in each run directory. See `schemas.md` for the exact schema.

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
    "harness_type": "descriptive string",
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

### Generating the Viewer

First, aggregate the benchmark data:
```bash
python <context-eval-path>/aggregate_benchmark.py \
  workspace/iteration-N \
  --harness-name "my-harness" \
  --harness-tokens 1500
```

Then generate the report:
```bash
python <context-eval-path>/generate_report.py \
  workspace/iteration-N \
  --harness-name "my-harness" \
  --harness-type "project coding guidelines" \
  --harness-tokens 1500
```

Then launch the interactive viewer:
```bash
# Server mode (opens in browser, saves feedback to workspace)
python <context-eval-path>/generate_viewer.py \
  workspace/iteration-N \
  --harness-name "my-harness"

# Static mode (for headless environments)
python <context-eval-path>/generate_viewer.py \
  workspace/iteration-N \
  --harness-name "my-harness" \
  --static report.html
```

The viewer has three tabs:
- **Outputs**: Side-by-side comparison of with-harness vs without-harness outputs, with assertion grading and discrimination badges. Navigate with arrow keys. Leave feedback per eval.
- **Benchmark**: Stat cards showing pass rates, delta, benefit-per-kilotoken, and per-eval breakdown.
- **Diagnosis**: Verdict, highest-impact areas, wasted context candidates, non-discriminating assertions, and recommendations.

When done reviewing, click "Submit All Reviews" to save feedback. In server mode, it saves to `workspace/feedback.json`. In static mode, it downloads as a file.

If the environment has no filesystem viewer, present results directly in conversation. For each eval, show the prompt, both outputs, and the grading. Ask for feedback inline.

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

## Advanced: Blind Comparison

For situations where you want a more rigorous comparison between with-harness and without-harness outputs (e.g., the user asks "is the harness actually better, or am I just seeing what I want to see?"), use the blind comparison system.

### How It Works

1. Take the outputs from a with-harness run and a without-harness run
2. Randomly assign them as "A" and "B"
3. Spawn a comparator subagent that reads `comparator.md`
4. The comparator judges quality without knowing which output used the harness
5. After the comparator picks a winner, spawn an analyzer subagent that reads `analyzer.md`
6. The analyzer "unblinds" the results and maps the harness sections to their impact

The comparator adds a **Context Signal** rubric dimension that evaluates domain-specific terminology, specificity, and edge case handling — the signatures of effective context engineering. This helps detect whether the harness is actually injecting useful knowledge or just adding tokens.

The analyzer produces a **section-by-section impact map** of the harness, classifying each section as HIGH / LOW / ZERO / NEGATIVE impact, along with token efficiency analysis and concrete improvement suggestions.

### When to Use

- When assertion-based evaluation isn't sufficient (subjective quality matters)
- When you want to understand *why* the harness helped, not just *whether* it helped
- When iterating on the harness and need precise guidance on what to change
- When presenting evidence to stakeholders who need more than pass rate numbers

This is optional, requires subagent support, and most users won't need it for initial evaluation. The assertion-based loop is usually sufficient for iteration.

---

## Advanced: Automated Harness Optimization

For users who want to optimize their harness automatically, the `optimize_harness.py` script proposes section-level modifications and tracks their impact.

### How It Works

```bash
python <context-eval-path>/optimize_harness.py \
  --harness /path/to/harness \
  --evals /path/to/evals.json \
  --workspace /path/to/optimize-workspace \
  --max-iterations 5 \
  --llm-cmd "your-llm-cli --prompt" \
  --verbose
```

The loop:
1. Analyzes the harness content and eval definitions
2. Uses an LLM (via a configurable CLI command) to propose ONE modification per iteration (prune, rewrite, expand, add)
3. Applies the modification to a copy of the harness
4. Saves each iteration's modified harness for re-evaluation
5. Repeats until max iterations or no more improvements

After the loop completes, re-run `context-eval` with the optimized harness to verify the changes actually improved outcomes.

### Requirements

An LLM CLI that accepts a prompt as an argument and returns a response on stdout. Configure it with `--llm-cmd`. Examples:

```bash
--llm-cmd "llm -m gpt-4o"      # Simon Willison's llm tool
--llm-cmd "claude -p"           # Anthropic CLI
--llm-cmd "aider --message"     # Aider
--llm-cmd "./run_llm.sh"       # Custom wrapper
```

If no LLM CLI is available, the script saves the prompt it would have sent and reports that manual mode is needed — you can read the prompt and apply modifications yourself.

### Integration with the Eval Loop

The optimizer is designed to be called *after* an initial evaluation round. The workflow:

1. Run context-eval → get a diagnosis (e.g., MARGINAL with specific weak spots)
2. Run optimize_harness.py → get proposed modifications
3. Re-run context-eval with the modified harness → verify improvement
4. Repeat until verdict is EFFECTIVE or benefit stabilizes

---

## Context Engineering Anti-Patterns to Flag

During evaluation, watch for these common failures and flag them to the user. See `anti-patterns.md` for the extended guide with eval signal detection and metric signatures.

**Token Firehose**: The harness dumps too much context, overwhelming the model. Signal: with-harness runs are *slower* and no more accurate. Recommendation: prune to high-signal content.

**Stale Context**: The harness contains outdated information. Signal: the agent follows instructions that produce wrong outputs for the current state. Recommendation: add freshness management.

**Vague Guidance**: The harness explains *what to know* but not *what to do*. Signal: the agent reads the context but doesn't change behavior. Recommendation: make instructions actionable and imperative.

**Contradictory Instructions**: The harness says conflicting things. Signal: with-harness runs show high variance. Recommendation: resolve contradictions, establish priority ordering.

**Redundant with Training**: The harness repeats what the model already knows. Signal: no benefit delta on any eval. Recommendation: focus context on proprietary, specific, or recent information.

**Over-Constraining**: The harness is so rigid that the agent can't adapt to edge cases. Signal: with-harness runs fail on novel tasks that baseline handles fine. Recommendation: explain the *why* instead of mandating the *how*.

---

## Adapting to Agent Capabilities

This skill adapts to whatever the host agent can do. Check for these capabilities and adjust accordingly:

**Subagent spawning** (parallel task execution): If available, use it for parallel with/without runs, blind comparison, and the analyzer. If not, run evals sequentially and skip blind comparison.

**Filesystem access**: If available, use the full workspace directory structure, generate the HTML viewer, and save feedback to JSON. If not, present results inline in conversation and collect feedback through dialogue.

**LLM CLI access**: If an LLM command-line tool is available, use `optimize_harness.py` for automated optimization. If not, propose modifications in conversation and let the user apply them.

**Browser / display**: If a browser is available, use `generate_viewer.py` in server mode. If headless, use `--static` to write a standalone HTML file. If neither, present results in conversation.

**CI/CD Integration**: The eval JSON and benchmark scripts can run in CI. Version-control `evals/evals.json` alongside the harness. The `context_eval_report.json` becomes a build artifact. Track benefit-per-kilotoken over time to catch regressions when the harness is modified.

---

## Reference Files

All files are in the same directory as this SKILL.md. Use paths relative to this skill's directory.

### Agents (read when spawning the relevant subagent)

- `comparator.md` — Blind comparison between with-harness and without-harness outputs. Adds a Context Signal rubric dimension.
- `analyzer.md` — Post-hoc analysis of *why* the harness helped/hurt. Produces section-level impact mapping and token efficiency analysis.

### References (loaded into context as needed)

- `grader.md` — Full grading protocol with discrimination classification
- `schemas.md` — JSON schemas for all eval artifacts
- `anti-patterns.md` — Extended guide to context engineering anti-patterns with metric signatures and detection checklist

### Scripts

- `generate_report.py` — Generates `context_eval_report.json` with verdict, benefit delta, and diagnosis
- `aggregate_benchmark.py` — Aggregates grading results into `benchmark.json` for the viewer
- `estimate_tokens.py` — Estimates token count of a harness file or directory
- `optimize_harness.py` — Automated harness optimization loop (requires any LLM CLI)
- `generate_viewer.py` — Self-contained HTML viewer with Outputs/Benchmark/Diagnosis tabs. Supports server mode and static mode.

---

## The Philosophical Bit

Research shows that LLM-generated context can actually *hurt* agent performance (ETH Zurich, 2025). Multiple independent studies (METR, Google, Bain, Goldman Sachs) show that context quality — not model capability — is the binding constraint in most agent deployments. This skill exists because context engineering is an empirical discipline: you build a harness, you measure its effect, you iterate. Intuition about what *should* help is frequently wrong. Measure it.
