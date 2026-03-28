---
name: topic-explainer
description: "Apply this skill whenever the user asks to have a topic, concept, technology, or idea explained to them. Triggers on phrases like 'explain X to me', 'what is X?', 'how does X work?', 'teach me about X', 'help me understand X', 'break down X', 'ELI5', 'explain like I'm five', 'give me an overview of X', 'I don't understand X', 'walk me through X', or any situation where the user wants to learn or understand something rather than produce an artifact. Also trigger when someone pastes a concept and asks for clarification, when they ask 'why' something works a certain way, or when they need a refresher on a topic they've encountered before. This skill does NOT apply to 'write documentation about X' (use technical-writing) or 'analyze X' (use reasoning skills). This skill is for when the human is the learner."
---

# Topic Explainer

**Core principle**: An explanation succeeds when the learner can use the concept, not when the explainer has covered every detail. The best explanation style depends on what the topic demands and what the learner needs — not on the explainer's preference. This skill matches explanation approach to topic shape before producing a single word of content.

The goal is not to be comprehensive. The goal is to produce the shortest explanation that changes the learner's mental model of the topic.

---

## How to Execute This Skill

### STEP 1 — Analyze the Topic

Before asking the user anything, classify the topic along these dimensions:

```
TOPIC ANALYSIS
Topic: [what the user wants explained]
Domain: [technical / scientific / conceptual / practical / business / creative]
Abstraction level: [concrete / mixed / abstract]
Prerequisite depth: [none / light / moderate / heavy]
Core challenge: [what makes this topic hard to understand]
  - Unfamiliar vocabulary?
  - Counterintuitive behavior?
  - Hidden complexity behind simple surface?
  - Too many interacting parts?
  - Requires prior concepts first?
  - Abstract with no obvious physical analogy?
```

Do not show this analysis to the user. It exists to drive the recommendation in Step 2.

---

### STEP 2 — Recommend Style and Depth

Using the topic analysis, select the best explanation style and verbosity level. Then present the recommendation to the user in a single interaction — one message with options they can confirm or adjust.

#### Explanation Styles

| Style | How it works | Best for | Avoid when |
|-------|-------------|----------|------------|
| **Feynman** | Strip away jargon, explain using only simple words and everyday analogies. Build from the most fundamental idea outward. | Abstract or complex topics where jargon masks understanding (quantum mechanics, monads, eventual consistency) | Topic is already simple; learner is an expert who needs precision |
| **Socratic** | Guide the learner through a sequence of questions that lead them to discover the concept themselves. Never state the answer directly until they've arrived at it. | Topics where understanding *why* matters more than *what*; correcting misconceptions; philosophical or design-thinking topics | Learner needs a quick factual answer; topic is purely procedural |
| **Example-First** | Start with a concrete, working example. Show the thing in action before explaining the theory behind it. Generalize from specific to abstract. | Programming concepts, practical skills, tools, APIs, anything the learner will *use* | Highly abstract topics with no natural concrete example (category theory, epistemology) |
| **Layered** | Start with a one-sentence version anyone could understand. Add a layer of detail. Add another. Each layer is complete — the learner can stop at any depth and still have a valid understanding. | Broad topics with natural depth levels (how the internet works, machine learning, compiler design) | Very narrow topics where layering adds no value |
| **Analogy Bridge** | Map the entire explanation to a domain the learner already knows. Maintain the mapping throughout, noting where it breaks down. | Unfamiliar domains that have structural parallels to common experience (databases ↔ libraries, networking ↔ postal system, Git ↔ save points in a video game) | When no good analogy exists, or when the analogy would mislead more than it clarifies |
| **Visual-Spatial** | Explain by building a mental picture, diagram, or map. Describe relationships spatially. Use system diagrams, flowcharts, or mental models as the primary vehicle. | Systems, architectures, processes, anything with components that interact (microservices, state machines, organizational structures) | Linear or sequential concepts with no spatial structure |

#### Verbosity Levels

| Level | What the learner gets | Length | When to recommend |
|-------|----------------------|--------|-------------------|
| **TL;DR** | One-sentence definition + one-sentence "why it matters" | 2-3 sentences | Learner asked casually, needs a quick anchor, or is evaluating whether to go deeper |
| **Brief** | Core concept + one example or analogy + key implication | 1-2 paragraphs | Learner has adjacent knowledge, needs to fill a specific gap |
| **Standard** | Full explanation with examples, analogies where helpful, and common pitfalls or misconceptions | 3-6 paragraphs | Default for most requests. Learner is genuinely trying to understand the topic |
| **Deep Dive** | Comprehensive treatment including edge cases, nuances, historical context, trade-offs, and connections to related concepts | 8+ paragraphs, possibly with sections | Learner explicitly asks to go deep, or the topic is complex enough that a standard explanation would be misleading |
| **Tutorial** | Step-by-step, hands-on walkthrough. The learner does something at each step and sees results. Theory is woven into practice. | Structured steps with embedded explanations | Learner wants to *do* something, not just understand it. Topic is practical and executable |

#### Recommendation Logic

Use this decision tree to select the default recommendation:

```
IF topic is abstract AND counterintuitive:
  → Feynman + Standard
  "Complex topics benefit from stripping away jargon and building from fundamentals."

IF topic is a design/philosophy question OR involves correcting a misconception:
  → Socratic + Standard
  "Understanding 'why' here matters more than memorizing 'what' — discovery sticks better."

IF topic is a tool, language feature, API, or practical skill:
  → Example-First + Standard (or Tutorial if hands-on is possible)
  "Seeing it work first gives you the anchor to understand the theory."

IF topic is broad with natural depth layers (e.g., "how does X work?"):
  → Layered + Standard
  "This topic has natural zoom levels — I'll start simple and add depth."

IF topic is from an unfamiliar domain AND has a strong structural analogy:
  → Analogy Bridge + Brief
  "Mapping this to something familiar will get you 80% of the way."

IF topic involves interacting components or system architecture:
  → Visual-Spatial + Standard
  "This is easiest to understand as a picture of parts and relationships."

IF user says "ELI5" or "simply":
  → Feynman + Brief
  (This is an explicit style request — honor it directly)

IF user says "quick overview" or "in a nutshell":
  → Layered + TL;DR
  (This is an explicit verbosity request — honor it directly)

IF user provides their own style preference:
  → Use their preference. Do not override.
```

#### Incompatible Combinations

Some style + verbosity combinations don't work. Detect and adjust:

- **Socratic + TL;DR**: Impossible. Socratic requires dialogue. Suggest: Feynman + TL;DR instead, or upgrade to Brief.
- **Tutorial + TL;DR/Brief**: A tutorial can't be brief. Suggest: Example-First + Brief as alternative, or upgrade to Tutorial verbosity.
- **Feynman + Deep Dive**: Tension. Feynman is about simplicity; deep dives add complexity. Suggest: Layered + Deep Dive instead, or Feynman + Standard.

---

### STEP 3 — Present Options to the User

Present the recommendation as a single interaction. Be concise — the user wants the explanation, not a lecture about explanation methodology.

```
I'd recommend explaining [topic] using [style] at [verbosity] depth.

[1-sentence reason why this style fits this topic.]

Want me to adjust the approach?
  Style: [recommended] / [alternative 1] / [alternative 2]
  Depth: TL;DR / Brief / Standard / Deep Dive / Tutorial
```

If the agent platform supports structured input (e.g., ask_user_input), use it to present the options as clickable choices rather than requiring the user to type. The first option in each group should be the recommended one.

**If the user signals impatience or just wants the answer** (e.g., they asked a simple question like "what is Redis?"), skip this step entirely — default to Example-First + Brief and deliver the explanation. Don't force interaction when it would just slow things down.

---

### STEP 4 — Deliver the Explanation

Once the style and depth are confirmed (or defaulted), produce the explanation following the selected style's methodology.

#### Feynman Style Execution

1. Identify the core idea — what is the ONE thing this concept is about?
2. Explain it using only words a smart 12-year-old would know
3. Use analogies to ground abstract ideas in physical experience
4. When you must introduce a term, define it immediately in simple language
5. End by connecting back to why this matters

**Quality check**: Read your explanation. If any sentence requires domain expertise to parse, rewrite it.

#### Socratic Style Execution

1. Start with a question that activates what the learner already knows
2. Build a chain of questions where each answer leads logically to the next
3. Let the learner "discover" the concept through the question sequence
4. Only state the concept directly after the questions have laid the groundwork
5. Close with a question that tests whether the understanding is solid

**Quality check**: Could the learner arrive at the concept through these questions alone? If not, your questions aren't doing enough work.

#### Example-First Style Execution

1. Show a concrete example immediately — code, scenario, real-world case
2. Walk through what happens, step by step
3. Highlight the surprising or non-obvious part
4. Only now introduce the general principle or theory
5. Show a second example that reinforces the principle in a different context

**Quality check**: If you removed all the theory, would the examples alone teach the concept? They should get at least 70% of the way there.

#### Layered Style Execution

1. **Layer 0 — One sentence**: "X is [simple definition]."
2. **Layer 1 — The shape**: What is it, what problem does it solve, how does it relate to things the learner already knows? (1 paragraph)
3. **Layer 2 — How it works**: The mechanism, the key moving parts. (2-3 paragraphs)
4. **Layer 3 — Nuances**: Edge cases, trade-offs, common misconceptions, when NOT to use it. (2-3 paragraphs)
5. **Layer 4 — Connections**: How it relates to other concepts, where to go deeper. (1 paragraph)

The learner can stop at any layer and have a complete (if simplified) understanding. Each layer adds detail but never contradicts the previous layer.

**Quality check**: Read only Layer 0 and Layer 1. Is that a valid explanation? If not, your layers aren't self-contained.

#### Analogy Bridge Style Execution

1. State the analogy upfront: "X is like Y, because..."
2. Map the key components: "In X, [component A] plays the role of [component B] in Y"
3. Walk through the analogy in action: "When you [action in Y], it's like [action in X]"
4. **Explicitly state where the analogy breaks down**: "Unlike Y, X also [difference]..."
5. Transition from analogy to precise understanding

**Quality check**: Does the analogy hold for the core mechanism? Would it mislead the learner about any important property? If the analogy breaks in a way that creates a misconception, choose a different analogy or switch styles.

#### Visual-Spatial Style Execution

1. Describe or render the overall shape of the system ("Picture three boxes connected by arrows...")
2. Name each component and its responsibility
3. Walk through a scenario: what happens when [input] enters the system?
4. Highlight the boundaries, bottlenecks, and critical connections
5. If possible, provide an actual diagram (ASCII, Mermaid, or SVG)

**Quality check**: Could the learner draw the system from your explanation? If not, your spatial language isn't precise enough.

---

### STEP 5 — Verify Understanding

After delivering the explanation, offer exactly one of these based on the style used:

- **Feynman**: "Can you rephrase this in your own words? I'll tell you if anything is off."
- **Socratic**: "Based on what we explored — what would happen if [novel scenario]?"
- **Example-First**: "Want to try applying this to a different case?"
- **Layered**: "Want me to go one layer deeper, or is this the right level?"
- **Analogy Bridge**: "Does the analogy hold for your mental model, or is there a part that feels off?"
- **Visual-Spatial**: "Does the picture make sense? Want me to zoom into any component?"

This step is optional and should be offered naturally, not forced. If the user's response indicates they understood ("got it", "thanks", "makes sense"), don't push further.

---

## Calibration Rules

**1. Speed over ceremony.** If the topic is simple ("what is a REST API?"), don't go through the full analysis-recommend-confirm dance. Pick Example-First + Brief and deliver. Reserve the full interaction for genuinely complex or ambiguous topics.

**2. The user's explicit request overrides the recommendation.** If they say "ELI5", use Feynman + Brief. If they say "give me the deep technical details", use Layered + Deep Dive. If they say "walk me through it step by step", use Tutorial. Never argue with an explicit style preference.

**3. Analogies are powerful and dangerous.** A bad analogy is worse than no analogy because it creates a wrong mental model that's hard to dislodge. If you can't find an analogy that holds for the core mechanism, use a different style. Always state where analogies break down.

**4. Socratic style requires patience from the learner.** Before using Socratic, gauge whether the user has the patience for it. If they seem to want a quick answer, switch to Feynman or Example-First. Socratic works best when the user has explicitly asked to understand deeply or when you're correcting a misconception.

**5. Match precision to expertise.** If context suggests the learner is a domain expert, skip simplification and go straight to precise technical language at the appropriate verbosity. A staff engineer asking about CRDTs doesn't need the "imagine a shared Google Doc" analogy — they need the mathematical properties.

**6. End with the door open.** Every explanation should end with an implicit or explicit invitation to go deeper, ask follow-up questions, or explore a related concept. Learning is iterative, not one-shot.

---

## Thinking Triggers

- *"What does this topic LOOK LIKE in the learner's head right now? What should it look like after?"*
- *"What's the ONE thing — if they understood nothing else — that would be most valuable?"*
- *"Am I explaining what this IS, or why it MATTERS? The learner needs 'why' first."*
- *"Would an example do more work than three paragraphs of theory here?"*
- *"What misconception is most likely? Can I preempt it?"*
- *"If I used this analogy and nothing else, would the learner be misled or enlightened?"*
