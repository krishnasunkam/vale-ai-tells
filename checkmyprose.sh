#!/usr/bin/env bash
# checkmyprose.sh — your prose fingerprint, told back to you.
# Lints files with the AiTells Vale package and reveals what it found.
# Read-only: your prose never leaves your machine. Bash 3.2 compatible.
set -u

# ---------- palette (respects NO_COLOR and non-TTY) ----------
if [ -n "${NO_COLOR:-}" ] || [ "${TERM:-dumb}" = "dumb" ] || [ ! -t 1 ]; then
  C1=""; C2=""; C3=""; DIM=""; BOLD=""; RST=""; OK=""; ERR=""
else
  C1=$(printf '\033[38;5;117m')   # sky
  C2=$(printf '\033[38;5;183m')   # lilac
  C3=$(printf '\033[38;5;222m')   # gold
  DIM=$(printf '\033[2m'); BOLD=$(printf '\033[1m'); RST=$(printf '\033[0m')
  OK=$(printf '\033[38;5;114m'); ERR=$(printf '\033[38;5;210m')
fi

say() { printf '%s\n' "$1"; }

fail() {
  say ""
  say "   ${ERR}✗${RST} $1"
  say "     ${DIM}$2${RST}"
  say ""
  exit 1
}

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
CFG="$SCRIPT_DIR/.vale.ini"

say ""
say "   ${C2}╭─${RST} ${C3}✦${RST} ${BOLD}c h e c k m y p r o s e${RST}"
say "   ${C2}│${RST}  ${DIM}the tells of machine-written text, found in yours${RST}"
say "   ${C2}╰─────────────────────────────────────${RST}"
say ""

# ---------- preflight ----------
command -v vale >/dev/null || fail "vale is not installed" "macOS: brew install vale · other platforms: https://vale.sh"
command -v python3 >/dev/null || fail "python3 is not installed" "it ships with macOS; on Linux: apt/dnf install python3"
[ -f "$CFG" ] || fail "package config not found" "run this from the vale-ai-tells directory"

# ---------- targets ----------
if [ $# -ge 1 ]; then
  TARGETS="$@"
else
  TARGETS=$(find . -maxdepth 2 -name '*.md' ! -path './.git/*' ! -name 'README.md' ! -name 'CONTRIBUTING.md' 2>/dev/null | head -20)
  [ -n "$TARGETS" ] || fail "no markdown files found here" "pass a file or directory: ./checkmyprose.sh path/to/doc.md"
  say "   ${DIM}no target given — checking markdown found nearby${RST}"
fi

say "   ${DIM}reading your prose… (it stays on this machine)${RST}"
say ""

# ---------- lint + reveal ----------
vale --config "$CFG" --output=JSON $TARGETS 2>/dev/null | python3 "$SCRIPT_DIR/report.py"

STATUS=$?

say "   ${C2}╭─${RST} ${BOLD}what now${RST}"
say "   ${C2}│${RST}  ${DIM}see every finding    vale --config $CFG <file>${RST}"
say "   ${C2}│${RST}  ${DIM}what each rule means README.md — the rule table${RST}"
say "   ${C2}│${RST}  ${DIM}fix it in your voice recast flagged lines yourself —${RST}"
say "   ${C2}│${RST}  ${DIM}                     the tool marks, it never rewrites${RST}"
say "   ${C2}│${RST}"
say "   ${C2}│${RST}  ${C3}your prose never left your machine.${RST}"
say "   ${C2}╰─────────────────────────────────────${RST}"
say ""
exit $STATUS
