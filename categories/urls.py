from django.urls import path
from categories import views

urlpatterns = [
    path('', views.category_view, name="category_view"),
    path('create', views.create_category, name="create_category"),
    path('<str:category>', views.category_each_view, name="category_each"),
    path('update/<int:pk>', views.update_category, name="update_category"),
    path('delete/<int:pk>', views.delete_category, name="delete_category")
]
