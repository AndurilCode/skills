#!/usr/bin/env python3
"""
Estimate the token count of a context harness file or directory.

Usage:
    python estimate_tokens.py /path/to/AGENTS.md
    python estimate_tokens.py /path/to/skill-directory/

Uses the approximation of ~4 characters per token (accurate within ~15%
for English text, which is sufficient for benefit-per-kilotoken calculations).
"""

import sys
from pathlib import Path

# Extensions we count as context files
CONTEXT_EXTENSIONS = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml",
    ".py", ".js", ".ts", ".sh", ".bash",
    ".xml", ".html", ".css",
    ".ctx", ".skill",
}

CHARS_PER_TOKEN = 4.0  # Approximate; good enough for estimation


def count_chars(path: Path) -> tuple[int, list[tuple[str, int]]]:
    """Count characters in a file or directory. Returns (total, breakdown)."""
    breakdown = []

    if path.is_file():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            chars = len(text)
            breakdown.append((str(path), chars))
            return chars, breakdown
        except Exception as e:
            print(f"Warning: could not read {path}: {e}", file=sys.stderr)
            return 0, []

    if path.is_dir():
        total = 0
        for f in sorted(path.rglob("*")):
            if f.is_file() and f.suffix.lower() in CONTEXT_EXTENSIONS:
                try:
                    text = f.read_text(encoding="utf-8", errors="replace")
                    chars = len(text)
                    total += chars
                    breakdown.append((str(f.relative_to(path)), chars))
                except Exception:
                    pass
        return total, breakdown

    return 0, []


def main():
    if len(sys.argv) < 2:
        print("Usage: python estimate_tokens.py <path>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    total_chars, breakdown = count_chars(path)
    total_tokens = int(total_chars / CHARS_PER_TOKEN)

    print(f"\n  Context Harness Token Estimate")
    print(f"  {'='*40}")
    print(f"  Path: {path}")
    print(f"  Total characters: {total_chars:,}")
    print(f"  Estimated tokens: ~{total_tokens:,}")
    print()

    if len(breakdown) > 1:
        print(f"  Breakdown:")
        for name, chars in sorted(breakdown, key=lambda x: -x[1]):
            tokens = int(chars / CHARS_PER_TOKEN)
            pct = (chars / total_chars * 100) if total_chars > 0 else 0
            print(f"    {tokens:>6,} tokens ({pct:4.1f}%)  {name}")
        print()

    # Print just the number for scripting
    print(f"  TOKEN_ESTIMATE={total_tokens}")


if __name__ == "__main__":
    main()
