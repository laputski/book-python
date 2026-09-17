<div align="center">

<img src="assets/logo.svg" width="140" alt="Advanced Python for RAG">

# Advanced Python for RAG

**A bilingual, single-file browser textbook on the Python mechanisms that
hybrid, graph, adaptive, and agentic retrieval systems stand on.**

[![ci](https://github.com/laputski/book-python/actions/workflows/ci.yml/badge.svg)](https://github.com/laputski/book-python/actions/workflows/ci.yml)
[![deploy](https://github.com/laputski/book-python/actions/workflows/deploy.yml/badge.svg)](https://github.com/laputski/book-python/actions/workflows/deploy.yml)
[![weekly](https://github.com/laputski/book-python/actions/workflows/weekly.yml/badge.svg)](https://github.com/laputski/book-python/actions/workflows/weekly.yml)
[![site](https://img.shields.io/badge/read-python.ragworld.org-0072B2)](https://python.ragworld.org)
[![python](https://img.shields.io/badge/python-3.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://python.ragworld.org)
[![languages](https://img.shields.io/badge/languages-EN%20%7C%20RU-555)](https://python.ragworld.org)
[![data](https://img.shields.io/badge/registry%20data-CC%20BY%204.0-97CA00)](https://ragworld.org)

**[Read it at python.ragworld.org →](https://python.ragworld.org)**

*Читайте документацию репозитория по-русски: [README.ru.md](README.ru.md)*

</div>

---

Fifteen chapters, five appendices, sixteen hand-drawn SVG diagrams, and
103 tool-verified code listings in one self-contained HTML file. A language
switch (EN/RU), three reading-depth levels, full-text search, term popovers,
print-to-PDF, day/night themes. Every chapter is anchored to a real
architecture from the [RAG World registry](https://ragworld.org), with its
maturity level stated and machine-checked.

## Repository layout

| Path | Purpose |
| --- | --- |
| `rag-python-advanced.html` | the assembled book; a build artifact, committed |
| `parts/` | sources: shell, Russian locale, English locale, page script |
| `build.sh` | assembles the book, substituting the registry build date |
| `examples/` | listings of both locales extracted from the book, plus typed stubs |
| `check_examples.sh` | full listing verification: parse, ruff, mypy |
| `data/anchors.json` | what the book claims about registry records and Python versions |
| `data/registry_meta.json` | RAG World registry summary as of the last sync |
| `tools/fetch_registry.py` | fetches the registry summary |
| `tools/check_drift.py` | staleness detector: levels, Python lifecycle, links |

## Working locally

```sh
./build.sh            # reassemble the book after editing parts/
./check_examples.sh   # extract the listings and run every check
python3 tools/check_drift.py   # sync check: registry, Python versions, links
```

Preview: `python3 -m http.server 8731`, then open
`http://localhost:8731/rag-python-advanced.html`.

## Deployment

GitHub Pages, deployed by `.github/workflows/deploy.yml` on every push to
`main`. The `python.ragworld.org` domain is bound automatically by the same
workflow; on the DNS side a single CNAME record `book → laputski.github.io`
is required. Enforce HTTPS in Settings → Pages once the certificate is issued.

## Self-updating

The rule: **data updates automatically, prose changes only through review.**

- `ci.yml` — on every push: the build is reproducible, and the listings of
  both locales pass parsing, ruff, and mypy on Python 3.13, 3.14, and the
  3.15 prerelease.
- `weekly.yml` — on Mondays, manually, or on a `registry-updated` event from
  rag-world: fetches the registry summary; on change, commits the data and
  redeploys the site (only the sync date in Appendix E.4 changes in the
  text); the staleness detector compares maturity levels, the Python release
  lifecycle, and external links, and opens a `drift`-labelled issue when they
  diverge — a human lands the prose fix through a PR.
- Scheduled workflows on public repositories go dormant after 60 days
  without commits; the workflow leaves a sync mark if the quiet stretch
  exceeds 45 days.

To have the book update the day the registry updates rather than on Mondays,
add one step to the rag-world data-pass workflow:

```yaml
- name: Notify the book
  env:
    GH_TOKEN: ${{ secrets.BOOK_DISPATCH_TOKEN }}   # fine-grained, repo book-python, contents:write
  run: gh api repos/laputski/book-python/dispatches -f event_type=registry-updated
```

## Licensing

RAG World registry data is distributed under CC BY 4.0 and is used with
attribution. The licence for the book's text has not been chosen yet.

*Note: code comments inside the book's Russian-locale listings are in
Russian by design — they are part of the Russian text of the textbook.
The English locale carries the same listings with English comments.*
