def check_long_sentence(input_text, BOUND=100):
    # BOUND보다 긴 문장을 찾아 html을 반환하는 함수
    lines = input_text.replace('\r', ' ').split(". ")
    results = []
    is_existed = False

    # 마지막 줄의 끝에 위치한 마침표 제거
    dot_idx = lines[-1].rfind('.')
    if dot_idx == 1 or dot_idx == 2 and lines[-1][-1] == ' ':
        lines[-1] = lines[-1][:-dot_idx]

    # bound 초과 검사
    for idx, line in enumerate(lines):
        if len(line.strip()) >= BOUND:
            results.append('<span name = "toolong">' + line+ '</span>')
            is_existed = True
        else:
            results.append(line)
            
    answer = {"html": ". ".join(results).replace('\n', '<br/>').replace("'", "\\'"), "is_existed": int(is_existed)}
    return answer
