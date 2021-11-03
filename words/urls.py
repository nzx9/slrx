from django.urls import path
from words import views

urlpatterns = [
    path('', views.words_view, name="words_view"),
    path("new/", views.add_new_words, name="add_new_words"),
    path("bulk/", views.bulk_upload, name="bulk_upload_words"),
    path("bulk/upload/", views.add_bulk_words_to_db, name="add_to_db"),
    path("view/<int:word_pk>", views.detailed_word_view, name="detailed_word_view"),
    path("update/<int:pk>", views.update_word, name="update_word"),
    path("delete/<int:pk>", views.delete_word, name="delete_word"),
]
