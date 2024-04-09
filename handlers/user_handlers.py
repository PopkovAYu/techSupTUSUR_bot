from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
# from database.database import user_dict_template, users_db
# from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
# from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
#                                     create_edit_keyboard)
from keyboards.keyboard import create_inline_kb, create_inline__url_kb
from keyboards.start_keyboard import create_start_kb
from lexicon.lexicon_ru import LEXICON
# from services.file_handling import book

router = Router()

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'], 
                        #  reply_markup=create_inline_kb(2, 'to_support', 'knowlage_base', button_1='Кнопка 1'),
                         reply_markup=create_start_kb()
                         )
    # if message.from_user.id not in users_db:
    #     users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(F.text == 'Начать')
async def process_start_button(message: Message):
    await message.answer(text=LEXICON['start'], 
                        reply_markup=create_inline_kb(1, 'to_support', 'check', 'knowlage_base'),
                        )

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'button_1' 

@router.callback_query(F.data == 'knowlage_base')
async def process_buttons_press(callback: CallbackQuery):
    if callback.message.text != LEXICON['knowlage_base']:
        await callback.message.edit_text(
            text=LEXICON['knowlage_base_choice'], 
            reply_markup=create_inline__url_kb(1, 'web_resources', 'mobile_app')
            )
    await callback.answer()
 