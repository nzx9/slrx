from django.urls import path
from words import views

urlpatterns = [
    path('', views.words_view, name="words_view"),
    path("new/", views.add_new_words, name="add_new_words"),
    path('delete/<str:pk>/', views.delete_word, name="delete_word"),
    path("bulk/", views.bulk_upload, name="bulk_upload_words"),
    path("bulk/upload/", views.add_bulk_words_to_db, name="add_to_db")
]
