from django.urls import path
from accounts import views

urlpatterns = [
    path("profile", views.profile_view, name="profile"),
    path("profile/update/user-info", views.user_info_update, name="user_info_update"),
    path("profile/update/account-info", views.acc_info_update, name="acc_info_update"),
    path(
        "profile/updates/user-notes", views.user_notes_update, name="user_notes_update"
    ),
    # path('delete/<int:pk>', views.delete_category, name="delete_category")
]
