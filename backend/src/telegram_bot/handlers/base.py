from aiogram import Router, types, F
from aiogram.enums import ContentType

router = Router()


@router.message(
    F.content_type.in_({
        ContentType.PHOTO,
        ContentType.DOCUMENT,
        ContentType.VIDEO,
        ContentType.AUDIO,
        ContentType.VOICE
    })
)
async def file_create(message: types.Message):
    await message.answer("Это файл")
