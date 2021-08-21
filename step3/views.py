from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from . import dividing

@csrf_exempt
def test(request):
    context = {}
    
    if request.method == 'POST':
        context = dividing.check_long_sentence(request.POST.get('hidden'))
        return render(request, 'step3.html', context)
    
    return render(request, 'index.html')