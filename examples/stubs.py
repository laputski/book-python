"""Вспомогательные имена для листингов учебника.

Листинги опираются на имена, реализация которых к предмету не относится:
типы предметной модели, обращения к внешним службам, разбиение текста на
предложения. Здесь они объявлены с настоящими типами, чтобы проверка типов
проверяла листинги по существу, а не обходила их стороной.

Файл сопровождается вручную вместе с extract_examples.py и в пособие не входит.
"""

from __future__ import annotations

import asyncio
import contextvars
import hashlib
import logging
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Iterator, Sequence
from contextlib import aclosing, asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from typing import Any, ClassVar, Literal, Protocol, Self, runtime_checkable

import numpy as np
import pytest
from pydantic import BaseModel as _BaseModel

# ─── Предметная модель ────────────────────────────────────────────────────────

UnitKind = Literal["passage", "proposition", "entity", "node_edge",
                   "page_image", "table_row", "summary_node"]


@dataclass(frozen=True, slots=True)
class Sentence:
    doc_id: str
    text: str
    start: int = 0
    end: int = 0


@dataclass(frozen=True, slots=True)
class Chunk:
    id: str
    doc_id: str
    text: str
    context: str = ""
    start: int = 0
    end: int = 0

    @property
    def embedding_input(self) -> str:
        return f"{self.context}\n\n{self.text}" if self.context else self.text

    @property
    def token_cost(self) -> int:
        return len(self.text) // 4

    @classmethod
    def from_sentences(cls, sentences: Sequence[Sentence]) -> Chunk:
        raise NotImplementedError

    def as_dict(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Scored:
    chunk: Chunk
    score: float
    source: str
    kind: UnitKind = "passage"


@dataclass(frozen=True, slots=True)
class DenseHit(Scored):
    pass


@dataclass(frozen=True, slots=True)
class LexicalHit(Scored):
    pass


@dataclass(frozen=True, slots=True)
class GraphHit(Scored):
    path: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Fused:
    chunk_id: str
    score: float
    sources: list[str]


@dataclass(frozen=True, slots=True)
class Query:
    text: str
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Cited:
    text: str
    sources: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Answer:
    text: str = ""
    partial: bool = False


@dataclass(frozen=True, slots=True)
class Node:
    id: str
    text: str
    token_cost: int = 0

    @classmethod
    def leaf(cls, chunk: Chunk) -> Node:
        raise NotImplementedError

    @classmethod
    def summary(cls, text: str) -> Node:
        raise NotImplementedError


class Tree:
    def __init__(self, leaves: Sequence[Node]) -> None: ...
    def add_level(self, level: Sequence[Node]) -> None: ...


@dataclass(frozen=True, slots=True)
class Budget:
    steps: int = 4
    tokens: int = 12_000
    spent_steps: int = 0
    spent_tokens: int = 0

    @property
    def exhausted(self) -> bool:
        return self.spent_steps >= self.steps or self.spent_tokens >= self.tokens


@dataclass(frozen=True, slots=True)
class Classify:
    kind: Literal["classify"] = "classify"
    question: str = ""


@dataclass(frozen=True, slots=True)
class Retrieve:
    kind: Literal["retrieve"] = "retrieve"
    query: str = ""
    context: tuple[Scored, ...] = ()


@dataclass(frozen=True, slots=True)
class Generate:
    kind: Literal["generate"] = "generate"
    context: tuple[Scored, ...] = ()


@dataclass(frozen=True, slots=True)
class Critique:
    kind: Literal["critique"] = "critique"
    draft: str = ""
    context: tuple[Scored, ...] = ()


State = Classify | Retrieve | Generate | Critique | Answer


class DraftScore(_BaseModel):
    draft_index: int
    supported: bool
    score: float
    problem: str | None = None


# ─── Внешние службы ───────────────────────────────────────────────────────────


class Retriever(Protocol):
    async def retrieve(self, query: str, k: int) -> list[Scored]: ...


class DenseRetriever:
    def __init__(self, name: str) -> None: ...

    async def retrieve(self, query: str, k: int) -> list[Scored]:
        raise NotImplementedError


class Bm25Retriever(DenseRetriever): ...
class GraphRetriever(DenseRetriever): ...


class FakeRetriever(DenseRetriever):
    def __init__(self, corpus: dict[str, str], fail_after: int | None = None) -> None: ...


class DenseIndex:
    matrix: np.ndarray
    codes: np.ndarray

    def search(self, query: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError


class VectorStore:
    def search(self, vector: np.ndarray, k: int) -> list[Scored]:
        raise NotImplementedError

    async def asearch(self, vector: np.ndarray, k: int) -> list[Scored]:
        raise NotImplementedError


class LexicalIndex:
    def search(self, query: str, k: int) -> list[Scored]:
        raise NotImplementedError

    async def asearch(self, query: str, k: int) -> list[Scored]:
        raise NotImplementedError


class Reranker:
    def rank(self, query: str, hits: Sequence[Scored]) -> list[Scored]:
        raise NotImplementedError


class Transaction:
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


class GraphStore:
    async def begin(self) -> Transaction:
        raise NotImplementedError


class Graph:
    def neighbors(self, node_id: str) -> Iterable[str]:
        raise NotImplementedError

    def node(self, node_id: str) -> Node:
        raise NotImplementedError

    def rank_neighbours(self, node_id: str, limit: int) -> list[tuple[str, float]]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Prompt:
    text: str = ""

    def continued(self, written: str) -> Prompt:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str

    @staticmethod
    def user(text: str) -> Message:
        raise NotImplementedError

    @staticmethod
    def assistant(text: str) -> Message:
        raise NotImplementedError


class Model:
    async def complete(self, prompt: Any, response_schema: Any = None) -> str:
        raise NotImplementedError

    def stream(self, prompt: Any) -> Any:
        raise NotImplementedError


class Span:
    def __enter__(self) -> Span: ...
    def __exit__(self, *exc: object) -> None: ...
    def end(self) -> None: ...


class Tracer:
    def span(self, name: str) -> Span:
        raise NotImplementedError

    def start(self, name: str) -> Span:
        raise NotImplementedError


class Pool:
    def acquire(self) -> Any:
        raise NotImplementedError

    async def release(self, conn: object) -> None: ...


class Tool:
    registry: ClassVar[dict[str, type[Tool]]] = {}
    name: str = ""
    description: str = ""

    async def run(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError


class SearchTool(Tool): ...
class GraphTool(Tool): ...
class SqlTool(Tool): ...


class Settings:
    url: str = ""


# ─── Исключения ───────────────────────────────────────────────────────────────


class RagError(Exception): ...
class ServiceUnavailable(RagError): ...
class RerankerUnavailable(RagError): ...
class TransientModelError(RagError): ...


class SourceUnavailable(RagError):
    def __init__(self, source: str = "") -> None:
        super().__init__(source)
        self.source = source


class SourceError(RagError):
    def __init__(self, source: str, cause: BaseException) -> None:
        super().__init__(f"источник {source} отказал: {cause}")
        self.source = source


class DegradedSearch(RagError):
    def __init__(self, failed: Sequence[str]) -> None:
        super().__init__(", ".join(failed))


class OutputContractError(RagError):
    def __init__(self, schema: str, raw: str) -> None:
        super().__init__(schema)


# ─── Постоянные величины ──────────────────────────────────────────────────────

DECAY: float = 0.8
THRESHOLD: float = 0.7
HYDE_PROMPT: str = "Напишите правдоподобный ответ на вопрос: {question}"
SENTINEL: str = "\x00"
SAMPLE_CORPUS: dict[str, str] = {}
PROMPT_VERSION: str = "0"
RETRYABLE: tuple[type[BaseException], ...] = (TimeoutError, ConnectionError, ServiceUnavailable)

# ─── Обращения, реализация которых к предмету не относится ────────────────────


def read_text(path: str) -> str: raise NotImplementedError
def normalize(text: str) -> str: raise NotImplementedError
def split_sentences(doc_id: str, text: str) -> Iterator[Sentence]: raise NotImplementedError
def find_sentence_end(buffer: str) -> int | None: raise NotImplementedError
def make_windows(sentences: Sequence[Sentence], size: int, overlap: int) -> Iterator[list[Sentence]]: raise NotImplementedError
def segment_file(path: str) -> Iterator[Chunk]: raise NotImplementedError
def cluster(matrix: np.ndarray, target_size: int) -> list[list[int]]: raise NotImplementedError
def summarize(nodes: Sequence[Node]) -> str: raise NotImplementedError
def embed(query: str) -> np.ndarray: raise NotImplementedError
def embed_one(text: str) -> np.ndarray: raise NotImplementedError
def embed_batch(texts: Sequence[str]) -> np.ndarray: raise NotImplementedError
async def search(query: str, k: int = 20, sources: Sequence[str] = ()) -> list[Scored]: raise NotImplementedError
async def retrieve(query: str) -> list[Scored]: raise NotImplementedError
async def generate(*args: Any, **kwargs: Any) -> str: raise NotImplementedError
async def rerank(query: str, hits: Sequence[Scored]) -> list[Scored]: raise NotImplementedError
async def compose(question: str, hits: Sequence[Scored], degraded: Sequence[str] = ()) -> Answer: raise NotImplementedError
def explain(error: Exception) -> str: raise NotImplementedError
async def route(question: str) -> Literal["simple", "single", "multi"]: raise NotImplementedError
def classify(question: str) -> str: raise NotImplementedError
def rewrite(question: str, draft: str) -> str: raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Groundedness:
    ok: bool
    probe: str = ""


async def grounded(draft: str, context: Sequence[Scored]) -> Groundedness: raise NotImplementedError
def spend(budget: Budget, steps: int = 0, tokens: int = 0) -> Budget: raise NotImplementedError
async def step(state: State, budget: Budget) -> tuple[State, Budget]: raise NotImplementedError
def build_prompt(question: str, context: Sequence[Scored], written: Sequence[str]) -> Prompt: raise NotImplementedError
def attach_citations(sentence: str, context: Sequence[Scored]) -> Cited: raise NotImplementedError
def strip_uncertain_spans(sentence: str) -> str: raise NotImplementedError
def sentences_with_confidence(parts: Any) -> AsyncIterator[tuple[str, float]]: raise NotImplementedError
def finish_without_lookahead(question: str, context: Sequence[Scored], written: Sequence[str]) -> AsyncIterator[str]: raise NotImplementedError
def render(hits: Sequence[Scored]) -> str: raise NotImplementedError
def render_context(chunks: Sequence[Chunk]) -> str: raise NotImplementedError
async def call_tool(name: str, args: dict[str, Any]) -> str: raise NotImplementedError
def json_schema_for(annotation: Any) -> dict[str, Any]: raise NotImplementedError
def wrap_public_methods(cls: type) -> None: raise NotImplementedError
def temporary_file() -> Any: raise NotImplementedError
def healthy_only(sources: dict[str, Retriever]) -> dict[str, Retriever]: raise NotImplementedError
async def fan_out(sources: dict[str, Retriever], query: str, k: int, budget: float = 1.5, limit: int = 8) -> Any: raise NotImplementedError
async def run_search(conn: object, tx: Transaction, query: str, dump_to: Any = None) -> list[Scored]: raise NotImplementedError
def reciprocal_rank_fusion(rankings: Sequence[Sequence[Scored]]) -> list[Scored]: raise NotImplementedError
def merge(*parts: Any) -> Any: raise NotImplementedError
def as_hits(lists: Sequence[Sequence[str]], scale: float = 1.0) -> list[list[Scored]]: raise NotImplementedError
def rrf_ids(rankings: Sequence[Sequence[Scored]], k: int = 10) -> list[str]: raise NotImplementedError
async def serve() -> None: raise NotImplementedError
async def main() -> None: raise NotImplementedError

# ─── Долгоживущие объекты ─────────────────────────────────────────────────────

vector_store = VectorStore()
bm25_index = LexicalIndex()
reranker = Reranker()
graph: Any = GraphStore()
model = Model()
tracer = Tracer()
pool = Pool()
settings = Settings()
log = logging.getLogger("rag")
request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")

# ─── Имена окружения, на которые опираются выдержки ───────────────────────────

query: str = ""
question: str = ""
prompt: Prompt = Prompt()
k: int = 20
vector: np.ndarray = np.zeros(128, dtype=np.float32)
queries: np.ndarray = np.zeros((32, 128), dtype=np.float32)
matrix: np.ndarray = np.zeros((1000, 128), dtype=np.float32)
scores: np.ndarray = np.zeros(1000, dtype=np.float32)
weights: np.ndarray = np.ones(1000, dtype=np.float32)
bias: np.ndarray = np.zeros(1000, dtype=np.float32)
freshness: np.ndarray = np.zeros(1000, dtype=np.float32)
index: DenseIndex = DenseIndex()
dense: Any = DenseRetriever("dense")
lexical: Any = DenseRetriever("lexical")
dense_hits: list[Scored] = []
lexical_hits: list[Scored] = []
sources: dict[str, Retriever] = {}
retrieved: list[Scored] = []
payload: Any = {}   # разбираемый ответ модели: может быть и отображением, и списком
kind: str = ""
module: Any = None
dense_source: Retriever = DenseRetriever("dense")
lexical_source: Retriever = DenseRetriever("lexical")
hyde: Retriever = DenseRetriever("hyde")
sentences: Any = None
