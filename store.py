"""
Stages 3 and 4 of the pipeline: embedding chunks and retrieving them.

Three things in here are worth knowing about, because they'd quietly break the
rest of the project if they were wrong:

1. The Chroma collection is created with cosine distance, explicitly. Chroma
   defaults to squared L2, and the 0.6 threshold the course uses is calibrated
   against cosine. Getting this wrong makes every distance number meaningless.

2. `search` returns the distance alongside each chunk. Milestone 4 has you
   compare distances, so they have to be visible.

3. The embedding model is the one Chroma bundles, not one loaded through
   `sentence-transformers`. It is the same model — `all-MiniLM-L6-v2`, 384
   dimensions — but it arrives as an ONNX build from Chroma's own CDN, so the
   install needs neither PyTorch nor a reachable Hugging Face. See `_embedder`.
"""

import os
import shutil
from dataclasses import dataclass

# Must be set BEFORE chromadb is imported. Without it, some Chroma versions
# print "Failed to send telemetry event ..." on every single call — which looks
# exactly like a real error, isn't one, and cost a previous cohort a lot of
# confused help-channel messages.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import chromadb  # noqa: E402

import config
from chunker import Chunk


@dataclass
class Result:
    """One retrieved chunk and how far it was from the question."""

    text: str
    source: str
    label: str
    distance: float   # LOWER IS BETTER. 0.3 is close, 0.9 is unrelated.
    produced_by: str
    category: str = "other"   # topic facet, see `category_of`


_model = None

# The model Chroma bundles. Anything else in config.EMBEDDING_MODEL means
# "fetch that one from Hugging Face instead" — see `_embedder`.
BUNDLED_MODEL = "all-MiniLM-L6-v2"

# Models embedded over the API rather than on this machine. Stretch feature 3.
# Anything not listed here and not the bundled model is looked for through
# sentence-transformers.
API_MODELS = {"gemini-embedding-001", "text-embedding-004"}


class _OnnxEmbedder:
    """
    Chroma's built-in embedder, wrapped to look like the other two.

    Chroma's embedding functions are called directly and hand back numpy
    arrays. The rest of this file wants `.encode(texts)`, so the adapter lives
    here rather than making every caller care which embedder it got.
    """

    def __init__(self):
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

        self._ef = ONNXMiniLM_L6_V2()

    def encode(self, texts, show_progress_bar: bool = False):
        return [vector.tolist() for vector in self._ef(list(texts))]


class _GeminiEmbedder:
    """
    Stretch feature 3: a second embedding model, called over the API.

    The course's suggested route for this is `sentence-transformers`, which
    brings PyTorch with it — about 2 GB. My connection could not finish that
    download, so I used the other kind of second model instead: a hosted one.
    It needs no download at all, reuses the `GEMINI_API_KEY` that is already in
    `.env`, and is a bigger change than swapping one local MiniLM for another —
    3072 dimensions against the bundled model's 384.

    Two things worth knowing:

    - Embedding calls are NOT the same quota as the answer calls in
      generate.py, and they do not go through its budget guard. Indexing the
      whole corpus is a handful of batched calls, not 88.
    - This is the one embedder here that needs the network at query time too,
      because the question has to be embedded before it can be searched.
    """

    # Well under the API's per-request cap, and it keeps one failure from
    # costing the whole corpus.
    BATCH = 32

    def __init__(self, name: str):
        self._name = name
        self._client = None

    def _get_client(self):
        if self._client is None:
            from google import genai

            key = os.getenv("GEMINI_API_KEY", "").strip()
            if not key:
                raise RuntimeError(
                    f"EMBEDDING_MODEL is {self._name!r}, which is embedded over "
                    f"the API, but there is no GEMINI_API_KEY in your .env."
                )
            self._client = genai.Client(api_key=key)
        return self._client

    def encode(self, texts, show_progress_bar: bool = False):
        texts = list(texts)
        vectors = []
        for start in range(0, len(texts), self.BATCH):
            window = texts[start : start + self.BATCH]
            response = self._get_client().models.embed_content(
                model=self._name, contents=window
            )
            vectors.extend(list(e.values) for e in response.embeddings)
        return vectors


def _sentence_transformer(name: str):
    """
    The escape hatch: any model that isn't the bundled one.

    Unit 2's "try a second embedding model" stretch option comes through here,
    and so does anything you set `EMBEDDING_MODEL` to. This path *does* need
    `sentence-transformers` and a reachable Hugging Face, neither of which the
    default install has — which is the whole point of the default install.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            f"config.EMBEDDING_MODEL is set to {name!r}, which isn't the model "
            f"Chroma bundles ({BUNDLED_MODEL!r}), so it has to be downloaded "
            f"from Hugging Face.\n"
            f"Install the optional dependency first:\n"
            f"    pip install 'sentence-transformers>=3.4,<3.5'\n"
            f"Or set EMBEDDING_MODEL back to {BUNDLED_MODEL!r}."
        ) from exc

    return SentenceTransformer(name)


def _embedder():
    """
    Load the embedding model once and keep it.

    First call is slow — it downloads about 80 MB. That's why setup happens
    before class.
    """
    global _model

    if _model is not None:
        return _model

    # Used only by this repo's own smoke test, which runs where no model can be
    # downloaded at all. Never set this yourself.
    if os.getenv("AI201_FAKE_EMBEDDINGS") == "1":
        from _smoke_embedder import FakeEmbedder

        _model = FakeEmbedder()
    elif config.EMBEDDING_MODEL == BUNDLED_MODEL:
        _model = _OnnxEmbedder()
    elif config.EMBEDDING_MODEL in API_MODELS:
        _model = _GeminiEmbedder(config.EMBEDDING_MODEL)
    else:
        _model = _sentence_transformer(config.EMBEDDING_MODEL)

    return _model


def embed(texts: list[str]) -> list[list[float]]:
    """Turn text into vectors. Runs on your machine, costs no API quota."""
    vectors = _embedder().encode(texts, show_progress_bar=False)
    # sentence-transformers and the smoke stand-in return something with a
    # .tolist(); _OnnxEmbedder has already done that conversion itself.
    return vectors.tolist() if hasattr(vectors, "tolist") else vectors


def _client():
    return chromadb.PersistentClient(
        path=str(config.CHROMA_DIR),
        settings=chromadb.config.Settings(anonymized_telemetry=False),
    )


def category_of(source: str) -> str:
    """The topic facet a source file belongs to.

    Stretch feature 1. Every filename in `campus_life` is prefixed with its
    topic — `dining_pellew_dining_hall.txt`, `housing_aldridge_hall.txt`,
    `course_biol_160.txt`, `admin_add_drop_deadline.txt` — so the prefix is a
    facet that already exists in the corpus rather than one I invented. A file
    with no underscore falls back to "other" instead of being dropped.
    """
    head = source.split("_", 1)[0]
    return head if "_" in source and head else "other"


def build_index(
    chunks: list[Chunk],
    corpus: str | None = None,
    variant: str = "default",
) -> int:
    """
    Embed every chunk and store it.

    `variant` lets you keep more than one index of the same corpus at the same
    time. In unit 2, when you compare two chunking strategies, index the second
    one as variant="v2" and you can query both instead of deleting the first
    and starting over.
    """
    name = config.collection_name(corpus, variant)
    client = _client()

    try:
        client.delete_collection(name)
    except Exception:
        pass

    collection = client.create_collection(
        name=name,
        # ⚠️ Do not remove. Chroma defaults to squared L2, and every distance
        # number in this course assumes cosine.
        metadata={"hnsw:space": "cosine"},
    )

    batch = 256
    for start in range(0, len(chunks), batch):
        window = chunks[start : start + batch]
        collection.add(
            ids=[f"{c.source}#{c.index}" for c in window],
            documents=[c.text for c in window],
            embeddings=embed([c.text for c in window]),
            metadatas=[
                {
                    "source": c.source,
                    "index": c.index,
                    "produced_by": c.produced_by,
                    # Stretch feature 1: the facet `--category` filters on.
                    "category": category_of(c.source),
                }
                for c in window
            ],
        )

    return len(chunks)


def search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
    where: dict | None = None,
) -> list[Result]:
    """
    Retrieve the chunks closest in meaning to a question.

    Returns them nearest-first, each with its distance.

    `where` is stretch feature 1: a Chroma metadata filter, applied before the
    nearest-neighbour search rather than after it, so `top_k` counts matches
    within the filter instead of being eaten by rows that get thrown away.
    Chroma matches metadata by equality, not substring — `{"category":
    "dining"}` or `{"source": "housing_aldridge_hall.txt"}`.
    """
    top_k = top_k or config.TOP_K
    name = config.collection_name(corpus, variant)

    try:
        collection = _client().get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"No index called '{name}'. Run `python app.py index` first."
        ) from exc

    raw = collection.query(
        query_embeddings=embed([question]),
        n_results=min(top_k, collection.count()),
        where=where or None,
    )

    results: list[Result] = []
    for text, meta, distance in zip(
        raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
    ):
        results.append(
            Result(
                text=text,
                source=str(meta.get("source", "unknown")),
                label=f"{meta.get('source', 'unknown')}#{meta.get('index', 0)}",
                distance=float(distance),
                produced_by=str(meta.get("produced_by", "unknown")),
                category=str(meta.get("category", "other")),
            )
        )
    return results


def index_exists(corpus: str | None = None, variant: str = "default") -> bool:
    """Is there an index here to search, without searching it?

    `serve.py`'s health check asks this. It deliberately does not embed
    anything: loading the embedding model takes 80 MB and a few seconds, and a
    health check that heavy is a health check nobody can afford to call.
    """
    try:
        collection = _client().get_collection(config.collection_name(corpus, variant))
        return collection.count() > 0
    except Exception:
        return False


def reset():
    """Delete every index. Occasionally the fastest way out of a mess."""
    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)
