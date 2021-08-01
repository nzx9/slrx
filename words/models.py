from django.db import models

# Create your models here.


class Word(models.Model):
    in_sinhala = models.CharField(max_length=50)
    in_english = models.CharField(max_length=50)
    recorde_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
