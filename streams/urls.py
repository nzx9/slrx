from django.urls import path
from streams import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    # path('upload/', views.uploadStreams, name="stream_uploads"),
    path('sub/', views.sub, name="sub")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
