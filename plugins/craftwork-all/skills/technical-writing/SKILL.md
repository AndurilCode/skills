---
name: technical-writing
description: "Apply this skill whenever the user needs to write, draft, review, or improve any form of technical document — including RFCs, design docs, ADRs, runbooks, postmortems, one-pagers, internal announcements, Slack threads, PR descriptions, or any prose that communicates technical information to an audience. Triggers on phrases like 'write a design doc', 'draft an RFC', 'help me write this up', 'document this decision', 'write a runbook', 'review my doc', 'make this clearer', 'I need to announce this', 'how should I communicate this?', 'write a postmortem', 'draft a one-pager', or any situation where technical information needs to be transformed into written communication for a specific audience. Also trigger when the user pastes a draft and asks for feedback, when they need to explain a technical decision to non-technical stakeholders, or when they provide their own template and want the agent to follow it. This skill covers the full spectrum from 2-line Slack msages to multi-page design documents."
---

# Technical Writing

**Core principle**: Writing isn't about explaining what you think. It's about changing what the reader thinks. Almost none of your readers will pay full attention — they'll read the first sentence, skim the next, and either skim the rest or stop entirely. Every technical document must therefore frontload its point, omit what doesn't serve the reader's decision, and respect the reader's time as the scarcest resource.

The goal is not to transplant your understanding into someone else's head. The goal is to give the reader enough context to either (a) trust your judgment, (b) make a decision, or (c) take a specific action — and nothing more.

---

## The Three Laws of Technical Writing

Every piece of technical writing, regardless of format, must obey these laws in order:

**Law 1 — Lead with the point.** The first sentence should contain your conclusion, recommendation, or request. If a reader stops after one sentence, they should still know what you want. This applies to Slack messages, emails, RFCs, and design docs equally.

**Law 2 — Write less than you think you should.** The biggest mistake engineers make is trying to communicate in too much detail and ending up communicating nothing at all. Omit subtle details. Cut context that doesn't change the reader's decision. If you can say it in one sentence, do that.

**Law 3 — Match depth to audience size.** A Slack message to your team can be one sentence. An ADR for 3-5 reviewers can go deep into trade-offs. A company-wide announcement should be scannable in 30 seconds. The narrower the audience, the more detail is justified.

---

## How to Execute This Skill

### STEP 1 — Classify the Document

Before writing anything, determine what kind of document this is. The document type dictates structure, depth, audience, and tone.

**If the user provides their own template**: Skip to STEP 1B — Template Adaptation.

**If no template is provided**, classify into one of the built-in types:

| Type | Purpose | Audience Size | Typical Length |
|------|---------|---------------|----------------|
| **RFC / Design Doc** | Propose a technical approach, surface trade-offs, get alignment | 5-20 engineers | 2-8 pages |
| **ADR** | Record a decision and its rationale for future reference | 3-10 (now), unlimited (later) | 0.5-2 pages |
| **One-Pager** | Pitch a project, get buy-in, secure resources | Leadership + stakeholders | 1 page, strict |
| **Runbook** | Enable someone to perform a task they've never done | On-call engineers | As long as needed, step-by-step |
| **Postmortem** | Learn from an incident, prevent recurrence | Broad engineering org | 1-3 pages |
| **Internal Announcement** | Inform a group about a change, decision, or event | Team → org → company | 3-10 sentences |
| **PR Description** | Give reviewers context to review effectively | 1-5 reviewers | 5-20 lines |
| **Technical Explanation** | Help someone understand a system or concept | Varies | Varies |
| **Slack/Async Message** | Get a response or decision quickly | 1-20 people | 1-5 sentences |

If the request doesn't fit these categories cleanly, ask: "What decision or action should the reader take after reading this?" — the answer determines the structure.

---

### STEP 1B — Template Adaptation

When the user provides their own template (company RFC format, team design doc structure, personal writing framework):

1. **Parse the template's skeleton**: Identify sections, required fields, and implicit expectations (e.g., "Background" implies the reader doesn't have full context; "Non-Goals" implies explicit scoping is valued)
2. **Preserve the template's structure exactly**: Don't add sections, rename headings, or reorder. The user's organization has built muscle memory around this format
3. **Apply the Three Laws within each section**: Lead with the point in each section, cut unnecessary detail, match depth to implied audience
4. **Flag template gaps**: If the template lacks something important for the specific document (e.g., no "Alternatives" section in a design doc), note it at the end as a suggestion — don't silently add it

```
TEMPLATE ADAPTATION BRIEF
Template source: [User-provided / Company standard / Framework X]
Sections identified: [List the template's sections]
Implied audience: [Who this template assumes is reading]
Gaps noted: [Anything missing that might matter — suggest, don't insert]
```

---

### STEP 2 — Audience Analysis

Before writing, answer these questions:

```
AUDIENCE BRIEF
Who reads this: [Specific roles — "backend engineers on payments team", not "engineers"]
What they already know: [Don't repeat what's shared context]
What decision they'll make: [Approve/reject? Understand? Execute? Trust?]
What they'll do after reading: [Specific action — review, implement, escalate, nothing]
Attention budget: [Seconds? Minutes? Deep read?]
```

The Audience Brief is not a section in the final document — it's a tool for calibrating every word you write. If you can't fill it in, the document will probably fail because you don't know who you're writing for.

---

### STEP 3 — Write the Key Sentence

Before writing the full document, write one sentence that captures the entire document. This sentence must:

- State the conclusion, not the topic ("We should use Redis for session caching" not "This document evaluates caching options")
- Be understandable by someone with zero context about the project
- Survive being read by someone who reads nothing else

The Key Sentence becomes the document's opening line, the Slack message summary, the subject line prefix, or the TL;DR. Everything else in the document supports this sentence.

If you can't write the Key Sentence, you haven't thought clearly enough to write the document. Stop and think before you write.

---

### STEP 4 — Draft Using the Appropriate Template

Select and fill in the template for the classified document type. Each template below encodes the structure that makes that specific type effective.

---

## Built-in Templates

### TEMPLATE: RFC / Design Doc

Based on patterns from Google, HashiCorp, Squarespace, and Sourcegraph. Optimized for surfacing trade-offs and getting alignment before implementation.

```markdown
# [Key Sentence as Title]

**Author(s)**: [names]
**Approvers**: [who must say yes before implementation starts]
**Status**: Draft | In Review | Approved | Superseded
**Date**: [created date]
**Last updated**: [date]

## TL;DR

[Key Sentence expanded to 2-3 sentences. A reader who stops here
should know what you're proposing and why.]

## Background

[Objective facts only. No opinions, no proposals.
What is the current state? What problem exists?
A newcomer to this project should be able to read this section
and fully understand why this RFC exists.
Link to prior art, previous decisions, related systems.]

## Goals and Non-Goals

### Goals
- [Specific, measurable where possible. "Reduce P95 latency from 2.1s to <1s"]
- [Tied to team/org OKRs where relevant]

### Non-Goals
- [Things that could reasonably be goals but are explicitly excluded]
- [This section prevents scope creep during review]

## Proposed Design

[Start with a high-level overview paragraph.
Then go into detail. Focus on trade-offs, not implementation steps.
Include diagrams where they clarify architecture.

The design section should make the reader understand WHY you chose
this approach, not just WHAT the approach is. If you're writing
implementation steps with no trade-off discussion, you probably
don't need an RFC.]

## Alternatives Considered

[This is one of the most important sections.
Always include "Do nothing" as a baseline.

For each alternative:
- What is it?
- What trade-offs does it make?
- Why was it not selected?

This section shows future readers your decision-making context
and prevents "why didn't you just..." questions.]

## Cross-Cutting Concerns

[Security, privacy, observability, accessibility, cost.
Address each that applies. Say "N/A" for ones that don't —
this shows you considered them.]

## Risks and Mitigations

[What could go wrong? What's the rollback plan?
Be specific: "If Redis fails, sessions are lost for ~5min
until the fallback cookie mechanism activates."]

## Open Questions

[Questions that need answers before or during implementation.
These invite reviewers to contribute knowledge, not just opinions.]
```

**Calibration**: The strongest signal that an RFC is unnecessary is when there are no real alternatives or trade-offs. If the solution is obvious, write an ADR instead.

---

### TEMPLATE: ADR (Architecture Decision Record)

Based on Michael Nygard's original format plus industry evolution. Optimized for future discoverability — the primary reader is an engineer 6+ months from now asking "why did we do it this way?"

```markdown
# ADR-[number]: [Decision title — verb phrase preferred]

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-[number]
**Date**: [decision date]
**Deciders**: [who was in the room]

## Context

[What situation prompted this decision?
Include constraints, requirements, and forces at play.
Write as if the reader has never seen this codebase.]

## Decision

[State the decision clearly in 1-2 sentences.
"We will use PostgreSQL for user data storage."
Not "After careful consideration of many factors..."]

## Consequences

### Positive
- [What becomes easier or better]

### Negative
- [What becomes harder or worse — be honest]

### Neutral
- [What changes without clear positive/negative valence]
```

**Calibration**: ADRs should be quick to write (15-30 minutes). If you're spending hours, you either need an RFC first or you're putting too much detail in.

---

### TEMPLATE: One-Pager

Optimized for leadership and cross-functional audiences. Strict length discipline — if it doesn't fit on one page, cut until it does.

```markdown
# [Project Name]: [Key Sentence]

**Author**: [name] | **Date**: [date] | **Ask**: [What you need — approval, resources, headcount, time]

## Problem

[2-3 sentences. What's broken or missing? Quantify impact if possible.
"We lose ~15% of checkout conversions due to payment timeout errors."]

## Proposal

[3-5 sentences. What will you do? What's the approach at the highest level?]

## Expected Impact

[Quantified where possible. Tied to metrics the audience cares about.
"Reduce checkout abandonment by ~8%, worth ~€2M ARR."]

## Cost

[Time, people, infrastructure. Be specific.
"2 engineers, 6 weeks. No new infrastructure cost."]

## Risks

[Top 2-3 risks, each one sentence. Include mitigation.]

## Timeline

[Key milestones only. 3-5 lines max.]
```

**Calibration**: One-pagers are persuasion documents. The reader should finish thinking "this is worth doing" or "this is not worth doing" — not "I need more information." If they need more information, your one-pager failed.

---

### TEMPLATE: Runbook

Optimized for execution under stress. The reader may be on-call at 3am, unfamiliar with this system, and under time pressure.

```markdown
# Runbook: [What This Enables — action phrase]

**Last verified**: [date someone actually followed these steps]
**Owner**: [team or person responsible for keeping this current]
**Estimated time**: [how long the procedure takes]

## When to Use This

[Specific triggers. "Use this when PagerDuty alerts on
'payment-service-high-latency' AND the dashboard shows P99 > 5s."]

## Prerequisites

- [Access needed: VPN, SSH keys, admin roles]
- [Tools needed: kubectl, aws-cli version X+]
- [Context needed: link to architecture diagram if helpful]

## Steps

### 1. [Action verb] — [what and why]

`[exact command to run]`

Expected output:
```
[what the user should see]
```

If this fails: [what to do instead]

### 2. [Action verb] — [what and why]

[Continue pattern. Every step has: the command, expected output,
and failure guidance.]

## Verification

[How to confirm the procedure worked.
"Run `curl https://api.example.com/health` — should return 200."]

## Rollback

[How to undo what you just did if things get worse.]

## Escalation

[Who to contact if this runbook doesn't solve the problem.
Include Slack channel, PagerDuty service, phone numbers.]
```

**Calibration**: A runbook is only valid if it's been tested. The "Last verified" date is the most important metadata. A runbook nobody has followed recently is a dangerous artifact — it creates false confidence.

---

### TEMPLATE: Postmortem / Incident Review

Optimized for organizational learning. The goal is preventing recurrence, not assigning blame.

```markdown
# Postmortem: [Incident title — what happened, not why]

**Date of incident**: [date]
**Duration**: [time from detection to resolution]
**Severity**: [your org's severity scale]
**Author**: [name]
**Reviewers**: [names]

## Summary

[3-5 sentences. What happened, what was the impact, how was it resolved.
Write this for someone who wasn't involved.]

## Timeline

[Chronological list of events. Use UTC timestamps.
Focus on detection, diagnosis, and resolution actions.
Include who did what.]

| Time (UTC) | Event |
|------------|-------|
| 14:32 | Monitoring alert fires for payment-service latency |
| 14:35 | On-call engineer acknowledges, begins investigation |
| ... | ... |

## Root Cause

[Technical root cause. Be specific.
"A database migration added an index on a 500M-row table
without `CONCURRENTLY`, locking writes for 12 minutes."]

## Impact

[Quantified. Users affected, revenue impact, SLA breaches,
data integrity issues.]

## What Went Well

[What worked during the response. Celebrate good practices.]

## What Went Poorly

[What slowed detection, diagnosis, or resolution. Be honest.]

## Action Items

| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|
| [Specific, verifiable action] | [name] | P1/P2/P3 | [date] |

[Every action item must be specific enough that you can verify
whether it was done. "Improve monitoring" is not an action item.
"Add alert when payment-service P99 > 3s for 5 minutes" is.]

## Lessons Learned

[1-3 broader lessons that apply beyond this specific incident.
These are the reusable insights.]
```

**Calibration**: The quality of a postmortem is measured by whether the action items get completed, not by the quality of the prose. Keep the writing tight so people focus on the actions.

---

### TEMPLATE: Internal Announcement

Optimized for maximum comprehension with minimum reader effort.

```markdown
**Subject**: [Key Sentence — what changed and what the reader should do]

[Key Sentence repeated or expanded. 1-2 sentences.]

**What's changing**: [2-3 sentences of factual description]

**Why**: [1-2 sentences. Connect to a goal the reader cares about]

**What you need to do**: [Specific action, or "Nothing — this is informational"]

**Timeline**: [When this takes effect]

**Questions?**: [Where to ask — Slack channel, office hours, document link]
```

**Calibration**: If your announcement is longer than 10 sentences, you're probably writing a document that should be linked from the announcement, not inlined into it.

---

### TEMPLATE: PR Description

Optimized for reviewer efficiency. The reviewer's first 30 seconds determine whether they'll do a careful review or a rubber-stamp.

```markdown
## What

[1-2 sentences. What this does, stated as a change.
"Adds Redis-based session caching to reduce auth service latency."]

## Why

[1-2 sentences. Link to issue/ticket if available.
What problem does this solve?]

## How

[Brief description of the approach. Only include what a reviewer
needs to know to understand the diff — not a line-by-line narration.]

## Testing

[How was this tested? What should the reviewer verify?]

## Risks / Rollback

[Only if this is a risky change. How to revert if needed.]
```

---

### TEMPLATE: Slack / Async Message

For when you need a decision or response in a thread.

```
[Key Sentence — what you need.]
[1-2 sentences of context — only what's needed for the decision.]
[Explicit ask — "Can you approve by EOD?" / "Which option: A or B?"]
```

**Anti-pattern**: Starting a Slack message with context before stating what you need. By the time you get to the ask, the reader has already moved on.

---

## STEP 5 — Review and Sharpen

After drafting, apply these checks:

**The First-Sentence Test**: Read the first sentence of each section. Does the document still make sense? If not, your first sentences aren't doing their job.

**The So-What Test**: For every paragraph, ask "So what? What should the reader do with this information?" If the answer is "nothing," cut the paragraph.

**The Stranger Test**: Could someone who just joined your team understand this? If not, you're relying on shared context that isn't in the document.

**The Compression Test**: Can you cut 30% of the words without losing meaning? Almost always yes on a first draft.

**The Decision Test**: After reading this, does the reader know what to decide or do? If the answer is unclear, the document hasn't served its purpose.

---

## Calibration Rules

**1. Structure is not a substitute for thinking.** A perfectly formatted RFC with no clear trade-off analysis is a waste of everyone's time. If you can't articulate why your proposed solution is better than the alternatives, you're not ready to write the document.

**2. Don't write documents that should be conversations.** If the audience is 2-3 people and the topic is uncontroversial, a Slack thread or 15-minute call is almost always more effective than a document. Write documents when you need durability, broad review, or async alignment.

**3. Every document has a shelf life.** An RFC is most valuable during review. An ADR is most valuable 6 months later. A runbook is most valuable at 3am. Write for the moment the document will be read, not the moment you're writing it.

**4. Good writing requires clear thinking.** If you can't write the Key Sentence, you haven't thought clearly enough about what you're proposing. The writing is the thinking — not a chore that happens after the thinking is done.

**5. Adapt to your organization.** These templates are starting points. If your team uses Confluence with specific sections, or your company has an RFC format, use that. The principles (frontload, cut, match depth to audience) apply regardless of format. See STEP 1B for template adaptation.

**6. Respect the reader's context.** Technical documents compete with every other document, Slack message, and meeting in the reader's day. You are not entitled to their full attention. You must earn it in the first sentence and justify it in every sentence after.

---

## Thinking Triggers

Before and during writing, ask yourself:

- *"If the reader only reads one sentence, which sentence must it be?"*
- *"What would I cut if this had to be half the length?"*
- *"Am I writing this for the reader or for myself?"*
- *"What decision does this document enable?"*
- *"Will this still be useful in 6 months? If not, does it need to be a document at all?"*
- *"Am I explaining what X is, or why X matters? The reader needs the why first."*
