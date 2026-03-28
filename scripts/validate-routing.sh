#!/usr/bin/env bash
#
# validate-routing.sh — Validate routing.yaml against actual skill files
#
# Checks:
#   1. Every skill listed in routing.yaml exists as a directory in skills/
#   2. Every skill in a group exists in the corresponding plugin directory
#   3. No edge references a skill that doesn't exist
#   4. No intra-group edge references a skill outside that group
#   5. Cross-group edges are correctly marked
#
# Requires: yq (https://github.com/mikefarah/yq)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROUTING="$REPO_ROOT/routing.yaml"
ERRORS=0

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow(){ printf '\033[0;33m%s\033[0m\n' "$*"; }

if ! command -v yq &>/dev/null; then
    red "ERROR: yq is required. Install with: brew install yq"
    exit 1
fi

echo "Validating routing.yaml..."
echo ""

# ── Check 1: All skills in groups exist as directories ──
echo "CHECK 1: Skills exist in skills/ directory"
for group in $(yq '.groups | keys | .[]' "$ROUTING"); do
    for skill in $(yq ".groups.$group.skills[]" "$ROUTING"); do
        if [[ ! -d "$REPO_ROOT/skills/$skill" ]]; then
            red "  MISSING: skills/$skill (listed in group '$group')"
            ERRORS=$((ERRORS + 1))
        fi
    done
done
if [[ $ERRORS -eq 0 ]]; then
    green "  OK: All skills exist in skills/"
fi

# ── Check 2: All skills in groups exist in plugin directories ──
PREV_ERRORS=$ERRORS
echo ""
echo "CHECK 2: Skills exist in plugin directories"
for group in $(yq '.groups | keys | .[]' "$ROUTING"); do
    plugin=$(yq ".groups.$group.plugin" "$ROUTING")
    for skill in $(yq ".groups.$group.skills[]" "$ROUTING"); do
        plugin_path="$REPO_ROOT/plugins/$plugin/skills/$skill"
        if [[ ! -d "$plugin_path" ]]; then
            red "  MISSING: plugins/$plugin/skills/$skill (listed in group '$group')"
            ERRORS=$((ERRORS + 1))
        fi
    done
done
if [[ $ERRORS -eq $PREV_ERRORS ]]; then
    green "  OK: All plugin skill directories exist"
fi

# ── Check 3: All edge references exist ──
PREV_ERRORS=$ERRORS
echo ""
echo "CHECK 3: Edge references point to existing skills"

# Collect all known skills
ALL_SKILLS=$(yq '.groups[].skills[]' "$ROUTING" | sort -u)

edge_count=$(yq '.edges | length' "$ROUTING")
for i in $(seq 0 $((edge_count - 1))); do
    from=$(yq ".edges[$i].from" "$ROUTING")
    to=$(yq ".edges[$i].to" "$ROUTING")

    if ! echo "$ALL_SKILLS" | grep -qx "$from"; then
        red "  UNKNOWN: edge[$i].from = '$from' not in any group"
        ERRORS=$((ERRORS + 1))
    fi
    if ! echo "$ALL_SKILLS" | grep -qx "$to"; then
        red "  UNKNOWN: edge[$i].to = '$to' not in any group"
        ERRORS=$((ERRORS + 1))
    fi
done
if [[ $ERRORS -eq $PREV_ERRORS ]]; then
    green "  OK: All edge references resolve"
fi

# ── Check 4: Cross-group edges are marked ──
PREV_ERRORS=$ERRORS
echo ""
echo "CHECK 4: Cross-group edges correctly marked"

# Build skill→group map as temp file (bash 3.2 compat — no associative arrays)
SKILL_GROUP_MAP=$(mktemp)
trap "rm -f $SKILL_GROUP_MAP" EXIT
for group in $(yq '.groups | keys | .[]' "$ROUTING"); do
    for skill in $(yq ".groups.$group.skills[]" "$ROUTING"); do
        echo "$skill=$group" >> "$SKILL_GROUP_MAP"
    done
done

lookup_group() {
    local skill="$1"
    grep "^${skill}=" "$SKILL_GROUP_MAP" | head -1 | cut -d= -f2
}

for i in $(seq 0 $((edge_count - 1))); do
    from=$(yq ".edges[$i].from" "$ROUTING")
    to=$(yq ".edges[$i].to" "$ROUTING")
    cross=$(yq ".edges[$i].cross_group // false" "$ROUTING")

    from_group=$(lookup_group "$from")
    to_group=$(lookup_group "$to")
    from_group="${from_group:-unknown}"
    to_group="${to_group:-unknown}"

    if [[ "$from_group" != "$to_group" && "$cross" != "true" ]]; then
        red "  UNMARKED: edge '$from' ($from_group) → '$to' ($to_group) crosses groups but cross_group is not true"
        ERRORS=$((ERRORS + 1))
    fi

    if [[ "$from_group" == "$to_group" && "$cross" == "true" ]]; then
        yellow "  WARN: edge '$from' → '$to' is marked cross_group but both are in '$from_group'"
    fi
done
if [[ $ERRORS -eq $PREV_ERRORS ]]; then
    green "  OK: Cross-group edges correctly marked"
fi

# ── Check 5: Chain steps reference existing skills ──
PREV_ERRORS=$ERRORS
echo ""
echo "CHECK 5: Chain steps reference existing skills"
for chain in $(yq '.chains | keys | .[]' "$ROUTING"); do
    for skill in $(yq ".chains.$chain.steps[]" "$ROUTING"); do
        if ! echo "$ALL_SKILLS" | grep -qx "$skill"; then
            red "  UNKNOWN: chain '$chain' references '$skill' which is not in any group"
            ERRORS=$((ERRORS + 1))
        fi
    done
done
if [[ $ERRORS -eq $PREV_ERRORS ]]; then
    green "  OK: All chain references resolve"
fi

# ── Check 6: Parallel set skills exist ──
PREV_ERRORS=$ERRORS
echo ""
echo "CHECK 6: Parallel set skills exist"
for pset in $(yq '.parallel_sets | keys | .[]' "$ROUTING"); do
    for skill in $(yq ".parallel_sets.$pset.skills[]" "$ROUTING"); do
        if ! echo "$ALL_SKILLS" | grep -qx "$skill"; then
            red "  UNKNOWN: parallel_set '$pset' references '$skill' which is not in any group"
            ERRORS=$((ERRORS + 1))
        fi
    done
done
if [[ $ERRORS -eq $PREV_ERRORS ]]; then
    green "  OK: All parallel set references resolve"
fi

# ── Summary ──
echo ""
echo "─────────────────────────────"
if [[ $ERRORS -eq 0 ]]; then
    green "PASS: All checks passed"
    exit 0
else
    red "FAIL: $ERRORS error(s) found"
    exit 1
fi
