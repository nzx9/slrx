from django.urls import path, include
from streams import views

urlpatterns = [
    path('', views.home),
    path('video/', views.videoFeed, name="video_feed"),
]
