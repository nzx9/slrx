# from typing import cast
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .forms import CreateUserForm
from django.contrib import messages
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
