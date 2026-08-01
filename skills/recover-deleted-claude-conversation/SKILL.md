---
name: recover-deleted-claude-conversation
app-name: recover-deleted-conversations
description: >-
  Recover a conversation, message, or generated artifact (docx/pdf) accidentally
  deleted from Claude Desktop or claude.ai, by extracting it from the Chromium
  blockfile cache before it's evicted. Manual trigger only — invoke by name
  when a Claude conversation was just deleted and needs to be pulled back out
  of cache; this is a race against cache eviction, so run it immediately.
app-description: 當 Claude Desktop 或 claude.ai 上的對話、訊息或產出的檔案（docx/pdf）被誤刪時，從 Chromium 瀏覽器快取中搶救回來，須在快取被覆蓋前立即執行。僅限使用者明確要求時手動呼叫，不自動觸發。
disable-model-invocation: true
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant with Bash/shell access (Claude Code, Codex, Cursor, etc.). Requires uv and git on the user's machine.
metadata:
  author: Lu Yi
  tags: recovery cache chromium claude-desktop data-loss forensics
  agentskills_spec: "1.0"
---

# Recover a deleted Claude conversation

The Claude Desktop app (and claude.ai in a browser) is a Chromium shell that aggressively caches every response it receives, including full conversation bodies and generated artifacts. A conversation deleted in the UI still exists as compressed HTTP bodies in that Chromium blockfile cache — until the cache evicts it. This is a **race**: every step below exists to win it, so freeze the source before doing anything else, including reading the rest of this file twice.

## 1. Freeze the source

Fully quit the Claude Desktop app — File -> Exit / Menu -> Quit, not the window's close button — then confirm no Claude process remains (`ps aux | grep -i claude` on macOS/Linux, Task Manager on Windows). Check twice. A running process can still write to the cache and evict the very entry you're trying to save.

Done when: the process list shows zero Claude matches, on two consecutive checks.

## 2. Snapshot the cache before touching anything else

Locate the OS-specific cache directory:

| OS | Path |
|---|---|
| Windows | `%APPDATA%\Claude\Cache\Cache_Data\` |
| macOS | `~/Library/Application Support/Claude/Cache/Cache_Data/` |
| Linux | `~/.config/Claude/Cache/Cache_Data/` |

Copy `index`, `data_0` through `data_3`, and the `f_*` files (filter by today's date to cut noise) to a separate backup directory. Never run extraction against the live cache directory — every later step operates on the **snapshot**, never the original.

If the conversation was lost on claude.ai in a browser instead of the Desktop app, the same recipe applies: fully close the browser first, then snapshot that browser's own `Cache_Data` directory. Same blockfile format; harder to search since other site traffic shares the cache.

Done when: the backup directory's file list matches the source directory's (same names, same byte sizes).

## 3. Prepare the extraction environment, isolated

Do this inside the backup directory, in a throwaway environment — never touch the system Python or any other project's environment:

```
uv venv
uv pip install brotli zstandard
uv pip install ccl_chromium_reader
```

`gzip`/`zlib`/`zipfile` are stdlib and need no install; blockfile bodies show up compressed in brotli, zstd, gzip, deflate, or zip.

If `ccl_chromium_reader` isn't on PyPI, clone it to a scratch path *outside* the venv and install from that local path — still into this same venv, never system-wide:

```
git clone https://github.com/cclgroupltd/ccl_chromium_reader.git /path/to/scratch/ccl_chromium_reader
uv pip install /path/to/scratch/ccl_chromium_reader
```

Done when: `uv run python -c "import ccl_chromium_reader.ccl_chromium_cache"` runs without error, inside this one venv.

## 4. Walk the cache and extract every entry

Use the `ccl_chromium_cache` module specifically — not a generic Chromium-cache parser — because the blockfile format has its own framing around compressed bodies that a generic parser will mis-decode. Walk every entry in the snapshot, decompress each HTTP body, and write it to its own file under a new `extracted/` subdirectory. On a decompression failure for one entry, log it and continue — don't let one bad entry abort the walk.

Done when: every entry in the cache index has a corresponding file under `extracted/` — exhaustive, not a sample.

## 5. Find the conversation

Grep `extracted/` for the conversation's UUID, or another distinctive phrase from it if the UUID isn't known. The conversation itself is whichever response body has a URL containing `/chat_conversations/<uuid>`. Generated artifacts (docx/pdf) surface as their own separate files in `extracted/` — check for them by filename and content type, not just by grepping the UUID.

Done when: either a match is found and confirmed to contain the expected conversation content, or the full `extracted/` set (already exhaustive from step 4) has been searched and the match is confirmed absent — say so plainly rather than suggesting more searching would help.

## Why this isn't guaranteed

Cache is not backup: eviction can happen at any time, and older entries get overwritten first. The odds are best when steps 1-2 happen within minutes of the deletion. If the snapshot in step 2 already shows the relevant `f_*`/`data_*` files are gone or truncated, say so — don't spend the user's time on steps 3-5 chasing data that already isn't there.
