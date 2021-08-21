# coding=utf8
import re
from konlpy.tag import Okt
from collections import defaultdict
import asyncio

okt = Okt()
ready = False


async def find_repeated(input_text):
    bound = int(len(input_text) / 250 + 3)
    preprocessed = okt.pos(input_text)
    repeat_count = defaultdict(int)
    treated = ('Adjective', 'Noun')

    for morph, tag in preprocessed:
        if tag in treated:
            repeat_count[morph] += 1

    words = []    # 중복 사용된 단어 list
    for morph, count in repeat_count.items():
        if count > bound:
            words.append(morph)

    words_idx = []

    for e, i in enumerate(words):
        for j in re.finditer(i, input_text):
            tmp = list(j.span())
            tmp.append(e + 1)
            words_idx.append(tmp)

    return {'words': words,
            'words_idx': words_idx,
            'edit': ['' for _ in range(len(words_idx))],
            'tag': 'repeated'}


if not ready:
    ready = True
    okt.pos("예열")
