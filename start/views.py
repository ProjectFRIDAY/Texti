from django.views.generic import TemplateView


class StartView(TemplateView):
    template_name = 'start.html'
