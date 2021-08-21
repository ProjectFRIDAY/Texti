from django.urls import path, include
from .views import StartView
    
urlpatterns = [

    path('', StartView.as_view(), name='start'),
    path('./step1/', include('step1.urls'), name='step1'),

]
