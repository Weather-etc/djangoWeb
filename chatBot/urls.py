from django.urls import path
from . import views

urlpatterns = [
    path("", views.content, name='room'),
]
