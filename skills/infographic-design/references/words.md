# Words

Most of an infographic's surface is text: the takeaway, section heads, labels
on boxes and arrows, chips, axis ticks, the source line. Words are the part
readers actually decode, and they are the easiest part to leave until last.

## Words are design material

Words appear in a design for one reason: to make it easier to understand, and
therefore easier to read. They are design material, not decoration. Bring the
same intentionality to copy that you would bring to spacing and colour. Before
writing anything, ask what the graphic needs to say, and how it can best be
said to help the person find their way through it.

Copy can make a design feel as templated as the design itself. A brief often
arrives without real wording, and it falls to you to write it — "Overview",
"Key Benefits", "Process Flow", "Conclusion" are the label equivalents of a
centred column of rounded cards.

## Write from the reader's side

Name things by what people recognise, never by how the system is built. A
lane is `Client` or `Your browser`, not `TLS initiator`; a step is `Verify the
certificate`, not `Cert validation subroutine`. If the subject's own community
uses a term, use theirs — but expand it once, where it first appears, unless
the audience is certain to know it.

Describe what something does in plain terms rather than selling it. Being
specific is always better than being clever: `Signup → activation loses 38%`
beats `The activation challenge`.

## One name per thing, everywhere

This is the rule diagrams break most often. A thing that appears more than
once keeps exactly one name at every appearance — on the arrow, in the card
that explains it, in the legend, and in the payoff line. If a chip says
`pre-master secret`, nothing downstream may call it "the shared seed"; if a
lane is `Server`, no caption may say "the host". A reader who cannot tell
whether two labels mean the same thing has to stop and reason about your
vocabulary instead of your subject.

Where a token recurs often enough that its full name crowds the drawing, give
it a short badge (`A`, `B`, `C`) and define each badge once in a footer
legend — the badge then *is* the one name.

One licensed exception: a graphic built so someone *remembers* (a retention
pull, SKILL step 1) may pair each technical term with the analogy it was
taught under — but the pairing must be total, not casual: the second name
comes from the source dialogue or the audience's own vernacular (never
invented while drawing), every appearance carries the same pair, and a
footer table maps the full pairing. Outside that purpose, one name only.
See `learn-loop-viz.md`.

Use active voice, and let a label say exactly what happens: `Sends the client
random`, not `Client random transmission`.

## Let each element do exactly one job

A label labels, a caption adds what the drawing cannot show, an annotation
points at one thing, and nothing quietly does double duty. When a caption
starts restating what its own label already said, cut it; when it starts
carrying the takeaway, the takeaway is in the wrong place — that belongs to
the headline.

Keep the register plain and tuned: plain verbs, sentence case, no filler, tone
matched to the subject and the audience.

## Decide the word budget before you draw

Label length is a design decision, not a discovery. When you plan a box, plan
how many words fit in it at the size you intend — roughly 20–24 characters per
line for a chip, 40–50 for a card body at 12–13px. Writing to that budget up
front means the words earn their space; discovering it afterwards means the
drawing has to move to accommodate a sentence nobody edited.

Two habits that buy the most room: drop articles and auxiliaries in labels
(`Server picks cipher` over `The server then picks a cipher`), and let the
drawing carry what it already shows — an arrow from A to B does not need a
caption reading "A sends to B".

## Attribution

The first, second, fourth and fifth sections above are adapted from
Anthropic's `frontend-design` skill (Apache-2.0); the examples and vocabulary
are retargeted from web interfaces to diagrams, and its guidance on error and
empty states is deliberately omitted as it has no analogue here. See the
skill's `NOTICE` file.
