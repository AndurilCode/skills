---
name: knowledge-architect
description: "Apply this skill whenever knowledge is at risk of being lost, needs to be captured, or a team needs to design how knowledge flows and persists. Triggers on phrases like 'document this decision', 'we should write this down', 'how do we make sure we don't forget this?', 'someone is leaving the team', 'new person is joining', 'why did we do it this way?', 'we keep re-debating this', 'set up our knowledge system', 'our docs are a mess', 'I can never find anything', 'this keeps getting lost', 'onboarding is painful', or any situation where implicit knowledge needs to become explicit and discoverable. Also trigger when the user has just resolved an incident, completed a migration, made a vendor choice, or finished a spike — these are high-value capture moments. This skill covers the full spectrum from capturing a single insight to designing a team's knowledge architecture."
---

# Knowledge Architect

**Core principle**: Knowledge that isn't discoverable isn't captured — it's just written down. The gap between "documented" and "discoverable" is where most knowledge management fails. This skill treats discoverability as the primary design constraint, not an afterthought.

The fundamental insight from decades of failed knowledge systems: capture must happen close to the moment (while context is fresh) but serve a reader far from the moment (months later, different person, different context). Every design decision in this skill resolves that tension.

---

## How to Execute This Skill

### STEP 1 — Detect the Mode

This skill operates in three modes. Classify the request:

| Mode | Trigger | What you produce |
|------|---------|-----------------|
| **Capture** | User has something specific to capture — a decision, a learning, a piece of context | A knowledge artifact in the right format at the right depth |
| **Detect** | A workflow moment has occurred that puts knowledge at risk | A capture prompt identifying what's at risk and drafting the artifact |
| **Design** | User wants to set up or improve how their team handles knowledge | A knowledge architecture: where things live, how they're found, who owns them |

If unclear, default to **Capture** — it's the most common need and the fastest to deliver.

---

## MODE 1: CAPTURE

### STEP C1 — Classify the Knowledge Type

All capturable knowledge falls into exactly three types. Each has a different shape, different audience, and different shelf life.

| Type | What it is | Example | Primary audience | Shelf life |
|------|-----------|---------|-----------------|------------|
| **Decision** | Why we chose X over Y. The reasoning, constraints, and trade-offs behind a choice. | "We chose PostgreSQL over MongoDB because our query patterns are heavily relational and our team has deeper SQL expertise." | Future-self asking "why did we do it this way?" | Long — until superseded |
| **Context** | The unwritten rules, domain knowledge, and tribal wisdom that code can't express. The stuff a new person needs to know but nobody thinks to tell them. | "The payment service has a 30-second timeout on webhook retries because the provider rate-limits at 2 req/s. Don't change this without talking to @payments-team." | New team member trying to understand the system | Medium — needs periodic refresh |
| **Learning** | What we discovered through doing — debugging insights, incident patterns, performance gotchas, migration lessons, vendor behaviors. Things we learned the hard way. | "When Elasticsearch reindexes during peak traffic, the cluster becomes unresponsive for 2-3 minutes. Schedule reindexing for the 03:00-05:00 UTC window." | Anyone who will face the same situation | Variable — valid until the system changes |

**Classification heuristic:**

```
IF someone could ask "why did we do it this way?" → Decision
IF someone could say "I wish someone had told me this when I joined" → Context
IF someone could say "we learned this the hard way" → Learning
IF it fits multiple types → use the one that matches the PRIMARY reader need
```

### STEP C2 — Choose the Capture Depth

Not every piece of knowledge deserves a full document. Use the Progressive Depth model — start with the minimum viable capture and grow only when value justifies effort.

| Depth | Time to create | What you produce | When to use |
|-------|---------------|-----------------|-------------|
| **Seed** | 2 minutes | 2-5 sentences: what happened, what we decided/learned, one key insight. No formatting, no structure — just the kernel of truth. | Default for everything. Most knowledge only needs this. A seed that exists beats a full doc that doesn't. |
| **Grow** | 15 minutes | Structured artifact with context, reasoning, links to related artifacts, and a discovery header. Follows the appropriate template below. | When the knowledge is reusable, affects multiple people, or the decision has significant consequences. |
| **Curate** | 30 minutes | Polished, reusable reference document connected to related knowledge. Includes examples, edge cases, and "when this doesn't apply." | High-stakes knowledge: architectural decisions, critical operational procedures, domain rules that affect multiple teams. |

**The golden rule**: Always start at Seed. Promote to Grow only when someone actually needs the deeper version. Most seeds never need to grow — and that's fine. A repo with 200 seeds is more valuable than a wiki with 5 perfect documents and 195 undocumented decisions.

### STEP C3 — Produce the Artifact

Select the template matching the knowledge type and depth.

---

#### DECISION — Seed

```
## Decision: [What was decided — verb phrase]
**Date**: [date] | **By**: [who] | **Status**: Active

[One paragraph: what we decided, why, and what we considered.
Include the "why not" for the most obvious alternative.]
```

#### DECISION — Grow

```
## Decision: [What was decided — verb phrase]

**Date**: [date]
**Deciders**: [who was involved]
**Status**: Active | Superseded by [link]
**Tags**: [domain tags for discovery — e.g., #database #infrastructure #vendor]
**Review trigger**: [when to revisit — e.g., "next database scaling discussion" or "Q4 2026"]

### Context
[What situation prompted this decision? What constraints were in play?
Write for someone who has ZERO context about this project.]

### Decision
[State the decision in 1-2 sentences.]

### Alternatives Considered
- **[Alternative A]**: [Why not — 1-2 sentences]
- **[Alternative B]**: [Why not — 1-2 sentences]
- **Do nothing**: [Why not, or why it was tempting]

### Consequences
- [What becomes easier]
- [What becomes harder]
- [What risks we accepted]

### Related
- [Links to related decisions, PRs, documents, Slack threads]
```

#### DECISION — Curate

Same as Grow, plus:

```
### Decision History
[If this supersedes a previous decision, link it and explain what changed]

### Applicability
[When does this decision apply? When does it NOT apply?
"This applies to all user-facing services. Internal tooling is exempt."]

### Verification
[How can someone verify this decision is still being followed?
"Check that all new services use the shared Postgres cluster, not local SQLite."]
```

---

#### CONTEXT — Seed

```
## Context: [What this is about]
**Area**: [system/domain/team] | **Owner**: [who knows most about this]

[One paragraph: the thing a new person needs to know.
Prioritize the non-obvious — don't restate what code already says.]
```

#### CONTEXT — Grow

```
## Context: [What this is about]

**Area**: [system, domain, or team this applies to]
**Owner**: [person or team responsible for this knowledge]
**Last verified**: [date someone confirmed this is still accurate]
**Tags**: [discovery tags — e.g., #payments #onboarding #gotcha]

### The Rule
[State the rule, convention, or constraint clearly. One paragraph max.]

### Why This Exists
[The reason behind the rule — what goes wrong if you ignore it.
Real examples are 10x more memorable than abstract explanations.]

### Common Mistakes
[What people typically get wrong about this — the misconceptions,
the shortcuts that seem reasonable but break things.]

### Exceptions
[When this rule DOESN'T apply, and how to recognize those situations.]

### Who to Ask
[The person or team with the deepest knowledge. Include a backup.]

### Related
[Links to code, ADRs, runbooks, or other context that connects.]
```

---

#### LEARNING — Seed

```
## Learning: [One-sentence summary of what we learned]
**Date**: [date] | **Source**: [incident / migration / spike / debugging session]

[One paragraph: what happened, what we discovered, what to do differently.
Focus on the TRANSFERABLE insight, not the blow-by-blow narrative.]
```

#### LEARNING — Grow

```
## Learning: [One-sentence summary of what we learned]

**Date**: [date]
**Source**: [what event produced this learning — link to incident, PR, or ticket]
**Applicability**: [what systems/situations this applies to]
**Tags**: [discovery tags — e.g., #elasticsearch #performance #migration]
**Confidence**: [High — well-validated / Medium — worked for us / Low — hypothesis]

### What Happened
[Brief narrative — 3-5 sentences. Enough to understand the situation,
not enough to be a full post-mortem.]

### What We Learned
[The transferable insight — stated as a principle, not a story.
"Elasticsearch reindexing under load causes 2-3 minute cluster unavailability"
not "Last Tuesday the cluster went down while we were reindexing."]

### Recommendation
[What to do with this knowledge — a specific, actionable prescription.
"Schedule reindexing in the 03:00-05:00 UTC window"
not "Be careful with reindexing."]

### Caveats
[When this learning might not apply. What would change the recommendation.]

### Evidence
[Links to incidents, monitoring dashboards, PRs, or data that backs this up.]
```

---

### STEP C4 — Add the Discovery Header

Every artifact at Grow depth or above gets a discovery header. This is what makes knowledge FINDABLE, not just written.

```
---
type: decision | context | learning
tags: [list of discovery tags]
area: [system, domain, or team]
owner: [person or team]
created: [date]
last_verified: [date]
review_trigger: [condition or date for next review]
status: active | superseded | archived
related: [list of links to related knowledge]
---
```

**Tagging discipline**: Use a flat, consistent tag vocabulary. Don't invent new tags for every artifact — reuse existing ones. Good tags answer "what would someone search for when they need this?" Tags are nouns and domains (`#payments`, `#kubernetes`, `#vendor-choice`, `#onboarding`), not adjectives (`#important`, `#urgent`).

---

## MODE 2: DETECT

### When to Fire Detection

These workflow moments are high-value capture opportunities. The skill should proactively prompt for capture when it detects these:

| Moment | Knowledge at risk | Suggested capture |
|--------|------------------|-------------------|
| **PR merged** with significant design choices | Why the approach was chosen over alternatives | Decision — Seed |
| **Incident resolved** | Debugging insights, root cause, system behavior under stress | Learning — Grow |
| **Team member leaving** | Tribal knowledge, undocumented conventions, relationship maps | Context — Grow (multiple artifacts) |
| **New member joining** | Gap between what's documented and what they actually need | Context audit — run context-gap-analyzer first |
| **Vendor/tool selected** | Selection criteria, trade-offs, what was rejected | Decision — Grow |
| **Migration completed** | Gotchas, unexpected behaviors, performance differences | Learning — Grow |
| **Spike/investigation finished** | Findings, dead ends, recommendations | Learning — Seed or Grow |
| **Repeated question in Slack** | Something everyone asks that nobody documents | Context — Seed |
| **Decision re-debated** | The original reasoning has been lost | Decision — Grow (retroactive) |
| **Workaround established** | Why the workaround exists and when it can be removed | Context — Seed with removal trigger |
| **Process changed** | Why the old process failed and why the new one is different | Decision — Grow |

### Detection Prompt Format

When detecting a capture moment, present it concisely:

```
CAPTURE MOMENT DETECTED

I notice [what happened — e.g., "you just resolved an incident involving the payment retry service"].

Knowledge at risk: [what might be lost — e.g., "the debugging path that led to the root cause and the Elasticsearch behavior under load"]

Suggested capture:
  Type: [Learning / Decision / Context]
  Depth: [Seed / Grow]
  Estimated time: [2 min / 15 min]

Want me to draft it from the available context?
```

If the user confirms, draft the artifact from available signals — PR descriptions, incident timelines, conversation history — and present it for review. The user edits rather than writes from scratch, which dramatically reduces friction.

---

## MODE 3: DESIGN

### When to Use Design Mode

Use this when the user wants to set up or improve their team's knowledge architecture — not capture a single artifact, but design the SYSTEM for how knowledge flows.

### STEP D1 — Audit Current State

Before designing anything, understand what exists:

```
KNOWLEDGE ARCHITECTURE AUDIT

Current state:
  Where does knowledge live today? [repo docs, wiki, Confluence, Notion, Slack bookmarks, people's heads]
  What works? [What knowledge is actually discoverable today?]
  What's broken? [What do people complain about? "I can never find..." / "Nobody told me..."]
  What's the team size? [affects formality needed]
  What tools does the team already use? [design FOR their workflow, not against it]

Capture moments currently happening:
  [Which of the detection moments above are occurring regularly?
   Which produce knowledge artifacts? Which don't?]

Knowledge debt:
  [What significant decisions/context/learnings exist only in people's heads?
   Estimate the volume — 5 items? 50? 500?]
```

### STEP D2 — Design the Architecture

A knowledge architecture has four components:

#### 1. Location Strategy — Where Things Live

```
LOCATION STRATEGY

Principle: Knowledge lives closest to where it's used.

Decisions → [in the repo, next to the code they affect — /docs/decisions/]
  Why: Decisions travel with the code. When someone reads the code, the "why" is right there.
  Format: Markdown files, numbered sequentially (001-use-postgres.md)

Context → [split between repo and wiki/Notion]
  System context → in repo (/docs/context/ or .ctx files, CLAUDE.md)
    Why: System context is consumed by both humans and agents
  Domain/team context → in wiki or Notion
    Why: Domain knowledge spans multiple repos

Learnings → [in repo /docs/learnings/ or team wiki depending on scope]
  Single-system learnings → in that system's repo
  Cross-system learnings → in team wiki/Notion
  Incident learnings → linked from the post-mortem

Onboarding → [curated index document that LINKS to the above]
  Why: An onboarding doc that duplicates knowledge rots. One that links stays fresh.
```

Adapt this to the team's actual tools. If they use Confluence, put it in Confluence. If they live in GitHub, put it in the repo. The best location is the one people already go to.

#### 2. Discovery Strategy — How Things Are Found

```
DISCOVERY STRATEGY

Search: [How do people find knowledge they don't know exists?]
  - Flat tag vocabulary applied to all artifacts
  - README index files in each knowledge directory
  - Search tool appropriate to the platform (GitHub search, Notion search, etc.)

Browse: [How do people explore knowledge in an area?]
  - Directory structure mirrors team/domain/system boundaries
  - Index documents per area that curate the most important items
  - Onboarding guide that provides a reading order for new members

Stumble: [How does knowledge find people who need it but aren't looking?]
  - Link knowledge artifacts from PRs, incident docs, and code comments
  - Reference decisions in code: // See decision-017-retry-strategy.md
  - Include "Related" links in every Grow+ artifact
```

#### 3. Ownership Strategy — Who Maintains What

```
OWNERSHIP STRATEGY

Principle: Every knowledge artifact has exactly one owner.
An artifact without an owner WILL rot.

Team-level ownership:
  - [Team/person] owns decisions in [area]
  - [Team/person] owns context for [system]
  - Learnings are owned by the person who captured them until transferred

Ownership transfer:
  - When an owner leaves, knowledge transfers to their replacement
  - The leaving person's final task includes a knowledge transfer session
  - Run knowledge-architect in Detect mode for departing team members

Orphan policy:
  - Artifacts without active owners are flagged for adoption or archival
  - Quarterly audit: list artifacts whose owner has left the team
```

#### 4. Freshness Strategy — How Knowledge Stays Alive

```
FRESHNESS STRATEGY

Principle: Outdated knowledge is worse than no knowledge.
It creates false confidence.

Review triggers:
  - TIME-BASED: Context artifacts reviewed every 6 months
  - EVENT-BASED: Decisions reviewed when the system they describe changes significantly
  - QUERY-BASED: If someone reads an artifact and finds it inaccurate, they flag it

Freshness signals:
  - Every artifact has a "last_verified" date
  - Artifacts not verified in >12 months get a STALE warning
  - Stale artifacts are either refreshed, archived, or deleted

Lightweight review process:
  1. Owner reads the artifact (5 minutes)
  2. Still accurate? → Update "last_verified" date
  3. Partially outdated? → Update the content, note what changed
  4. Fully outdated? → Archive with a note explaining what replaced it
  5. No longer relevant? → Delete. Dead knowledge clutters search.

Quarterly knowledge health check:
  - How many artifacts exist per type?
  - How many are stale (>12 months unverified)?
  - What areas have zero coverage?
  - What questions keep getting asked that don't have artifacts?
```

### STEP D3 — Bootstrap Plan

For teams starting from zero, provide a phased plan:

```
BOOTSTRAP PLAN

Week 1-2: Seed the critical gaps
  - Identify the 10 most important undocumented decisions → capture as Seeds
  - Identify the 5 things every new person asks → capture as Context Seeds
  - Set up the directory structure and index files
  - Total effort: ~2 hours

Week 3-4: Build the habit
  - Add knowledge capture to the definition of done for incidents
  - Add "any decisions to document?" to retro agendas
  - Grow 3-5 seeds into full artifacts for the highest-value items
  - Total effort: ~1 hour/week

Month 2-3: Establish ownership
  - Assign owners to all existing artifacts
  - Run first quarterly health check
  - Create the onboarding index document
  - Total effort: ~2 hours one-time

Ongoing: Maintain the flywheel
  - Capture at workflow moments (2 min seeds)
  - Grow when needed (15 min, triggered by reuse)
  - Quarterly health check (30 min)
  - Knowledge transfer on team changes (1-2 hours)
```

---

## Calibration Rules

**1. Existence beats quality.** A 2-minute seed with a rough sentence about why we chose Postgres is infinitely more valuable than no record at all. Never let "I don't have time to write it properly" prevent capturing the kernel. Seeds are valid, permanent artifacts — not drafts of something that should be bigger.

**2. Capture at the moment, curate later.** The hardest thing about knowledge capture is remembering to do it. The best time to capture is immediately after the decision, incident, or learning — even if the capture is messy. Clean it up later. Or don't. A messy seed is still a seed.

**3. Discoverable > comprehensive.** A well-tagged seed that people can find is more valuable than a comprehensive document nobody knows exists. Invest more in discovery metadata (tags, links, index files) than in content completeness.

**4. Don't duplicate what code says.** If the code clearly expresses a behavior, documenting that behavior is waste. Knowledge artifacts capture what code CANNOT say: the why, the alternatives rejected, the gotchas, the human context. If you're describing what a function does, you're writing the wrong thing.

**5. Design for the question, not the answer.** Every artifact should be findable by the question someone would ask when they need it. "Why do we use Postgres?" should lead to the decision record. "What happens during Elasticsearch reindexing?" should lead to the learning. If you can't state the question, the artifact probably isn't useful.

**6. Knowledge without an owner rots.** Every artifact at Grow depth needs a human who will answer "is this still true?" when asked. If nobody owns it, it will decay silently. An ownerless artifact should either gain an owner or be archived.

**7. Measure knowledge by questions answered, not documents written.** The success metric is not "we have 200 knowledge artifacts." It's "new engineers can answer 'why did we do it this way?' without asking a person." If the artifacts exist but people still ask Slack, the knowledge system is failing — the problem is discoverability, not volume.

**8. Adapt to the team's existing tools.** The best knowledge system is the one people actually use. If the team lives in GitHub, put knowledge in the repo. If they live in Notion, put it in Notion. If they use Slack bookmarks as their informal knowledge system, formalize that pattern rather than fighting it. Never force a new tool for knowledge capture alone.

---

## Thinking Triggers

- *"If the person who knows this left tomorrow, what would be lost?"*
- *"What question would a new team member ask that has no written answer?"*
- *"Six months from now, will anyone — including me — remember why we did this?"*
- *"Is this something the code can say, or something only a human knows?"*
- *"Would I be able to FIND this artifact if I needed it and had forgotten it existed?"*
- *"What's the simplest capture that would still be useful in a year?"*
