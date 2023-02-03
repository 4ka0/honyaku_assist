from django.urls import path

from .views import input_page_view, output_page_view


urlpatterns = [
    path('input', input_page_view, name='input_page'),
    path('output', output_page_view, name='output_page'),
]
