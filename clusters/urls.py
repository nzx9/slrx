from django.urls import path
from clusters import views

urlpatterns = [
    path('', views.clusters_view, name="clusters_view"),
    path('verify', views.cluster_verify, name="clusters_verify")
]
