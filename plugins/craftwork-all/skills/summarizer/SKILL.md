---
name: summarizer
description: "Apply this skill whenever the user asks to summarize, condense, distill, or compress any content — a document, article, meeting notes, conversation, codebase, book, research paper, video transcript, or any other source material. Triggers on phrases like 'summarize this', 'give me the TL;DR', 'condense this', 'what are the key points?', 'distill this down', 'brief me on this', 'what's the gist?', 'BLUF this', 'executive summary', 'compress this for me', or any request to reduce content while preserving its essential value. Also trigger when the user pastes a long text and implicitly wants it shortened, when they share a link and ask 'what does this say?', or when they ask for meeting notes or action items from a transcript. This skill does NOT apply to 'explain X to me' (use topic-explainer) or 'write a summary section for my doc' (use technical-writing). This skill is for when source material exists and needs to be compressed."
---

# Summarizer

**Core principle**: A summary is lossy compression. What you choose to lose defines whether the summary is useful or dangerous. The right summarization approach depends on what the reader will *do* with the summary — not on how long the source is. A summary for a decision-maker must lead with the conclusion. A summary for future reference must preserve retrievability. A summary for sharing must be self-contained. Different purposes demand different shapes.

The goal is not to make something shorter. The goal is to produce the smallest artifact that preserves the value the reader needs.

---

## How to Execute This Skill

### STEP 1 — Analyze the Source

Before asking the user anything, classify the summarization task:

```
SOURCE ANALYSIS
Content type: [article / document / transcript / conversation / code / research paper / book / multi-source collection]
Source length: [short (<1000 words) / medium (1-5K) / long (5-20K) / very long (20K+) / multi-document]
Information density: [sparse — lots of filler / mixed / dense — most sentences carry signal]
Structure: [well-structured with sections / loosely structured / unstructured stream]
Contains: [arguments / data / narrative / instructions / mixed]
```

Do not show this analysis to the user. It drives the recommendation in Step 2.

---

### STEP 2 — Recommend Style and Compression

Present the recommendation as a single interaction — one message with options the user can confirm or adjust.

#### Summarization Styles

| Style | How it works | Best for | Avoid when |
|-------|-------------|----------|------------|
| **BLUF** | Bottom Line Up Front. State the conclusion/recommendation/decision in the first sentence. Then provide supporting evidence in descending order of importance. Reader can stop at any point and has received the most important information first. | Decision-makers, busy stakeholders, status updates, any summary where "what should we do?" matters more than "what happened?" | Source is exploratory with no clear conclusion; reader needs to form their own opinion |
| **Key Points** | Extract the N most important claims, findings, or ideas as a structured list. Each point is self-contained. No narrative flow — optimized for scanning. | Meeting notes, research papers, long reports, anything where the reader needs to quickly find specific information | Source is a narrative or argument where the logic between points matters as much as the points themselves |
| **Narrative** | Rewrite the content as a coherent short-form narrative that preserves the logical flow and argumentation structure. Reads like a well-written paragraph, not a list. | Articles, essays, arguments, stories, anything where the *reasoning chain* matters — not just the conclusions | Source is a data dump or reference material where flow doesn't matter |
| **Briefing** | Self-contained summary designed to be shared with people who haven't seen the source. Includes enough context that the reader doesn't need the original. Structured with: situation → key findings → implications → recommended actions. | Sharing summaries with teammates, leadership updates, cross-team communication, async briefings | Reader has access to the original and just needs a compressed version for themselves |
| **Progressive** | Multi-layer summary. Layer 1: one sentence. Layer 2: one paragraph. Layer 3: full summary with key details. Reader chooses their depth. | Reference material, notes for future self, content you'll revisit later, knowledge management | One-time summaries where the reader won't return to the content |
| **Action-Oriented** | Extract only what requires action: decisions made, action items, owners, deadlines, open questions. Everything else is discarded. | Meeting transcripts, planning sessions, retrospectives, any content where "what do we do next?" is the only question that matters | Content is informational with no actions (use Key Points instead) |
| **Comparative** | Synthesize multiple sources into a single summary that highlights agreements, disagreements, and unique contributions from each. | Literature reviews, competitive analysis, multi-article research, any multi-source input | Single-source summarization |

#### Compression Levels

| Level | Ratio | Output | When to recommend |
|-------|-------|--------|-------------------|
| **Headline** | ~98% compression | 1 sentence | "What is this about?" — maximum compression, minimum nuance |
| **Snapshot** | ~90% compression | 2-4 sentences | Quick orientation. Reader decides if they want to go deeper |
| **Standard** | ~75% compression | 1-3 paragraphs | Default. Captures the substance without the detail |
| **Detailed** | ~50% compression | Multiple paragraphs | When nuance, evidence, or caveats matter. Preserves reasoning chains |
| **Comprehensive** | ~30% compression | Structured document | Long or complex sources where too much compression destroys value |

#### Fidelity Mode

Every summary makes a trade-off between readability and source accuracy. Make this explicit:

| Mode | What it means | When to use |
|------|------------|-------------|
| **Faithful** | Stays close to the source language. Preserves original terminology, attributions, and qualifications. Prioritizes accuracy over fluency. | Legal, medical, scientific, compliance — anywhere distortion is dangerous |
| **Rewritten** | Rephrases freely in clear, simple language. May restructure arguments for clarity. Prioritizes readability over verbatim accuracy. | General content, articles, blog posts, meeting notes — anywhere clarity matters more than exact wording |

Default to **Rewritten** unless the content is in a high-stakes domain or the user asks for faithfulness.

#### Recommendation Logic

```
IF source is a meeting transcript or conversation:
  → Action-Oriented + Standard + Rewritten
  "Meetings are about decisions and next steps — I'll extract what matters."

IF source is a research paper or technical document:
  → Key Points + Detailed + Faithful
  "Dense technical content benefits from structured extraction with preserved precision."

IF source is an article, essay, or blog post:
  → Narrative + Standard + Rewritten
  "This reads as an argument — I'll preserve the reasoning chain."

IF user says "brief my team" or "share with leadership":
  → Briefing + Standard + Rewritten
  "I'll make this self-contained so they don't need the original."

IF user says "TL;DR" or "gist" or "quick summary":
  → BLUF + Snapshot + Rewritten
  (Explicit speed request — honor it directly)

IF user says "action items" or "what do we need to do":
  → Action-Oriented + Standard + Rewritten
  (Explicit action request — honor it directly)

IF multiple sources are provided:
  → Comparative + Standard + Rewritten
  "Multiple sources — I'll synthesize rather than summarize individually."

IF user wants to save for future reference or notes:
  → Progressive + Detailed + Rewritten
  "Multi-layer summary so you can scan at any depth later."

IF source is legal, medical, financial, or compliance-related:
  → Key Points + Detailed + Faithful
  "High-stakes content — I'll preserve source language and qualifications."
```

#### Incompatible Combinations

- **Action-Oriented + Headline**: Actions need enough detail to be actionable. Suggest Snapshot minimum.
- **Comparative + Headline**: Can't synthesize multiple sources in one sentence. Suggest Standard minimum.
- **Progressive + Headline/Snapshot**: Progressive IS multi-level — it already contains a headline. Use Progressive at Standard or Detailed.
- **Faithful + Headline**: Impossible to be faithful at 98% compression. Suggest Snapshot + Faithful.
- **Briefing + Headline**: Briefings need context to be self-contained. Suggest Standard minimum.

---

### STEP 3 — Present Options to the User

Present the recommendation concisely. The user wants the summary, not a lecture about summarization theory.

Format:

```
I'd recommend a [style] summary at [compression] depth, [fidelity mode].

[1-sentence reason why this approach fits this content.]

Want me to adjust?
  Style: [recommended] / [alt 1] / [alt 2]
  Depth: Headline / Snapshot / Standard / Detailed / Comprehensive
  Fidelity: Faithful / Rewritten
```

If the agent platform supports structured input (e.g., ask_user_input), use it for frictionless selection.

**Speed override**: If the user pastes content and says "TL;DR" or "summarize this quickly", skip the interaction entirely. Default to BLUF + Snapshot + Rewritten and deliver immediately. Don't add friction to an explicitly fast request.

---

### STEP 4 — Produce the Summary

Once style, compression, and fidelity are confirmed (or defaulted), produce the summary following the selected style's structure.

#### BLUF Execution

```
BOTTOM LINE: [Conclusion / recommendation / key finding in 1-2 sentences]

SUPPORTING DETAIL:
[Most important evidence or context — 1-2 sentences]
[Second most important — 1-2 sentences]
[Additional context if compression level allows]

SO WHAT: [Why this matters to the reader — 1 sentence]
```

**Quality check**: Cover the "BOTTOM LINE" section. If someone reads only that, do they have what they need to act? If not, your bottom line isn't bottom-line enough.

#### Key Points Execution

```
KEY POINTS FROM: [source title/description]

1. [Point — stated as a complete, self-contained claim. Not a topic label.]
2. [Point]
3. [Point]
...N points (scale to compression level: Snapshot=3, Standard=5-7, Detailed=8-12)

NOTABLE OMISSIONS: [Anything important you had to cut — 1 sentence]
```

**Quality check**: Read each point in isolation. Does it make sense without the others? If a point says "The authors also discussed methodology" — that's a topic label, not a key point. Rewrite as "The study used a randomized control trial with 500 participants across 12 months."

#### Narrative Execution

Write a coherent short passage that preserves the source's reasoning structure:

1. Open with the core thesis or finding
2. Walk through the key supporting arguments in order
3. Note the most important caveats or counterarguments
4. Close with the implication or conclusion

**Quality check**: Does the summary have a logical flow a reader can follow without jumping? If you removed the source entirely, could someone understand the argument from your summary alone?

#### Briefing Execution

```
BRIEFING: [Title]
Source: [what this summarizes]
Date: [when the source was created/published]
Prepared for: [intended audience, if known]

SITUATION: [Context the reader needs to understand why this matters — 2-3 sentences]

KEY FINDINGS:
- [Finding 1]
- [Finding 2]
- [Finding 3]

IMPLICATIONS: [What this means for the reader's work/decisions — 1-2 sentences]

RECOMMENDED ACTIONS: [What should happen next, if applicable]

OPEN QUESTIONS: [Unresolved issues from the source]
```

**Quality check**: Send this to someone who hasn't seen the source. Can they understand it fully? If they need to ask "but what was the original about?" — the briefing isn't self-contained enough.

#### Progressive Execution

```
## Layer 1 — One Sentence
[The single most important takeaway]

## Layer 2 — One Paragraph
[Core message expanded with 2-3 supporting points]

## Layer 3 — Full Summary
[Detailed summary preserving key evidence, caveats, and nuance.
 Structured with subheadings if the source has natural sections.]
```

**Quality check**: Each layer must be a complete, valid summary on its own. Layer 1 shouldn't require Layer 2 to make sense. A reader should be able to stop at any layer and walk away informed.

#### Action-Oriented Execution

```
DECISIONS MADE:
- [Decision 1 — stated clearly, with who decided if known]
- [Decision 2]

ACTION ITEMS:
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Specific action] | [Name] | [Date] | Open |

OPEN QUESTIONS:
- [Unresolved question 1 — who needs to answer it?]
- [Unresolved question 2]

PARKING LOT: [Topics raised but deferred — 1-2 sentences if any]
```

**Quality check**: Could someone who missed the meeting read this and know exactly what they need to do? If any action item says "Follow up on X" without specifying what "follow up" means concretely, it's not actionable enough.

#### Comparative Execution

```
SYNTHESIS: [Sources compared — list titles/descriptions]

CONSENSUS: [What all/most sources agree on]
- [Shared finding 1]
- [Shared finding 2]

DIVERGENCE: [Where sources disagree]
- [Source A says X; Source B says Y — the tension is about Z]

UNIQUE CONTRIBUTIONS: [What only one source covers]
- [Source C uniquely argues/provides...]

GAP: [What none of the sources address but probably should]
```

**Quality check**: Does each source get fair representation? Could a reader identify the distinct contribution of each source? If you removed one source, would the synthesis change — and can the reader see how?

---

### STEP 5 — Offer Follow-up

After delivering the summary, offer exactly one follow-up based on style:

- **BLUF**: "Want me to expand on any of the supporting detail?"
- **Key Points**: "Want me to elaborate on any specific point?"
- **Narrative**: "Want me to compress this further or expand a particular section?"
- **Briefing**: "Should I adjust this for a different audience?"
- **Progressive**: "Want me to add a Layer 4 — your own executive annotation?"
- **Action-Oriented**: "Want me to draft follow-up messages for any of these action items?"
- **Comparative**: "Want me to deep-dive into any of the divergences?"

Offer naturally. Don't force if the user signals completion.

---

## Calibration Rules

**1. Speed is the default virtue.** Most summarization requests are time-saving requests. If the user says "summarize this," they want it now, not after a configuration dance. Reserve the full interaction for ambiguous or high-stakes content. Simple content gets a fast default.

**2. Compression is not deletion.** Removing sentences is not summarization. Good compression preserves information density while reducing volume. Bad compression throws away signal along with noise. After producing any summary, check: "Did I lose anything the reader would want back?"

**3. Attributions survive compression.** If the source attributes a claim to a specific person, study, or organization, the summary must preserve that attribution. "AI will replace 40% of jobs" is different from "An MIT study estimates AI could automate 40% of current job tasks." Dropping attributions is a form of distortion.

**4. Caveats survive compression.** If the source says "X, but only under conditions Y," the summary cannot say just "X." Qualifications are not filler — they're precision. Dropping caveats is the most common way summaries become misleading.

**5. Faithful mode means faithful.** When faithfulness is selected, do not rephrase claims. Use the source's terminology. Preserve hedging language ("may," "suggests," "could"). In high-stakes domains, a casually rephrased summary can change the meaning enough to cause harm.

**6. The user's explicit request overrides everything.** If they say "just bullet points," use Key Points. If they say "action items only," use Action-Oriented. If they say "one sentence," give them a Headline. Never argue with an explicit format preference.

**7. Flag what you cut.** At Standard compression or above, signal to the reader what was omitted. "NOTABLE OMISSIONS" or "This summary does not cover..." helps the reader decide if they need the original. Invisible omissions are the most dangerous kind.

**8. Multi-source requires synthesis, not concatenation.** If given multiple sources, never summarize them independently and stack the results. The Comparative style exists because the value of multi-source summarization is in the cross-referencing — agreements, tensions, and gaps — not in parallel compression.

---

## Thinking Triggers

- *"What will the reader DO after reading this summary? That determines what to preserve."*
- *"If this summary is the only version that survives, what would be lost?"*
- *"Am I compressing or am I distorting? Where's the line for this content?"*
- *"Does my summary preserve the 'why' or only the 'what'?"*
- *"Could someone make a wrong decision based on what I omitted?"*
- *"If the source author read my summary, would they say 'yes, that's what I meant'?"*
