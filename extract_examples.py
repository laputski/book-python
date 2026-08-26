#!/usr/bin/env python3
"""Extract the book's listings into separate files for tool verification."""
import html
import pathlib
import re

SRC = pathlib.Path("rag-python-advanced.html")
OUT = pathlib.Path("examples")

FIGURE = re.compile(r'<figure class="code"[^>]*>(.*?)</figure>', re.S)
CHAPTER = re.compile(r'<section class="chapter" id="([^"]+)"')
FILENAME = re.compile(r'<span class="file">([^<]+)</span>')
CODE = re.compile(r"<pre><code>(.*?)</code></pre>", re.S)


def chapters(text: str):
    marks = [(m.start(), m.group(1)) for m in CHAPTER.finditer(text)]
    def at(pos: int) -> str:
        current = "intro"
        for start, name in marks:
            if start <= pos:
                current = name
            else:
                break
        return current
    return at


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    where = chapters(text)
    en_start = text.find('<div class="locale" data-locale="en">')
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.py"):
        if old.name != "stubs.py":       # the stubs are maintained by hand
            old.unlink()

    counters: dict[str, int] = {}
    written = 0
    for match in FIGURE.finditer(text):
        body = match.group(1)
        code = CODE.search(body)
        if not code:
            continue
        source = html.unescape(code.group(1)).strip("\n")
        chapter = where(match.start())
        locale_key = ("en:" if 0 <= en_start <= match.start() else "ru:") + chapter
        counters[locale_key] = counters.get(locale_key, 0) + 1
        named = FILENAME.search(body)
        stem = named.group(1).rsplit("/", 1)[-1].removesuffix(".py") if named else "listing"
        stem = re.sub(r"[^a-z0-9_]", "_", stem.lower())
        prefix = "en_" if 0 <= en_start <= match.start() else ""
        path = OUT / f"{prefix}{chapter.replace('-', '_')}_{counters[locale_key]:02d}_{stem}.py"
        path.write_text(source + "\n", encoding="utf-8")
        written += 1
    print(f"listings extracted: {written}")


if __name__ == "__main__":
    main()
