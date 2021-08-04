from django.urls import path
from words import views

urlpatterns = [
    path('', views.words_view, name="words_view"),
    path("submit/", views.submit_new_word, name="word_submit")
]
