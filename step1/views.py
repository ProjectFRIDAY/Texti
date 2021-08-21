from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from . import repeated_expression, replacing, result_to_html
import asyncio

def do_async(original_text):
    async def main(original_text):
        result = []
        try:
            futures = [asyncio.ensure_future(repeated_expression.find_repeated(original_text)), asyncio.ensure_future(replacing.remove_double_plural(original_text)), asyncio.ensure_future(replacing.remove_double_passive(original_text))]
            result = await asyncio.gather(*futures)
        except Exception as e:
            try:
                while "  " in original_text:
                    original_text = original_text.replace("  ", "")
                futures = [asyncio.ensure_future(repeated_expression.find_repeated(original_text)), asyncio.ensure_future(replacing.remove_double_plural(original_text)), asyncio.ensure_future(replacing.remove_double_passive(original_text))]
                result = await asyncio.gather(*futures)
            except Exception as e:
                print("Error:", e, original_text)
                return {"error" : 1, "original_text": "", "edited_text": {"html": "", "rev_repeated": {}, "rev_plural": {}, "rev_passive": {}}}

        # dict 형태 = {words, words_idx, edit, tag}
        repeated_dict = result[0]
        plural_dict = result[1]
        passive_dict = result[2]
        final_html = await result_to_html.final_return(repeated_dict, plural_dict, passive_dict, original_text)
        result = {"error" : 0, "original_text": original_text, "edited_text": {"html": final_html, "rev_repeated": repeated_dict, "rev_plural": plural_dict, "rev_passive": passive_dict}}

        # print(result)
        return result
    return asyncio.run(main(original_text))

@csrf_exempt
def test(request):
    if request.method == 'POST':
        original_text = request.POST.get('original_text').strip()
        return render(request, 'step1.html', do_async(original_text))
    return render(request, 'index.html')

