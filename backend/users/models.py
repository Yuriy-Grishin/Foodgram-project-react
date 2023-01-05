from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.authtoken.models import Token


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Пользователи"


class Subscriber(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    class Meta:
        verbose_name_plural = "Подписчики"


class ProxyToken(Token):

    class Meta:
        proxy = True
        verbose_name_plural = "Токены"
