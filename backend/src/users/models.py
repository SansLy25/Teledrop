from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)

from storage.models import Folder


class UserManager(models.Manager):
    def create_user(self, email=None, password=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email) if email else None,
            **extra_fields,
        )

        if password:
            user.set_password(password)

        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField(null=True, blank=True)
    first_name = models.CharField(null=True, blank=True)
    last_name = models.CharField(null=True, blank=True)
    language_code = models.CharField(null=True, blank=True)
    root_folder = models.OneToOneField(
        Folder, on_delete=models.CASCADE, related_name="user_root"
    )
    current_folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="current_users",
        null=True,
        blank=True,
    )
    date_joined = models.DateField(auto_now_add=True)
    username = None
    last_login = None
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not hasattr(self, "root_folder") and not Folder.objects.filter(
            owner=self, parent__isnull=True
        ):
            self.root_folder = Folder.objects.create(name="", owner=self)

        super().save()
