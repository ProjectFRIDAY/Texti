from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def test(request):
    context = {}

    if request.method == 'POST':
        context = {
            "original_text": request.POST.get('hidden')
          }
        return render(request, 'step2.html', context)
    return render(request, 'index.html')
