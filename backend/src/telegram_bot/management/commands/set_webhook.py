from asgiref.sync import async_to_sync
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = "Set Telegram webhook"

    def handle(self, *args, **options):
        if not hasattr(settings, "TELEGRAM_WEBHOOK_URL"):
            self.stdout.write(
                self.style.ERROR("TELEGRAM_WEBHOOK_URL not set in settings")
            )
            return

        if not hasattr(apps.get_app_config("telegram_bot"), "bot"):
            self.stdout.write(self.style.ERROR("Bot application not initialized"))
            return

        url = settings.TELEGRAM_WEBHOOK_URL
        self.stdout.write(f"Setting webhook to {url}")

        async_to_sync(apps.get_app_config("telegram_bot").bot.set_webhook)(url)
        self.stdout.write(self.style.SUCCESS("Webhook set successfully"))
