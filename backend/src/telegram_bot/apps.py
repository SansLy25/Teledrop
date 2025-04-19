from aiogram import Dispatcher
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from asgiref.sync import async_to_sync

from django.apps import AppConfig

from telegram_bot.storage import DjangoCacheStorage


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"

    def ready(self):
        from django.conf import settings

        if not hasattr(settings, "TELEGRAM_BOT_TOKEN"):
            return


        self.dp = Dispatcher(
            storage=DjangoCacheStorage() if settings.CACHES else MemoryStorage()
        )

        from telegram_bot.handlers import commands, base, conversation

        self.dp.include_router(commands.router)
        self.dp.include_router(conversation.router)
        self.dp.include_router(base.router)

        self.set_webhook(
            f"https://{settings.HOST_NAME}/api/telegram/bot/webhook",
            settings.SECRET_KEY,
        )

    def set_webhook(self, url, token):
        from telegram_bot.bot import bot

        async_to_sync(bot.set_webhook)(url, secret_token=token)
