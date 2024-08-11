from aiogram import Router
from aiogram.types import Message


# инициализация роутера
router = Router()

# хэндлер будет реагировать на любые сообщения бота, непредусмотренные логикой работы бота
@router.message()
async def any_message(message: Message):
    await message.answer(
        text="Это сообщение не входит в функционал бота.\nВоспользуйтесь комагдой /help"
    )