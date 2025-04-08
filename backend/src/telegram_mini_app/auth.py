from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from telegram_webapp_auth.auth import TelegramAuthenticator
from telegram_webapp_auth.errors import InvalidInitDataError

from users.models import User


class TelegramInitDataAuth(BaseAuthentication):
    keyword = "tma"

    def __init__(self):
        self._telegram_authenticator = TelegramAuthenticator(
            settings.TELEGRAM_SECRET_KEY
        )

    def validate_header(self, header):
        if header is None:
            raise ValidationError()

        if len(header.split()) != 2:
            raise ValidationError()

        method, auth_cred = header.split()

        if method.lower() != self.keyword:
            raise ValidationError()

        return auth_cred

    @staticmethod
    def get_current_user(init_data):
        tg_id = init_data.user.id

        user, created = User.objects.update_or_create(
            telegram_id=tg_id,
            defaults={
                "telegram_username": init_data.user.username,
                "first_name": init_data.user.first_name,
                "last_name": init_data.user.last_name,
                "language_code": init_data.user.language_code,
            },
        )

        return user

    def authenticate(self, request):
        header = request.headers.get("Authorization", None)
        try:
            auth_cred = self.validate_header(header)
            init_data = self._telegram_authenticator.validate(auth_cred)
        except (InvalidInitDataError, ValidationError):
            return None

        if not init_data.user:
            return None

        return self.get_current_user(init_data), None
