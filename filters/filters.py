from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


# проверяет что коллбэк состоит только из цифр; то есть номер страницы
class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        await callback.data.isdigit()


# проверяет что колбэк отоносится к кнопке удаления страницы
class IsDelCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        await callback.data.endswith("_del") and callback.data[:3].isdigit()

