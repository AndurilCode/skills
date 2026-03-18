#!/usr/bin/env python3
"""
Generate a context eval report from grading results.

Usage:
    python generate_report.py <workspace>/iteration-N --harness-name "name" --harness-type "type" --harness-tokens 1500

Reads grading.json files from each eval directory, computes the delta,
and writes context_eval_report.json + a human-readable summary.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, stdev


def load_grading(eval_dir: Path) -> dict | None:
    """Load grading.json from an eval directory."""
    grading_path = eval_dir / "grading.json"
    if grading_path.exists():
        with open(grading_path) as f:
            return json.load(f)
    return None


def load_timing(run_dir: Path) -> dict | None:
    """Load timing.json from a run directory."""
    timing_path = run_dir / "timing.json"
    if timing_path.exists():
        with open(timing_path) as f:
            return json.load(f)
    return None


def load_eval_metadata(eval_dir: Path) -> dict | None:
    """Load eval_metadata.json from an eval directory."""
    meta_path = eval_dir / "eval_metadata.json"
    if meta_path.exists():
        with open(meta_path) as f:
            return json.load(f)
    return None


def compute_stats(values: list[float]) -> dict:
    """Compute mean and stddev for a list of values."""
    if not values:
        return {"mean": 0.0, "stddev": 0.0}
    m = mean(values)
    s = stdev(values) if len(values) > 1 else 0.0
    return {"mean": round(m, 3), "stddev": round(s, 3)}


def classify_verdict(mean_benefit: float, per_eval_benefits: list[float]) -> str:
    """Classify the harness effectiveness."""
    if mean_benefit < 0:
        return "HARMFUL"
    if mean_benefit < 0.05:
        return "INEFFECTIVE"
    if mean_benefit < 0.25:
        return "MARGINAL"
    # Check consistency: majority of evals should show improvement
    improving = sum(1 for b in per_eval_benefits if b > 0)
    if improving > len(per_eval_benefits) / 2:
        return "EFFECTIVE"
    return "MARGINAL"


def generate_report(iteration_dir: Path, harness_name: str, harness_type: str, harness_tokens: int) -> dict:
    """Generate the context eval report from an iteration directory."""

    eval_dirs = sorted([
        d for d in iteration_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])

    per_eval = []
    with_pass_rates = []
    without_pass_rates = []
    with_times = []
    without_times = []
    with_tokens_list = []
    without_tokens_list = []
    all_non_discriminating = []

    for eval_dir in eval_dirs:
        meta = load_eval_metadata(eval_dir)
        grading = load_grading(eval_dir)

        if not grading:
            continue

        eval_name = meta.get("eval_name", eval_dir.name) if meta else eval_dir.name
        eval_id = meta.get("eval_id", 0) if meta else 0

        summary = grading.get("summary", {})
        wh = summary.get("with_harness", {})
        woh = summary.get("without_harness", {})

        wh_rate = wh.get("pass_rate", 0.0)
        woh_rate = woh.get("pass_rate", 0.0)
        benefit = round(wh_rate - woh_rate, 3)

        with_pass_rates.append(wh_rate)
        without_pass_rates.append(woh_rate)

        # Collect timing if available
        for config, time_list, token_list in [
            ("with_harness", with_times, with_tokens_list),
            ("without_harness", without_times, without_tokens_list),
        ]:
            run_dir = eval_dir / config
            timing = load_timing(run_dir)
            if timing:
                if "total_duration_seconds" in timing:
                    time_list.append(timing["total_duration_seconds"])
                if "total_tokens" in timing:
                    token_list.append(timing["total_tokens"])

        # Classify assertions
        discriminating = []
        non_discriminating = []
        for a in grading.get("assertions", []):
            disc = a.get("discrimination", "unknown")
            text = a.get("text", "")
            if disc == "discriminating":
                discriminating.append(text)
            elif disc.startswith("non_discriminating"):
                non_discriminating.append(text)
                all_non_discriminating.append(text)

        per_eval.append({
            "eval_id": eval_id,
            "eval_name": eval_name,
            "with_harness_pass_rate": wh_rate,
            "without_harness_pass_rate": woh_rate,
            "benefit": benefit,
            "discriminating_assertions": discriminating,
            "non_discriminating_assertions": non_discriminating,
        })

    # Compute aggregate stats
    benefits = [e["benefit"] for e in per_eval]
    mean_benefit = mean(benefits) if benefits else 0.0

    benefit_per_kt = round(mean_benefit / (harness_tokens / 1000), 3) if harness_tokens > 0 else 0.0

    verdict = classify_verdict(mean_benefit, benefits)

    # Build reasoning
    if verdict == "EFFECTIVE":
        reasoning = f"The harness improved pass rates by {mean_benefit:.0%} on average with strong discrimination. Token cost ({harness_tokens}) is justified."
    elif verdict == "MARGINAL":
        reasoning = f"The harness shows some improvement ({mean_benefit:.0%}) but results are inconsistent across evals. Consider targeted improvements."
    elif verdict == "INEFFECTIVE":
        reasoning = f"The harness produced negligible improvement ({mean_benefit:.0%}). The context may be redundant with the model's training data or too vague to change behavior."
    else:
        reasoning = f"The harness made outcomes worse ({mean_benefit:.0%}). It may contain stale information, contradictory instructions, or over-constraining rules."

    report = {
        "metadata": {
            "harness_name": harness_name,
            "harness_type": harness_type,
            "harness_token_cost": harness_tokens,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "num_evals": len(per_eval),
            "iteration": int(iteration_dir.name.split("-")[-1]) if "-" in iteration_dir.name else 1,
        },
        "results": {
            "with_harness": {
                "pass_rate": compute_stats(with_pass_rates),
                "time_seconds": compute_stats(with_times),
                "tokens": compute_stats(with_tokens_list),
            },
            "without_harness": {
                "pass_rate": compute_stats(without_pass_rates),
                "time_seconds": compute_stats(without_times),
                "tokens": compute_stats(without_tokens_list),
            },
            "delta": {
                "pass_rate": f"+{mean_benefit:.2f}" if mean_benefit >= 0 else f"{mean_benefit:.2f}",
                "benefit_per_kilotoken": benefit_per_kt,
            },
        },
        "per_eval_breakdown": per_eval,
        "diagnosis": {
            "verdict": verdict,
            "reasoning": reasoning,
            "non_discriminating_assertions": list(set(all_non_discriminating)),
            "highest_impact_areas": [],
            "wasted_context": [],
            "recommendations": [],
        },
    }

    return report


def print_summary(report: dict):
    """Print a human-readable summary."""
    meta = report["metadata"]
    results = report["results"]
    diag = report["diagnosis"]

    print(f"\n{'='*60}")
    print(f"  CONTEXT EVAL REPORT: {meta['harness_name']}")
    print(f"{'='*60}")
    print(f"  Type:    {meta['harness_type']}")
    print(f"  Tokens:  {meta['harness_token_cost']}")
    print(f"  Evals:   {meta['num_evals']}")
    print(f"  Verdict: {diag['verdict']}")
    print(f"{'='*60}\n")

    wh = results["with_harness"]["pass_rate"]
    woh = results["without_harness"]["pass_rate"]
    print(f"  With harness:    {wh['mean']:.0%} ± {wh['stddev']:.0%}")
    print(f"  Without harness: {woh['mean']:.0%} ± {woh['stddev']:.0%}")
    print(f"  Benefit:         {results['delta']['pass_rate']}")
    print(f"  Benefit/kToken:  {results['delta']['benefit_per_kilotoken']}")
    print()

    print(f"  {diag['reasoning']}")
    print()

    if report["per_eval_breakdown"]:
        print(f"  Per-eval breakdown:")
        for e in report["per_eval_breakdown"]:
            marker = "+" if e["benefit"] > 0 else ("−" if e["benefit"] < 0 else "=")
            print(f"    {marker} {e['eval_name']}: {e['benefit']:+.0%} "
                  f"({e['with_harness_pass_rate']:.0%} vs {e['without_harness_pass_rate']:.0%})")
        print()

    nd = diag.get("non_discriminating_assertions", [])
    if nd:
        print(f"  Non-discriminating assertions ({len(nd)}):")
        for a in nd[:5]:
            print(f"    - {a}")
        if len(nd) > 5:
            print(f"    ... and {len(nd) - 5} more")
        print()


def main():
    parser = argparse.ArgumentParser(description="Generate context eval report")
    parser.add_argument("iteration_dir", help="Path to iteration directory")
    parser.add_argument("--harness-name", required=True, help="Name of the harness")
    parser.add_argument("--harness-type", default="other", help="Type of harness")
    parser.add_argument("--harness-tokens", type=int, default=1000, help="Token cost of harness")
    parser.add_argument("--output", help="Output path (default: iteration_dir/context_eval_report.json)")
    args = parser.parse_args()

    iteration_dir = Path(args.iteration_dir)
    if not iteration_dir.exists():
        print(f"Error: {iteration_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    report = generate_report(
        iteration_dir,
        args.harness_name,
        args.harness_type,
        args.harness_tokens,
    )

    output_path = Path(args.output) if args.output else iteration_dir / "context_eval_report.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print_summary(report)
    print(f"  Report saved to: {output_path}")


if __name__ == "__main__":
    main()
