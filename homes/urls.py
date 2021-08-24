from django.urls import path
from homes import views

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('terms', views.terms_view, name="terms")
]
