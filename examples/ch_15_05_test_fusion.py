# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import as_hits, rrf_ids  # noqa: F401
# ─── листинг ───
from hypothesis import given, strategies as st

rankings = st.lists(st.lists(st.text(min_size=1, max_size=6), max_size=20, unique=True),
                    min_size=1, max_size=4)

@given(rankings)
def test_scale_invariance(lists: list[list[str]]) -> None:
    """Умножение всех оценок источника на положительное число не меняет исход."""
    original = rrf_ids(as_hits(lists, scale=1.0), k=10)
    scaled = rrf_ids(as_hits(lists, scale=137.0), k=10)
    assert original == scaled

@given(rankings)
def test_agreement_wins(lists: list[list[str]]) -> None:
    """Документ, найденный всеми источниками на первом месте, стоит первым."""
    common = "общий"
    lists = [[common] + rest for rest in lists]
    assert rrf_ids(as_hits(lists), k=5)[0] == common
