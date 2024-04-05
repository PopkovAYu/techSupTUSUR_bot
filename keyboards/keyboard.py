from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON


# Функция, генерирующая клавиатуру для стартового сообщения
def create_start_keyboard() -> InlineKeyboardMarkup:
    # Создаем объекты инлайн-кнопок
    knowlage_base_button = InlineKeyboardButton(
        text=LEXICON['knowlage_base'],
        url=LEXICON['knowlage_base_url']
        )
    to_support_button = InlineKeyboardButton(
        text=LEXICON['to_support'],
        url=LEXICON['to_support_url']
        )

    # Создаем объект инлайн-клавиатуры
    kb_builder = InlineKeyboardMarkup(
        inline_keyboard=[[knowlage_base_button],
                        [to_support_button]]
        )
    
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder
