from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from telegram.auth import TelegramInitDataAuth


class PrimaryTelegramAuthView(GenericAPIView):
    authentication_classes = [TelegramInitDataAuth, JWTAuthentication]

    @extend_schema()
    def post(self, request):
        return Response({"user": str(request.user.telegram_id)}, 200)
