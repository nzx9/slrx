# from typing import cast
import re
from django.shortcuts import render, redirect, HttpResponse

from .forms import CreateUserForm
from django.contrib import messages
from accounts.models import UserData, Pins
from django.contrib.auth.models import User
import json
import os
import random
import dotenv
from pathlib import Path
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

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

                data.address = "" if data.address == None else data.address

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
                    "address": "",
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
            user_data.address = request.POST["address"]
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

            if request.POST["payment_method"] == "Bank Transfer":
                user_data.account_number = request.POST["account_number"]
                user_data.account_holder = request.POST["account_holder"]
                user_data.account_bank = request.POST["account_bank"]
                user_data.account_bank_branch = request.POST["account_bank_branch"]
                user_data.payment_method = "Bank Transfer"
            elif request.POST["payment_method"] == "Cheque":
                user_data.account_holder = request.POST["account_holder"]
                user_data.payment_method = "Cheque"
            elif request.POST["payment_method"] == "Cash":
                user_data.payment_method = "Cash"
            elif request.POST["payment_method"] == "":
                user_data.payment_method = None
            else:
                return redirect("profile")
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


def set_envs():
    BASE_DIR = Path(__file__).resolve().parent.parent
    dotenv_file = os.path.join(BASE_DIR, ".env")
    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)


# def send_verification_email(request):
#     set_envs()
#     if request.method == "POST" and request.user.is_authenticated:
#         pin = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

#         if Pins.objects.filter(user=request.user).exists():
#             pins_user = Pins.objects.get(user=request.user)
#         else:
#             pins_user = Pins()

#         pins_user.email_pin = pin

#         url = os.environ["TRUSTIFI_URL"] + "/api/i/v1/email"
#         payload = json.dumps(
#             {
#                 "recipients": [
#                     {
#                         "email": request.user.email,
#                         "name": request.user.username,
#                         # "phone": {"country_code": "+94", "phone_number": "1111111111"},
#                     }
#                 ],
#                 "attachments": [],
#                 "title": "DSC Email Verification PIN",
#                 "html": '<div><div><div><h3>Please use this PIN to verify your email.<br><b style="color: red">Don\'t share this PIN with others.</b></h3></div><div style="padding-top:10px;"><h1>PIN: {}</h1></div><div style="padding-top:10px;"><a href="https://dscapp.herokuapp.com">Click here to goto DSC App</a><br><b><h3>Thank you</h3></b></div></div></div>'.format(
#                     pin
#                 ),
#                 "methods": {
#                     "postmark": False,
#                     "secureSend": False,
#                     "encryptContent": False,
#                     "secureReply": False,
#                 },
#             }
#         )
#         headers = {
#             "x-trustifi-key": os.environ["TRUSTIFI_KEY"],
#             "x-trustifi-secret": os.environ["TRUSTIFI_SECRET"],
#             "Content-Type": "application/json",
#         }

#         response = requests.request("POST", url, headers=headers, data=payload)
#         print(response.json())
#         return HttpResponse(response.json())
#         # response = requests.request("POST", url, headers=headers, data=payload)
#     else:
#         print("Not A POST REQUEST")


def send_verification_email(request):
    if request.method == "POST" and request.user.is_authenticated:
        set_envs()
        pin = "".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        if Pins.objects.filter(user=request.user).exists():
            pins_user = Pins.objects.get(user=request.user)
        else:
            pins_user = Pins()
            pins_user.user = request.user

        pins_user.email_pin = pin
        pins_user.save()

        message = Mail(
            from_email="dscapp@mail.com",
            to_emails=request.user.email,
            subject="DSC APP Email Verification",
            html_content='<div><div><div><h3>Please use this PIN to verify your email.<br><b style="color: red">Don\'t share this PIN with others.</b></h3></div><div style="padding-top:10px;"><h1>PIN: {}</h1></div><div style="padding-top:10px;"><a href="https://dscapp.herokuapp.com">Click here to goto DSC App</a><br><b><h3>Thank you</h3></b></div></div></div>'.format(
                pin
            ),
        )
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            return HttpResponse(
                json.dumps(
                    {
                        "type": "success",
                        "in": "send",
                        "msg": "Verification Email Send to <b>{}</b>".format(
                            request.user.email
                        ),
                    }
                )
            )
        except Exception as e:
            print(e.message)
            json.dumps(
                {
                    "type": "error",
                    "in": "send",
                    "msg": "Email Sent failed. Reason: {}".format(e.message),
                }
            )
    else:
        return render(request, "403.html")


def verify_email(request):
    if request.method == "POST" and request.user.is_authenticated:
        if Pins.objects.filter(user=request.user).exists():
            body_data = json.loads(request.body)
            pins = Pins.objects.get(user=request.user)
            if (
                re.match("[0-9]{6}", body_data["email-pin"])
                and body_data["email-pin"] == pins.email_pin
            ):
                if UserData.objects.filter(user=request.user).exists():
                    ud = UserData.objects.get(user=request.user)
                else:
                    ud = UserData()
                    ud.user = request.user
                pins.email_pin = None
                pins.save()
                ud.email_verified = True
                ud.save()
                return HttpResponse(
                    json.dumps(
                        {"type": "success", "in": "validate", "msg": "Email Verified!"}
                    )
                )
            else:
                return HttpResponse(
                    json.dumps(
                        {
                            "type": "error",
                            "in": "validate",
                            "msg": "Invalid PIN. Try again later.",
                        }
                    )
                )
        else:
            return HttpResponse(
                json.dumps(
                    {
                        "type": "error",
                        "in": "validate",
                        "msg": "Create PIN Before Validate",
                    }
                ),
                content_type="application/json",
            )
    else:
        return render(request, "403.html")


def send_verification_sms(request):
    if request.method == "POST" and request.user.is_authenticated:
        if UserData.objects.filter(user=request.user).exists():
            user_data = UserData.objects.get(user=request.user)
            if user_data.mobile_number != None:
                set_envs()
                pin = "".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
                if Pins.objects.filter(user=request.user).exists():
                    pins_user = Pins.objects.get(user=request.user)
                else:
                    pins_user = Pins()
                    pins_user.user = request.user

                pins_user.mobile_pin = pin
                pins_user.save()

                account_sid = os.environ["TWILIO_SID"]
                auth_token = os.environ["TWILIO_AUTH_TOKEN"]
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body="Your mobile number verification PIN: {}. Don't share this PIN with others. Thank You!".format(
                        pin
                    ),
                    from_=os.environ["TWILIO_NUMBER"],
                    to="+94{}".format(user_data.mobile_number[1:]),
                )
                print(message.sid)
                return HttpResponse(
                    json.dumps(
                        {
                            "type": "success",
                            "in": "send",
                            "msg": "Verification PIN sent to {}".format(
                                user_data.mobile_number
                            ),
                        }
                    ),
                    content_type="application/json",
                )
        return HttpResponse(
            json.dumps(
                {
                    "type": "error",
                    "in": "send",
                    "msg": "Please provide mobile number to sent verification SMS",
                }
            ),
            content_type="application/json",
        )
    else:
        return render(request, "403.html")


def verify_sms(request):
    if request.method == "POST" and request.user.is_authenticated:
        if Pins.objects.filter(user=request.user).exists():
            body_data = json.loads(request.body)
            pins = Pins.objects.get(user=request.user)
            if body_data["mobile-pin"] == pins.mobile_pin:
                if UserData.objects.filter(user=request.user).exists():
                    ud = UserData.objects.get(user=request.user)
                else:
                    ud = UserData()
                    ud.user = request.user
                pins.mobile_pin = None
                pins.save()
                ud.mobile_verified = True
                ud.save()
                return HttpResponse(
                    json.dumps(
                        {
                            "type": "success",
                            "in": "validate",
                            "msg": "Mobile Number Verified!",
                        }
                    )
                )
            else:
                return HttpResponse(
                    json.dumps(
                        {
                            "type": "error",
                            "in": "validate",
                            "msg": "Invalid PIN. Try again later.",
                        }
                    )
                )
        else:
            return HttpResponse(
                json.dumps(
                    {
                        "type": "error",
                        "in": "validate",
                        "msg": "Create PIN Before Validate",
                    }
                ),
                content_type="application/json",
            )
    else:
        return render(request, "403.html")


def request_payment(request):
    if request.method == "POST" and request.user.is_authenticated:
        if UserData.objects.filter(user=request.user).exists():
            user_data = UserData.objects.get(user=request.user)
            if user_data.email_verified and user_data.is_eligible_to_get_payed:
                user_data.payment_request_status = "Pending"
                user_data.payment_requested = True
                user_data.save()
                print("Approved")
            else:
                return HttpResponse(
                    "You are not eligible to request payment. Verify your email, Complete all the recordings if you haven't completed, Also check the `Eligable To Get Paid > True`. If you think this is a mistake then sent a email to dscapp@mail.com"
                )

    return redirect(request, "403.html")
