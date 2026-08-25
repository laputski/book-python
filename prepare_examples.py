#!/usr/bin/env python3
"""Готовит извлечённые листинги к проверке типов.

Выдержки, у которых await или return стоят на верхнем уровне, оборачиваются в
функцию: без этого их нельзя откомпилировать, а значит и проверить. Затем к
каждому файлу дописывается импорт тех имён, реализация которых вынесена в
заглушки. Сами листинги в пособии при этом не меняются.
"""
import json
import pathlib
import subprocess
import textwrap

OUT = pathlib.Path("examples")
HEADER = "# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.\n"
MARK = "# ─── листинг ───\n"


def undefined_names() -> dict[str, list[str]]:
    raw = subprocess.run(
        ["ruff", "check", "--select", "F821", "--output-format", "json", str(OUT)],
        capture_output=True, text=True).stdout
    found: dict[str, set[str]] = {}
    for item in json.loads(raw) if raw.strip() else []:
        message = item["message"]
        if not message.startswith("Undefined name `"):
            continue
        name = message.split("`")[1]
        found.setdefault(pathlib.Path(item["filename"]).name, set()).add(name)
    return {k: sorted(v) for k, v in found.items()}


def wrap_if_needed() -> int:
    wrapped = 0
    for path in sorted(OUT.glob("*.py")):
        if path.name == "stubs.py":
            continue
        source = path.read_text(encoding="utf-8")
        try:
            compile(source, str(path), "exec")
        except SyntaxError:
            body = textwrap.indent(source.rstrip("\n"), "    ")
            path.write_text("from typing import Any\n\n\nasync def _excerpt() -> Any:\n" + body + "\n", encoding="utf-8")
            wrapped += 1
    return wrapped


def inject_imports(names: dict[str, list[str]]) -> int:
    touched = 0
    for path in sorted(OUT.glob("*.py")):
        if path.name == "stubs.py":
            continue
        needed = names.get(path.name, [])
        if not needed:
            continue
        source = path.read_text(encoding="utf-8")
        line = "from stubs import " + ", ".join(needed) + "  # noqa: F401\n"
        path.write_text(HEADER + line + MARK + source, encoding="utf-8")
        touched += 1
    return touched


def main() -> None:
    print("обёрнуто выдержек:", wrap_if_needed())
    print("файлов с импортом заглушек:", inject_imports(undefined_names()))
    left = undefined_names()
    left.pop("stubs.py", None)
    if left:
        print("осталось неопределённым:")
        for name, items in sorted(left.items()):
            print(" ", name, items)
    else:
        print("неопределённых имён не осталось")


if __name__ == "__main__":
    main()
