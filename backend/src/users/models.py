from enum import unique

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField(null=True, blank=True)
    first_name = models.CharField(null=True, blank=True)
    last_name = models.CharField(null=True, blank=True)
    language_code = models.CharField(null=True, blank=True)
    username = None
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []