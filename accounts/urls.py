from django.urls import path
from accounts import views

urlpatterns = [
    path('profile', views.profile_view, name="profile"),
    #path('update', views.create_category, name="create_category"),
    #path('delete', views.category_each_view, name="category_each"),
    #path('update/<int:pk>', views.update_category, name="update_category"),
    #path('delete/<int:pk>', views.delete_category, name="delete_category")
]
