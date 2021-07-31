from django.urls import path, include
from streams import views

urlpatterns = [
    path('', views.home),
    path('upload/', views.uploadStreams, name="stream_uploads"),
    path('sub/', views.sub, name="sub")
]
