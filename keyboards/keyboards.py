from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_RU
from services.services import shops


# Функция создает инлайн клавиатуру с запросом н вывод списка магазинов
def get_addresses_kb() -> InlineKeyboardMarkup:
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


# Функция создает инлайн клавиатуру с адресами магазинов
def addresses_list_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for k, v in shops.items():
        kb_builder.row(InlineKeyboardButton(
            text=f'{k}: {v}',
            callback_data=k
            )
        ),
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['cancel'],
            callback_data='cancel'
        )
    )
    return kb_builder.as_markup()


# Функция создает клавиатуру с кнопками Да и Нет
def yes_no_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(
        InlineKeyboardButton(
            text=LEXICON_RU['yes'],
            callback_data='yes'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['no'],
            callback_data='no'
        )
    )
    return kb_builder.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(
        InlineKeyboardButton(
            text=LEXICON_RU['cancel'],
            callback_data='cancel'
        )
    )
    return kb_builder.as_markup()