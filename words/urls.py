from django.urls import path
from words import views

urlpatterns = [
    path('', views.words_view, name="words_view"),
]
