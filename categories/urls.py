from django.urls import path
from categories import views

urlpatterns = [
    path('', views.category_view, name="category_view"),
    path('create', views.create_category, name="create_category")
]
