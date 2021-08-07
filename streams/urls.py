from django.urls import path
from streams import views
from django.conf import settings
from django.conf.urls.static import static

import streams

urlpatterns = [
    path('', views.streams_view, name="streams_view"),
    path('rec/<str:pk>/', views.streams_rec_view, name="streams_rec_view"),
    # path('upload/', views.uploadStreams, name="stream_uploads"),
    path('sub/', views.sub, name="sub")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
