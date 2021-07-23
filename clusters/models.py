from django.db import models

# Create your models here.


class Cluster(models.Model):
    name = models.TextField()
    timestamp = models.TextField()
    createdby = models.TextField()
    availableat = models.TextField()
