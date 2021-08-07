from django.contrib import admin

# Register your models here.
from .models import Stream, User_Stream

admin.site.register(Stream)
admin.site.register(User_Stream)
