#!/usr/bin/env python3
"""Measure criterion 4: are my chunks whole files, uncut?

    python check_chunks.py                     seeds 201, 202, 203
    python check_chunks.py --seeds 1 2 3       pick your own
    python check_chunks.py --size 5            chunks per sample

Criterion 4 in criteria.md says: "In a random sample of 5 chunks, 5 out of 5
will contain the exact, complete text of a single source file without being
cut." The other four criteria are measured by `run_eval.py`, which asks
questions. This one isn't about questions at all — it's about what
`chunker.py::split_documents` did to the corpus on the way in — so it needs its
own script rather than a column in that run log.

A chunk passes if both of these hold:

  whole  — its text is exactly its source file's text, nothing trimmed or added
  alone  — that source file produced no other chunk, so the chunk isn't a piece

Both are needed. "Whole" alone would pass a file that was duplicated into two
identical chunks; "alone" alone would pass a single chunk that dropped half its
file.

Three seeds rather than one, because the criterion says *random sample* and the
submission asks for three runs. A fixed seed run three times is the same five
chunks three times, which satisfies the format and tests nothing. Three seeds
are three genuinely different samples, and writing the seeds down keeps it
reproducible. Nothing here calls a model or touches the index, so the only
source of variation is the sample itself.
"""

import argparse
import datetime as dt
import random

import chunker
import config
import ingest


def sample_chunks(seed: int, size: int = 5):
    """One sample of `size` chunks, judged whole-and-alone. Deterministic in seed."""
    documents = ingest.load_documents()
    chunks = chunker.split_documents(documents)

    doc_text = {d.source: d.text for d in documents}
    by_source: dict[str, list] = {}
    for chunk in chunks:
        by_source.setdefault(chunk.source, []).append(chunk)

    rng = random.Random(seed)
    size = min(size, len(chunks))
    sample = rng.sample(chunks, size)

    rows = []
    for chunk in sample:
        source_text = doc_text[chunk.source]
        whole = chunk.text.strip() == source_text.strip()
        alone = len(by_source[chunk.source]) == 1
        rows.append(
            {
                "source": chunk.source,
                "whole": whole,
                "alone": alone,
                "passed": whole and alone,
                "chunk_chars": len(chunk.text),
                "file_chars": len(source_text),
                "siblings": len(by_source[chunk.source]),
                "text": chunk.text,
            }
        )

    return rows, {"documents": len(documents), "chunks": len(chunks), "files": len(by_source)}


def corpus_wide():
    """The same check over every chunk, not just a sample."""
    documents = ingest.load_documents()
    chunks = chunker.split_documents(documents)
    doc_text = {d.source: d.text for d in documents}

    by_source: dict[str, list] = {}
    for chunk in chunks:
        by_source.setdefault(chunk.source, []).append(chunk)

    split_files = {s: len(v) for s, v in by_source.items() if len(v) > 1}
    altered = [c.source for c in chunks if c.text.strip() != doc_text[c.source].strip()]
    return {
        "chunks": len(chunks),
        "files": len(by_source),
        "split_files": split_files,
        "altered": altered,
    }


def main():
    parser = argparse.ArgumentParser(description="Measure criterion 4 on sampled chunks.")
    parser.add_argument("--seeds", type=int, nargs="+", default=[201, 202, 203])
    parser.add_argument("--size", type=int, default=5)
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    samples = []
    stats = {}
    for seed in args.seeds:
        rows, stats = sample_chunks(seed, args.size)
        passed = sum(r["passed"] for r in rows)
        samples.append({"seed": seed, "rows": rows, "passed": passed})
        print(f"seed {seed}: {passed} of {len(rows)} whole and uncut")
        for row in rows:
            mark = "PASS" if row["passed"] else "FAIL"
            print(
                f"  [{mark}] {row['source']}  "
                f"chunk {row['chunk_chars']} / file {row['file_chars']} chars, "
                f"{row['siblings']} chunk(s) from this file"
            )

    wide = corpus_wide()
    print(
        f"\nCorpus-wide: {wide['chunks']} chunks from {wide['files']} files, "
        f"{len(wide['split_files'])} file(s) split across chunks, "
        f"{len(wide['altered'])} chunk(s) whose text differs from its file"
    )

    write_report(samples, stats, wide, args)


def write_report(samples, stats, wide, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"chunks_{stamp}{label}.md"

    lines = [
        f"# Chunk boundary check{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `check_chunks.py::sample_chunks` and "
        "`check_chunks.py::corpus_wide`",
        "- Chunks from: `chunker.py::split_documents`, documents from "
        "`ingest.py::load_documents`",
        f"- Corpus: `{config.CORPUS}` — {stats.get('documents', 0)} documents, "
        f"{stats.get('chunks', 0)} chunks",
        f"- Sample size: {args.size} · seeds: {', '.join(str(s) for s in args.seeds)}",
        f"- When: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "This is the evidence for criterion 4 in criteria.md: \"In a random sample",
        "of 5 chunks, 5 out of 5 will contain the exact, complete text of a single",
        "source file without being cut.\"",
        "",
        "A chunk passes if its text is exactly its source file's text (**whole**)",
        "and that file produced no other chunk (**alone**). No model is called and",
        "the index is not touched, so each seed is a different sample of the same",
        "fixed chunking — the three runs differ only in which chunks they look at.",
        "",
        "| Run | Seed | Passed |",
        "|---|---|---|",
    ]

    for i, s in enumerate(samples, start=1):
        lines.append(f"| Run {i} | {s['seed']} | {s['passed']} of {len(s['rows'])} |")

    lines += [
        "",
        "## Corpus-wide, not just the samples",
        "",
        f"- {wide['chunks']} chunks from {wide['files']} source files",
        f"- Files split across more than one chunk: **{len(wide['split_files'])}**"
        + (f" — {wide['split_files']}" if wide["split_files"] else ""),
        f"- Chunks whose text differs from their source file: "
        f"**{len(wide['altered'])}**"
        + (f" — {wide['altered'][:10]}" if wide["altered"] else ""),
        "",
        "---",
        "",
        "## The sampled chunks",
        "",
    ]

    for i, s in enumerate(samples, start=1):
        lines += [f"### Run {i} — seed {s['seed']}", ""]
        for row in s["rows"]:
            lines += [
                f"**{row['source']}** — "
                f"{'PASS' if row['passed'] else 'FAIL'} "
                f"(whole: {row['whole']}, alone: {row['alone']})",
                "",
                f"- chunk {row['chunk_chars']} chars / file {row['file_chars']} chars",
                f"- chunks from this file: {row['siblings']}",
                "",
                "```",
                row["text"],
                "```",
                "",
            ]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
