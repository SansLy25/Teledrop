from aiogram import Router, types


router = Router()


@router.message(
    lambda message: any(
        [
            message.document,
            message.photo,
            message.video,
            message.audio,
            message.voice,
            message.video_note,
            message.sticker,
        ]
    )
)
async def file_create(message: types.Message):
    await message.answer("Это файл")
