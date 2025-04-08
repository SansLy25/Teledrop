from aiogram import Dispatcher
from asgiref.sync import async_to_sync

from django.apps import AppConfig


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        from django.conf import settings
        if not hasattr(settings, 'TELEGRAM_BOT_TOKEN'):
            return

        self.dp = Dispatcher()

        from telegram_bot.handlers.commands import router
        self.dp.include_router(router)
        self.set_webhook(settings.TELEGRAM_WEBHOOK_URL,
                         settings.SECRET_KEY)

    def set_webhook(self, url, token):
        from telegram_bot.bot import bot
        async_to_sync(bot.set_webhook)(url, secret_token=token)
