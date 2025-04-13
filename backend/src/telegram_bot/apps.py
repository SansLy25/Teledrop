from aiogram import Dispatcher
from asgiref.sync import async_to_sync

from django.apps import AppConfig


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"

    def ready(self):
        from django.conf import settings

        if not hasattr(settings, "TELEGRAM_BOT_TOKEN"):
            return

        self.dp = Dispatcher()

        from telegram_bot.handlers import commands, base, conversation

        self.dp.include_router(commands.router)
        self.dp.include_router(base.router)
        self.dp.include_router(conversation.router)

        self.set_webhook(
            f"https://{settings.HOST_NAME}/api/telegram/bot/webhook",
            settings.SECRET_KEY,
        )

    def set_webhook(self, url, token):
        from telegram_bot.bot import bot

        async_to_sync(bot.set_webhook)(url, secret_token=token)
