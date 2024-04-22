from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, User

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import get_addresses_kb, addresses_list_kb, yes_no_kb
from services.services import shops
from filters.filters import IsShopKey, IsShopKeyInput

router = Router()


# Этот хендлер срабатывает на команду /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хендлер срабатывает на команду /help
@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хендлер срабатывает на команду /contacts
@router.message(Command('contacts'))
async def contacts_command(message: Message):
    await message.answer(text=LEXICON_RU['/contacts'])


# Этот хендлер срабатывает на команду /service
@router.message(Command('service'))
async def service_command(message: Message):
    await message.answer(text=LEXICON_RU['/service'])


# Этот хендлер срабатывает на команду /replace
@router.message(Command('replace'))
async def replace_command(message: Message):
    await message.answer(
        text=LEXICON_RU['replace'],
        reply_markup=get_addresses_kb()
    )


# Этот хендлер срабатывает на кнопку "Отмена" и сбрасывает состояние FSM
@router.callback_query(F.data == 'cancel')
async def process_press_cancel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LEXICON_RU['/help']
    )
    await state.clear()


# Этот хендлер срабатывает на кнопку "Список адресов"
@router.callback_query(F.data == 'addresses_list')
async def process_address_list(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(
        text=LEXICON_RU['choose_address'],
        reply_markup=addresses_list_kb(),
    )


# Этот хендлер срабатывает на кнопку с адресом магазина
@router.callback_query(IsShopKey())
async def process_shop_button(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(
        text=f"{LEXICON_RU['is_right_choose']}: {shops[callback.data]}",
        reply_markup=yes_no_kb()
    )


@router.message(IsShopKeyInput())
async def process_shop_button(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        text=f"{LEXICON_RU['is_right_choose']}: {shops[message.text]}",
        reply_markup=yes_no_kb()
    )
