from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_RU


# Функция создает инлайн клавиатуру с запросом н вывод списка магазинов
def get_addresses_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['get_addresses'],
            callback_data='addresses_list'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['cancel'],
            callback_data='cancel'
        ),
        width=1
    )
    return kb_builder.as_markup()
