import asyncio
import datetime

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, User

from lexicon.lexicon import LEXICON_RU

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
