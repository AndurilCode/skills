# Craftwork

50 agent skills for reasoning, context engineering, and professional work. Works with Claude Code, Cursor, Codex, and [40+ agents](https://github.com/vercel-labs/skills#available-agents).

## Install

```bash
# All skills (any agent)
npx skills add gpavanello/skills

# List available skills first
npx skills add gpavanello/skills --list

# Specific skills only
npx skills add gpavanello/skills --skill reasoning-orchestrator --skill agent-instruction-forge

# Specific agent only
npx skills add gpavanello/skills -a claude-code
```

### Claude Code Plugin (selective install by category)

```bash
# Add the marketplace
/plugin marketplace add https://github.com/gpavanello/skills

# Install by category
/plugin install reasoning@craftwork              # 22 thinking frameworks
/plugin install context-engineering@craftwork     # 11 context/agent tools
/plugin install professional@craftwork            # 17 architecture/communication skills
/plugin install all@craftwork              # everything
```

---

## Plugins

### reasoning (22 skills)

Thinking frameworks for analysis, decisions, and problem-solving.

| Category | Skills |
|----------|--------|
| **Understand the System** | [systems-thinking](plugins/reasoning/skills/system-thinking/SKILL.md), [first-principles-thinking](plugins/reasoning/skills/first-principles-thinking/SKILL.md), [cynefin-framework](plugins/reasoning/skills/cynefin-framework/SKILL.md), [epistemic-mapping](plugins/reasoning/skills/epistemic-mapping/SKILL.md) |
| **Find What's Broken** | [theory-of-constraints](plugins/reasoning/skills/theory-of-constraints/SKILL.md), [five-whys-root-cause](plugins/reasoning/skills/five-whys-root-cause/SKILL.md), [causal-inference](plugins/reasoning/skills/casual-inference/SKILL.md), [cognitive-bias-detection](plugins/reasoning/skills/cognitive-bias-detection/SKILL.md) |
| **Stress-Test** | [inversion-premortem](plugins/reasoning/skills/inversion-premortem/SKILL.md), [red-teaming](plugins/reasoning/skills/red-teaming/SKILL.md), [second-order-thinking](plugins/reasoning/skills/second-order-thinking/SKILL.md) |
| **Navigate Uncertainty** | [probabilistic-thinking](plugins/reasoning/skills/probabilistic-thinking/SKILL.md), [fermi-estimation](plugins/reasoning/skills/fermi-estimation/SKILL.md), [scenario-planning](plugins/reasoning/skills/scenario-planning/SKILL.md), [game-theoretic-analysis](plugins/reasoning/skills/game-theoretic-analysis/SKILL.md) |
| **Generate Options** | [lateral-thinking](plugins/reasoning/skills/lateral-thinking/SKILL.md), [analogical-thinking](plugins/reasoning/skills/analogical-thinking/SKILL.md), [bisociative-creativity](plugins/reasoning/skills/bisociative-creativity/SKILL.md) |
| **Decide** | [decision-synthesis](plugins/reasoning/skills/decision-synthesis/SKILL.md), [decision-intelligence](plugins/reasoning/skills/decision-intelligence/SKILL.md), [retrospective-counterfactual](plugins/reasoning/skills/retrospective-counterfactual/SKILL.md), [evidence-synthesis](plugins/reasoning/skills/evidence-synthesis/SKILL.md) |
| **Orchestrate** | [reasoning-orchestrator](plugins/reasoning/skills/reasoning-orchestrator/SKILL.md) — entry point, triages and routes to the right framework |

### context-engineering (11 skills)

Build, evaluate, and debug agent context — instructions, harnesses, evals, and documentation.

| Skill | Purpose |
|-------|---------|
| [agent-instruction-forge](plugins/context-engineering/skills/agent-instruction-forge/SKILL.md) | Create instruction rules for coding agents (CLAUDE.md, AGENTS.md, .cursorrules) |
| [rule-quality-evaluator](plugins/context-engineering/skills/rule-quality-evaluator/SKILL.md) | Score instruction rules on Seven Properties, detect redundancies, test behaviorally |
| [context-cartography](plugins/context-engineering/skills/context-cartography/SKILL.md) | Design what goes into an agent's context window |
| [context-gap-analyzer](plugins/context-engineering/skills/context-gap-analyzer/SKILL.md) | Find implicit context missing from a codebase |
| [context-debugging](plugins/context-engineering/skills/context-debugging/SKILL.md) | Diagnose agent failures that originate in the context layer |
| [context-eval](plugins/context-engineering/skills/context-eval/SKILL.md) | Measure whether a context harness actually improves outcomes |
| [edd](plugins/context-engineering/skills/edd/SKILL.md) | Eval-Driven Development — TDD for context, not code |
| [llms-txt-generator](plugins/context-engineering/skills/llms-txt-generator/SKILL.md) | Generate token-efficient context documents for LLM consumption |
| [deep-document-processor](plugins/context-engineering/skills/deep-document-processor/SKILL.md) | Multi-pass reading to extract decision-relevant context from large documents |
| [business-logic-extractor](plugins/context-engineering/skills/business-logic-extractor/SKILL.md) | Extract domain rules and business logic from code into structured references |
| [test-challenger](plugins/context-engineering/skills/test-challenger/SKILL.md) | Find false positives in AI-generated tests |

### professional (17 skills)

Architecture, code quality, process design, communication, and leadership.

| Skill | Purpose |
|-------|---------|
| [architecture-evaluation](plugins/professional/skills/architecture-evaluation/SKILL.md) | Evaluate system design decisions and produce ADRs |
| [code-review-amplifier](plugins/professional/skills/code-review-amplifier/SKILL.md) | Amplify human code reviewers with structured pre-scanning |
| [debugging-methodology](plugins/professional/skills/debugging-methodology/SKILL.md) | Systematic debugging: reproduce, observe, hypothesize, isolate |
| [execution-planning](plugins/professional/skills/execution-planning/SKILL.md) | Decompose decisions into executable plans with dependencies |
| [experimental-design](plugins/professional/skills/experimental-design/SKILL.md) | Design rigorous experiments to validate assumptions |
| [process-design](plugins/professional/skills/process-design/SKILL.md) | Design or redesign workflows using Lean and value stream analysis |
| [financial-modeling](plugins/professional/skills/financial-modeling/SKILL.md) | Unit economics, cost-benefit analysis, NPV/IRR, scenario modeling |
| [argument-craft](plugins/professional/skills/argument-craft/SKILL.md) | Structure recommendations into persuasive arguments |
| [narrative-construction](plugins/professional/skills/narrative-construction/SKILL.md) | Turn analysis into compelling stories |
| [negotiation-strategy](plugins/professional/skills/negotiation-strategy/SKILL.md) | Prepare for negotiations with BATNA, ZOPA, and concession planning |
| [difficult-conversations](plugins/professional/skills/difficult-conversations/SKILL.md) | Navigate conflict, feedback, and emotionally charged discussions |
| [facilitation-design](plugins/professional/skills/facilitation-design/SKILL.md) | Design meetings and workshops that produce decisions |
| [stakeholder-power-mapping](plugins/professional/skills/stakeholder-power-mapping/SKILL.md) | Map influence networks and design engagement strategies |
| [ethical-reasoning](plugins/professional/skills/ethical-reasoning/SKILL.md) | Surface moral implications using multiple ethical frameworks |
| [fairness-auditing](plugins/professional/skills/fairness-auditing/SKILL.md) | Audit systems for equitable outcomes across groups |
| [learning-strategy](plugins/professional/skills/learning-strategy/SKILL.md) | Build structured plans for closing knowledge gaps |
| [casual-inference](plugins/professional/skills/casual-inference/SKILL.md) | Distinguish causation from correlation in metrics and experiments |

---

## Chaining Skills

Skills compose. Common sequences:

**Evaluating something** — Cynefin → Systems Thinking → Theory of Constraints → 5 Whys → Causal Inference

**Validating a plan** — Epistemic Mapping → First Principles → Inversion/Pre-mortem → Second-Order → Decision Synthesis

**High-stakes decision** — Scenario Planning → Probabilistic Thinking → Fermi Estimation → Red Teaming → Decision Synthesis

**Stuck with no options** — Epistemic Mapping → Lateral Thinking → Analogical Thinking → First Principles

**After something goes wrong** — Retrospective/Counterfactual → 5 Whys → Epistemic Mapping → Decision Synthesis

**Full context engineering lifecycle** — Context Gap Analyzer → Agent Instruction Forge → Rule Quality Evaluator → Context Eval → EDD

**Creating agent instructions** — Context Gap Analyzer (audit) → Agent Instruction Forge (create) → Rule Quality Evaluator (score) → EDD (validate)

---

## Structure

```
skills/                        # flat — npx skills discovers these
├── reasoning-orchestrator/
├── first-principles-thinking/
├── agent-instruction-forge/
├── context-eval/
├── ...50 skills total
│   └── SKILL.md

plugins/                       # Claude Code marketplace overlay (symlinks)
├── reasoning/          → 22 skills
├── context-engineering/ → 11 skills
├── professional/       → 17 skills
└── all/                → 50 skills

.claude-plugin/
└── marketplace.json           # craftwork marketplace
```

Skills live flat at root for `npx skills` compatibility. The `plugins/` directory contains symlinks grouped by category for the Claude Code marketplace.

---

## License

MIT
