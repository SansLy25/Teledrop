from telegram.ext import MessageHandler, filters

def setup(application):
    """Базовые хендлеры."""
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

async def echo(update, context):
    """Эхо-ответ на текстовые сообщения."""
    await update.message.reply_text(update.message.text)