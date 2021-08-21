# coding=utf8
import asyncio

async def final_return(repeated, plural, passive, original_text):
    if len(original_text.rstrip()) == 0:
        return ''

    result = {'html' : original_text}
    indexs = sorted([x + [plural['tag']] for x in plural['words_idx']] + [x + [repeated['tag']] for x in repeated['words_idx']] + [x + [passive['tag']] for x in passive['words_idx']])
    length_weight = 0

    for front, back, num, tag in indexs:
        tag_front = '<span name = "{}{}">'.format(tag, num)
        tag_back = '</span>'
        result['html'] = result['html'][:front + length_weight] + tag_front + result['html'][front + length_weight:back + length_weight] + tag_back + result['html'][back + length_weight:]
        length_weight += len(tag_front) + len(tag_back)

    return result['html']