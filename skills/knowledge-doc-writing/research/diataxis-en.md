# Diátaxis — Core Concepts and Practical Examples

> Diátaxis derives four kinds of documentation from two axes of craft, and gives you a compass to decide which one you are writing at any moment.
>
> Source: <https://diataxis.fr/> (whole site, by Daniele Procida). Content confirmed as of 2026-07.

---

## 1. The one idea

Diátaxis derives four documentation types from two axes of *craft*, not from a list of genres. A practitioner's relationship to a skill has two independent dimensions:

- **Action vs cognition** — knowing *how* (what we do) vs knowing *that* (what we think).
- **Acquisition vs application** — being at study vs being at work.

Because the map has exactly two dimensions, it has exactly four quadrants. The number four isn't arbitrary and there is no fifth type, because there is no territory left to cover.

| | Tutorial | How-to guide | Reference | Explanation |
|---|---|---|---|---|
| Serves the need for | learning | goals | information | understanding |
| Answers | "Can you teach me to…?" | "How do I…?" | "What is…?" | "Why…?" |
| What it does | introduce, educate, lead | guide | state, describe, inform | explain, clarify, discuss |
| Form | a lesson | a series of steps | dry description | discursive discussion |
| Cooking analogy | teaching a child to cook | a recipe | back of a food packet | *On Food and Cooking* |

Each type has one job, and that job is defined by contrast with the other three.

---

## 2. The tool you actually use: the compass

The map is reference material; the compass is what you use at your desk. It reduces the two-dimensional problem to two questions: *action or cognition?* and *acquisition or application?*

| If the content informs… | …and serves the user's… | …then it is |
|---|---|---|
| action | acquisition of skill | a tutorial |
| action | application of skill | a how-to guide |
| cognition | application of skill | reference |
| cognition | acquisition of skill | explanation |

Use the compass flexibly — *action* means practical steps and doing, *cognition* means thinking, *acquisition* means study, *application* means work. It is most useful when intuition gives you a confident answer but something still feels wrong; it forces you to stop and recheck. Apply it at any zoom level: a whole document, a section, or a single sentence.

---

## 3. Type by type: principles, anti-patterns, language

### 3.1 Tutorial — learning-oriented

A tutorial is a lesson: a practical activity in which the learner acquires skill by doing, under guidance. Its purpose is not to get a job done but to build competence and confidence.

The first rule of teaching is: **don't try to teach**. Your job is to provide an experience through which learning can happen, not to transmit knowledge by telling.

**Principles**

- **Show where they're going.** Say "in this tutorial we will create and deploy a scalable web application". Do *not* say "in this tutorial you will learn…" — that's presumptuous and a poor pattern.
- **Deliver visible results early and often.** Every step should produce a comprehensible result, however small.
- **Maintain a narrative of the expected.** "After a few moments, the server responds with…" Show actual expected output. Flag likely failure signs in advance.
- **Point out what to notice.** Learners are too focused on doing to observe; close the learning loop for them (e.g. how the shell prompt changes).
- **Target the feeling of doing.** Tie purpose and action together so skill becomes rhythm and pleasure.
- **Encourage repetition.** Learners repeat steps just to confirm the same thing really happens again. Make that possible.
- **Ruthlessly minimise explanation.** One line ("we use HTTPS because it's safer") plus a link. Explanation is only relevant at the moment the *user* wants it — that's not the author's call.
- **Focus on the concrete.** Learning moves from the particular to the general; the general will emerge on its own.
- **Ignore options and alternatives.** Stay on the single path to the conclusion.
- **Aspire to perfect reliability.** You are required to be present but condemned to be absent. It must work for every user, every time — which means testing with real users.

**Anti-pedagogical temptations to resist:** abstraction and generalisation, explanation, choices, extra information.

**Language patterns**

- "We…" — the first-person plural affirms the tutor/learner relationship.
- "First, do x. Now, do y." — no ambiguity.
- "The output should look something like…" — set expectations.
- "Notice that… Remember that… Let's check…" — orientation clues.
- Close by describing what the learner has accomplished.

**Cost warning:** tutorials are the most expensive documentation to maintain. Changes cascade through the whole narrative rather than staying local, and a fast-moving product forces repeated rework.

### 3.2 How-to guide — goal/task-oriented

A how-to guide addresses a real-world goal, for an already-competent user who is at work.

**Write from the user's project, not the machinery's capabilities.** The common failure mode is a guide defined by what the tool can do rather than what a human needs to accomplish. These *look* like guidance but aren't:

- "To shut off the flow of water, turn the tap clockwise."
- "To deploy the desired database configuration, select the appropriate options and press **Deploy**."

They're useless because any competent practitioner already knows them, and because they're disconnected from purpose. What the user actually needs is how much water to run for a given purpose, or which configuration options align with which real-world needs.

**Principles**

- **Address real-world complexity.** A guide useful only for exactly your narrow case is rarely worth having; leave room for adaptation.
- **Omit the unnecessary.** Practical usability beats completeness. Unlike a tutorial, it needn't be end-to-end — start and end somewhere reasonable and let the reader join it to their work.
- **Provide an executable set of instructions.** A contract: in this situation, these steps get you through. "Actions" includes thinking and judgement, not just keystrokes.
- **Describe a logical sequence.** Sometimes order is forced; sometimes one step usefully sets up the user's thinking for the next — that's still a reason to order it.
- **Seek flow.** Don't make the user switch contexts repeatedly or hold thoughts open too long. At its best, a how-to guide anticipates the user, like a helper handing you the tool you were about to reach for.
- **Pay attention to naming.**
  - good: *How to integrate application performance monitoring*
  - bad: *Integrating application performance monitoring* (maybe it's about whether you should)
  - very bad: *Application performance monitoring* (could be how, whether, or what)

**Scope test:** "How to use fixtures in pytest" or "How to configure reconnection back-off policies" are how-to guides. "How to build a web application" is not — that's an open-ended sphere of skill.

**Language patterns:** "This guide shows you how to…"; "If you want x, do y" (conditional imperatives); "Refer to the x reference guide for the full list of options."

**Also note:** a how-to guide is not merely a linear procedure. Real problems fork, overlap, and have multiple entry and exit points, and often require the user's judgement.

### 3.3 Reference — information-oriented

Reference is technical description: propositional knowledge consulted during work. Its content is led by the product, not by user needs. You don't read reference, you *consult* it.

**Principles**

- **Describe and only describe.** Neutral description is unnatural to write — the pull toward instructing, explaining and opining is strong. Link out instead.
- **Adopt standard patterns.** Reference is useful when it's consistent and predictable. It is not the place to display range of style.
- **Respect the structure of the machinery.** If a method belongs to a class in a module, the documentation should show the same relationship. A map is useful because it corresponds to the territory.
- **Provide examples.** A usage example illustrates without sliding into explanation or instruction.

**Style:** austere, uncompromising, neutral, objective, factual.

**Language patterns:** state facts about behaviour; list commands, options, flags, limitations, error messages; give warnings where appropriate ("You must not apply b unless c").

**The food-packet test:** you expect "May contain traces of wheat" and "Net weight: 1000g", in standard places, so you can find and trust them fast. Recipes or marketing claims mixed into that would be, literally, dangerous. Reference labelling on food is often governed by law — the same seriousness should apply to technical reference.

### 3.4 Explanation — understanding-oriented

Explanation is discursive treatment that permits reflection. Its viewpoint is higher and wider than the other three; it's the one kind of documentation it might make sense to read in the bath. It answers "Can you tell me about…?"

Understanding doesn't *come from* explanation, but explanation weaves the web that holds a practitioner's knowledge together. Without it, knowledge of a craft is loose, fragmented, and its exercise is anxious.

**Principles**

- **Make connections,** including to things outside the immediate topic.
- **Provide context** — design decisions, historical reasons, technical constraints, implications.
- **Talk *about* the subject.** You should be able to put an implicit "About…" in front of every title: *About user authentication*, *About database connection policies*.
- **Admit opinion and perspective.** Explanation can and must consider alternatives, counter-examples, and competing approaches. This is legitimate here and nowhere else.
- **Keep it closely bounded.** Explanation absorbs other things if you let it. Use a real or imagined *why* question as the prompt, since the topic has no natural stopping point.

**Naming:** the section need not be called *Explanation* — *Discussion*, *Background*, *Conceptual guides*, or *Topics* all work.

**Language patterns:** "The reason for x is historically, y…"; "W is better than z, because…"; "An x in system y is analogous to a w in system z, however…"; "Some users prefer w, which can be a good approach, but…"

**Status warning:** explanation is less *urgent* than the other three, which leads people to treat it as less *important*. It isn't a luxury.

---

## 4. The two confusions that cause most damage

### 4.1 Tutorial vs how-to guide

This is the single most common conflation in software product documentation, and the most harmful, because it blocks exactly the newcomers you're trying to convert into committed users.

They look alike: both are practical, both are ordered sequences of steps, both promise a successful conclusion, and neither makes sense to someone who isn't at the machinery. The difference is the need served — **study or work**.

The site's medical example is the clearest test. A student suturing a synthetic skin pad in a lab, fumbling and dropping the needle under a tutor's correction, is in a **tutorial**. A surgical team following a clinical manual through an appendectomy is using a **how-to guide**.

| Tutorial | How-to guide |
|---|---|
| Builds basic competence | Helps an already-competent user do a task |
| Carefully managed path | Path can't be managed — it's the real world |
| Familiarises with tools and language | Assumes familiarity |
| Contrived setting; eliminates the unexpected | Real world; must prepare for the unexpected |
| Single line, no choices | Forks and branches: *if this, then that* |
| Must be safe and repeatable | Cannot promise safety; often one chance |
| Responsibility lies with the teacher | Responsibility lies with the user |
| Learner may not know what to ask | Assumes the user is asking the right question |
| Explicit about basic and bodily things | Relies on implicit, even bodily, knowledge |
| Concrete and particular | General, because real cases vary |
| Teaches transferable skill | Completes one particular task |

**The trap:** this is *not* the difference between basic and advanced. How-to guides can and should cover mundane procedures like paperwork or materials disposal. Tutorials can be highly advanced — an anaesthetist of many years taking a course on difficult neonatal intubations is still in a tutorial. The difference is study vs work, nothing else.

**Why it matters:** a clinical manual that tried to teach while guiding a live procedure would kill people. Software documentation gets away with more, but every conflated guide costs users and, eventually, the product.

### 4.2 Reference vs explanation

Both belong to the theory half of the map; the split is again study vs work. Usually easy, but slippery.

**Rules of thumb**

- If it's boring and unmemorable, it's probably **reference**.
- Lists (classes, methods, attributes) and tables of information are **reference**.
- If you can imagine reading it in the bath, it's **explanation**.
- If it's the answer to "can you tell me more about X?" over a drink, it's **explanation**.

**Where the slippage happens:** writing reference, you add an illustrative example — legitimate — and then the example gets fun, and starts saying *why*, or *what if*, or how it came to be. That damages both: the reference is interrupted, and the explanation never gets to develop properly.

**The real test:** would someone turn to this while actually executing a task, or only after stepping away to think about it?

---

## 5. The workflow (the part people skip)

Diátaxis runs counter to accepted documentation wisdom: it discourages planning and top-down workflows in favour of small, responsive iterations from which the overall pattern emerges.

**The loop**

1. **Choose something** — whatever is in front of you: the file you're in, the last page you read, or something at random. Don't go hunting for problems.
2. **Assess it** — preferably small, a page at most, better a paragraph or sentence. Ask: what user need does this represent? How well does it serve that need? What can be added, moved, removed or changed? Do its language and logic match its mode?
3. **Decide one next action** that produces an immediate improvement.
4. **Do it, and consider it done** — publish or at least commit. Then start again.

This removes the most paralysing part of documentation work: figuring out what to do next.

**Two emphatic warnings**

- **Don't create four empty sections** for tutorials / how-to / reference / explanation and then try to fill them. Structure emerges from the inside out as content improves; imposing it from above doesn't work.
- **Diátaxis is a guide, not a plan.** It's a map for checking that you're in the right place going in the right direction, not a checklist to complete.

**Organic growth model.** Structure is guaranteed by healthy development at the cellular level, not by a shape imposed from outside. Documentation, like a plant, is **never finished** but can be **always complete** — appropriate to its current stage, useful now, ready to grow.

---

## 6. Structure and complex hierarchies

**Default shape**

```
Home                      <- landing page
    Tutorial              <- landing page
        Part 1 / Part 2 / Part 3
    How-to guides         <- landing page
        Install / Deploy / Scale
    Reference             <- landing page
        Command-line tool / Endpoints / API
    Explanation           <- landing page
        Best practice / Security overview / Performance
```

Add a layer of hierarchy when a section needs grouping (e.g. Install → local, Docker, VM, Linux container).

**Contents and landing pages**

- Lists longer than about **seven items** are hard to read unless mechanically ordered. Break them up.
- A landing page should **read like an overview**, not present a bare list of links: headings plus short introductory text that provides context. You are authoring for a human, not satisfying a scheme.

**Two-dimensional problems.** When Diátaxis collides with another axis — user types (users / developers / contributors), deployment targets (each cloud with different workflows and APIs), or usage contexts (land / sea / air) — there's no single correct nesting order.

The resolution is **user-first thinking**: document the product *as it exists in the user's hands and mind*, not as its creators conceive it. If land, sea and air are effectively three different products for three different users, start there. It may make sense to let developer-facing tutorial content follow on from user-facing material while separating contributor how-to guides entirely.

**Diátaxis is an approach, not four boxes.** The clean four-way split is a typical outcome of good practice, not its goal. Let documentation be as complex as it needs to be — complex structures are navigable as long as they're logical and fit user needs.

---

## 7. Blur and collapse

There is a natural affinity between neighbouring quadrants, and a natural tendency for the boundaries to blur:

| shared property | neighbours that blur |
|---|---|
| guide action | tutorials ↔ how-to guides |
| serve application of skill | how-to guides ↔ reference |
| contain propositional knowledge | reference ↔ explanation |
| serve acquisition of skill | explanation ↔ tutorials |

When boundaries blur, writing style and content migrate into the wrong places, which causes structural problems, which makes the writing discipline still harder to maintain. In the worst case tutorials and how-to guides collapse into each other and neither need is met.

**The journey around the map.** Users don't move through the four types in a fixed order — they enter anywhere. But there is a real cycle in becoming expert: learn by doing → put the skill to work → consult reference when work exceeds what you hold in your head → step away and reflect to understand the whole → and back again, for something new or something deeper.

---

## 8. Quality: what Diátaxis can and can't do

| Functional quality | Deep quality |
|---|---|
| accuracy, completeness, consistency, precision, usefulness | flow, fitting human needs, anticipating the user, beauty, feeling good to use |
| independent characteristics | interdependent characteristics |
| objective — measured against the world | subjective — assessed against the human |
| measured | judged |
| a precondition of deep quality | conditional on functional quality |
| experienced by the author as constraint | experienced by the author as liberation |

Documentation can be accurate, complete, consistent — and still useless or unpleasant. But nothing inaccurate or inconsistent will ever be experienced as beautiful; deep quality is conditional on functional quality.

**Diátaxis cannot deliver functional quality.** That comes from technical skill and conscientious craft. What it does:

- **Exposes lapses.** Making reference mirror the architecture of the code makes gaps visible. Stripping explanatory verbiage out of a tutorial reveals where the reader was silently left to work something out.
- **Creates conditions for deep quality.** Its categories exist as responses to needs, so it helps documentation fit those needs; and it directly protects **flow** by preventing the kind of disruption that happens when a digression into explanation interrupts a how-to guide.

**Its limits.** Diátaxis offers principles, not a formula. It doesn't make documentation beautiful by itself, and it's no short-cut past user experience, interaction design or visual design. It lays down conditions for the *possibility* of deep quality; it doesn't guarantee it.

---

## 9. If you take one thing

Run the compass on the next page you touch. Make one change. Ship it.

The site itself is explicit that you shouldn't read all of it before starting, and that you won't understand Diátaxis until you've used it — which is itself a Diátaxis principle. Treat the site as a toolbox you return to with a specific problem.

---

## Sources

All pages of <https://diataxis.fr/>, by Daniele Procida:

- Home — <https://diataxis.fr/>
- Start here — <https://diataxis.fr/start-here/>
- Applying Diátaxis — <https://diataxis.fr/application/>
- Tutorials — <https://diataxis.fr/tutorials/>
- How-to guides — <https://diataxis.fr/how-to-guides/>
- Reference — <https://diataxis.fr/reference/>
- Explanation — <https://diataxis.fr/explanation/>
- The compass — <https://diataxis.fr/compass/>
- Workflow / Diátaxis as a guide to work — <https://diataxis.fr/how-to-use-diataxis/>
- Understanding Diátaxis — <https://diataxis.fr/theory/>
- Foundations — <https://diataxis.fr/foundations/>
- The map — <https://diataxis.fr/map/>
- Quality — <https://diataxis.fr/quality/>
- Tutorial vs how-to guide — <https://diataxis.fr/tutorials-how-to/>
- Reference vs explanation — <https://diataxis.fr/reference-explanation/>
- Complex hierarchies — <https://diataxis.fr/complex-hierarchies/>

Content confirmed as of July 2026. This is a paraphrased distillation, not a reproduction of the original text.
