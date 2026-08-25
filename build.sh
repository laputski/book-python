#!/bin/sh
cd "$(dirname "$0")"
cat parts/00-head.html parts/10-body.html parts/99-tail.html > rag-python-advanced.html
echo "собрано: $(wc -c < rag-python-advanced.html) байт, $(grep -c 'class="chapter"' rag-python-advanced.html) разделов"
