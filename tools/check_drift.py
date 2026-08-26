#!/usr/bin/env python3
"""The book's staleness detector.

Checks three things and prints a markdown report:
  1. Registry maturity levels against what the book claims
     (data/anchors.json against data/registry_meta.json).
  2. The Python release lifecycle against the book's baseline version
     (endoflife.date against data/anchors.json).
  3. The availability of the assembled book's external links.

Exit codes: 0 — no drift; 4 — drift found, report on stdout.
The script never edits the book's text: prose changes are a human's call.
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
        actual = levels.get(record_id, "record missing")
        if actual == claim["level"]:
            continue
        chapters = ", ".join(str(c) for c in claim["chapters"])
        report.append(
            f"- **{record_id}**: the book claims {claim['level']}, "
            f"the registry gives {actual} (role: {claim['kind']}; chapters {chapters})")
        if claim["kind"] == "anchor" and str(actual) < "L2":
            report.append(
                "  - the record no longer satisfies the anchor rule (L2 and above): "
                "the prose needs editing, not a digit swap")


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
                f"- Python {name} is out (released {cycle.get('releaseDate')}): "
                f"the book mentions nothing newer than {known}; "
                f"revisit Chapter 1 and Appendix E")
        if name == baseline:
            support = str(cycle.get("support") or "")
            if support and support < today:
                report.append(
                    f"- the baseline Python {baseline} left active support "
                    f"({support}): revisit the baseline choice in Section 0.3")


class LinkCollector(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":          # preconnect and stylesheet roots answer 404; skip them
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
                    report.append(f"- link answers {resp.status}: {url}")
        except urllib.error.HTTPError as err:
            if err.code == 405:  # HEAD forbidden, yet the address is alive
                continue
            report.append(f"- link answers {err.code}: {url}")
        except Exception as err:
            report.append(f"- link unreachable ({err.__class__.__name__}): {url}")


def main() -> int:
    report: list[str] = []
    check_levels(report)
    check_python(report)
    if "--no-links" not in sys.argv:
        check_links(report)
    if not report:
        print("no drift")
        return 0
    print("## Staleness detected\n")
    print("\n".join(report))
    print("\nThe book's text was not modified: each item above needs an edit.")
    return 4


if __name__ == "__main__":
    sys.exit(main())
