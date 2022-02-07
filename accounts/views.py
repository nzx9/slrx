# from typing import cast
import re
from django.shortcuts import render, redirect

from .forms import CreateUserForm
from django.contrib import messages
from accounts.models import UserData
from django.contrib.auth.models import User
import re

# Create your views here.


def registerPage(request):
    form = CreateUserForm

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created for " + form.cleaned_data.get("username")
            )
            messages.success(request, "Please login to access to the site")

        else:
            messages.success(request, "")
    contex = {"form": form}
    return render(request, "registration/register.html", contex)


# user = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name="user")
#    email_verified = models.BooleanField(default=False)
#    mobile_number = models.CharField(max_length=12, null=True)
#    mobile_number_verified = models.BooleanField(default=False)
#    is_eligible_to_get_payed = models.BooleanField(default=False)
#    payed_proof_img_link = models.CharField(max_length=1500)
#    is_payment_done = models.BooleanField(default=False)
#    payment_method = models.CharField(max_length=50)
#    account_number = models.CharField(max_length=25)
#    account_holder= models.CharField(max_length=50)
#    account_bank = models.CharField(max_length=50)
#    account_bank_branch = models.CharField(max_length=50)
#    payment_requested = models.BooleanField(default=False)
#    payment_request_status = models.CharField(max_length=500)
#    user_remarks = models.CharField(max_length=1500)
#    admin_remarks = models.CharField(max_length=1500)
#    nic = models.CharField(max_length=20)
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)


def profile_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if UserData.objects.filter(user=request.user).exists():
                data = UserData.objects.get(user=request.user)
                exist = True
                data.mobile_number = (
                    "" if data.mobile_number == None else data.mobile_number
                )
                data.nic = "" if data.nic == None else data.nic
                data.account_number = (
                    "" if data.account_number == None else data.account_number
                )
                data.account_holder = (
                    "" if data.account_holder == None else data.account_holder
                )
                data.account_bank = (
                    "" if data.account_bank == None else data.account_bank
                )
                data.account_bank_branch = (
                    "" if data.account_bank_branch == None else data.account_bank_branch
                )

            else:
                data = {
                    "user": request.user,
                    "email_verified": False,
                    "mobile_number": "",
                    "mobile_number_verified": False,
                    "is_eligible_to_get_payed": False,
                    "payed_proof_img_link": None,
                    "is_payment_done": False,
                    "account_number": "",
                    "account_holder": "",
                    "account_bank": "",
                    "account_bank_branch": "",
                    "payment_requested": False,
                    "payment_request_status": None,
                    "user_remarks": None,
                    "admin_remarks": None,
                    "nic": "",
                    "created_at": None,
                    "updated_at": None,
                }
                exist = False
            return render(request, "profile_view.html", {"exist": exist, "data": data})
    return render(request, "403.html")


def user_info_update(request):
    email_changed = False
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.email != request.POST["email"]:
                user = User.objects.get(pk=request.user.pk)
                user.email = request.POST["email"]
                user.save()
                email_changed = True

            if UserData.objects.filter(user=request.user).exists():
                user_data = UserData.objects.get(user=request.user)
                if (
                    user_data.mobile_number != None
                    and user_data.mobile_number != request.POST["mobile_number"]
                ):
                    user_data.mobile_number = request.POST["mobile_number"]
                    user_data.mobile_number_verified = False
            else:
                user_data = UserData()
                user_data.user = request.user
                user_data.mobile_number = request.POST["mobile_number"]
            if email_changed:
                user_data.email_verified = False
            user_data.nic = request.POST["nic"]
            user_data.save()
            return redirect("profile")
        else:
            return render(request, "403.html")
    else:
        return redirect("profile")


def acc_info_update(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if UserData.objects.filter(user=request.user).exists():
                user_data = UserData.objects.get(user=request.user)
                if user_data.payment_requested:
                    return render(request, "403.html")
            else:
                user_data = UserData()
                user_data.user = request.user
            user_data.account_number = request.POST["account_number"]
            user_data.account_holder = request.POST["account_holder"]
            user_data.account_bank = request.POST["account_bank"]
            user_data.account_bank_branch = request.POST["account_bank_branch"]
            user_data.save()
            return redirect("profile")
        else:
            return render(request, "403.html")
    else:
        return redirect("profile")


def user_notes_update(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if UserData.objects.filter(user=request.user).exists():
                user_data = UserData.objects.get(user=request.user)
            else:
                user_data = UserData()
                user_data.user = request.user
            if (
                request.POST["user_remarks"] == ""
                or request.POST["user_remarks"] == "None"
                or request.POST["user_remarks"] == " "
            ):
                user_data.user_remarks = None
            else:
                user_data.user_remarks = request.POST["user_remarks"].strip()
            user_data.save()
            return redirect("profile")
        else:
            return render(request, "403.html")
    else:
        return redirect("profile")
