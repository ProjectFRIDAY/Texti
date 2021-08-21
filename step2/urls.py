from django.urls import path, include
import step2.views

urlpatterns = [

    path('', step2.views.test, name='step2'),
    path('./step3/', include('step3.urls'), name='step3'),

]
