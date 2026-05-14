from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings



class User(AbstractUser):
    votes = models.IntegerField(default=0, null=True)
    polls_voted = models.ManyToManyField("polls.Question", blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
