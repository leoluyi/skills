# learn — Claude Code hooks

Optional, **Claude-Code-only** guardrails for the `learn` skill. The skill in
`../SKILL.md` stays tool-portable (Claude Code, Codex, …); these hooks add
deterministic enforcement for the one tool that supports them. Nothing here is
required for the skill to work — a machine without them just loses the guard.

## guard-vault-path.sh

`PreToolUse(Write|Edit)` guard. Denies a `learning - *` note that would be
written outside the learn vault or `~/learn-outbox` — the CWD-confusion failure
`learn` warns about. Fail-open: it only denies when certain, and allows on any
uncertainty, so it never blocks normal editing.

### Register (Claude Code)

Hooks only take effect from a loaded settings source. At user scope that is
`~/.claude/settings.json` (NOT `settings.local.json` — the user-level `.local`
variant is not read). Add:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'S=\"$HOME/.skills/skills/learn/hooks/guard-vault-path.sh\"; [ -f \"$S\" ] && exec bash \"$S\" || exit 0'"
          }
        ]
      }
    ]
  }
}
```

The `[ -f "$S" ]` wrapper keeps it a no-op on any machine that has the settings
but not this repo cloned. Override the vault root with `LEARN_VAULT` if it
differs from the skill's default.
