from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    word_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=CASCADE)
    last_edit_by = models.ForeignKey(
        User, null=True, on_delete=SET_NULL, related_name="last_edit_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
