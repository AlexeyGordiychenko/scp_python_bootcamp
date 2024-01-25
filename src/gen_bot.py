import asyncio
import json
import logging
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import Message, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv
import msg_text
from random import choice

load_dotenv()
TOKEN = getenv('TOKEN_GEN_BOT')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()

with open(os.path.join(os.path.dirname(__file__), 'data/gen_data.json'), 'r') as f:
    data = json.load(f)

lvl1_builder = ReplyKeyboardBuilder()
lvl2_buttons = {}
for lvl1 in data.keys():
    lvl1_builder.add(KeyboardButton(text=lvl1))
    lvl2_builder = ReplyKeyboardBuilder()
    for lvl2 in data.get(lvl1).keys():
        lvl2_builder.add(KeyboardButton(text=lvl2))
    lvl2_builder.add(KeyboardButton(text=msg_text.back))
    lvl2_builder.adjust(1)
    lvl2_buttons[lvl1] = lvl2_builder.as_markup()
lvl1_builder.adjust(1)
lvl1_buttons = lvl1_builder.as_markup()


class MenuStates(StatesGroup):
    lvl1 = State()
    lvl2 = State()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer(msg_text.gen_welcome)
    await main_menu(message, state)


async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MenuStates.lvl1)
    await message.answer(msg_text.gen_choose_type, reply_markup=lvl1_buttons)


@router.message(MenuStates.lvl1)
async def handle_lvl1(message: Message, state: FSMContext):
    await state.update_data(lvl1_choice=message.text)
    await state.set_state(MenuStates.lvl2)
    await message.answer(msg_text.gen_choose_category, reply_markup=lvl2_buttons.get(message.text))


@router.message(MenuStates.lvl2)
async def handle_lvl2(message: Message, state: FSMContext):
    if message.text == msg_text.back:
        await main_menu(message, state)
        return
    choices = await state.get_data()
    lvl1_choice = choices.get('lvl1_choice')
    lvl2_choice = message.text

    await message.answer(f"{choice(data[lvl1_choice][lvl2_choice][0])} {choice(data[lvl1_choice][lvl2_choice][1])}")
    await main_menu(message, state)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_my_commands()  # temp
    await bot.set_chat_menu_button()  # temp

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
