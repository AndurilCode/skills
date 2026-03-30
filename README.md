# Craftwork

58 agent skills for reasoning, context engineering, and professional work. Works with Claude Code, Cursor, Codex, and [40+ agents](https://github.com/vercel-labs/skills#available-agents).

## Install

```bash
# All skills (any agent)
npx skills add AndurilCode/craftwork

# List available skills first
npx skills add AndurilCode/craftwork --list

# Specific skills only
npx skills add AndurilCode/craftwork --skill reasoning-orchestrator --skill agent-instruction-forge

# Specific agent only
npx skills add AndurilCode/craftwork -a claude-code
```

### Claude Code Plugin (selective install by category)

```bash
# Add the marketplace
/plugin marketplace add https://github.com/AndurilCode/craftwork

# Install by category
/plugin install craftwork-reasoning@craftwork              # 23 thinking frameworks (includes orchestrator)
/plugin install craftwork-context-engineering@craftwork     # 12 context/agent tools (includes orchestrator)
/plugin install craftwork-professional@craftwork            # 23 architecture/communication skills (includes orchestrator)
/plugin install craftwork-all@craftwork                     # everything (58 skills)
```

---

## Plugins

### reasoning (23 skills)

Thinking frameworks for analysis, decisions, and problem-solving. Includes its own orchestrator for guided routing.

| Category | Skills |
|----------|--------|
| **Understand the System** | [systems-thinking](plugins/craftwork-reasoning/skills/system-thinking/SKILL.md), [first-principles-thinking](plugins/craftwork-reasoning/skills/first-principles-thinking/SKILL.md), [cynefin-framework](plugins/craftwork-reasoning/skills/cynefin-framework/SKILL.md), [epistemic-mapping](plugins/craftwork-reasoning/skills/epistemic-mapping/SKILL.md) |
| **Find What's Broken** | [theory-of-constraints](plugins/craftwork-reasoning/skills/theory-of-constraints/SKILL.md), [five-whys-root-cause](plugins/craftwork-reasoning/skills/five-whys-root-cause/SKILL.md), [causal-inference](plugins/craftwork-reasoning/skills/casual-inference/SKILL.md), [cognitive-bias-detection](plugins/craftwork-reasoning/skills/cognitive-bias-detection/SKILL.md) |
| **Stress-Test** | [inversion-premortem](plugins/craftwork-reasoning/skills/inversion-premortem/SKILL.md), [red-teaming](plugins/craftwork-reasoning/skills/red-teaming/SKILL.md), [second-order-thinking](plugins/craftwork-reasoning/skills/second-order-thinking/SKILL.md), [limit-thinking](plugins/craftwork-reasoning/skills/limit-thinking/SKILL.md) |
| **Navigate Uncertainty** | [probabilistic-thinking](plugins/craftwork-reasoning/skills/probabilistic-thinking/SKILL.md), [fermi-estimation](plugins/craftwork-reasoning/skills/fermi-estimation/SKILL.md), [scenario-planning](plugins/craftwork-reasoning/skills/scenario-planning/SKILL.md), [game-theoretic-analysis](plugins/craftwork-reasoning/skills/game-theoretic-analysis/SKILL.md) |
| **Generate Options** | [lateral-thinking](plugins/craftwork-reasoning/skills/lateral-thinking/SKILL.md), [analogical-thinking](plugins/craftwork-reasoning/skills/analogical-thinking/SKILL.md), [bisociative-creativity](plugins/craftwork-reasoning/skills/bisociative-creativity/SKILL.md) |
| **Decide** | [decision-synthesis](plugins/craftwork-reasoning/skills/decision-synthesis/SKILL.md), [decision-intelligence](plugins/craftwork-reasoning/skills/decision-intelligence/SKILL.md), [retrospective-counterfactual](plugins/craftwork-reasoning/skills/retrospective-counterfactual/SKILL.md), [evidence-synthesis](plugins/craftwork-reasoning/skills/evidence-synthesis/SKILL.md) |
| **Orchestrate** | [reasoning-orchestrator](plugins/craftwork-reasoning/skills/reasoning-orchestrator/SKILL.md) — entry point, triages and routes to the right framework |

### context-engineering (12 skills)

Build, evaluate, and debug agent context — instructions, harnesses, evals, and documentation. Includes its own orchestrator for guided routing.

| Skill | Purpose |
|-------|---------|
| [agent-instruction-forge](plugins/craftwork-context-engineering/skills/agent-instruction-forge/SKILL.md) | Create instruction rules for coding agents (CLAUDE.md, AGENTS.md, .cursorrules) |
| [rule-quality-evaluator](plugins/craftwork-context-engineering/skills/rule-quality-evaluator/SKILL.md) | Score instruction rules on Seven Properties, detect redundancies, test behaviorally |
| [context-cartography](plugins/craftwork-context-engineering/skills/context-cartography/SKILL.md) | Design what goes into an agent's context window |
| [context-gap-analyzer](plugins/craftwork-context-engineering/skills/context-gap-analyzer/SKILL.md) | Find implicit context missing from a codebase |
| [context-debugging](plugins/craftwork-context-engineering/skills/context-debugging/SKILL.md) | Diagnose agent failures that originate in the context layer |
| [context-eval](plugins/craftwork-context-engineering/skills/context-eval/SKILL.md) | Measure whether a context harness actually improves outcomes |
| [edd](plugins/craftwork-context-engineering/skills/edd/SKILL.md) | Eval-Driven Development — TDD for context, not code |
| [llms-txt-generator](plugins/craftwork-context-engineering/skills/llms-txt-generator/SKILL.md) | Generate token-efficient context documents for LLM consumption |
| [deep-document-processor](plugins/craftwork-context-engineering/skills/deep-document-processor/SKILL.md) | Multi-pass reading to extract decision-relevant context from large documents |
| [business-logic-extractor](plugins/craftwork-context-engineering/skills/business-logic-extractor/SKILL.md) | Extract domain rules and business logic from code into structured references |
| [test-challenger](plugins/craftwork-context-engineering/skills/test-challenger/SKILL.md) | Find false positives in AI-generated tests |
| **Orchestrate** | [context-engineering-orchestrator](plugins/craftwork-context-engineering/skills/context-engineering-orchestrator/SKILL.md) — entry point, routes to the right context skill |

### professional (23 skills)

Architecture, code quality, process design, communication, and leadership. Includes its own orchestrator for guided routing.

| Skill | Purpose |
|-------|---------|
| [architecture-evaluation](plugins/craftwork-professional/skills/architecture-evaluation/SKILL.md) | Evaluate system design decisions and produce ADRs |
| [code-review-amplifier](plugins/craftwork-professional/skills/code-review-amplifier/SKILL.md) | Amplify human code reviewers with structured pre-scanning |
| [debugging-methodology](plugins/craftwork-professional/skills/debugging-methodology/SKILL.md) | Systematic debugging: reproduce, observe, hypothesize, isolate |
| [execution-planning](plugins/craftwork-professional/skills/execution-planning/SKILL.md) | Decompose decisions into executable plans with dependencies |
| [experimental-design](plugins/craftwork-professional/skills/experimental-design/SKILL.md) | Design rigorous experiments to validate assumptions |
| [process-design](plugins/craftwork-professional/skills/process-design/SKILL.md) | Design or redesign workflows using Lean and value stream analysis |
| [financial-modeling](plugins/craftwork-professional/skills/financial-modeling/SKILL.md) | Unit economics, cost-benefit analysis, NPV/IRR, scenario modeling |
| [argument-craft](plugins/craftwork-professional/skills/argument-craft/SKILL.md) | Structure recommendations into persuasive arguments |
| [narrative-construction](plugins/craftwork-professional/skills/narrative-construction/SKILL.md) | Turn analysis into compelling stories |
| [negotiation-strategy](plugins/craftwork-professional/skills/negotiation-strategy/SKILL.md) | Prepare for negotiations with BATNA, ZOPA, and concession planning |
| [difficult-conversations](plugins/craftwork-professional/skills/difficult-conversations/SKILL.md) | Navigate conflict, feedback, and emotionally charged discussions |
| [facilitation-design](plugins/craftwork-professional/skills/facilitation-design/SKILL.md) | Design meetings and workshops that produce decisions |
| [stakeholder-power-mapping](plugins/craftwork-professional/skills/stakeholder-power-mapping/SKILL.md) | Map influence networks and design engagement strategies |
| [ethical-reasoning](plugins/craftwork-professional/skills/ethical-reasoning/SKILL.md) | Surface moral implications using multiple ethical frameworks |
| [fairness-auditing](plugins/craftwork-professional/skills/fairness-auditing/SKILL.md) | Audit systems for equitable outcomes across groups |
| [learning-strategy](plugins/craftwork-professional/skills/learning-strategy/SKILL.md) | Build structured plans for closing knowledge gaps |
| [casual-inference](plugins/craftwork-professional/skills/casual-inference/SKILL.md) | Distinguish causation from correlation in metrics and experiments |
| [technical-writing](plugins/craftwork-professional/skills/technical-writing/SKILL.md) | Write RFCs, design docs, ADRs, runbooks, postmortems, one-pagers, announcements |
| [topic-explainer](plugins/craftwork-professional/skills/topic-explainer/SKILL.md) | Explain concepts, technologies, or ideas using the best style for the topic |
| [summarizer](plugins/craftwork-professional/skills/summarizer/SKILL.md) | Summarize documents, articles, transcripts, or multi-source content |
| [presentation-craft](plugins/craftwork-professional/skills/presentation-craft/SKILL.md) | Create presentation scripts with narrative arc, slide visuals, and speaker notes |
| [knowledge-architect](plugins/craftwork-professional/skills/knowledge-architect/SKILL.md) | Capture decisions, context, and learnings; design team knowledge systems |
| **Orchestrate** | [professional-orchestrator](plugins/craftwork-professional/skills/professional-orchestrator/SKILL.md) — entry point, routes to the right professional skill |

---

## Chaining Skills

Skills compose. Common sequences:

**Evaluating something** — Cynefin → Systems Thinking → Theory of Constraints → 5 Whys → Causal Inference

**Validating a plan** — Epistemic Mapping → First Principles → Inversion/Pre-mortem → Second-Order → Decision Synthesis

**High-stakes decision** — Scenario Planning → Probabilistic Thinking → Fermi Estimation → Red Teaming → Decision Synthesis

**Stuck with no options** — Epistemic Mapping → Lateral Thinking → Analogical Thinking → First Principles

**Scaling decision** — Limit Thinking → Second-Order Thinking → Scenario Planning → Decision Synthesis

**After something goes wrong** — Retrospective/Counterfactual → 5 Whys → Epistemic Mapping → Decision Synthesis

**Full context engineering lifecycle** — Context Gap Analyzer → Agent Instruction Forge → Rule Quality Evaluator → Context Eval → EDD

**Creating agent instructions** — Context Gap Analyzer (audit) → Agent Instruction Forge (create) → Rule Quality Evaluator (score) → EDD (validate)

**Architecture decision** — Architecture Evaluation → Argument Craft → Execution Planning

**Navigating organizational resistance** — Stakeholder Power Mapping → Negotiation Strategy → Difficult Conversations

**Building a business case** — Financial Modeling → Argument Craft → Execution Planning

Each plugin group has its own orchestrator that routes within its skills. When multiple groups are installed, cross-group chains are documented in `routing.yaml`.

---

## Structure

```
skills/                        # flat — npx skills discovers these
├── reasoning-orchestrator/
├── context-engineering-orchestrator/
├── professional-orchestrator/
├── first-principles-thinking/
├── agent-instruction-forge/
├── context-eval/
├── ...58 skills total
│   └── SKILL.md

plugins/                       # Claude Code marketplace plugins
├── craftwork-reasoning/          → 23 skills (includes orchestrator)
├── craftwork-context-engineering/ → 12 skills (includes orchestrator)
├── craftwork-professional/       → 23 skills (includes orchestrator)
└── craftwork-all/                → 58 skills (all orchestrators)

routing.yaml                   # single source of truth for skill composition
scripts/validate-routing.sh    # validates routing.yaml against actual skills

.claude-plugin/
└── marketplace.json           # craftwork marketplace
```

Skills live flat at root for `npx skills` compatibility. The `plugins/` directory groups skills by category for the Claude Code marketplace.

---

## License

MIT
