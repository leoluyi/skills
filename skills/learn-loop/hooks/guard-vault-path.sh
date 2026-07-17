#!/usr/bin/env bash
# guard-vault-path.sh — Claude Code PreToolUse guard for the `learn-loop` skill.
#
# Denies a Write/Edit of a learning-note-shaped file that would land OUTSIDE the
# learn vault (or the temp outbox). It targets exactly one failure mode: the
# cross-tool CWD confusion `learn-loop` warns about, where a capture note titled
# `learning - <concept>` gets written to the current directory instead of VAULT.
#
# Design: FAIL-OPEN. On any uncertainty — no jq, unparseable payload, missing
# fields, a relative path with no cwd — it ALLOWS the write. It only ever denies
# when it is certain: a `learning - *` file resolving outside every sanctioned
# root. A guard that runs on every Write/Edit must never brick normal editing.
#
# This is a Claude-Code-only layer. The `learn-loop` skill itself stays tool-portable;
# this hook is optional determinism for the one tool that supports hooks.
# Registration + rationale: see the sibling README.md.

set -u

allow() { exit 0; }   # emit nothing, exit 0 => Claude Code proceeds normally

# jq parses the hook payload safely. No jq => cannot judge => allow.
command -v jq >/dev/null 2>&1 || allow

payload="$(cat)" || allow
[ -n "$payload" ] || allow

file_path="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty' 2>/dev/null)" || allow
cwd="$(printf '%s' "$payload" | jq -r '.cwd // empty' 2>/dev/null)"
[ -n "$file_path" ] || allow

base="$(basename -- "$file_path")"

# Is this a `learn-loop` capture note? Step 1 titles it `learning - <concept>`. That
# prefix is the fingerprint; normal code edits never match it. No match => the
# guard has no opinion.
case "$base" in
  "learning - "*) ;;
  *) allow ;;
esac

# Resolve to an absolute path. cwd is supplied in the hook payload.
abs="$file_path"
case "$abs" in
  "~/"*) abs="$HOME/${abs#\~/}" ;;
esac
case "$abs" in
  /*) ;;                                              # already absolute
  *) [ -n "$cwd" ] && abs="$cwd/$abs" || allow ;;     # relative w/o cwd => cannot judge
esac

# Sanctioned roots. LEARN_VAULT mirrors the skill's own VAULT resolution order.
VAULT="${LEARN_VAULT:-/Users/leoluyi/Library/CloudStorage/Dropbox/__notes-vault}"
OUTBOX="$HOME/learn-loop-outbox"

case "$abs" in
  "$VAULT"/*|"$OUTBOX"/*) allow ;;                    # inside a sanctioned root => fine
esac

# Certain: a learn note heading outside the vault. Deny with an actionable reason.
reason="guard-vault-path：「${base}」要寫到 ${abs}，不在 learn vault（${VAULT}）或 outbox（${OUTBOX}）底下。learn 一律用 VAULT 絕對路徑，這通常是 CWD 混淆。若這不是 learn 寫入，讓檔名別以 'learning - ' 開頭即可放行。"

jq -cn --arg r "$reason" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: $r
  }
}'
exit 0
