#!/usr/bin/env python3
"""Вставка блока в главу перед указанным якорем."""
import sys, re

PATH = 'parts/10-body.html'

def insert(chapter_id: str, block: str, anchor: str = '<div class="quiz">') -> None:
    s = open(PATH, encoding='utf-8').read()
    start = s.index(f'<section class="chapter" id="{chapter_id}">')
    end = s.index('</section>', start)
    pos = s.index(anchor, start)
    if pos > end:
        raise SystemExit(f'якорь не найден внутри {chapter_id}')
    out = s[:pos] + block.strip() + '\n\n' + s[pos:]
    open(PATH, 'w', encoding='utf-8').write(out)
    print(f'{chapter_id}: вставлено {len(block)} байт')

if __name__ == '__main__':
    chapter_id = sys.argv[1]
    block = sys.stdin.read()
    insert(chapter_id, block)
