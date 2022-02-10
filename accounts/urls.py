from django.urls import path
from accounts import views

urlpatterns = [
    path("profile", views.profile_view, name="profile"),
    path("profile/update/user-info", views.user_info_update, name="user_info_update"),
    path("profile/update/account-info", views.acc_info_update, name="acc_info_update"),
    path(
        "profile/updates/user-notes", views.user_notes_update, name="user_notes_update"
    ),
    path(
        "profile/verify/send-email",
        views.send_verification_email,
        name="send_verification_email",
    ),
    path(
        "profile/verify/email",
        views.verify_email,
        name="verify_email",
    ),
    path(
        "profile/verify/send-sms",
        views.send_verification_sms,
        name="send_verification_sms",
    ),
    path(
        "profile/verify/sms",
        views.verify_sms,
        name="verify_sms",
    ),
    path(
        "profile/request/payment",
        views.request_payment,
        name="request_payment",
    ),
]
