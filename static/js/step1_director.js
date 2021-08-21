function step1_director(edited_text, error) {
    console.log(edited_text);
    if (error === 1) {
        // 오류가 발생한 경우 종료
        alert("분석에 실패하였습니다.");
        history.back();
        return;
    }

    // 초기 변수
    var answer = edited_text;
    var original_text = document.getElementById('original_text');
    var edited_text = document.getElementById('edited_text');
    var hidden = document.getElementById('hidden');
    
    const EMPHATIC_TEXT = "emphatic_text";
    const RED_COLOR = "red_emphatic";

    original_text.innerHTML = answer['html'];
    hidden.innerHTML = original_text.innerHTML.replace(/(<|<\/)SPAN(.*?)>/gi, '')

    if (answer['rev_plural']['words'].length > 0 || answer['rev_passive']['words'].length > 0 || answer['rev_repeated']['words'].length > 0) edited_text.innerHTML = ''

    for (let i = 1; i <= answer['rev_plural']['words'].length; i++) {
        let comment = document.createElement("div");
        comment.id = `right_plural${i}`;
        comment.title = "클릭하여 모두 수정하기";
        comment.innerText = `❌ [이중 복수 표현 경고] : '${answer['rev_plural']['words'][i - 1]}'은(는) 이중 복수 표현입니다.`;
        edited_text.appendChild(comment);
    }
        
    for (let i = 1; i <= answer['rev_passive']['words'].length; i++) {
        let comment = document.createElement("div");
        comment.id = `right_passive${i}`;
        comment.title = "클릭하여 모두 수정하기";
        comment.innerText = `❌ [이중 피동 표현 경고] : '${answer['rev_passive']['words'][i - 1]}'은(는) 이중 피동 표현입니다.`;
        edited_text.appendChild(comment);
    }
    
    for (let i = 1; i <= answer['rev_repeated']['words'].length; i++) {
        let comment = document.createElement("div");
        comment.id = `right_repeated${i}`;
        comment.innerText = `😣 [중복 어휘 주의] : '${answer['rev_repeated']['words'][i - 1]}'이(가) 과도하게 사용되었습니다.`;
        edited_text.appendChild(comment);
    }

    // 중복 어휘
    for (let t = 1; t <= answer['rev_repeated']['words'].length; t++) {
        (function (i) {
            let changers = document.getElementsByName('repeated' + i);
            let target = document.getElementById('right_repeated' + i);
            
            // 텍스트 강조 마우스 이벤트
            target.addEventListener('mouseover', function () {
                target.classList.add(EMPHATIC_TEXT);
                changers.forEach((changer) => changer.classList.add(EMPHATIC_TEXT));
            }, false);
            
            target.addEventListener('mouseout', function () {
                target.classList.remove(EMPHATIC_TEXT);
                changers.forEach((changer) => changer.classList.remove(EMPHATIC_TEXT));
            }, false);
            /*target.addEventListener('click', function(){
                target.style.display = "none";
                for(let j = 0; j < changers.length; j++){
                    changers[j].innerText = answer['rev_repeated']['edit'][j]
                }
            }, false);*/
        }(t));
    }

    // 이중 복수
    for (let t = 1; t <= answer['rev_plural']['words'].length; t++) {
        (function (i) {
            let changers = document.getElementsByName('plural' + i);
            let target = document.getElementById('right_plural' + i);

            target.addEventListener('mouseover', function () {
                target.classList.add(RED_COLOR);
                target.classList.add(EMPHATIC_TEXT);
                changers.forEach((changer) => changer.classList.add(RED_COLOR));
                changers.forEach((changer) => changer.classList.add(EMPHATIC_TEXT));
            }, false);
            
            target.addEventListener('mouseout', function () {
                target.classList.remove(RED_COLOR);
                target.classList.remove(EMPHATIC_TEXT);
                changers.forEach((changer) => changer.classList.remove(RED_COLOR));
                changers.forEach((changer) => changer.classList.remove(EMPHATIC_TEXT));
            }, false);
            
            target.addEventListener('click', function () {
                target.style.display = "none";
                for (let j = 0; j < changers.length; j++) {
                    changers[j].innerText = answer['rev_plural']['edit'][i - 1];
                    hidden.innerHTML = original_text.innerHTML.replace(/(<|<\/)SPAN(.*?)>/gi, '');
                    }
            }, false);
        }(t));
    }

    // 이중 피동
    for (let t = 1; t <= answer['rev_passive']['words'].length; t++) {
        (function (i) {
            let changers = document.getElementsByName('passive' + i);
            let target = document.getElementById('right_passive' + i);

            target.addEventListener('mouseover', function () {
                target.classList.add(RED_COLOR);
                target.classList.add(EMPHATIC_TEXT);
                changers.forEach((changer) => changer.classList.add(RED_COLOR));
                changers.forEach((changer) => changer.classList.add(EMPHATIC_TEXT));
            }, false);
            
            target.addEventListener('mouseout', function () {
                target.classList.remove(RED_COLOR);
                target.classList.remove(EMPHATIC_TEXT);
                changers.forEach((changer) => changer.classList.remove(RED_COLOR));
                changers.forEach((changer) => changer.classList.remove(EMPHATIC_TEXT));
            }, false);
            
            target.addEventListener('click', function () {
                target.style.display = "none";
                for (let j = 0; j < changers.length; j++) {
                    changers[j].innerText = answer['rev_passive']['edit'][i - 1];
                    hidden.innerHTML = original_text.innerHTML.replace(/(<|<\/)SPAN(.*?)>/gi, '');
                    }
            }, false);
        }(t));
    }
}