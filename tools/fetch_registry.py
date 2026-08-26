#!/usr/bin/env python3
"""Забирает сводку реестра RAG World для сверки и подстановки при сборке.

Пишет data/registry_meta.json: дату сборки реестра, дату забора и уровни
зрелости всех записей. Возвращает код 0, если данные не изменились,
и 3, если изменились (сигнал для автокоммита).
"""
import json
import pathlib
import ssl
import sys
import urllib.request

URL = "https://ragworld.org/data/registry.json"


def tls_context() -> ssl.SSLContext:
    """Системное хранилище сертификатов, а при его отсутствии certifi.

    Питон с python.org на macOS поставляется без корневых сертификатов,
    пока не запущен Install Certificates.command; certifi закрывает этот случай.
    """
    context = ssl.create_default_context()
    if context.cert_store_stats()["x509_ca"] == 0:
        import certifi
        context = ssl.create_default_context(cafile=certifi.where())
    return context
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "registry_meta.json"


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
    print(f"реестр: сборка {meta['built_at']}, записей {meta['count']}, "
          f"{'изменился' if changed else 'без изменений'}")
    return 3 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
