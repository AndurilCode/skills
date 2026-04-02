---
name: kintsugi
description: "Apply kintsugi (金継ぎ) repair visibility philosophy to any codebase — finding invisible repairs and making them legible with 'gold' context. Triggers on '/kintsugi', 'kintsugi this codebase', 'repair visibility audit', 'are our fixes documented?', 'why was this changed?', 'undocumented fixes', 'invisible patches', 'git archaeology', 'missing context on past fixes', 'why does this workaround exist?', or any request to understand or document the history behind code changes. Also trigger when someone asks 'why is this code like this?', 'what incident caused this?', 'who knows why we do it this way?', or when tribal knowledge about past repairs is at risk of being lost. This skill audits the history layer of a codebase — not what the code does today, but whether past breaks and repairs are visible and legible to future developers."
---

# Kintsugi (金継ぎ) — Codebase Repair Visibility

Every bugfix, workaround, hotfix, and defensive pattern has a story. When tible, the codebase loses institutional memory and future developers repeat past mistakes. The **gold** is context — comments, ADRs, test annotations, and documentation that make past repairs legible.

---

## Input Modes

### Standard: `/kintsugi`
Scan full codebase and recent git history for invisible repairs. Produce a gilding backlog.

### Focused: `/kintsugi "focus description"`
Scope the scan. Examples: `"auth module"`, `"last 3 months of hotfixes"`, `"defensive null checks"`, `"dependency pins"`.

When focused: lead with focus findings, mark others `[ALSO NOTED]`, still scan all scar types.

---

## The Scar Taxonomy

Scars are past repairs. Each either has **gold** (context explaining why) or is **bare** (repair exists, story is lost).

| Scar type | Detection signal |
|---|---|
| **Workaround** | Code avoiding a known issue without explaining which issue |
| **Defensive guard** | Null check, try/catch, retry not in original design, no comment on what fails |
| **Magic value** | Hardcoded timeout, try count, batch size, threshold without rationale |
| **Regression test** | Test exists because something broke, but name/description doesn't reference what |
| **Dependency pin** | Version pin without comment explaining what breaks if upgraded |
| **Reverted pattern** | Code redone differently with no trace of why the previous approach failed |
| **Silent migration** | Compatibility shim handling "old format" without migration explanation |
| **Config override** | Non-default value without explaining why the default doesn't work |

---

## Five Dimensions — Execute in Order

### D1 — Scar Discovery (傷の発見)

**Vector A — Git archaeology**: Scan commit messages for repair keywords:
`fix`, `bugfix`, `hotfix`, `patch`, `workaround`, `revert`, `rollback`, `handle edge case`, `prevent`, `guard against`, `fallback`, `retry`, `defensive`, `incident`, `postmortem`, `outage`, `regression`

Per repair commit: `SCAR [sha] [date] | Message: [...] | Files: [...] | Gold: [yes/no]`

**Vector B — Code pattesource for each scar type from the taxonomy table above.

**Output**: `SCAR INVENTORY — Total: [N] (git: [N], code: [N], lookback: [period])`

---

### D2 — Gold Audit (金の監査)

Grade each scar's visibility:

| Level | Meaning |
|---|---|
| 🥇 **Full gold** | Why documented, linked to ticket/incident, immediately understandable |
| 🥈 **Partial gold** | Some context but incomplete — "fix for prod issue" with no specifics |
| ⬜ **Bare scar** | Story completely invisible |

Per scar:
```
[SCAR] [type]
📍 [file:line or commit]
Visibility: [🥇 | 🥈 | ⬜]
Story: [reconstructed from git context — state confidence and evidence]
Missing gold: [what context is absent]
```

---

### D3 — Gilding Backlog (金継ぎバックログ)

**Primary deliverable.** Prioritize bare and partial-gold scars.

**Scoring** (each 1–3):
- **Blast radius**: Shared utility=3, isolated file=1
- **Decay risk**: Author left=3, still on team=1
- **Confusion potential**: Looks like dead code=3, obviously defens

**Gold types to apply**:

| Gold type | Example |
|---|---|
| Inline comment | `// Retry 3x: Service Y cold-start up to 30s (#1234)` |
| Block comment | `/* WORKAROUND: API returns stale cache ~5min after deploy... */` |
| Test annotation | Rename test + description linking to original bug |
| ADR | `docs/adr/003-sync-vs-async-payments.md` |
| Pin comment | `// Pinned: v3.0 breaks SSO callback, see #5678` |
| CHANGELOG entry | Date + explanation of significant past fix |

```
金継ぎ GILDING BACKLOG
#  Score  Type            Scar                           Gold to apply
1  3.0    Inline comment  Bare retry payments.ts:89      Add incident context
2  2.7    Pin comment     Lodash pinned 4.17.21          Explain breaking change
...
```

**Cap at 10 items.** Each implementable in a single small PR.

---

### D4 — Kintsugi Health Score (金継ぎ健康スコア)

```
KINTSUGI HEALTH
Total scars: [N]  |  🥇 [N] ([%])  |  🥈 [N] ([%])  |  ⬜ [N] ([%])
Health score: [% with full or partial gold]  Target:ntion Compass (予防の羅針盤)

Each rated `🟢 In place | 🟡 Partial | 🔴 Missing`:

```
COMMIT HYGIENE:  [Message standards enforced? Template/hook?]
FIX TEMPLATES:   [PR template prompts "what broke and why"?]
INCIDENT LINKS:  [Postmortem learnings linked back to code?]
TEST NAMING:     [Test names carry story of what they prevent?]
PIN DISCIPLINE:  [Convention for commenting dependency pins?]
```

---

## Report Assembly

1. **Header**: Codebase, focus or "Full scan", date, git lookback
2. **Health Score** (D4) — headline
3. **Gilding Backlog** (D3) — hero section
4. **Scar Inventory** (D1) — counts by type
5. **Detailed findings** (D2) — bare scars with reconstruction, grouped by type
6. **Prevention Compass** (D5)

*"金継ぎの心: 傷は隠すものではなく、金で照らすもの。"*

---

## Calibration Rules

1. **Gold, not noise**: `// fix` is not gold. Gold carries the *why*. Low-context comments are bare scars disguised as gold.
2. **Reconstruct honestly**: State confideunsupported claims.
3. **Don't gild the obvious**: A try/catch around file I/O needs no explanation. Gild only where the *reason for this specific pattern* is non-obvious.
4. **Prioritize by decay risk**: Author left recently → urgent. Stable team with shared knowledge → can wait.
5. **One PR, one scar**: Don't bundle unrelated context additions.
6. **Git lookback**: Default 6 months unless user specifies otherwise.
7. **Never change behavior**: Gold is *always documentation*. Never modify logic, refactor, or change tests.
