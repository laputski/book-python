#!/usr/bin/env python3
"""Детектор устаревания учебника.

Сверяет три вещи и печатает markdown-отчёт:
  1. Уровни зрелости записей реестра против того, что утверждает учебник
     (data/anchors.json против data/registry_meta.json).
  2. Жизненный цикл версий Python против базовой версии учебника
     (endoflife.date против data/anchors.json).
  3. Доступность внешних ссылок собранного пособия.

Код возврата: 0 — дрейфа нет; 4 — дрейф найден, отчёт в stdout.
Текст пособия скрипт не меняет никогда: решение о правке принимает человек.
"""
import datetime
import html.parser
import json
import pathlib
import ssl
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EOL_URL = "https://endoflife.date/api/python.json"


def tls_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    if context.cert_store_stats()["x509_ca"] == 0:
        import certifi
        context = ssl.create_default_context(cafile=certifi.where())
    return context


def check_levels(report: list[str]) -> None:
    anchors = json.loads((ROOT / "data" / "anchors.json").read_text(encoding="utf-8"))
    meta = json.loads((ROOT / "data" / "registry_meta.json").read_text(encoding="utf-8"))
    levels = meta["levels"]
    for record_id, claim in anchors["claims"].items():
        actual = levels.get(record_id, "запись отсутствует")
        if actual == claim["level"]:
            continue
        chapters = ", ".join(str(c) for c in claim["chapters"])
        report.append(
            f"- **{record_id}**: учебник утверждает {claim['level']}, "
            f"реестр даёт {actual} (роль: {claim['kind']}; главы {chapters})")
        if claim["kind"] == "anchor" and str(actual) < "L2":
            report.append(
                "  - запись перестала удовлетворять правилу опорных (L2 и выше): "
                "нужна редакция текста, а не замена цифры")


def check_python(report: list[str]) -> None:
    anchors = json.loads((ROOT / "data" / "anchors.json").read_text(encoding="utf-8"))
    with urllib.request.urlopen(EOL_URL, timeout=30, context=tls_context()) as resp:
        cycles = json.load(resp)
    known = anchors["python_mentioned_max"]
    baseline = anchors["python_baseline"]
    today = datetime.date.today().isoformat()
    for cycle in cycles:
        name = str(cycle["cycle"])
        if name.startswith("3.") and int(name[2:]) > int(known[2:]):
            report.append(
                f"- вышла версия Python {name} (релиз {cycle.get('releaseDate')}): "
                f"учебник упоминает версии не новее {known}; пересмотреть главу 1 и приложение E")
        if name == baseline:
            support = str(cycle.get("support") or "")
            if support and support < today:
                report.append(
                    f"- базовая версия Python {baseline} вышла из активной поддержки "
                    f"({support}): пересмотреть выбор базовой версии в разделе 0.3")


class LinkCollector(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":          # preconnect и стили не проверяются: корни отвечают 404
            return
        for name, value in attrs:
            if name == "href" and value and value.startswith("https://"):
                self.urls.add(value)


def check_links(report: list[str]) -> None:
    page = (ROOT / "rag-python-advanced.html").read_text(encoding="utf-8")
    collector = LinkCollector()
    collector.feed(page)
    context = tls_context()
    for url in sorted(collector.urls):
        request = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "book-linkcheck"})
        try:
            with urllib.request.urlopen(request, timeout=20, context=context) as resp:
                if resp.status >= 400:
                    report.append(f"- ссылка отвечает {resp.status}: {url}")
        except urllib.error.HTTPError as err:
            if err.code == 405:  # HEAD запрещён, но адрес жив
                continue
            report.append(f"- ссылка отвечает {err.code}: {url}")
        except Exception as err:
            report.append(f"- ссылка недоступна ({err.__class__.__name__}): {url}")


def main() -> int:
    report: list[str] = []
    check_levels(report)
    check_python(report)
    if "--no-links" not in sys.argv:
        check_links(report)
    if not report:
        print("дрейфа нет")
        return 0
    print("## Обнаружено устаревание\n")
    print("\n".join(report))
    print("\nТекст пособия не изменён: каждое из перечисленного требует редакции.")
    return 4


if __name__ == "__main__":
    sys.exit(main())
