# from typing import cast
from django.shortcuts import render

from .forms import CreateUserForm
from django.contrib import messages
from accounts.models import UserData
# Create your views here.


def registerPage(request):
    form = CreateUserForm

    if(request.method == "POST"):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created for " +
                             form.cleaned_data.get("username"))
            messages.success(request, "Please login to access to the site")

        else:
            messages.success(request, "")
    contex = {'form': form}
    return render(request, "registration/register.html", contex)


#user = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name="user")
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
            if(request.user.is_authenticated):
                if(UserData.objects.filter(user=request.user).exists()):
                    data = UserData.objects.get(user=request.user)
                    exist = True
                else:
                    data = {
                        "user": request.user,
                        "email_verified": False,
                        "mobile_number": "",
                        "mobile_number_verified": False,
                        "is_eligible_to_get_payed": False,
                        "payed_proof_img_link" : None,
                        "is_payment_done" : False,
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
                        "updated_at": None
                        }
                    exist = False
                return render(request, "profile_view.html", {"exist": exist, "data": data})
    return render(request, "403.html")