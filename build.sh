#!/bin/sh
# Assemble the book: shell, Russian locale, English locale, page script.
# The {{REGISTRY_BUILT_AT}} placeholder is filled from data/registry_meta.json.
cd "$(dirname "$0")"
BUILT_AT=$(python3 -c "import json; print(json.load(open('data/registry_meta.json'))['built_at'])")
{
  cat parts/00-head.html
  printf '\n<div class="locale" data-locale="ru">\n'
  cat parts/10-body.html
  printf '\n</div>\n<div class="locale" data-locale="en">\n'
  if [ -f parts/20-body-en.html ]; then cat parts/20-body-en.html; fi
  printf '\n</div>\n'
  cat parts/99-tail.html
} | sed "s/{{REGISTRY_BUILT_AT}}/$BUILT_AT/g" > rag-python-advanced.html
echo "built: $(wc -c < rag-python-advanced.html) bytes, registry of $BUILT_AT"
