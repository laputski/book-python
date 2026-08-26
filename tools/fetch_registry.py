#!/usr/bin/env python3
"""Fetch the RAG World registry summary for drift checks and the build.

Writes data/registry_meta.json: the registry build date, the fetch date,
and the maturity level of every record. Exits with 0 when nothing changed
and with 3 when the data changed (the signal for an auto-commit).
"""
import json
import pathlib
import ssl
import sys
import urllib.request

URL = "https://ragworld.org/data/registry.json"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "registry_meta.json"


def tls_context() -> ssl.SSLContext:
    """The system trust store, falling back to certifi when it is empty.

    Python.org builds on macOS ship without root certificates until
    Install Certificates.command has been run; certifi covers that case.
    """
    context = ssl.create_default_context()
    if context.cert_store_stats()["x509_ca"] == 0:
        import certifi
        context = ssl.create_default_context(cafile=certifi.where())
    return context


def level_of(record: dict) -> str | None:
    raw = record.get("level")
    return raw.get("level") if isinstance(raw, dict) else raw


def main() -> int:
    with urllib.request.urlopen(URL, timeout=30, context=tls_context()) as resp:
        registry = json.load(resp)
    meta = {
        "built_at": registry["built_at"],
        "count": registry["count"],
        "levels": {r["id"]: level_of(r) for r in registry["technologies"]},
    }
    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    changed = {k: meta[k] for k in ("built_at", "count", "levels")} != \
              {k: previous.get(k) for k in ("built_at", "count", "levels")}
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(f"registry: build {meta['built_at']}, {meta['count']} records, "
          f"{'changed' if changed else 'unchanged'}")
    return 3 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
