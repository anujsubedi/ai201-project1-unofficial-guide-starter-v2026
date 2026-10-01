# Run log — after_hybrid

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::hybrid_search` via `store.py::retrieve` — semantic + BM25, fused by reciprocal rank (RRF k=60)
- Chunks from `chunker.py::split_documents`
- Corpus: `campus_life` (index variant `default`)
- top-k: 5 · relevance cutoff: 0.7
- Runs per question: 3, caching off
- When: 2026-09-30 20:55

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| How often can you change your meal plan? | pass | pass | pass |
| What is the printing quota for each student? | pass | pass | pass |
| When do the study abroad applications open? | pass | pass | pass |
| What is the best time to do your laundry at Aldridge Hall? | pass | pass | pass |
| How much does the campus shuttle charge? | pass | pass | pass |

---

## Rank and margin of the answer chunk

Produced by `run_eval.py::answer_rank_and_margin`. Criterion 1 is a
count, and a count cannot show how close the call was. **Margin** is
the cosine distance from the answer chunk to the nearest non-answer
chunk retrieved: bigger is safer, and a margin near zero is a pass
that nearly wasn't. Distances are cosine in both the semantic and the
hybrid runs, so these numbers compare directly between logs.

| Question | Rank | Margin (run 1) |
|---|---|---|
| How often can you change your meal plan? | 1 | +0.3772 |
| What is the printing quota for each student? | 1 | +0.2027 |
| When do the study abroad applications open? | 1 | +0.4419 |
| What is the best time to do your laundry at Aldridge Hall? | 1 | +0.1786 |
| How much does the campus shuttle charge? | 1 | +0.0176 |

---

## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.7. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### How often can you change your meal plan? — run 1

- Best distance: 0.2991 (passed the gate)
- Sources retrieved: admin_meal_plan_changes.txt, admin_pass_fail_option.txt, advising_registration.txt, dining_verrill_street_grill.txt, dining_verrill_street_grill_followup.txt

```
You can change your meal plan tier once, within the first ten days of the semester. 

Source: admin_meal_plan_changes.txt
```

### How often can you change your meal plan? — run 2

- Best distance: 0.2991 (passed the gate)
- Sources retrieved: admin_meal_plan_changes.txt, admin_pass_fail_option.txt, advising_registration.txt, dining_verrill_street_grill.txt, dining_verrill_street_grill_followup.txt

```
You can change your meal plan tier once, within the first ten days of the semester. After that, it is locked. 

Source: admin_meal_plan_changes.txt
```

### How often can you change your meal plan? — run 3

- Best distance: 0.2991 (passed the gate)
- Sources retrieved: admin_meal_plan_changes.txt, admin_pass_fail_option.txt, advising_registration.txt, dining_verrill_street_grill.txt, dining_verrill_street_grill_followup.txt

```
You can change your meal plan tier once, during the first ten days of the semester. 

Source: admin_meal_plan_changes.txt
```

### What is the printing quota for each student? — run 1

- Best distance: 0.3338 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_printing_quota.txt, admin_wifi_and_accounts.txt, money_jobs.txt, money_textbooks.txt

```
Every student receives $30 of printing per semester, which is approximately 600 black-and-white pages (admin_printing_quota.txt).
```

### What is the printing quota for each student? — run 2

- Best distance: 0.3338 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_printing_quota.txt, admin_wifi_and_accounts.txt, money_jobs.txt, money_textbooks.txt

```
Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages. (Source: admin_printing_quota.txt)
```

### What is the printing quota for each student? — run 3

- Best distance: 0.3338 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_printing_quota.txt, admin_wifi_and_accounts.txt, money_jobs.txt, money_textbooks.txt

```
Every student receives $30 of printing per semester, which is approximately 600 black-and-white pages. (admin_printing_quota.txt)
```

### When do the study abroad applications open? — run 1

- Best distance: 0.2312 (passed the gate)
- Sources retrieved: admin_study_abroad.txt, course_cs_340.txt, course_cs_340_exams.txt, course_cs_340_workload.txt, transit_shuttle.txt

```
Applications for the study abroad open in October for the following academic year (admin_study_abroad.txt).
```

### When do the study abroad applications open? — run 2

- Best distance: 0.2312 (passed the gate)
- Sources retrieved: admin_study_abroad.txt, course_cs_340.txt, course_cs_340_exams.txt, course_cs_340_workload.txt, transit_shuttle.txt

```
Study abroad applications open in October for the following academic year. 

Source: admin_study_abroad.txt
```

### When do the study abroad applications open? — run 3

- Best distance: 0.2312 (passed the gate)
- Sources retrieved: admin_study_abroad.txt, course_cs_340.txt, course_cs_340_exams.txt, course_cs_340_workload.txt, transit_shuttle.txt

```
Study abroad applications open in October for the following academic year (admin_study_abroad.txt).
```

### What is the best time to do your laundry at Aldridge Hall? — run 1

- Best distance: 0.3100 (passed the gate)
- Sources retrieved: dining_pellew_dining_hall_followup.txt, housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court_laundry.txt

```
The best time to do laundry at Aldridge Hall is Tuesday or Wednesday morning. 

Source: `housing_aldridge_hall_laundry.txt` (also mentioned in `housing_aldridge_hall.txt` regarding laundry details).
```

### What is the best time to do your laundry at Aldridge Hall? — run 2

- Best distance: 0.3100 (passed the gate)
- Sources retrieved: dining_pellew_dining_hall_followup.txt, housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court_laundry.txt

```
The best time to do laundry at Aldridge Hall is Tuesday or Wednesday morning. 

Source: `housing_aldridge_hall_laundry.txt` (also mentioned in `housing_aldridge_hall.txt`).
```

### What is the best time to do your laundry at Aldridge Hall? — run 3

- Best distance: 0.3100 (passed the gate)
- Sources retrieved: dining_pellew_dining_hall_followup.txt, housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court_laundry.txt

```
The best time to do laundry at Aldridge Hall is Tuesday or Wednesday morning. 

Source: housing_aldridge_hall_laundry.txt (also mentioned in housing_aldridge_hall.txt for laundry details).
```

### How much does the campus shuttle charge? — run 1

- Best distance: 0.5791 (passed the gate)
- Sources retrieved: admin_printing_quota.txt, dining_verrill_street_grill.txt, housing_innisfree_hall.txt, money_textbooks.txt, transit_shuttle.txt

```
The campus shuttle is free with a student ID (transit_shuttle.txt).
```

### How much does the campus shuttle charge? — run 2

- Best distance: 0.5791 (passed the gate)
- Sources retrieved: admin_printing_quota.txt, dining_verrill_street_grill.txt, housing_innisfree_hall.txt, money_textbooks.txt, transit_shuttle.txt

```
The campus shuttle is free with a student ID. 

Source: transit_shuttle.txt
```

### How much does the campus shuttle charge? — run 3

- Best distance: 0.5791 (passed the gate)
- Sources retrieved: admin_printing_quota.txt, dining_verrill_street_grill.txt, housing_innisfree_hall.txt, money_textbooks.txt, transit_shuttle.txt

```
The campus shuttle is free with a student ID (transit_shuttle.txt).
```
