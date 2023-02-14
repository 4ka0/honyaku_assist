from django.urls import path

from .views import input_page_view


urlpatterns = [
    path('', input_page_view, name='input_page'),
]
