#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PLATFORM="codex"
PROJECT_ROOT=""
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: ./install.sh [--platform codex|claude|all] [--project PATH] [--dry-run]

Installs this checkout as a symlinked Agent Skill.

Options:
  --platform NAME  Install for codex, claude, or all (default: codex)
  --project PATH   Install at repository scope instead of user scope
  --dry-run        Print the planned operation without writing
  -h, --help       Show this help

User-scope destinations can be overridden with AGENTS_SKILLS_DIR and
CLAUDE_SKILLS_DIR. Existing non-symlink paths and unrelated symlinks are
never overwritten.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      if [[ $# -lt 2 ]]; then
        usage >&2
        exit 2
      fi
      PLATFORM="$2"
      shift 2
      ;;
    --project)
      if [[ $# -lt 2 || -z "$2" ]]; then
        usage >&2
        exit 2
      fi
      PROJECT_ROOT="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$PLATFORM" in
  codex|claude|all) ;;
  *)
    echo "ERROR: --platform must be codex, claude, or all" >&2
    exit 2
    ;;
esac

if [[ ! -f "$ROOT/SKILL.md" ]]; then
  echo "BLOCKED: repository root is missing SKILL.md: $ROOT" >&2
  exit 1
fi

if [[ -n "$PROJECT_ROOT" ]]; then
  if [[ ! -d "$PROJECT_ROOT" ]]; then
    echo "BLOCKED: project directory does not exist: $PROJECT_ROOT" >&2
    exit 1
  fi
  PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd -P)"
fi

platforms=()
targets=()

add_platform() {
  local platform="$1"
  local parent

  if [[ -n "$PROJECT_ROOT" ]]; then
    if [[ "$platform" == "codex" ]]; then
      parent="$PROJECT_ROOT/.agents/skills"
    else
      parent="$PROJECT_ROOT/.claude/skills"
    fi
  elif [[ "$platform" == "codex" ]]; then
    parent="${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"
  else
    parent="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
  fi

  platforms+=("$platform")
  targets+=("$parent/merge-when-awesome")
}

if [[ "$PLATFORM" == "codex" || "$PLATFORM" == "all" ]]; then
  add_platform codex
fi
if [[ "$PLATFORM" == "claude" || "$PLATFORM" == "all" ]]; then
  add_platform claude
fi

# Preflight every destination before creating any directory or symlink.
for target in "${targets[@]}"; do
  case "$target" in
    /*) ;;
    *)
      echo "BLOCKED: destination must be absolute: $target" >&2
      exit 1
      ;;
  esac

  if [[ -L "$target" ]]; then
    if [[ "$target" -ef "$ROOT" ]]; then
      continue
    fi
    echo "BLOCKED: refusing to replace unrelated symlink: $target" >&2
    exit 1
  fi
  if [[ -e "$target" ]]; then
    echo "BLOCKED: refusing to overwrite non-symlink path: $target" >&2
    exit 1
  fi

  parent="$(dirname "$target")"
  ancestor="$parent"
  while [[ ! -e "$ancestor" && ! -L "$ancestor" ]]; do
    previous="$ancestor"
    ancestor="$(dirname "$ancestor")"
    if [[ "$ancestor" == "$previous" ]]; then
      break
    fi
  done
  if [[ ! -d "$ancestor" ]]; then
    echo "BLOCKED: destination parent is not a directory: $ancestor" >&2
    exit 1
  fi
done

for index in "${!targets[@]}"; do
  platform="${platforms[$index]}"
  target="${targets[$index]}"
  parent="$(dirname "$target")"

  if [[ -L "$target" && "$target" -ef "$ROOT" ]]; then
    echo "PASS: $platform already points to $ROOT"
    continue
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    printf 'DRY RUN: mkdir -p %q\n' "$parent"
    printf 'DRY RUN: ln -s %q %q\n' "$ROOT" "$target"
    continue
  fi

  mkdir -p "$parent"
  ln -s "$ROOT" "$target"
  echo "PASS: installed for $platform at $target"
done

if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete. No files were changed."
else
  echo "Installation complete. Start a new agent session before first use."
fi
