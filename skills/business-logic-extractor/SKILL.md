---
name: business-logic-extractor
description: "Extract and document business logic, domain models, and product rules from a codebase into a structured llms.txt-style reference. Use this skill whenever someone asks to 'document the business logic', 'extract domain rules', 'what are the business rules in this codebase', 'map the domain model', 'document product behavior', 'what does this system actually do', 'reverse-engineer the business rules', 'create a domain reference', 'what are the invariants', 'how does pricing work in this codebase', 'what validations exist', 'document entity relationships', or any request to make implicit product knowledge explicit from code. Also trigger when an agent or developer is onboarding to a codebase and needs to understand what the system does (not how it's built). This is the context engineer's domain knowledge extraction tool — it turns code into a product behavior reference."
---

# Business Logic Extractor

**What this produces**: A single, structured Markdown document that captures the *product and domain knowledge* embedded in a codebase — the entities, their relationships, the business rules that govern them, and the invariants that must hold. Same llms.txt format (H2 sections, annotated code, token-budgeted) but focused on *what the system does* rather than *how to use its APIs*.

**Why this matters**: Business logic is the most expensive context to lose. It lives scattered across models, validators, services, tests, and config files. When it's implicit, every new developer (or agent) has to re-derive it from code. This skill makes it explicit.

**Key difference from llms-txt-generator**: That skill documents a library's *public API surface* from its docs. This skill documents a codebase's *product behavior* from its source code. The input is code, not documentation. The sections are domain concepts, not API topics.

---

## Execution

This skill operates on the current codebase only. The agent must have filesystem access to the project being analyzed.

**Pre-flight check**: Confirm you can see the codebase root. Look for a manifest file (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `*.csproj`) to orient yourself. If you can't find one, ask the user to confirm the project root.

---

## PHASE 1 — Domain Surface Scan

Map the codebase to find where business logic lives. Not all code carries domain knowledge — focus on the high-signal locations.

### High-signal locations (scan these first)

| What to look for | Why it matters | Typical paths |
|---|---|---|
| **ORM models / schemas** | Define entities, fields, relationships, constraints | `models/`, `entities/`, `schema/`, `prisma/schema.prisma`, `**/models.py`, `**/*Entity.java` |
| **Validation logic** | Encodes business rules as code | `validators/`, `rules/`, `guards/`, `**/validate*`, `**/*.guard.ts` |
| **Service / use-case layer** | Orchestrates business operations | `services/`, `usecases/`, `domain/`, `**/service*`, `**/*Service.*` |
| **Tests (especially integration)** | Tests assert expected behavior — they're a goldmine | `test/`, `spec/`, `__tests__/`, `**/test_*`, `**/*.spec.*` |
| **Constants and config** | Thresholds, limits, feature flags, pricing tiers | `constants/`, `config/`, `**/*constants*`, `**/*config*`, `.env.example` |
| **Enums and status types** | Lifecycle states, categories, permission levels | `types/`, `enums/`, `**/status*`, `**/state*` |
| **Migration files** | Schema evolution reveals domain model decisions | `migrations/`, `db/migrate/`, `alembic/versions/` |
| **API route handlers / controllers** | The verbs of the system — what operations exist | `routes/`, `controllers/`, `api/`, `app/api/` |
| **Middleware / interceptors** | Cross-cutting business rules (auth, rate limits, tenant isolation) | `middleware/`, `interceptors/`, `pipes/` |

### Scan procedure

```bash
# 1. Find the tech stack
cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || cat go.mod 2>/dev/null || cat Cargo.toml 2>/dev/null

# 2. Find model/entity files
find . -type f \( -name "*.model.*" -o -name "*.entity.*" -o -name "*.schema.*" \
  -o -name "models.py" -o -name "schema.prisma" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" | head -50

# 3. Find business logic layers
find . -type f \( -name "*.service.*" -o -name "*.usecase.*" -o -name "*.rule.*" \
  -o -name "*.validator.*" -o -name "*.guard.*" -o -name "*.policy.*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" | head -50

# 4. Find test files (prioritize integration/e2e)
find . -type f \( -name "*.spec.*" -o -name "*.test.*" -o -name "test_*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" | head -50

# 5. Find constants, enums, config
find . -type f \( -name "*constant*" -o -name "*enum*" -o -name "*config*" \
  -o -name "*status*" -o -name "*types*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" | head -50
```

Read the files you find. Build a mental inventory of what domain concepts exist before proceeding.

**Output of Phase 1**: A file inventory organized by signal type, plus a first-pass list of domain entities and operations you've spotted.

---

## PHASE 2 — Domain Model Extraction

From the files discovered in Phase 1, identify and document the domain model.

### What to extract

For each **entity** (model, aggregate, value object):

1. **Name and purpose**: What real-world concept does this represent?
2. **Fields and their semantics**: Not just `status: string` — what are the valid values, what do they mean?
3. **Relationships**: How does this entity connect to others? (belongs to, has many, references)
4. **Invariants**: What must always be true? Look for:
   - Database constraints (unique, not null, foreign keys, check constraints)
   - Validation rules applied before persistence
   - Business rules in setters or lifecycle hooks
   - Test assertions that check "this should never happen"
5. **Lifecycle**: Does this entity have states? What transitions are allowed? (look for status enums, state machines, workflow logic)

### Where invariants hide

Invariants are rarely labeled as such. Look for them in:

- **Model validations**: `@IsNotEmpty()`, `validates :email, presence: true`, Zod/Yup schemas
- **Database constraints**: `NOT NULL`, `UNIQUE`, `CHECK`, foreign key cascades
- **Guard clauses**: `if (!user.isActive) throw ...`, early returns in service methods
- **Test assertions**: `expect(order.total).toBeGreaterThan(0)` — this IS a business rule
- **Comments with "must" or "should"**: Developers annotate invariants informally
- **Migration files**: `ALTER TABLE ... ADD CONSTRAINT` reveals rules added after initial design

### How to document entities

For each entity, produce a section following this format:

```markdown
## {Entity Name}

{1-3 sentences: what this entity represents in the business domain, its core purpose, and its most important invariant or lifecycle characteristic.}

```{language}
// Key fields with business-relevant annotations
// Relationships indicated by comments
// Invariants and constraints called out explicitly

// Example: from the actual codebase, annotated
type Order = {
  id: string
  userId: string                    // belongs to User
  status: OrderStatus               // lifecycle: draft → confirmed → shipped → delivered | cancelled
  items: OrderItem[]                // has many OrderItems, min 1
  total: number                     // invariant: must equal sum of items × prices, must be > 0
  currency: Currency                // set at creation, immutable after
  createdAt: Date
  confirmedAt: Date | null          // set when status transitions to 'confirmed'
}

// Valid status transitions (from state machine or service logic)
// draft → confirmed (requires: items.length > 0, total > 0)
// confirmed → shipped (requires: payment.status === 'captured')
// confirmed → cancelled (allowed within 24h of confirmation)
// shipped → delivered (external trigger from logistics)
```
```

---

## PHASE 3 — Business Rule Extraction

Business rules are the behavioral constraints that go beyond the data model. They answer: "Under what conditions can X happen?"

### What qualifies as a business rule

- **Validation rules**: Input constraints beyond type safety (min length, format, allowed values, cross-field dependencies)
- **Authorization rules**: Who can do what, under what conditions (role checks, ownership checks, time-based access)
- **Calculation rules**: How derived values are computed (pricing formulas, tax calculations, discount logic, scoring algorithms)
- **Eligibility rules**: Conditions that must be met before an operation (can this user place an order? can this item be returned?)
- **Rate limits and thresholds**: Maximum orders per day, minimum balance for withdrawal, cooling-off periods
- **Side effects and triggers**: When X happens, Y must also happen (send email on signup, create audit log on deletion, sync to external system)

### Where business rules hide

- **Service methods**: The if/else chains in `createOrder()`, `processRefund()`, `upgradeSubscription()` are business rules
- **Middleware/guards**: Authentication and authorization logic
- **Validators**: Input schemas with business constraints (not just type validation)
- **Test descriptions**: `it('should not allow checkout with empty cart')` — the test name IS the rule
- **Constants files**: `MAX_ITEMS_PER_ORDER = 50`, `REFUND_WINDOW_DAYS = 30`
- **Config/feature flags**: `ENABLE_LOYALTY_DISCOUNT`, `MIN_ORDER_AMOUNT`
- **Error messages**: `'Cannot cancel order after shipment'` — the error string states the rule

### How to document business rules

Group related rules by domain operation or concept. Each section covers one operation or rule cluster:

```markdown
## {Operation / Rule Cluster Name}

{1-3 sentences: what business operation this covers and why these rules exist.}

```{language}
// Extracted and annotated from the actual codebase
// Each rule is called out with a comment explaining the business reason

async function processRefund(orderId: string, reason: string) {
  const order = await getOrder(orderId)

  // Rule: can only refund completed orders
  if (order.status !== 'delivered') throw new Error('Order not eligible')

  // Rule: refund window is 30 days from delivery
  const daysSinceDelivery = daysBetween(order.deliveredAt, now())
  if (daysSinceDelivery > REFUND_WINDOW_DAYS) throw new Error('Refund window expired')

  // Rule: refund amount cannot exceed original total
  const refundAmount = Math.min(requestedAmount, order.total)

  // Rule: refunds over €500 require manager approval
  if (refundAmount > 500) {
    await requestManagerApproval(orderId, refundAmount)
    return { status: 'pending_approval' }
  }

  // Side effect: trigger payment provider reversal
  await paymentProvider.refund(order.paymentId, refundAmount)

  // Side effect: update inventory (restock)
  await restockItems(order.items)
}
```
```

### Extraction technique: read tests first

Tests are the single best source of business rules because they state behavior as assertions. Read test files and extract rules by pattern:

| Test pattern | Extracted rule |
|---|---|
| `it('should reject orders with 0 items')` | Order must have ≥1 item |
| `it('should apply 10% discount for premium users')` | Premium users get 10% discount |
| `it('should not allow cancellation after shipping')` | Cancellation blocked after shipment |
| `expect(user.loginAttempts).toBeLessThan(5)` | Account locks after 5 failed logins |

After extracting rules from tests, cross-reference with the service/model code to confirm and add implementation detail.

---

## PHASE 4 — Assembly

Combine domain model and business rule sections into the final document.

### Document structure

```markdown
# {Project Name} — Domain & Business Logic Reference

{2-3 sentence overview: what this system does as a product, who uses it, and what the core domain is.}

## Domain Model

### {Entity 1}
{fields, relationships, invariants, lifecycle}

### {Entity 2}
...

## Business Rules

### {Rule Cluster 1}
{rules + annotated code}

### {Rule Cluster 2}
...

## Summary

{1-2 paragraphs: how the domain entities and business rules compose into the system's actual product behavior. Key workflows, critical invariants that span multiple entities, and the most important "gotchas" a developer or agent would need to know.}
```

**Note on heading structure**: This skill uses a two-level hierarchy — `## Domain Model` and `## Business Rules` as top-level groupings, with `###` for individual entities and rule clusters. This differs from the library llms.txt format (flat H2s) because domain knowledge has natural grouping that aids RAG retrieval. A query about "order validation" should retrieve the Order entity AND the order-related business rules — the grouping headers help retrievers do this.

### Assembly rules

1. The H1 includes the project name and the qualifier "Domain & Business Logic Reference" to distinguish from API references.
2. Entity sections come before business rule sections — you need to understand the nouns before the verbs.
3. Order entities by centrality: the core domain entity first (e.g., `Order` in an e-commerce system), then entities that relate to it, then supporting entities.
4. Order business rules by frequency: the most commonly triggered operations first, edge cases last.
5. Cross-reference between sections using entity names — if a business rule references an entity, use the same name as in the domain model section.
6. The Summary ties domain model and rules together: "Orders go through these states, governed by these rules, interacting with these entities."

### Token budget

Same approach as llms-txt-generator:
- Overview: ~200 tokens
- Domain model: ~40% of remaining budget
- Business rules: ~50% of remaining budget
- Summary: ~200 tokens
- Default total: 10K tokens. Use 5K for small codebases, 15-20K for complex domains.

---

## PHASE 5 — Output

### File naming

- Default: `{project-name}.business-logic.md`
- Alternative: `{project-name}.domain.md`
- If user specifies a name: use it

### Save location

- If in a codebase: save to repo root or `docs/`
- Always copy to `/mnt/user-data/outputs/` for download

---

## Quality Checklist

Before saving, verify:

- [ ] Every entity section includes: purpose, key fields with semantics, relationships, and at least one invariant
- [ ] Every business rule is stated as a plain-English condition, not just code
- [ ] Code examples are from the actual codebase, annotated — not synthetic examples
- [ ] Lifecycle/state transitions are documented for entities that have them
- [ ] Rules extracted from tests are cross-referenced with implementation code
- [ ] The document answers "what does this system do" not "how is it built"
- [ ] No framework/infrastructure details unless they encode business rules (e.g., a Prisma `@unique` IS a business rule)
- [ ] Summary connects entities and rules into coherent product behavior
- [ ] Cross-references between entities and rules use consistent naming

---

## Edge Cases

- **No tests**: Lean harder on service layer code, validation files, and constants. Warn the user that confidence in extracted rules is lower without test coverage.
- **Anemic domain model**: If models are just data bags and all logic is in services, document the services as the primary source of truth and note the architecture pattern.
- **Microservices / distributed**: Focus on the current service's bounded context. Document integration contracts (what this service expects from others) as a separate section if relevant.
- **Heavy ORM magic**: If the ORM hides business logic (ActiveRecord callbacks, Hibernate lifecycle hooks, Prisma middleware), explicitly surface these — they're invisible business rules.
- **Feature flags**: Document the behavior under each flag state. Feature flags ARE business rules — they control which logic executes.
- **Legacy codebase with no clear structure**: Scan all files, look for the densest clusters of conditionals and validation. Follow the money — trace the core transaction flow (e.g., "what happens when a user pays?") and document what you find along the way.
