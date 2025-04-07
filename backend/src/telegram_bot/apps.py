from aiogram import Dispatcher, Bot
from django.apps import AppConfig


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        from django.conf import settings
        if not hasattr(settings, 'TELEGRAM_BOT_TOKEN'):
            return

        self.dp = Dispatcher()
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        from telegram_bot.handlers.commands import router
        self.dp.include_router(router)
