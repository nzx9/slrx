from django.contrib import admin

# Register your models here.
from .models import UserData, Pins

admin.site.register(UserData)
admin.site.register(Pins)
