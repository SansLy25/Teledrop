from aiogram.filters import Command
from aiogram import Router, types


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот на Django + aiogram!")
