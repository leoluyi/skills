# Recover a Deleted Claude Conversation

This skill pulls a conversation, message, or generated artifact (docx/pdf) back out of the Chromium cache after it's been accidentally deleted from Claude Desktop or claude.ai. It is invoke-only — it never triggers on its own, you have to name it — and it is time-sensitive: the moment something is deleted, the underlying cache entry is a target for eviction, so treat this as a race and run it immediately rather than reading further first.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a recover-deleted-claude-conversation -y
```

To update later:

```
npx skills update recover-deleted-claude-conversation
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/recover-deleted-claude-conversation/SKILL.md)

Requires `uv` and `git` on the machine, plus shell access for the agent running it. It has no dependency on any particular AI assistant — it works on any agent with Bash/shell access (Claude Code, Codex, Cursor, etc.), because the whole procedure is just shell commands against a local cache directory.

## What it does

The Claude Desktop app (and claude.ai in a browser) is a Chromium shell that caches every HTTP response it receives, including full conversation bodies and generated files. Deleting a conversation in the UI removes it from the visible list but does not necessarily remove it from that cache. This skill:

1. Has you fully quit the Claude process so nothing can keep writing to (and evicting) the cache.
2. Copies the OS-specific Chromium blockfile cache directory (`Cache_Data` and its `index`/`data_*`/`f_*` files) to a separate backup location.
3. Sets up an isolated `uv` virtual environment with `ccl_chromium_reader` and the relevant decompression libraries (brotli, zstandard, plus stdlib gzip/zlib/zip).
4. Walks every cache entry in the snapshot, decompresses each HTTP body, and writes it out to an `extracted/` directory.
5. Greps the extracted files for the conversation's UUID (or a distinctive phrase) to find the recovered conversation or artifact.

## When to use

Invoke it by name the moment a conversation, message, or generated artifact was just deleted from Claude Desktop or claude.ai and you want it back. Because this is invoke-only, nothing happens unless you call it explicitly — but when you do, do it now, not after finishing other work, since every minute increases the chance the cache entry gets evicted.

## When not to

Don't reach for this for ordinary chat-history or export questions — it's not a general-purpose history browser. It also isn't the tool for generic cache-clearing questions that have nothing to do with recovering lost data. If nothing was actually deleted, there's nothing here to run.

## How it works

Chromium-based apps store HTTP responses in a "blockfile" cache: a fixed set of index and data files that get reused and overwritten as new responses come in. Nothing is deleted from disk the instant it disappears from the UI — the entry just becomes eligible to be overwritten the next time the cache needs the space. That's the entire reason speed matters: the cache doesn't wait for you, and once an entry's storage blocks get reused by something else, the original bytes are gone. Freezing the app first (so it can't write anything new) and snapshotting the cache before doing any exploration is what gives the extraction step something stable to work against. The blockfile framing is specific enough that a generic cache parser will misread it, which is why the skill relies on a library built for this exact format rather than parsing it by hand.

## Related skills

This is a standalone recovery tool. It doesn't depend on, and isn't a step in, any other skill in this repository.
