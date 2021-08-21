from konlpy.tag import Kkma
from jamo import h2j, j2hcj, j2h
import asyncio

kma = Kkma()
ready = False

async def get_pos(word):
    return kma.pos(word)

async def chang_josa(previous_letter, josa):
    changer_vowel = ('와', '를', '가', '는')
    changer_conso = ('과', '을', '이', '은')
    bot_conso = "ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄹ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅄ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ".split()
    bot = j2hcj(h2j(previous_letter))[-1]

    if bot in bot_conso:
        if josa in changer_vowel:
            return changer_conso[changer_vowel.index(josa)]
        else:
            return josa
    else:
        if josa in changer_conso:
            return changer_vowel[changer_conso.index(josa)]
        else:
            return josa


async def remove_double_plural(input_text):
    # 이중 복수 제거 함수
    if len(input_text.rstrip()) == 0:
        return {'words': [], 'words_idx': [], 'edit':  [], 'tag': 'plural'}

    plural_table = ((('수많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNG'), ('들', 'XSN')),
                    (('수많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNP'), ('들', 'XSN')),
                    (('수많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'UN'), ('들', 'XSN')),
                    (('많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNG'), ('들', 'XSN')),
                    (('많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNP'), ('들', 'XSN')),
                    (('많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'UN'), ('들', 'XSN')),
                    (('여러', 'MDT'), ('<_AL_>', 'NNG'), ('들', 'XSN')),
                    (('여러', 'MDT'), ('<_AL_>', 'NNP'), ('들', 'XSN')),
                    (('여러', 'MDT'), ('<_AL_>', 'UN'), ('들', 'XSN')),
                    (('무리', 'NNG'), ('들', 'XSN'))
                    )

    result = ""
    pass_count = 0
    words_idx = []
    words_edit = []
    words_origin = []
    idx = 1
    for line in input_text.split(". "):
        words = line.split(" ")

        for word_idx, word in enumerate(words):
            if word == "":
                result += ' '
                continue
            if pass_count > 0:
                pass_count -= 1
                continue

            morphs = (await get_pos(word))
            is_pattern_same = True
            used_word = 1

            for case in plural_table:
                for c, (rep, tag) in enumerate(case):
                    if len(morphs) <= c:
                        break

                    morph_check = rep != '<_AL_>' and rep != morphs[c][0]

                    if tag != morphs[c][1] and morph_check:
                        is_pattern_same = False
                        break

                    if len(morphs) <= c + 1 and len(words) > word_idx+1:
                        morphs.extend(await get_pos(words[word_idx+1]))
                        used_word += 1

                if is_pattern_same:
                    break

            if is_pattern_same:
                pass_count = used_word - 1

                for i in range(used_word-1):
                    result += words[word_idx + i]
                    result += ' '

                front = words[word_idx + used_word - 1][:words[word_idx + used_word - 1].rfind('들')]
                back = words[word_idx + used_word - 1][words[word_idx + used_word - 1].rfind('들') + 1:]
                new_back = ''
                change_count = 1

                if len(back) > 0 and len(front) > 0 and back[0] in ('은', '는', '이', '가', '을', '를', '와', '과'):
                    new_back = await chang_josa(front[-1], back[0]) + back[1:]
                    change_count += 1

                result += front
                words_idx.append([len(result), len(result) + change_count, idx])
                words_origin.append('들' + back)
                words_edit.append(new_back)
                result += '들' + (new_back if len(new_back) > 0 else back)
                result += ' '
                idx += 1
            else:
                result += word
                result += ' '

        if result[-1] == ' ':
            result = result[:-1]
        result += '. '

    return {'words': words_origin, 'words_idx': words_idx, 'edit':  words_edit, 'tag': 'plural'}


async def remove_double_passive(input_text):
    # 이중피동 제거 함수
    replacing = ["이", "히", "리", "기"]
    words = input_text.split(" ")
    words_for_result = []
    edits = []
    indexs = []
    index_num = 1
    result = ""
    now_length = 0

    for word_idx, word in enumerate(words):
        if word == "":
            result += " "
            now_length += 1
            continue
            
        changed_word = ""
        is_changed = False
        pass_count = 0
        tagged_morphs = await get_pos(word)

        for morph_idx, morph in enumerate(tagged_morphs):
            flag = True

            if pass_count > 0:
                pass_count -= 1
                continue

            if flag and morph[1] == "VV":
                if morph_idx < len(tagged_morphs) - 2 and tagged_morphs[morph_idx + 1][1] == "ECS" and tagged_morphs[morph_idx + 2][1] == "VXV":
                    for rep_idx, replaced in enumerate(["이어지", "히어지", "리어지", "기어지"]):
                        target = morph[0] + tagged_morphs[morph_idx+1][0] + tagged_morphs[morph_idx+2][0]
                        for idx in range(len(target)-2):
                            if replaced == target[idx:idx+3]:
                                changed_word += target[:idx] + replacing[rep_idx]
                                pass_count = 2
                                is_changed = True
                                flag = False
                else:
                    for rep_idx, replaced in enumerate(["여지", "혀지", "려지", "겨지"]):
                        target = morph[0]
                        for idx in range(len(target)-1):
                            if replaced == target[idx:idx+2]:
                                changed_word += target[:idx] + replacing[rep_idx]
                                is_changed = True
                                flag = False

                if flag:
                    changed_word += morph[0]

            else:
                nieun_flag = False
                
                if is_changed and len(morph[0]) > 0 and morph[0][0] == 'ㄴ' and len(changed_word) > 0:
                    front = list(j2hcj(h2j(changed_word[-1])))
                    back =  list(j2hcj(h2j(morph[0][0])))
                    if len(front) == 2:
                        try:
                            front.extend(back)
                            changed_word = changed_word[:-1] + j2h(*front)
                            if len(morph[0]) > 1:
                                changed_word += morph[0][1:]
                            nieun_flag = True
                        except:
                            pass

                if not nieun_flag:
                    changed_word += morph[0]

        if is_changed:
            result += " " + word
            
            words_for_result.append(word.replace('\n', '').replace('\r', ' '))
            indexs.append([now_length, now_length + len(word), index_num])
            edits.append(changed_word)
            now_length += len(word) + 1
            index_num += 1
        else:
            result += " " + word
            now_length += len(word) + 1
    # print(result)
    return {'words' : words_for_result, 'words_idx' : indexs, 'edit':  edits, 'tag' : 'passive'}

if not ready:
    ready = True
    kma.pos("예열")
