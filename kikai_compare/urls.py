from django.urls import path

from .views import InputPageView


urlpatterns = [
    path('', InputPageView.as_view(), name='home'),
]
