from django.shortcuts import render

# Create your views here.


def home_view(request):
    return render(request, "home.html")


def terms_view(request):
    return render(request, "terms.html")
