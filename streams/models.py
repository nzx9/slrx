import streams
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import User
from words.models import Word

# Create your models here.


class Stream(models.Model):
    userId = models.ForeignKey(User, on_delete=CASCADE)
    wordId = models.ForeignKey(Word, on_delete=CASCADE)
    pos_server = models.CharField(max_length=200)
    pos_firebase = models.CharField(max_length=200)
    verified = models.BooleanField(null=True)
    verified_by = models.ForeignKey(
        User, null=True, on_delete=SET_NULL, related_name="verified_by")
    reason = models.CharField(max_length=100, null=True)
    comment = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Stream(models.Model):
    userId = models.ForeignKey(User, on_delete=CASCADE)
    streamId = models.ForeignKey(Stream, on_delete=CASCADE)
    wordId = models.ForeignKey(Word, on_delete=CASCADE)
