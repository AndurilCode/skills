# JSON Schemas

Defines the JSON structures used by context-eval.

---

## evals.json

Defines the evaluation suite for a context harness. Located at `evals/evals.json`.

```json
{
  "harness_name": "payment-service-agents-md",
  "harness_type": "agents-md",
  "harness_path": "/path/to/AGENTS.md",
  "harness_token_estimate": 1500,
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic task prompt",
      "expected_output": "Description of what good output looks like",
      "files": ["evals/files/sample-input.json"],
      "assertions": [
        "The output includes the retry backoff schedule",
        "The agent referenced the Stripe webhook handler correctly"
      ]
    }
  ]
}
```

**Fields:**
- `harness_name`: Identifier for the context artifact
- `harness_type`: One of: `skill`, `agents-md`, `claude-md`, `ctx-file`, `system-prompt`, `mcp-config`, `rag`, `few-shot`, `custom-instructions`, `other`
- `harness_path`: Path to the artifact being evaluated
- `harness_token_estimate`: Approximate token count of the context artifact
- `evals[].id`: Unique integer identifier
- `evals[].prompt`: The task to execute
- `evals[].expected_output`: Human-readable description of success
- `evals[].files`: Optional input files (relative paths)
- `evals[].assertions`: Verifiable statements about expected outcomes

---

## eval_metadata.json

Per-eval metadata. Located at `<workspace>/iteration-N/eval-<name>/eval_metadata.json`.

```json
{
  "eval_id": 1,
  "eval_name": "payment-handoff-doc",
  "prompt": "The task prompt",
  "harness_path": "/path/to/AGENTS.md",
  "assertions": [
    "The document includes the retry backoff schedule",
    "The agent referenced the Stripe webhook handler correctly"
  ]
}
```

---

## grading.json

Output from the grader. Located at `<run-dir>/grading.json`.

```json
{
  "assertions": [
    {
      "text": "The output includes the retry backoff schedule",
      "with_harness": {
        "passed": true,
        "evidence": "Found in output section 3: exponential backoff with jitter, 1s/2s/4s/8s intervals"
      },
      "without_harness": {
        "passed": false,
        "evidence": "Output mentions retries but uses a generic 'retry after 5 seconds' pattern"
      },
      "discrimination": "discriminating"
    }
  ],
  "summary": {
    "with_harness": {"passed": 4, "failed": 1, "total": 5, "pass_rate": 0.80},
    "without_harness": {"passed": 2, "failed": 3, "total": 5, "pass_rate": 0.40},
    "discriminating_assertions": 2,
    "non_discriminating_assertions": 2,
    "inverse_assertions": 0,
    "benefit": 0.40
  },
  "behavioral_observations": {
    "approach_difference": "With-harness agent went directly to the Stripe handler; without-harness explored three different files first",
    "precision_difference": "With-harness used exact function names; without-harness used generic descriptions",
    "efficiency_difference": "With-harness: 8 tool calls. Without-harness: 14 tool calls."
  },
  "assertion_feedback": {
    "suggestions": [],
    "overall": "Assertions are well-targeted. The retry schedule assertion is particularly discriminating."
  }
}
```

---

## timing.json

Wall clock timing per run. Located at `<run-dir>/timing.json`.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "configuration": "with_harness"
}
```

**Fields:**
- `total_tokens`: From subagent task notification (if available)
- `duration_ms`: From subagent task notification (if available)
- `total_duration_seconds`: Computed wall clock time
- `configuration`: `"with_harness"` or `"without_harness"`

---

## context_eval_report.json

The final evaluation report. Located at `<workspace>/context_eval_report.json`.

```json
{
  "metadata": {
    "harness_name": "payment-service-agents-md",
    "harness_type": "agents-md",
    "harness_token_cost": 1500,
    "timestamp": "2026-03-18T10:30:00Z",
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
      "eval_name": "payment-handoff-doc",
      "with_harness_pass_rate": 0.85,
      "without_harness_pass_rate": 0.40,
      "benefit": 0.45,
      "discriminating_assertions": ["The output includes the retry backoff schedule"],
      "non_discriminating_assertions": ["The output is a markdown file"]
    }
  ],
  "diagnosis": {
    "verdict": "EFFECTIVE",
    "reasoning": "The AGENTS.md improved pass rates by 45% with strong discrimination on domain-specific assertions. The token cost (1500) is justified by the benefit.",
    "non_discriminating_assertions": ["The output is a markdown file"],
    "highest_impact_areas": ["Domain-specific terminology", "Architecture accuracy"],
    "wasted_context": ["The section on deployment history didn't influence any eval"],
    "recommendations": [
      "Prune the deployment history section (300 tokens) — it wasn't used in any eval",
      "Expand the webhook handler documentation — it was the highest-value context"
    ]
  }
}
```

**Verdict values:**
- `EFFECTIVE`: mean_benefit ≥ 0.25 AND majority of evals show improvement
- `MARGINAL`: 0.05 ≤ mean_benefit < 0.25 OR improvement is inconsistent
- `INEFFECTIVE`: mean_benefit < 0.05
- `HARMFUL`: mean_benefit < 0 (harness makes outcomes worse)

---

## iteration_history.json

Tracks improvement progression across iterations. Located at workspace root.

```json
{
  "harness_name": "payment-service-agents-md",
  "started_at": "2026-03-18T10:30:00Z",
  "iterations": [
    {
      "iteration": 1,
      "verdict": "MARGINAL",
      "benefit": 0.15,
      "harness_tokens": 2000,
      "changes": "Initial version",
      "is_current_best": false
    },
    {
      "iteration": 2,
      "verdict": "EFFECTIVE",
      "benefit": 0.45,
      "harness_tokens": 1500,
      "changes": "Pruned deployment history, expanded webhook docs",
      "is_current_best": true
    }
  ]
}
```
