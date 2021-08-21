from django.urls import path, include
import step1.views

urlpatterns = [

    path('', step1.views.test, name='step1'),
    path('./step2/', include('step2.urls'), name='step2'),

] 