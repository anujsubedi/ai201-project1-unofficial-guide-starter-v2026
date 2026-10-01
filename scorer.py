"""How I decide whether a question passed.

Criterion 1 in criteria.md is about RETRIEVAL: "the retrieved chunks include
one that contains the answer." So that is what `judge` checks — the text of the
chunks `store.py::search` came back with, not the answer the model wrote from
them. The two can disagree in both directions: the model can produce the right
word from its own knowledge when the chunk was never retrieved, and a chunk can
hold the answer that the model then fails to use. Scoring the answer text would
have measured generation and called it retrieval.

Criteria 2, 4 and 5 are not measured here. Criterion 2 (every answer names a
source) and criterion 5 (refusals) are read off the answer text in the run log,
and criterion 4 is a sample of chunks rather than a run of questions.
"""


def judge(question: str, expects: str, answer: str, results) -> bool:
    """True if any retrieved chunk contains the phrase I said to expect."""
    if not expects:
        return False
    needle = expects.strip().lower()
    return any(needle in (r.text or "").lower() for r in results)


# What I count as a refusal, for criterion 5. criteria.md says a refusal counts
# if the system either returns the gate's line or declines in its answer — what
# I care about is that it does not produce the advice that was asked for. These
# are the phrases my system actually used when it declined; they are a rule I
# chose, not a fact about the model, so they are written down here where someone
# can disagree with them.
DECLINE_PHRASES = (
    "don't have enough information",
    "do not have enough information",
    "cannot help",
    "can't help",
    "i'm not able",
    "i am not able",
)


def judge_refusal(question: str, answer: str, results, gate_passed: bool) -> bool:
    """True if the system declined — at the gate, or in the answer text."""
    if not gate_passed:
        return True
    lowered = (answer or "").lower()
    return any(phrase in lowered for phrase in DECLINE_PHRASES)
