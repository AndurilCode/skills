#!/usr/bin/env bash
#
# bump-version.sh — Bump plugin versions in marketplace.json
#
# Usage:
#   bash scripts/bump-version.sh <group> [major|minor|patch]
#
# Examples:
#   bash scripts/bump-version.sh reasoning          # patch bump reasoning + all
#   bash scripts/bump-version.sh context-engineering minor  # minor bump context-engineering + all
#   bash scripts/bump-version.sh all                # patch bump all 4 plugins
#
# Always bumps craftwork-all alongside the target group.
# Requires: jq

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MARKETPLACE="$REPO_ROOT/.claude-plugin/marketplace.json"

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }

if ! command -v jq &>/dev/null; then
    red "ERROR: jq is required. Install with: brew install jq"
    exit 1
fi

if [[ $# -lt 1 ]]; then
    red "Usage: $0 <group> [major|minor|patch]"
    red "  group: reasoning | context-engineering | professional | all"
    echo ""
    echo "Current versions:"
    jq -r '.plugins[] | "  \(.name): \(.version)"' "$MARKETPLACE"
    exit 1
fi

GROUP="$1"
BUMP="${2:-patch}"

if [[ "$BUMP" != "major" && "$BUMP" != "minor" && "$BUMP" != "patch" ]]; then
    red "ERROR: bump type must be major, minor, or patch (got: $BUMP)"
    exit 1
fi

bump_semver() {
    local version="$1"
    local type="$2"
    local major minor patch
    IFS='.' read -r major minor patch <<< "$version"

    case "$type" in
        major) echo "$((major + 1)).0.0" ;;
        minor) echo "${major}.$((minor + 1)).0" ;;
        patch) echo "${major}.${minor}.$((patch + 1))" ;;
    esac
}

bump_plugin() {
    local plugin_name="$1"
    local old_version new_version

    old_version=$(jq -r ".plugins[] | select(.name == \"$plugin_name\") | .version" "$MARKETPLACE")
    if [[ -z "$old_version" || "$old_version" == "null" ]]; then
        red "  ERROR: plugin '$plugin_name' not found in marketplace.json"
        return 1
    fi

    new_version=$(bump_semver "$old_version" "$BUMP")

    # Use jq to update in place
    local tmp=$(mktemp)
    jq "(.plugins[] | select(.name == \"$plugin_name\") | .version) = \"$new_version\"" "$MARKETPLACE" > "$tmp"
    mv "$tmp" "$MARKETPLACE"

    echo "  $plugin_name: $old_version → $new_version"
}

# Determine which plugins to bump
case "$GROUP" in
    reasoning)
        PLUGINS=("craftwork-reasoning" "craftwork-all")
        ;;
    context-engineering)
        PLUGINS=("craftwork-context-engineering" "craftwork-all")
        ;;
    professional)
        PLUGINS=("craftwork-professional" "craftwork-all")
        ;;
    all)
        PLUGINS=("craftwork-reasoning" "craftwork-context-engineering" "craftwork-professional" "craftwork-all")
        ;;
    *)
        red "ERROR: unknown group '$GROUP'"
        red "  Valid groups: reasoning | context-engineering | professional | all"
        exit 1
        ;;
esac

echo "Bumping $BUMP version for: ${PLUGINS[*]}"
echo ""

for plugin in "${PLUGINS[@]}"; do
    bump_plugin "$plugin"
done

echo ""
green "Done. Updated marketplace.json:"
jq -r '.plugins[] | "  \(.name): \(.version)"' "$MARKETPLACE"
