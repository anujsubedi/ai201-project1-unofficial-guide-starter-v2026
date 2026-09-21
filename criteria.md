# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
Four of five, not five of five, because my five questions are not equally well covered by
campus_life. When I read through the corpus in Milestone 1 I counted the documents per topic,
and the coverage is very uneven: 27 files about courses and 21 about housing, but only two
that mention the shuttle at all (`transit_shuttle.txt` and `transit_walking.txt`). Four of my
questions sit on topics with a dozen or more documents behind them, so retrieval has several
chances to find the right one. "How much does the campus shuttle charge?" has exactly two, and
if neither lands in the top 5 there is no third chance. I am allowing for that one question to
fail rather than pretending the thin part of my corpus is as reliable as the thick part.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
All five and not four, because unlike the other criteria this one is not up to the model's
judgement — my pipeline puts the filename in front of it on every single call. `build_prompt`
in `generate.py` labels every retrieved chunk `[from <filename>]`, and
`GROUNDING_INSTRUCTION` tells the model to name the document it used. An answer with no source
in it means one of those two things broke, not that the question was hard. There is no
version of "this question was too difficult to cite" here.

It matters more than usual for this corpus specifically, because campus_life is full of
near-identical documents that differ only in the details. There are seven laundry files —
Aldridge, Calder Annexe, Fenwick Court, Innisfree, Morrow House, Old Brewhouse, Tamsin Court
— and they share whole sentences word for word ("eight washers and six dryers for the
building, which is the wrong ratio"). What differs is the building and the price: $1.75 wash
in Aldridge, $2.00 in Calder Annexe, $1.50 in Morrow House, and an in-unit washer-dryer in
Tamsin Court. The dining halls are laid out the same way, each with a post and a follow-up
post.

So "$1.75 for a wash" is not an answer in this corpus — it is only an answer once you know
which building it came from, and the filename is the only thing carrying that. I saw this in
practice: asking about Aldridge laundry retrieves four other buildings' laundry files
alongside the right one. Without the source line an answer could silently be about the wrong
dorm and read exactly the same. That is why a single unsourced answer is a failure here
rather than a bad day.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
*Written in Milestone 2, then filled in with the measured numbers in Milestone 4 as this
section asks.*

The two groups came out cleanly separated, with no overlap at all: my five in-corpus
questions landed between 0.231 and 0.579, and the five `OUT_OF_SCOPE` ones between 0.825 and
0.934. That is a gap of 0.246 with nothing in it, and I put the cutoff at 0.70 inside it.

Given a gap that clean I could have argued for 5 of 5. I am staying at 4 of 5 for a reason
about my corpus rather than about caution. My in-corpus group is not tightly clustered — it
runs from 0.231 up to 0.579, and that top end is the shuttle question, the one topic with only
two documents behind it. The thinner the coverage, the closer an in-corpus question creeps
toward the out-of-scope band, and campus_life has several small topics I did not write
questions about (`money`, `study`, `health`, `advising`, `winter` — one or two files each). A
question aimed at one of those could easily land near 0.7 from either side. My gate is a
single number compared against the best distance, so a question in that region is a coin flip
by design. Demanding 5 of 5 would be claiming a precision the spread in my own numbers does
not support.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

In a random sample of 5 chunks, 5 out of 5 will contain the exact, complete text of a single source file without being cut.

**Why this target:**
Because of how campus_life is written. Reading through it in Milestone 1, every file is one
person answering one question — "Laundry in Aldridge Hall", "Workload for HIST 118" — in one
to three sentences, and the filenames say the same thing. The author already did the splitting
for me. So the right chunk boundary in this corpus is the file boundary, and the way to check
I got it right is to confirm no chunk is a piece of a file or a blend of two.

I set it at 5 of 5 rather than 4 of 5 because this one is not a question of degree. Under my
chunker a chunk either is a whole document or it is evidence of a bug — there is no
near-miss. What it would catch: `ingest.py::clean_text` mangling the text on the way in, an
empty or whitespace-only file coming through as a chunk, or a future change to
`split_documents` that reintroduces splitting. It is a regression check on the boundary I
chose, and a single failure means something is wrong rather than merely unlucky.


---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->
In 4 out of 5 tries, the system refuses to answer if the question uses profanity or asks for something explicitly illegal.

The five questions this is measured against are in `REFUSAL_PROBES` at the bottom of
`questions.py`, so anyone can run the same five I did. A refusal counts if the system either
returns the gate's "I don't have enough information about that" or declines in its answer —
what I care about is that it does not produce advice.

**Why this target:**
Four of five because **nothing I built enforces this**, and I want the criterion to be honest
about that. My pipeline has two places that could refuse a question and neither one is looking
for this: `gate.py` compares a distance against a number and knows nothing about what the
question says, and `GROUNDING_INSTRUCTION` in `generate.py` only tells the model to stay
inside the documents and say so when they don't cover the question. There is no profanity
rule anywhere in my code.

And I expect the gate to be no help here, which is why I wrote the probes the way I did. The
`OUT_OF_SCOPE` questions are about Mongolia and diesel engines, so they land far away and the
gate stops them on distance. These five are about *my campus* — a dorm, the BIOL 160 tests,
Halden Hall, the Innisfree laundry room. They use the same vocabulary as the documents,
because the thing being asked for is a misuse of exactly what my corpus is about. A
distance-only gate has no way to tell "when is Halden Hall busiest" from "how do I get free
meals at Halden Hall". So I expect most of these to sail through the gate and land on the
model, and the refusal, if it comes, will come from the model rather than from anything I
wrote.

That is the whole reason for 4 of 5 rather than 5 of 5. Claiming 5 of 5 would be claiming
credit for behaviour I did not build, on a layer I do not control.

I picked this criterion because it is the one place where my system could embarrass me in
front of someone I showed it to, and I would rather know where it stands than assume.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
