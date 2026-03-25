---
name: deep-document-processor
description: >
  Apply disciplined multi-pass reading to extract token-efficient, decision-relevant
  context from large documents, codebases, or research papers. Use this skill whenever
  an agent needs to process a document longer than ~2000 tokens and produce a compressed
  context representation — not a summary for humans, but a context artifact optimized
  for downstream agent reasoning. Triggers on: "read this and extract what matters",
  "process this document for context", "what's relevant in this for our task?",
  "distill this", "context-extract", or any situation where a large input must be
  compressed into a smaller, high-signal context window. Also trigger when an agent
  is about to dump an entire document into context — this skill replaces naive
  full-inclusion with structured extraction. Do NOT use for simple summarization
  requests aimed at human readers — this skill optimizes for agent consumption.
---

# Deep Document Processor

## Purpose

Transform large documents into token-efficient context artifacts optimized for
downstream agent reasoning. The goal is NOT human-readable summaries — it's
**maximum decision-relevant signal per token**.

## Why This Exists

Agents face a fundamental tension: large documents contain critical context, but
including them wholesale wastes tokens and dilutes attention. Naive approaches fail
in predictable ways:
- **Full inclusion**: Blows token budget, buries signal in noise
- **Naive truncation**: Loses structure, misses late-document insights
- **Single-pass summary**: Misses cross-references, flattens hierarchy

This skill applies a disciplined multi-pass protocol inspired by expert reading
heuristics, adapted for agent context engineering.

## The Protocol: Four Passes

### Pass 1 — Structural Survey (≤30 seconds)

Extract the document's skeleton before reading content. This creates a mental map
that guides where to spend attention in later passes.

**Extract:**
- Document type and purpose (paper? spec? report? guide?)
- Table of contents / section headings / file tree
- Total length estimate (pages, sections, or tokens)
- Key entities mentioned (people, systems, concepts)
- Publication date and freshness signal

**Output format:**
```
STRUCTURE:
- Type: [document type]
- Sections: [numbered list of headings/sections]
- Length: [estimate]
- Key entities: [comma-separated]
- Freshness: [date or "undated"]
```

Why this matters: surveying first prevents the agent from committing deep-read
tokens to sections that turn out to be irrelevant. It's the difference between
reading a map before driving and just heading north.

### Pass 2 — Selective Extraction (The 20% Rule)

Read each section and extract ONLY the content that meets one of these criteria:
1. **Decision-relevant**: Would change a downstream choice or recommendation
2. **Constraint-defining**: Sets boundaries on what's possible or allowed
3. **Counter-intuitive**: Contradicts likely assumptions an agent might hold
4. **Dependency-creating**: Other facts depend on this being known

**Hard constraint**: Extracted content must be ≤20% of original token count.
If you find yourself extracting more, you're not being selective enough — stop
and re-evaluate what's truly decision-relevant vs. merely interesting.

**Extraction format** — use dense, telegram-style notes, not prose:
```
EXTRACT [Section Name]:
- [fact/constraint/insight in ≤15 words]
- [fact/constraint/insight in ≤15 words]
- COUNTER-INTUITIVE: [thing that contradicts common assumption]
```

### Pass 3 — Cross-Reference and Conflict Scan

Review your Pass 2 extracts and identify:
- **Internal contradictions**: Does section 3 contradict section 7?
- **Cross-references**: Does understanding X require knowing Y from another section?
- **Missing context**: Are there terms, acronyms, or concepts used without definition?
- **Implicit assumptions**: What does the document assume the reader already knows?

This pass catches what single-pass extraction misses — the relationships between
facts, not just the facts themselves.

**Output format:**
```
CROSS-REFS:
- [Section X] depends on [Section Y]: [why]
- CONFLICT: [Section A] says X, but [Section B] implies Y
- UNDEFINED: [term/concept] used but never defined
- ASSUMES: [implicit knowledge required]
```

### Pass 4 — Context Artifact Assembly

Combine passes 1-3 into a single context artifact structured for agent consumption.
This is the final deliverable.

**Template:**
```
=== CONTEXT: [Document Title] ===
Type: [type] | Freshness: [date] | Compression: [X% of original]

STRUCTURE MAP:
[Pass 1 skeleton — 2-3 lines max]

KEY EXTRACTS:
[Pass 2 content, organized by relevance not document order]

DEPENDENCIES & CONFLICTS:
[Pass 3 findings — only if non-empty]

AGENT NOTES:
- [Any warnings about document quality, bias, or missing info]
- [Suggested follow-up if context is insufficient]
===
```

## Quality Checks

After assembly, verify:
1. **Compression ratio**: Output is ≤20% of input tokens. If not, cut more.
2. **Standalone test**: Could an agent with ONLY this artifact make the same
   decisions as one with the full document? If not, what's missing?
3. **No filler**: Every line must pass the "would removing this change a decision?" test.
   If no — delete it.
4. **Telegram density**: Notes should read like telegrams, not prose. Cut articles,
   hedging language, and qualifiers ruthlessly.

## Anti-Patterns to Avoid

- **Summarizing for humans**: This isn't a book report. Don't write flowing prose.
- **Preserving document order**: Organize by relevance, not by where things appeared.
- **Including "interesting but irrelevant"**: If it doesn't affect decisions, cut it.
- **Over-extracting definitions**: Only define terms the downstream agent won't know.
- **Hedging**: "The document seems to suggest..." — No. State what it says. Flag
  uncertainty explicitly if needed, but don't hedge the extraction itself.
