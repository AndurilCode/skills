# Craftwork — Agent Instructions

## What This Repo Is

A skill library for Claude Code and other agents. **52 skills** organized into 3 plugin groups (reasoning, context-engineering, professional), each with its own orchestrator. Skills are the primary artifact — everything else (plugins, routing, scripts) exists to distribute and compose them.

## Repo Layout

```
skills/{name}/SKILL.md          — canonical skill files (flat, for npx skills)
plugins/craftwork-{group}/skills/ — copies of skills grouped for Claude Code marketplace
routing.yaml                    — single source of truth for skill composition
scripts/validate-routing.sh     — validates routing.yaml (run after any change)
.claude-plugin/marketplace.json — marketplace metadata (versions, descriptions)
```

**Two copies of each skill exist**: one in `skills/` (canonical) and one in `plugins/craftwork-{group}/skills/`. When editing a skill, edit the canonical `skills/` version, then copy it to the appropriate plugin group directory. For skills that appear in `craftwork-all`, also copy there.

## Plugin Groups

| Group | Plugin dir | Orchestrator | Skill count |
|-------|-----------|-------------|-------------|
| reasoning | `plugins/craftwork-reasoning/` | `reasoning-orchestrator` | 22 |
| context-engineering | `plugins/craftwork-context-engineering/` | `context-engineering-orchestrator` | 12 |
| professional | `plugins/craftwork-professional/` | `professional-orchestrator` | 18 |
| all (bundle) | `plugins/craftwork-all/` | all 3 orchestrators | 52 |

**Scoping rule**: The reasoning-orchestrator in `craftwork-reasoning` only references reasoning skills. The version in `craftwork-all` references all 52 skills. This prevents orphan references when a user installs a single group.

## routing.yaml

The single source of truth for how skills compose. Contains:
- **groups**: which skills belong to which plugin group
- **edges**: directed `from → to` composition links with conditions and `cross_group` flags
- **chains**: named canonical sequences (e.g., `context-engineering-lifecycle`)
- **parallel_sets**: skills that can run concurrently

**After any change to routing.yaml**, run: `bash scripts/validate-routing.sh`

This checks: skills exist on disk, edges point to real skills, cross-group edges are marked, chains reference valid skills.

## How to Add a New Skill

1. Create `skills/{skill-name}/SKILL.md` with frontmatter (`name`, `description`)
2. Create `plugins/craftwork-{group}/skills/{skill-name}/SKILL.md` (copy)
3. Create `plugins/craftwork-all/skills/{skill-name}/SKILL.md` (copy)
4. Add the skill to the appropriate group in `routing.yaml`
5. Add any composition edges to `routing.yaml` (mark `cross_group: true` if it connects to a skill in another group)
6. Update the group's orchestrator SKILL.md with a routing entry for the new skill
7. Update the `craftwork-all` orchestrator if the skill should be routable from there
8. Run `bash scripts/validate-routing.sh` — must pass
9. Run `bash scripts/bump-version.sh {group}` — bumps the plugin version
10. Update `README.md`: skill count, table entry

## How to Edit an Existing Skill

1. Edit the canonical file at `skills/{skill-name}/SKILL.md`
2. Copy to `plugins/craftwork-{group}/skills/{skill-name}/SKILL.md`
3. Copy to `plugins/craftwork-all/skills/{skill-name}/SKILL.md`
4. If composition relationships changed, update `routing.yaml` and the relevant orchestrator(s)
5. Run `bash scripts/validate-routing.sh`
6. Run `bash scripts/bump-version.sh {group}` — bumps the version for the changed group (and `all`)

## How to Edit an Orchestrator

Orchestrators live at `skills/{name}-orchestrator/SKILL.md` (canonical) and are copied to plugin dirs. The `craftwork-reasoning` orchestrator has a **scoped** version (only reasoning skills) in its plugin dir and a **full** version in `craftwork-all`.

When editing the reasoning-orchestrator:
- Edit `skills/reasoning-orchestrator/SKILL.md` (full version, goes to craftwork-all)
- Edit `plugins/craftwork-reasoning/skills/reasoning-orchestrator/SKILL.md` separately (scoped version)
- These are NOT identical — the scoped version omits cross-group references

## Versioning

Plugin versions in `marketplace.json` use semver. The `bump-version.sh` script handles this:
- `bash scripts/bump-version.sh reasoning` — bumps `craftwork-reasoning` + `craftwork-all`
- `bash scripts/bump-version.sh context-engineering` — bumps `craftwork-context-engineering` + `craftwork-all`
- `bash scripts/bump-version.sh professional` — bumps `craftwork-professional` + `craftwork-all`
- `bash scripts/bump-version.sh all` — bumps all 4 plugins
- Default bump is patch. Pass `minor` or `major` as second arg: `bash scripts/bump-version.sh reasoning minor`

## Commit Conventions

- Skill changes: `Add/Update/Remove {skill-name} skill`
- Orchestrator changes: `Update {group} orchestrator routing`
- Routing changes: `Update routing.yaml: {what changed}`
- Infrastructure: `Update {script/config}: {what changed}`

## Things to Watch

- **Never reference a skill from another group** in a group-scoped orchestrator. The user may only have that one group installed.
- **Cross-group edges in routing.yaml** must have `cross_group: true`. The validator catches this.
- **Skill counts in README.md and marketplace.json** must match the actual directory counts. Verify after adding/removing skills.
- **The reasoning-orchestrator exists in two forms**: full (craftwork-all) and scoped (craftwork-reasoning). They must be edited separately.
