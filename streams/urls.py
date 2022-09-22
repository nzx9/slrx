from django.urls import path
from streams import views
from django.conf import settings
from django.conf.urls.static import static

import streams

urlpatterns = [
    path("", views.streams_view, name="streams_view"),
    path("rec/<int:pk>/", views.streams_rec_view, name="streams_rec_view"),
    # path('upload/', views.uploadStreams, name="stream_uploads"),
    path("submit/<int:pk>/", views.submit, name="submit"),
    path("verification", views.streams_verification, name="stream_verification"),
    path("get/<int:pk>", views.get_stream, name="get_stream"),
    path("verify/<int:pk>", views.verify_stream, name="verify_stream"),
    path("table", views.streams_table_home, name="streams_table_home"),
    # path("by/<int:pk>", views.views.streams_from_users, name="streams_from_users"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
