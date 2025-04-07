from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
)
from telegram_bot.states import States

def setup(application):
    """Хендлеры для диалогов с состояниями."""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("register", start_registration)],
        states={
            States.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            States.AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

async def start_registration(update, context):
    """Начало регистрации."""
    await update.message.reply_text("Введите ваше имя:")
    return States.NAME

async def get_name(update, context):
    """Получение имени."""
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"Приятно познакомиться, {update.message.text}! Сколько вам лет?")
    return States.AGE

async def get_age(update, context):
    """Получение возраста."""
    context.user_data['age'] = update.message.text
    await update.message.reply_text(
        f"Спасибо за регистрацию!\n"
        f"Имя: {context.user_data['name']}\n"
        f"Возраст: {context.user_data['age']}"
    )
    return ConversationHandler.END

async def cancel(update, context):
    """Отмена регистрации."""
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END