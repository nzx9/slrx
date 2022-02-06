from django.db import models
from django.db.models.deletion import  SET_NULL
from django.contrib.auth.models import User
# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name="user")
    email_verified = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=12, null=True)
    mobile_number_verified = models.BooleanField(default=False)
    is_eligible_to_get_payed = models.BooleanField(default=False)
    payed_proof_img_link = models.CharField(max_length=1500, null=True)
    is_payment_done = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, null=True)
    account_number = models.CharField(max_length=25, null=True)
    account_holder= models.CharField(max_length=50, null=True)
    account_bank = models.CharField(max_length=50, null=True)
    account_bank_branch = models.CharField(max_length=50, null=True)
    payment_requested = models.BooleanField(default=False)
    payment_request_status = models.CharField(max_length=500, null=True)
    user_remarks = models.CharField(max_length=1500, null=True)
    admin_remarks = models.CharField(max_length=1500, null=True)
    nic = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
