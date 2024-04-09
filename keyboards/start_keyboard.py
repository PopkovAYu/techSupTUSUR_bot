from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from lexicon.lexicon_ru import LEXICON, LEXICON_BUTTONS


def create_start_kb() -> ReplyKeyboardMarkup:
    button_start = KeyboardButton(text=LEXICON_BUTTONS['start'])
    
    
    kb_builder = ReplyKeyboardMarkup(
        keyboard=[[button_start]],
        resize_keyboard=True
        )
    
    return kb_builder

