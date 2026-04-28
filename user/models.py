from django.db import models
from django.contrib.auth.models import AbstractUser

from polls.models import Questions


class User(AbstractUser):
    votes = models.IntegerField(default=0, null=True)
    polls_voted = models.ManyToManyField(to=Questions, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
