import asyncio
import datetime

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, User

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import get_addresses_keyboard

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
        reply_markup=get_addresses_keyboard()
    )


# Этот хендлер срабатывает на кнопку "Отмена" и сбрасывает состояние FSM
@router.callback_query(F.data == 'cancel')
async def process_press_cancel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LEXICON_RU['/help']
    )
    await state.clear()