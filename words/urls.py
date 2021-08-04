from django.urls import path
from words import views

urlpatterns = [
    path('', views.words_view, name="words_view"),
    path("new/", views.add_new_words, name="add_new_words"),
    path('delete/<str:pk>/', views.delete_word, name="delete_word"),
]
