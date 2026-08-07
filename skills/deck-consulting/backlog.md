# deck-consulting backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md).

Closed items do not stay here — see `design-notes.md`, `evals/`, and commits.

## Open

- **Seven of the eight cases have one repetition each.** All eight now run with-skill against vanilla
  and the skill wins all eight, but only case 3 was repeated. A one-assertion margin on a
  single-repetition case cannot be separated from sampling noise — that applies to case 2, where
  vanilla's only loss was building a claim on a figure it derived rather than one the material
  contained. Worth a second rep on 2, 6 and 7 before treating those margins as real.

- **The remaining nodes have never been run in an eval.** The suite exercises `positioning`,
  `distill`, `headline`, `outline`, `storyline` and `slidecheck`. `onepager`, `opening`, `closing`,
  `delivery` and `layoutspec` have no case, so their entry checks, their soft-prerequisite paths and
  the shared-section discipline in `script.md` are untested. `closing` is the one to write first: it
  is the only node that reads a named subsection out of another node's section (`承諾清單` inside
  `開場`), which makes it the most likely place a lookup silently misses.

- **Nothing has ever exercised a real multi-node session.** Every case is a single turn against
  inlined artifacts; no run has actually written a file and had a later node read it back. The
  file-handoff contract — the thing the whole skill is built on — is therefore verified only by
  reading. A scripted two-node run (`positioning` then `opening`, on disk, in a scratch directory)
  would settle it, and would also be the only thing that can catch a section-name drift between two
  reference files.

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
