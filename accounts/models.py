from statistics import mode
from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User

# Create your models here.


class UserData(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name="user")
    email_verified = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=12, null=True, default=None)
    mobile_number_verified = models.BooleanField(default=False)
    is_eligible_to_get_payed = models.BooleanField(default=False)
    payed_proof_img_link = models.CharField(max_length=1500, null=True, default=None)
    is_payment_done = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, null=True, default=None)
    account_number = models.CharField(max_length=25, null=True, default=None)
    account_holder = models.CharField(max_length=50, null=True, default=None)
    account_bank = models.CharField(max_length=50, null=True, default=None)
    account_bank_branch = models.CharField(max_length=50, null=True, default=None)
    payment_requested = models.BooleanField(default=False)
    payment_request_status = models.CharField(max_length=500, null=True, default=None)
    user_remarks = models.CharField(max_length=1500, null=True, default=None)
    admin_remarks = models.CharField(max_length=1500, null=True, default=None)
    nic = models.CharField(max_length=20, null=True, default=None)
    address = models.CharField(max_length=1000, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Pins(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name="u")
    email_pin = models.CharField(max_length=6, null=True, default=None)
    mobile_pin = models.CharField(max_length=6, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
