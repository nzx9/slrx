from django.db import models
from categories.models import Category
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User
# Create your models here.


class Word(models.Model):
    in_sinhala = models.CharField(max_length=50)
    in_english = models.CharField(max_length=50)
    in_singlish = models.CharField(max_length=50, null=True)
    recorde_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    last_edit_by = models.ForeignKey(
        User, null=True, on_delete=SET_NULL, related_name="updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("in_sinhala", "in_english"),)
