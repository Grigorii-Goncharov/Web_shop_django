from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MaxLengthValidator
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта',validators=[EmailValidator()])
    image = models.ImageField(upload_to='images/', verbose_name='Аватар', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Телефон',validators=[MaxLengthValidator(11)])
    country = models.CharField(max_length=50, verbose_name='Страна')
    token = models.CharField(max_length=120, verbose_name='Токен', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = ("Пользователь")
        verbose_name_plural = ("Пользователи")

