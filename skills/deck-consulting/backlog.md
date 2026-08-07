# deck-consulting backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md).

Closed items do not stay here — see `design-notes.md`, `evals/`, and commits.

## Open

- **The first eval round covered four of the seven cases, once each.** Cases 1, 3, 4 and 5 ran
  with-skill against vanilla and the skill won all four; cases 2, 6 and 7 — the navigation-page
  boundary, the injection probe, and the zh-request-over-English-source language case — have not
  been run at all, and no configuration was repeated, so a narrow margin cannot be separated from
  sampling noise. See the iteration log in `design-notes.md`. The next round should close the three
  unrun cases first, then repeat the narrow one (case 3).

- **Nothing exercises an English-language session.** `trigger-queries.json` treats an English request
  as in scope and `SKILL.md` now states that artifact file and section names stay Chinese while their
  contents follow the request. That rule has never been run. A case with an English prompt, asserting
  which language each side of that split comes out in, would settle whether the exemption reads
  clearly enough to be obeyed.

- **Three eval expectations measure conformance rather than reader outcome.** `one-named-starting-point`
  (case 1), `says-where-it-wrote` (case 1) and `viewing-condition-settled` (case 5) each restate an
  instruction from `SKILL.md` or a reference rather than something the reader gets. They were kept
  because each has a real user consequence behind it — a session that starts nowhere, an artifact the
  user cannot find, a review whose findings silently depend on an unstated assumption — but the
  phrasing should be rewritten to name that consequence instead of the instruction.

- **`layoutspec` cannot verify its own output.** The node produces a layout spec and an image prompt,
  and neither harness has an image tool, so nothing checks that the spec is buildable or that the
  prompt produces a usable plate. The reference is explicit that no image is generated, which keeps
  the user's expectations right, but it leaves the node's actual quality unmeasured — the spec could
  be internally inconsistent (a reading order that contradicts the visual ranking, a reserved empty
  region that the element list would fill) and nothing in the loop would catch it. Options are a
  self-consistency checklist inside the node, or accepting it as a documented limit.

- **`onepager` writing into `outline.md` may be the wrong call.** It appends a `單頁濃縮` section to
  the outline's file deliberately, so a structural change leaves the compression visibly stale next
  to it. The cost is that a user who wants only the one-pager — a real entry case, since that page
  gets forwarded on its own — has to extract it from a file that also holds the full structure, and
  any tooling that reads artifacts by filename cannot address it. Decide after the first sessions
  that actually go through this node, not before.

- **The eleven-node table may be too wide a menu for a first-time user.** When the invocation names
  no node and describes no problem, `SKILL.md` says to show the table and ask. Eleven rows of
  unfamiliar node names is a plausible way to lose someone whose actual question was 「我的簡報
  怎麼救」. The mitigation already in place is one line saying `positioning` is where this normally
  starts; whether that is enough, or whether the fallback should offer three common entry points and
  keep the full table behind a follow-up, is an open question for the first eval round to look at.
