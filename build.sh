#!/bin/sh
# Сборка пособия: каркас, русская локаль, английская локаль, сценарий.
cd "$(dirname "$0")"
{
  cat parts/00-head.html
  printf '\n<div class="locale" data-locale="ru">\n'
  cat parts/10-body.html
  printf '\n</div>\n<div class="locale" data-locale="en">\n'
  if [ -f parts/20-body-en.html ]; then cat parts/20-body-en.html; fi
  printf '\n</div>\n'
  cat parts/99-tail.html
} > rag-python-advanced.html
echo "собрано: $(wc -c < rag-python-advanced.html) байт"
