from django.db import models

# Create your models here.


class Word(models.Model):
    in_sinhala = models.CharField(max_length=50)
    in_english = models.CharField(max_length=50)
    in_singlish = models.CharField(max_length=50, null=True)
    recorde_count = models.IntegerField(default=0)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("in_sinhala", "in_english"),)
