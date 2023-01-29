from django.views.generic import TemplateView


class InputPageView(TemplateView):
    template_name = "input.html"


class OutputPageView(TemplateView):
    template_name = "output.html"
