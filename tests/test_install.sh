#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
TEST_TMP_BASE="${TMPDIR:-/tmp}"
TEST_TMP_BASE="${TEST_TMP_BASE%/}"
TEST_ROOT="$(mktemp -d "$TEST_TMP_BASE/merge-when-awesome-test.XXXXXX")"

cleanup() {
  case "$TEST_ROOT" in
    "$TEST_TMP_BASE"/merge-when-awesome-test.*)
      rm -rf -- "$TEST_ROOT"
      ;;
    *)
      echo "WARNING: refusing to remove unexpected test path: $TEST_ROOT" >&2
      ;;
  esac
}
trap cleanup EXIT

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

user_agents="$TEST_ROOT/user-agents"
user_claude="$TEST_ROOT/user-claude"

AGENTS_SKILLS_DIR="$user_agents" \
CLAUDE_SKILLS_DIR="$user_claude" \
  "$ROOT/install.sh" --platform all

[[ -L "$user_agents/merge-when-awesome" ]] || fail "Codex user symlink missing"
[[ -L "$user_claude/merge-when-awesome" ]] || fail "Claude user symlink missing"
[[ "$user_agents/merge-when-awesome" -ef "$ROOT" ]] || fail "Codex symlink points elsewhere"
[[ "$user_claude/merge-when-awesome" -ef "$ROOT" ]] || fail "Claude symlink points elsewhere"

AGENTS_SKILLS_DIR="$user_agents" \
CLAUDE_SKILLS_DIR="$user_claude" \
  "$ROOT/install.sh" --platform all >/dev/null

dry_agents="$TEST_ROOT/dry-agents"
dry_claude="$TEST_ROOT/dry-claude"
AGENTS_SKILLS_DIR="$dry_agents" \
CLAUDE_SKILLS_DIR="$dry_claude" \
  "$ROOT/install.sh" --platform all --dry-run >/dev/null
[[ ! -e "$dry_agents" ]] || fail "dry run created Codex destination"
[[ ! -e "$dry_claude" ]] || fail "dry run created Claude destination"

conflict_agents="$TEST_ROOT/conflict-agents"
conflict_claude="$TEST_ROOT/conflict-claude"
mkdir -p "$conflict_agents/merge-when-awesome"
if AGENTS_SKILLS_DIR="$conflict_agents" \
  CLAUDE_SKILLS_DIR="$conflict_claude" \
  "$ROOT/install.sh" --platform all >/dev/null 2>&1; then
  fail "installer overwrote a non-symlink conflict"
fi
[[ ! -e "$conflict_claude" ]] || fail "preflight allowed a partial all-platform install"

parent_conflict_agents="$TEST_ROOT/parent-conflict-agents"
parent_conflict_claude="$TEST_ROOT/parent-conflict-claude"
touch "$parent_conflict_claude"
if AGENTS_SKILLS_DIR="$parent_conflict_agents" \
  CLAUDE_SKILLS_DIR="$parent_conflict_claude" \
  "$ROOT/install.sh" --platform all >/dev/null 2>&1; then
  fail "installer accepted a non-directory destination parent"
fi
[[ ! -e "$parent_conflict_agents" ]] || fail "parent preflight allowed a partial all-platform install"

project="$TEST_ROOT/project"
mkdir -p "$project"
"$ROOT/install.sh" --platform all --project "$project" >/dev/null
[[ "$project/.agents/skills/merge-when-awesome" -ef "$ROOT" ]] || fail "Codex project install failed"
[[ "$project/.claude/skills/merge-when-awesome" -ef "$ROOT" ]] || fail "Claude project install failed"

echo "Installer integration tests passed"
