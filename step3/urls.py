from django.urls import path, include
import step3.views

urlpatterns = [

    path('', step3.views.test, name='step3'),

]
