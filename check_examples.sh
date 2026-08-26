#!/bin/sh
# Extract the listings from the assembled book and verify them with tools.
set -e
cd "$(dirname "$0")"
python3 extract_examples.py
python3 -c '
import ast, pathlib, sys
bad = 0
for f in sorted(pathlib.Path("examples").glob("*.py")):
    try:
        ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    except SyntaxError as e:
        bad += 1
        print(f"{f.name}:{e.lineno}: {e.msg}")
print(f"syntax check: {bad} errors")
sys.exit(1 if bad else 0)'
ruff check --select E9,F63,F7,F82,B,SIM,RUF,PIE,C4,PERF \
  --ignore F821,F704,F706,F401,RUF001,RUF002,RUF003,SIM105,PERF203,PIE790,RUF005,RUF023,B905 \
  --output-format concise examples
python3 prepare_examples.py
python3 -m mypy --config-file examples/mypy.ini examples
