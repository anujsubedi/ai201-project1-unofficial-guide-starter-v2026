#!/usr/bin/env python3
"""
Stretch feature 3: compare two embedding models on the same questions.

The point of this script is that the README table is *generated*, not typed.
Anyone can re-run it and get the same numbers.

It runs all five in-corpus QUESTIONS and all five OUT_OF_SCOPE questions from
questions.py against two indexes of the same corpus:

    the bundled model   all-MiniLM-L6-v2   384 dimensions, indexed as "default"
    the second model    all-mpnet-base-v2  768 dimensions, indexed as "mpnet"

and prints, for each question, the best distance under each model, which
source came back first, and the change.

Build both indexes first:

    python app.py index
    python app.py --variant mpnet --embedding-model all-mpnet-base-v2 index

Then:

    python compare_embeddings.py

Nothing here calls the hosted model. Retrieval only, so it costs no API quota.
"""

import argparse

import config
from questions import QUESTIONS, OUT_OF_SCOPE

BUNDLED = ("all-MiniLM-L6-v2", "default")
SECOND = ("all-mpnet-base-v2", "mpnet")


def best_for(questions, model_name, variant, corpus):
    """Best distance and top source for each question, under one model.

    The embedder is cached in a module global in store.py, so switching models
    inside one process means resetting it. That reset is the only reason this
    reaches into a private name.
    """
    import store

    config.EMBEDDING_MODEL = model_name
    store._model = None  # noqa: SLF001 — force the next call to reload

    rows = []
    for question in questions:
        try:
            results = store.search(question, corpus=corpus, variant=variant)
        except RuntimeError as exc:
            raise SystemExit(
                f"{exc}\n\nBuild it with:\n"
                f"    python app.py --variant {variant} "
                f"--embedding-model {model_name} index"
            )
        if results:
            rows.append((results[0].distance, results[0].source))
        else:
            rows.append((None, "—"))
    return rows


def table(title, questions, left, right):
    print(f"\n### {title}\n")
    print(
        "| Question | MiniLM (384d) | top source | mpnet (768d) | top source | change |"
    )
    print("|---|---|---|---|---|---|")
    for question, (ld, ls), (rd, rs) in zip(questions, left, right):
        delta = "—"
        if ld is not None and rd is not None:
            diff = rd - ld
            arrow = "closer" if diff < 0 else "further"
            delta = f"{diff:+.3f} ({arrow})"
        same = " " if ls == rs else " ⚠️ "
        print(
            f"| {question} | {ld:.3f} | `{ls}` | {rd:.3f} |{same}`{rs}` | {delta} |"
        )


def summarise(name, in_scope, out_scope):
    """The two groups and the gap between them, for one model."""
    lo = [d for d, _ in in_scope if d is not None]
    hi = [d for d, _ in out_scope if d is not None]
    gap = min(hi) - max(lo)
    print(f"\n**{name}**")
    print(f"- in-corpus:     {min(lo):.3f} – {max(lo):.3f}")
    print(f"- out-of-scope:  {min(hi):.3f} – {max(hi):.3f}")
    print(f"- gap:           {max(lo):.3f} → {min(hi):.3f}  (width {gap:.3f})")
    print(f"- midpoint cutoff this implies: **{(max(lo) + min(hi)) / 2:.2f}**")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", default=None)
    args = parser.parse_args()
    corpus = args.corpus or config.CORPUS

    in_questions = [q["question"] for q in QUESTIONS]

    print(f"# Embedding model comparison — {corpus}")
    print(f"\n{BUNDLED[0]} (variant `{BUNDLED[1]}`) vs "
          f"{SECOND[0]} (variant `{SECOND[1]}`)")
    print("\nLower distance = closer match. Retrieval only; no model calls.")

    # One model fully, then the other — loading an embedder is the slow part,
    # so this does it twice rather than once per question.
    a_in = best_for(in_questions, *BUNDLED, corpus)
    a_out = best_for(OUT_OF_SCOPE, *BUNDLED, corpus)
    b_in = best_for(in_questions, *SECOND, corpus)
    b_out = best_for(OUT_OF_SCOPE, *SECOND, corpus)

    table("In-corpus questions", in_questions, a_in, b_in)
    table("Out-of-scope questions", OUT_OF_SCOPE, a_out, b_out)

    print("\n⚠️ marks a question where the two models disagreed about which "
          "document is closest.\n")
    print("## Where the cutoff lands under each model")
    summarise(f"{BUNDLED[0]} — current cutoff {config.THRESHOLD}", a_in, a_out)
    summarise(SECOND[0], b_in, b_out)


if __name__ == "__main__":
    main()
