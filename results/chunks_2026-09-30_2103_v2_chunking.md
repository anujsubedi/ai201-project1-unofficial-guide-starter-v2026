# Chunk boundary check — v2_chunking

- Produced by: `check_chunks.py::sample_chunks` and `check_chunks.py::corpus_wide`
- Chunks from: `chunker.py::split_documents`, documents from `ingest.py::load_documents`
- Corpus: `campus_life` — 88 documents, 224 chunks
- Sample size: 5 · seeds: 201, 202, 203
- Chunker: `chunker.py::fallback_split` — chunk_size 200, overlap 50
- When: 2026-09-30 21:03

This is the evidence for criterion 4 in criteria.md: "In a random sample
of 5 chunks, 5 out of 5 will contain the exact, complete text of a single
source file without being cut."

A chunk passes if its text is exactly its source file's text (**whole**)
and that file produced no other chunk (**alone**). No model is called and
the index is not touched, so each seed is a different sample of the same
fixed chunking — the three runs differ only in which chunks they look at.

| Run | Seed | Passed |
|---|---|---|
| Run 1 | 201 | 0 of 5 |
| Run 2 | 202 | 0 of 5 |
| Run 3 | 203 | 0 of 5 |

## Corpus-wide, not just the samples

- 224 chunks from 88 source files
- Files split across more than one chunk: **88** — {'admin_add_drop_deadline.txt': 2, 'admin_campus_jobs_and_financial_aid.txt': 2, 'admin_declaring_a_major.txt': 2, 'admin_dining_dollars.txt': 2, 'admin_grade_appeals.txt': 2, 'admin_graduation_requirements.txt': 2, 'admin_housing_lottery.txt': 3, 'admin_library_holds.txt': 2, 'admin_meal_plan_changes.txt': 2, 'admin_parking_permits.txt': 3, 'admin_pass_fail_option.txt': 2, 'admin_printing_quota.txt': 2, 'admin_study_abroad.txt': 2, 'admin_transcript_requests.txt': 2, 'admin_wifi_and_accounts.txt': 2, 'admin_withdrawal_deadline.txt': 3, 'advising_registration.txt': 2, 'course_biol_160.txt': 3, 'course_biol_160_exams.txt': 2, 'course_biol_160_workload.txt': 2, 'course_cs_210.txt': 3, 'course_cs_210_exams.txt': 2, 'course_cs_210_workload.txt': 2, 'course_cs_340.txt': 3, 'course_cs_340_exams.txt': 2, 'course_cs_340_workload.txt': 2, 'course_econ_101.txt': 3, 'course_econ_101_exams.txt': 2, 'course_econ_101_workload.txt': 2, 'course_engl_205.txt': 3, 'course_engl_205_exams.txt': 2, 'course_engl_205_workload.txt': 2, 'course_hist_118.txt': 3, 'course_hist_118_exams.txt': 2, 'course_hist_118_workload.txt': 2, 'course_math_220.txt': 3, 'course_math_220_exams.txt': 2, 'course_math_220_workload.txt': 2, 'course_phys_130.txt': 3, 'course_phys_130_exams.txt': 2, 'course_phys_130_workload.txt': 2, 'course_stat_150.txt': 3, 'course_stat_150_exams.txt': 2, 'course_stat_150_workload.txt': 2, 'dining_halden_hall.txt': 3, 'dining_halden_hall_followup.txt': 3, 'dining_kestrel_commons.txt': 3, 'dining_kestrel_commons_followup.txt': 3, 'dining_north_kitchen.txt': 3, 'dining_north_kitchen_followup.txt': 3, 'dining_pellew_dining_hall.txt': 3, 'dining_pellew_dining_hall_followup.txt': 3, 'dining_the_atrium.txt': 3, 'dining_the_atrium_followup.txt': 3, 'dining_the_ridgeway_cafe.txt': 3, 'dining_the_ridgeway_cafe_followup.txt': 3, 'dining_verrill_street_grill.txt': 3, 'dining_verrill_street_grill_followup.txt': 3, 'health_center.txt': 3, 'housing_aldridge_hall.txt': 3, 'housing_aldridge_hall_laundry.txt': 2, 'housing_aldridge_hall_noise.txt': 2, 'housing_calder_annexe.txt': 3, 'housing_calder_annexe_laundry.txt': 2, 'housing_calder_annexe_noise.txt': 2, 'housing_fenwick_court.txt': 3, 'housing_fenwick_court_laundry.txt': 2, 'housing_fenwick_court_noise.txt': 2, 'housing_innisfree_hall.txt': 4, 'housing_innisfree_hall_laundry.txt': 2, 'housing_innisfree_hall_noise.txt': 2, 'housing_morrow_house.txt': 4, 'housing_morrow_house_laundry.txt': 3, 'housing_morrow_house_noise.txt': 2, 'housing_old_brewhouse.txt': 4, 'housing_old_brewhouse_laundry.txt': 3, 'housing_old_brewhouse_noise.txt': 3, 'housing_tamsin_court.txt': 3, 'housing_tamsin_court_laundry.txt': 2, 'housing_tamsin_court_noise.txt': 2, 'money_jobs.txt': 3, 'money_textbooks.txt': 3, 'orientation_what_matters.txt': 3, 'study_group_rooms.txt': 3, 'study_library_hours.txt': 3, 'transit_shuttle.txt': 3, 'transit_walking.txt': 3, 'winter_gear.txt': 3}
- Chunks whose text differs from their source file: **220** — ['admin_add_drop_deadline.txt', 'admin_add_drop_deadline.txt', 'admin_campus_jobs_and_financial_aid.txt', 'admin_campus_jobs_and_financial_aid.txt', 'admin_declaring_a_major.txt', 'admin_declaring_a_major.txt', 'admin_dining_dollars.txt', 'admin_dining_dollars.txt', 'admin_grade_appeals.txt', 'admin_grade_appeals.txt']

---

## The sampled chunks

### Run 1 — seed 201

**admin_meal_plan_changes.txt** — FAIL (whole: False, alone: False)

- chunk 199 chars / file 222 chars
- chunks from this file: 2

```
On the meal plan changes

You can change your meal plan tier once, in the first ten days of the semester. After that it's locked. Downgrading refunds the difference to your student account; upgrading
```

**housing_morrow_house_noise.txt** — FAIL (whole: False, alone: False)

- chunk 125 chars / file 276 chars
- chunks from this file: 2

```
who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.
```

**course_math_220_exams.txt** — FAIL (whole: False, alone: False)

- chunk 36 chars / file 186 chars
- chunks from this file: 2

```
sense afterwards rather than during.
```

**dining_kestrel_commons.txt** — FAIL (whole: False, alone: False)

- chunk 200 chars / file 369 chars
- chunks from this file: 3

```
ng worth going for is the stir-fry station, made to order. The thing to know is that the salad bar wilts after 1:30.

Hours are 7:00am to 9:00pm weekdays, 9:00am to 8:00pm weekends. Costs one meal swi
```

**admin_add_drop_deadline.txt** — FAIL (whole: False, alone: False)

- chunk 200 chars / file 300 chars
- chunks from this file: 2

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript
```

### Run 2 — seed 202

**housing_tamsin_court.txt** — FAIL (whole: False, alone: False)

- chunk 119 chars / file 419 chars
- chunks from this file: 3

```
ting if you're new.

Laundry costs in-unit washer-dryer. On noise: quiet, structurally — concrete floors between units.
```

**course_stat_150_workload.txt** — FAIL (whole: False, alone: False)

- chunk 200 chars / file 244 chars
- chunks from this file: 2

```
Workload for STAT 150 Applied Statistics

People keep asking so: 5 to 6 hours a week outside class. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest
```

**housing_fenwick_court_noise.txt** — FAIL (whole: False, alone: False)

- chunk 125 chars / file 275 chars
- chunks from this file: 2

```
who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.
```

**dining_pellew_dining_hall.txt** — FAIL (whole: False, alone: False)

- chunk 79 chars / file 379 chars
- chunks from this file: 3

```
entre.

Hours are 7:00am to 8:00pm daily. Costs one meal swipe, or $11.75 cash.
```

**dining_halden_hall_followup.txt** — FAIL (whole: False, alone: False)

- chunk 186 chars / file 336 chars
- chunks from this file: 3

```
ying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: closes at 7:00pm, which catches people out. Nobody tells you this at orientation.
```

### Run 3 — seed 203

**admin_pass_fail_option.txt** — FAIL (whole: False, alone: False)

- chunk 109 chars / file 259 chars
- chunks from this file: 2

```
ht, after you've seen your midterm. A pass needs a C- or better. Two per year, maximum eight across a degree.
```

**admin_graduation_requirements.txt** — FAIL (whole: False, alone: False)

- chunk 199 chars / file 282 chars
- chunks from this file: 2

```
On the graduation requirements

120 credit hours, a completed major, and the general education requirements. The one that trips people is the writing-intensive requirement: two courses, and they must
```

**transit_shuttle.txt** — FAIL (whole: False, alone: False)

- chunk 199 chars / file 379 chars
- chunks from this file: 3

```
The campus shuttle

Runs a loop every 20 minutes from 7am to 11pm on weekdays and every 40 minutes on weekends. The published timetable is optimistic by about five minutes in the morning and accurate
```

**dining_the_atrium.txt** — FAIL (whole: False, alone: False)

- chunk 200 chars / file 421 chars
- chunks from this file: 3

```
h going for is genuinely good sandwiches restocked twice a day. The thing to know is that picked clean by 1:15 and not restocked again until the next morning.

Hours are 8:00am to 6:00pm weekdays. Cos
```

**housing_calder_annexe.txt** — FAIL (whole: False, alone: False)

- chunk 200 chars / file 430 chars
- chunks from this file: 3

```
e good: the cluster lounges mean you meet people without having to try.

The bad: the singles are small — about 90 square feet — and the desks are fixed.

Laundry costs $2.00 wash, $1.75 dry, app-base
```
