# The Unofficial Guide

Anuj Subedi. I picked the campus_life corpus. 

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->
This system is an AI-powered Q&A tool designed to answer student questions about university housing, dining, academic policies, and campus life. It uses the `campus_life` corpus, which consists of short, crowdsourced text files containing unofficial student advice. When a user asks a question, the system retrieves the most relevant files and uses them to generate a grounded answer, refusing to answer if the topic is not covered in the documents.    
## Chunking Strategy

**Chunk size:** 1 entire document (no character limit)
**Overlap:** 0

Because I selected the `campus_life` corpus, my documents consist of very short 1-3 sentence text files (like quick reviews of a dining hall or a specific class). Standard character-based chunking would arbitrarily slice these short thoughts in half and destroy the context. Therefore, I wrote a custom chunker that treats each individual text file as exactly one chunk with zero overlap, ensuring the AI reads the complete thought every time.

Here is what I actually measured in my own corpus, which is where those numbers came from:

| Measurement | campus_life |
|---|---|
| Documents | 88 |
| Total characters | 27,908 |
| Average document length | 317 characters |
| Median document length | 309 characters |
| Shortest / longest document | 178 / 549 characters |
| Documents longer than 800 characters | **0** |

That last row is the one that decided it. The starter cuts at 800 characters, and **not a single
document in campus_life reaches 800** — the longest is 549. So the starter's chunker was already
emitting 88 chunks from 88 documents and never splitting anything.

**An honest note about what my chunker changed.** Because nothing hits the 800-character
threshold, my `split_documents` produces the *same 88 chunks* the starter's `fallback_split`
did on this corpus — identical text, identical boundaries. I verified this by running both
functions over the same documents and comparing the summary lines; they match exactly
(88 chunks, 317 average, 178 shortest, 549 longest). What actually changed is the *rule*, not
this run's output: under the starter, a post that ever grew past 800 characters would be cut
mid-sentence and the tail would become a fragment (the starter's own docs note a 2-character
chunk appearing on `advice_threads` for exactly this reason). Under mine, a whole post stays a
whole post no matter how long it gets. I am stating this plainly rather than claiming an
improvement I did not measure.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
"What is the best time to do your laundry at Aldridge Hall?"
**Answer:**

Run verbatim from `python app.py ask "What is the best time to do your laundry at Aldridge Hall?"`:

```
  (best distance 0.310, cutoff 0.7)

The best time to do your laundry at Aldridge Hall is Tuesday or Wednesday morning.

Source: housing_aldridge_hall_laundry.txt

Sources retrieved: dining_halden_hall.txt, housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court_laundry.txt
```

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->


My relevance cutoff: 0.70

I set the cutoff to 0.70 because my in-scope questions ranged from 0.231 to 0.579, while my out-of-scope questions ranged from 0.825 to 0.934. The gap was between 0.579 and 0.825, so 0.70 safely splits the difference, ensuring the system answers valid questions but refuses irrelevant ones.

| Question | In corpus? | Best distance |
|---|---|---|
| How often can you change your meal plan? | Yes | 0.299 |
| What is the printing quota for each student? | Yes | 0.334 |
| When do the study abroad applications open? | Yes | 0.231 |
| What is the best time to do your laundry at Aldridge Hall? | Yes | 0.310 |
| How much does the campus shuttle charge? | Yes | 0.579 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.896 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
Moment 1: I used AI (Gemini) to write the custom split_documents function in chunker.py. I explained that my campus_life corpus consisted of very short 1-3 sentence files. The AI suggested that slicing them by character count would destroy the context, and wrote a script that treats one entire document as exactly one chunk. I reviewed the code, replaced the fallback_split call with it, and tested the output to ensure the files remained fully intact.
**2.**
Moment 2: I also used it to pressure-test my custom acceptance criterion for the test questions. I gave the AI a half-written rule about the system refusing to answer if a question used profanity or asked for something harmful, but I wasn't sure how to scope it. The AI helped me frame it in a better way, so I adapted that specific angle into my final criteria.md file.

## Stretch Features

I am attempting all three stretch options. Declaring them here before I build them:

**1. Metadata filtering.** Every filename in `campus_life` carries a topic prefix —
`admin_`, `course_`, `dining_`, `housing_`. I will store that prefix as a `category` field
on each chunk at index time and add `--category` and `--source` flags so retrieval can be
narrowed to one facet. I will show the same query run with and without the filter and say
what moved.

**2. Conversational memory.** A follow-up like "is it crowded then?" retrieves nothing on its
own and my gate correctly refuses it, so memory has to act *before* retrieval, not just at
answer time. I will condense each follow-up into a standalone question using the previous
turn, then retrieve on the condensed version. I will show a two-turn exchange where turn 2
is unanswerable without turn 1.

**3. A second embedding model.** I will index the same corpus a second time under a separate
variant using a different embedding model, then run all ten of my questions through both and
record which distances moved and in which direction. I expect my 0.70 cutoff to need
changing, because a different model means a different distance distribution.

*Written before implementation. Results for each are in the three subsections that follow
once built.*

---

### Stretch 1 — Metadata filtering

**What I added.** Every file in `campus_life` is named with a topic prefix, so the facet was
already in the corpus and I only had to store it. `store.py::category_of` takes the text
before the first underscore, and `build_index` writes it onto each chunk as `category`.
`store.search` now takes a `where` dict handed straight to Chroma, so the filter is applied
*before* the nearest-neighbour search rather than filtering the top 5 afterwards — otherwise
a `--category dining` search would keep throwing rows away and return fewer than 5.

`python app.py categories` lists what is filterable:

| category | documents |
|---|---|
| course | 27 |
| housing | 21 |
| admin | 16 |
| dining | 14 |
| money | 2 |
| study | 2 |
| transit | 2 |
| advising, health, orientation, winter | 1 each |

**The same query, with and without the filter.** I picked *"when is it busiest?"* because it
is deliberately ambiguous — nothing in it says whether I mean a dining hall or a course.

Without the filter — `python app.py retrieve "when is it busiest?"`:

```
#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.5473     course_stat_150_workload.txt     Workload for STAT 150 Applied Statistics  People kee...
2   0.5600     course_econ_101_workload.txt     Workload for ECON 101 Introduction to Economics  Peo...
3   0.5626     housing_calder_annexe_noise.txt  Noise levels in Calder Annexe  Asked about this a lo...
4   0.5678     course_cs_210_workload.txt       Workload for CS 210 Data Structures  People keep ask...
5   0.5818     course_math_220_workload.txt     Workload for MATH 220 Linear Algebra  People keep as...

Gate: best distance 0.547 is under the 0.7 cutoff
```

With the filter — `python app.py retrieve "when is it busiest?" --category dining`:

```
Question: when is it busiest?
Filter:   {'category': 'dining'}

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.6000     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...
2   0.6093     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...
3   0.6266     dining_the_ridgeway_cafe_followup.txt Re: The Ridgeway Café  Adding to what people have sa...
4   0.6317     dining_verrill_street_grill_followup.txt Re: Verrill Street Grill  Adding to what people have...
5   0.6377     dining_kestrel_commons_followup.txt Re: Kestrel Commons  Adding to what people have said...
```

**What changed, and the thing I didn't expect.** All five results changed — four of the five
unfiltered hits were course-workload documents, which match the *phrasing* of "when is it
busiest" (they all contain "People keep asking so...") without being about crowds at all.
Filtered, all five are dining wait-time posts, which is what the question actually meant.

The unexpected part is the direction of the numbers: **the best distance got worse, 0.547 →
0.600, while the answer got better.** I had assumed a filter would improve the distance. It
does the opposite, and the reason is that the filter removes documents that were genuinely
closer *in wording* than anything in `dining` is. That is a concrete demonstration that a low
distance means "similar text", not "correct answer" — and it means my 0.7 cutoff is doing less
work than I thought, because a confidently wrong result sat at 0.547, well inside the gate.

I also added `--source FILE.txt` for narrowing to a single document, and both flags can be
combined (Chroma `$and`). Matching is exact, not substring; an unmatched filter prints a
message pointing at `python app.py categories` rather than failing silently.

---

### Stretch 2 — Conversational memory

**What I added.** The naive version of this — paste the last turn into the answer prompt —
does not work with a relevance gate in front of it, and finding that out is most of what I
learned here. A follow-up like *"Is it crowded then?"* contains no searchable content, so
retrieval brings back the wrong documents and the answer fails **before** the prompt is ever
assembled. Memory has to act earlier than the prompt.

So `generate.py::condense_question` rewrites the follow-up into a standalone question using
the previous turn, and `ask_pipeline` retrieves on *that*. History is also passed into
`build_prompt`, explicitly labelled as context for resolving references and not as a source of
facts, so grounding still comes only from retrieved chunks.

**The control — the same two turns without `--memory`:**

```
--- Turn 2 ---
> Is it crowded then?
  (best distance 0.636, cutoff 0.7)

I do not have enough information to answer whether the housing is crowded.

Sources retrieved: housing_aldridge_hall.txt, housing_calder_annexe.txt, housing_fenwick_court.txt, housing_fenwick_court_noise.txt, housing_tamsin_court.txt
```

**The two-turn exchange with memory** —
`python app.py ask --memory "What is the best time to do your laundry at Aldridge Hall?" "Is it crowded then?"`:

```
--- Turn 1 ---
> What is the best time to do your laundry at Aldridge Hall?
  (best distance 0.310, cutoff 0.7)

The best time to do your laundry at Aldridge Hall is Tuesday or Wednesday morning.

Source: housing_aldridge_hall_laundry.txt

Sources retrieved: dining_halden_hall.txt, housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court_laundry.txt


--- Turn 2 ---
> Is it crowded then?
  (follow-up rewritten for search: "Is the laundry room at Aldridge Hall crowded on Tuesday or Wednesday morning?")
  (best distance 0.364, cutoff 0.7)

Based on the documents provided, Tuesday or Wednesday morning is listed as the best time to do laundry at Aldridge Hall, whereas Sunday evenings are crowded and you will have to wait.

Source: `housing_aldridge_hall_laundry.txt`

Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_aldridge_hall_noise.txt, housing_morrow_house_noise.txt, housing_old_brewhouse_noise.txt
```

**Turn 2 depends on turn 1 in two separate ways**, which is why I chose this pair:

- *"it"* is the Aldridge laundry room — named only in turn 1's question.
- *"then"* is **Tuesday or Wednesday morning** — a fact that appears nowhere in turn 2 and was
  produced by turn 1's *answer*, not its question. Carrying the question forward alone would
  not have been enough.

**What changed, measurably.** Best distance on turn 2 went **0.636 → 0.364**, and the outcome
went from a refusal to a grounded answer citing `housing_aldridge_hall_laundry.txt`. The
rewritten query is printed on every memory turn so the rewrite is visible rather than hidden.

Two deliberate details: refusals are not appended to the history, since resolving a later
follow-up against *"I don't have enough information"* would make things worse; and if the
rewrite call fails or returns something malformed, it falls back to the question as typed, so
memory can never cost you an answer you would otherwise have got.

---

### Stretch 3 — A second embedding model

**Which model, and why not the suggested one.** The assignment suggests `sentence-transformers`
with a second local model. I tried that first and could not finish the install — it brings
PyTorch with it, and the download stalled repeatedly on my connection. Rather than drop the
feature I swapped in the *other* kind of second model: a hosted one,
**`gemini-embedding-001`**, reached through the `google-genai` package the starter already
installs and the key already in my `.env`. Nothing to download, and it is a larger change than
one local MiniLM for another — **3072 dimensions against the bundled model's 384**.

`store.py::_GeminiEmbedder` implements it behind the same `.encode(texts)` interface the other
two embedders use, batching 32 chunks per request, so nothing else in the pipeline had to
change. `app.py --embedding-model NAME` picks the model for a run, and `--variant` keeps the
two indexes side by side instead of overwriting:

```
python app.py index                                                          # 384d, local
python app.py --variant gemini --embedding-model gemini-embedding-001 index  # 3072d, API
```

Indexing all 88 chunks through the API took **5.9 seconds and 3 batched requests**.

**The comparison**, generated by `python compare_embeddings.py` rather than typed by hand:

#### In-corpus questions

| Question | MiniLM (384d) | top source | Gemini (3072d) | top source | change |
|---|---|---|---|---|---|
| How often can you change your meal plan? | 0.299 | `admin_meal_plan_changes.txt` | 0.195 | `admin_meal_plan_changes.txt` | -0.104 (closer) |
| What is the printing quota for each student? | 0.334 | `admin_printing_quota.txt` | 0.133 | `admin_printing_quota.txt` | -0.201 (closer) |
| When do the study abroad applications open? | 0.231 | `admin_study_abroad.txt` | 0.196 | `admin_study_abroad.txt` | -0.035 (closer) |
| What is the best time to do your laundry at Aldridge Hall? | 0.310 | `housing_aldridge_hall_laundry.txt` | 0.129 | `housing_aldridge_hall_laundry.txt` | -0.181 (closer) |
| How much does the campus shuttle charge? | 0.579 | `transit_shuttle.txt` | 0.204 | `transit_shuttle.txt` | **-0.375 (closer)** |

#### Out-of-scope questions

| Question | MiniLM (384d) | top source | Gemini (3072d) | top source | change |
|---|---|---|---|---|---|
| What is the capital of Mongolia? | 0.825 | `course_hist_118_exams.txt` | 0.528 | ⚠️ `course_hist_118_workload.txt` | -0.297 (closer) |
| How do I change the oil in a diesel engine? | 0.934 | `admin_meal_plan_changes.txt` | 0.529 | ⚠️ `housing_calder_annexe_laundry.txt` | -0.405 (closer) |
| Who won the 1994 World Cup? | 0.886 | `course_hist_118_exams.txt` | 0.538 | ⚠️ `course_hist_118.txt` | -0.348 (closer) |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | `money_textbooks.txt` | 0.493 | ⚠️ `health_center.txt` | -0.351 (closer) |
| How do I write a for loop in Rust? | 0.896 | `course_hist_118_exams.txt` | 0.506 | ⚠️ `course_cs_210_workload.txt` | -0.390 (closer) |

⚠️ = the two models disagreed about which document is closest.

#### What moved, and in which direction

**1. Every single distance went down.** All ten, in-corpus and out-of-scope alike, by between
0.035 and 0.405. The whole scale compressed toward zero. This is the thing that would have
broken my system silently: a distance is only meaningful relative to the model that produced
it, and none of my numbers transfer.

**2. The two groups separated further, even though everything got closer.**

| | MiniLM (384d) | Gemini (3072d) |
|---|---|---|
| in-corpus range | 0.231 – 0.579 | 0.129 – **0.204** |
| out-of-scope range | 0.825 – 0.934 | 0.493 – 0.538 |
| gap | 0.579 → 0.825 | 0.204 → 0.493 |
| **gap width** | 0.246 | **0.290** |
| cutoff the gap implies | 0.70 | **0.35** |

The in-corpus band is the striking part: it collapsed from a 0.348-wide spread to a 0.075-wide
one. Gemini is far more *consistent* about what counts as a match, not just more confident.

**3. My weakest question stopped being weak.** "How much does the campus shuttle charge?" was
my worst in-corpus result under MiniLM at 0.579 — nearly double every other question, and the
reason my in-corpus band was so wide, because `transit` is only 2 documents out of 88. Under
Gemini it lands at **0.204, in line with everything else**. The bigger model was not bothered
by the thin coverage that MiniLM was.

**4. The models disagree about *every* out-of-scope question, and Gemini is more sensible about
it.** MiniLM sent three of the five to `course_hist_118_exams.txt`, which is just the document
it falls back to when nothing matches. Gemini routes the ibuprofen question to
`health_center.txt` and the Rust question to `course_cs_210_workload.txt` — still the wrong
answer, but the nearest thing the corpus has, which is the behaviour you want from a model that
is about to be refused anyway.

**5. The part that actually matters: keeping my cutoff would have broken the gate.** At 0.70 on
the Gemini index, *every one of my five out-of-scope questions passes the gate*, because the
worst of them scores 0.538. I ran it to be sure:

```
$ python app.py --variant gemini --embedding-model gemini-embedding-001 ask "What is the capital of Mongolia?"
  (best distance 0.528, cutoff 0.7)

I do not have enough information to answer the question.

Sources retrieved: course_econ_101.txt, course_econ_101_exams.txt, course_hist_118.txt, course_hist_118_exams.txt, course_hist_118_workload.txt
```

The gate **let it through** and spent a model call on it. I still got an honest refusal, but
from the grounding instruction in `generate.py` — the second layer — and not from the gate. My
criterion 3 would have passed for the wrong reason. With the cutoff the data actually implies,
the gate does its own job again:

```
$ python app.py --variant gemini --embedding-model gemini-embedding-001 ask "What is the capital of Mongolia?" --threshold 0.35
  (best distance 0.528, cutoff 0.35)

I don't have enough information about that.
```

So the honest summary is: switching embedding model made retrieval better on every measure I
have, and would have silently disabled my relevance gate if I had not re-measured. **0.70 is
not a property of my corpus. It is a property of my corpus and MiniLM together.**

*Note: I left `config.THRESHOLD` at 0.70 and `EMBEDDING_MODEL` at the bundled model, because
that is the pairing the rest of this README documents. The Gemini index lives alongside it
under `--variant gemini`, so both are there to compare.*


---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
