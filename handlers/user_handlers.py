from copy import deepcopy
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from database.db import user_dict, users_db
from filters.filters import IsDelCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import create_edit_keyboard, creater_bookmark_keyboard
from keyboards.pagen_kb import create_pagin_keyboard
from lexicon.lexicon_RU import LEXICON
from services.file_handling import book


# инициализация роутера
router = Router()

# хендлер срабатывает на команд /start
# если пользователя нет в базе, добавляет его
# отправляет пользователю приветственное сообщение
@router.message(Command(commands="start"))
async def process_command_start(message: Message):
    await message.answer(  # ответ на стартовую команду
        LEXICON[message.text] 
    )

    # если юзера нет в базе данных - добавляется
    if message.from_user.id not in users_db:  
        users_db[message.from_user.id] = deepcopy(user_dict)


# обработчик команды help
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(  # ответ на хелп
        LEXICON[message.text]
    )


# хандлер на команду beginning
@router.message(Command(commands="beginning"))
async def process_command_beginning(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagin_keyboard(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )


# хэнделер на команду continue
# отправляет страницу книги на которой закончено последнее взимодействие с ботом
@router.message(Command(commands="continue"))
async def process_command_continue(message: Message):
    pg = message.from_user.id["page"]  # страница на которой пользователь сейчас
    await message.answer(
        text=book[pg],
        reply_markup=create_pagin_keyboard(
            'backward',
            f'{pg}/{len(book)}',
            'forward'
        )
    )


# хэндлер списка закладок
@router.message(Command(commands='bookmarks'))
async def process_command_bookmarks(message: Message):
    if users_db[message.from_user.id]['marks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=creater_bookmark_keyboard(
                *users_db[message.from_user.id]['marks']
            )
        )
    else:
        await message.answer(
            text=LEXICON['no_bookmarks']
        )


# нажатие кнопки forward
@router.callback_query(F.data == 'forward')
async def process_froward(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagin_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]['page']}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


# нажатие кнопки backword
@router.callback_query(F.data == "backward")
async def procces_backward(callback: CallbackQuery):
    if users_db[callback.from_user.id]["page"] > 1:
        users_db[callback.from_user.id]["page"] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagin_keyboard(
                "backward",
                f'{users_db[callback.from_user.id]['page']}/{len(book)}',
                "forward"
            )
        )
    await callback.answer()


# нажатие на центральную кнопку пагинации
# т.е. добавление страницы в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_add_marks(callback: CallbackQuery):
    users_db[callback.from_user.id['marks']].add(
        users_db[callback.from_user.id['page']]
    )
    await callback.answer('Страница добавлена в закладки.')


# хэндлер на нажатие кнопки из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_mark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id['page']] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagin_keyboard(
            "backward",
            f'{callback.from_user.id['page']}/{len(book)}',
            "forward"
        )
    )


# хэндлер на нажатие кнопки редактировать
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]["marks"]
        )
    )


# хэндлер на кнопку отмена
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['cancel_text']
    )


# хэндлер удаления закладки 
@router.callback_query(IsDelCallbackData())
async def process_del_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['marks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['marks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])

