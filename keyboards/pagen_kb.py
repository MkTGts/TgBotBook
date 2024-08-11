from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_RU import LEXICON


# функция генерирующая клавиатуру пагинации страниц книг
def create_pagin_keyboard(*args: str) -> InlineKeyboardMarkup:
    # инициализация инлайн билдера 
    kb_inline_builder = InlineKeyboardBuilder()

    #добавление в билдер ряд кнопок
    kb_inline_builder.row([
        InlineKeyboardButton(
            text=LEXICON[but] if but in LEXICON else but, 
            callback_data=but)
        for but in args]
    )

    # функция возвращает объект-инлайнклавиатуру
    return kb_inline_builder.as_markup()