from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_RU import LEXICON
from services.file_handling import book


# функция создает клавиатуру закладок
def creater_bookmark_keyboard(*args: int) -> InlineKeyboardMarkup:
    # создание объекта билдера инлайн клавиатуры
    kb_inline_builder = InlineKeyboardBuilder()

    # наполнение клавиатуры кнопками закладок
    for but in sorted(args):
        kb_inline_builder.row(InlineKeyboardButton(
            text=f'{but} - {book[but][:100]}',
            callback_data=str(but)
        ))

    # добавление в клавиатуру двух кнопок: Редактировать и Отменить
    kb_inline_builder.row(InlineKeyboardButton(
        text=LEXICON['edit_bookmarks_but'],
        callback_data='edit_bookmarks_but'
    ),
    InlineKeyboardButton(
        text=LEXICON['cancel_but'],
        callback_data='cancel_but'
        ), 
        #width=2 ???????????
    )

    return kb_inline_builder.as_markup()


# функция вызванной инлайн клавиатуры по редактированию закладок
def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    # создание инлайн билдера
    kb_inline_builder = InlineKeyboardBuilder()

    # наполнение клавиатуры кнопками редактирования(по сути только удаления) закладок
    for but in sorted(args):
        kb_inline_builder.row(
            InlineKeyboardButton(
                text=f'{LEXICON["del"]}{but} - {LEXICON[but][:100]}',
                callback_data=f'{but}_del'
            )
        )

    # добавляем в конец клавиатуры кнопку отменить
    kb_inline_builder.row(
        InlineKeyboardButton(
            text=LEXICON["cancel_but"],
            callback_data="cancel_but"
        )
    )

    return kb_inline_builder.as_markup()