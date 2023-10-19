
from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    login_tg = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    chat_id = models.IntegerField(verbose_name='chat_id')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
