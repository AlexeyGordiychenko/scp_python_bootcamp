import asyncio
import logging
from aiogram import F, BaseMiddleware, Bot, Dispatcher, Router, types, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import (Message, BotCommand, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery)
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv
from db import Character, Session
import kb
import msg_text

load_dotenv()
TOKEN = getenv('TOKEN')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()


class LoginState(StatesGroup):
    register = State()
    sign_in = State()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(msg_text.welcome, reply_markup=kb.login_menu)


@router.message(F.text == "Exit to main menu")
async def menu(msg: Message):
    await msg.answer(msg_text.welcome, reply_markup=kb.login_menu)


@router.callback_query(F.data == "register")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(LoginState.register)
    await clbck.message.answer(msg_text.enter_name)


@router.callback_query(F.data == "sign_in")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(LoginState.sign_in)
    await clbck.message.answer(msg_text.enter_name)


@router.message(LoginState.register)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    with Session() as session:
        existing_character = session.query(
            Character).filter_by(name=name).first()
        if existing_character:
            await message.answer(msg_text.character_exists, reply_markup=kb.login_menu)
        else:
            new_character = Character(name=name)
            session.add(new_character)
            session.commit()
            await message.answer(msg_text.register_succ)


@router.message(LoginState.sign_in)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    with Session() as session:
        character = session.query(Character).filter_by(name=name).first()
        if character:
            await message.answer(msg_text.sign_in_succ)
        else:
            await message.answer(msg_text.character_not_found, reply_markup=kb.login_menu)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_my_commands()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        level=logging.INFO
    )
    asyncio.run(main())
