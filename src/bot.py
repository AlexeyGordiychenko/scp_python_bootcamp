import asyncio
import logging
from random import randint
from aiogram import F, BaseMiddleware, Bot, Dispatcher, Router, types, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import (Message, BotCommand, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery, MenuButtonDefault)
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv
import db
import kb
import msg_text
from sqlalchemy import inspect, select
from sqlalchemy.orm import selectinload, LoaderCallableStatus
import html

load_dotenv()
TOKEN = getenv('TOKEN')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()


class MenuStates(StatesGroup):
    create_character = State()


async def send_edit_message(callback_query: CallbackQuery, msg: str, reply_markup: types.InlineKeyboardMarkup):
    if html.unescape(msg) != html.unescape(callback_query.message.html_text):
        await callback_query.message.edit_text(msg, reply_markup=reply_markup)


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    with db.Session() as session:
        existing_character = session.execute(
            select(db.Character)
            .where(db.Character.id == message.from_user.id)
        ).scalar_one_or_none()
    if existing_character:
        await state.update_data(character=existing_character)
        await message.answer(msg_text.msg_welcome.format(name=existing_character.name), reply_markup=kb.main_menu)
    else:
        await message.answer(msg_text.msg_welcome_new, reply_markup=kb.create_character_menu)


@router.callback_query(F.data == "main_menu")
async def main_menu(callback_query: CallbackQuery):
    await send_edit_message(callback_query, msg_text.msg_choose_action, reply_markup=kb.main_menu)


@router.callback_query(F.data == "create_character")
async def input_character_name(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(MenuStates.create_character)
    await clbck.message.answer(msg_text.msg_enter_name)


@router.message(MenuStates.create_character)
async def create_character(message: Message, state: FSMContext):
    name = message.text
    new_character = db.Character(id=message.from_user.id, name=name)
    with db.Session() as session:
        session.add(new_character)
        session.commit()

        await state.update_data(character=new_character)
    await message.answer(msg_text.msg_create_succ, reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_location")
async def get_location(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    await send_edit_message(callback_query, msg_text.msg_current_location.format(location=character.whereami().name), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_stats")
async def get_stats(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    await send_edit_message(callback_query, msg_text.msg_stats.format(health=character.hp, level=character.level), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_inventory")
async def get_inventory(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    with db.Session() as session:
        session.add(character)
        inventory_msg = '\n'.join(
            [f'{item.item.name}: {item.count}' for item in character.inventory])
    await send_edit_message(callback_query, f'{msg_text.msg_current_inventory}{inventory_msg}', reply_markup=kb.main_menu)


@router.callback_query(F.data == "change_location")
async def change_location(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    linked_locations = character.whereami().get_linked_locations()
    builder = InlineKeyboardBuilder()
    for location in linked_locations:
        builder.button(text=location.name,
                       callback_data=f'set_location:{location.id}')
    builder.button(text=msg_text.msg_back, callback_data='main_menu')
    builder.adjust(2)

    await send_edit_message(callback_query, msg_text.msg_change_location_ask, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("set_location:"))
async def set_location(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    _, location_id = callback_query.data.split(':')
    character.go(location_id)
    await send_edit_message(callback_query, msg_text.msg_change_location_succ.format(location=character.whereami().name, desc=character.whereami().description), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_npcs")
async def get_npcs(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    npcs = character.whereami().get_npcs()

    if npcs:
        builder = InlineKeyboardBuilder()
        for idx, npc in enumerate(npcs):
            builder.button(text=npc.name,
                           callback_data=f'talk_to_npc:{idx}:1')
        builder.button(text=msg_text.msg_back, callback_data='main_menu')
        builder.adjust(1)

        await send_edit_message(callback_query, msg_text.msg_pick_npc, reply_markup=builder.as_markup())
    else:
        await send_edit_message(callback_query, msg_text.msg_no_npcs_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("talk_to_npc:"))
async def talk_to_npc(callback_query: CallbackQuery, state: FSMContext):
    _, npc_idx, stage_id = callback_query.data.split(':')
    stage_id = int(stage_id)
    data = await state.get_data()
    if stage_id == 1:
        character = data.get('character')
        npc = character.whereami().npcs[int(npc_idx)]
        dialogs = character.talk_to(npc)
        dialog = next(dialogs)
    else:
        dialogs = data.get('current_conversation')
        dialog = dialogs.send(stage_id)

    await state.update_data(current_conversation=dialogs)
    builder = InlineKeyboardBuilder()
    for response in dialog.responses:
        if response.next_stage_id:
            builder.button(text=response.text,
                           callback_data=f"talk_to_npc:{npc_idx}:{response.next_stage_id}")
        else:
            builder.button(text=response.text, callback_data='leave_npc')
    builder.adjust(2)

    await send_edit_message(callback_query, msg_text.format_string(dialog.npc_text), reply_markup=builder.as_markup())


@router.callback_query(F.data == "leave_npc")
async def leave_npc(callback_query: CallbackQuery):
    await send_edit_message(callback_query, msg_text.msg_leave_npc, reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_enemies")
async def get_enemies(callback_query: CallbackQuery, state: FSMContext):
    buttons = await get_buttons_for_enemies(state)
    if buttons:
        await send_edit_message(callback_query, msg_text.msg_pick_enemy, reply_markup=buttons)
    else:
        await send_edit_message(callback_query, msg_text.msg_no_enemies_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("fight:"))
async def fight(callback_query: CallbackQuery, state: FSMContext):
    _, enemy_idx = callback_query.data.split(':')
    data = await state.get_data()
    character = data.get('character')
    enemy = character.whereami().get_enemies()[int(enemy_idx)]
    res, loot = character.attack(enemy)
    if res and enemy.loot_id:
        result_text = msg_text.msg_fight_succ.format(
            enemy=enemy.name, level=character.level, loot=loot.name)
    elif res:
        result_text = msg_text.msg_fight_succ_no_loot.format(
            enemy=enemy.name, level=character.level)
    else:
        result_text = msg_text.msg_fight_fail.format(
            enemy=enemy.name, hp=character.hp)

    buttons = await get_buttons_for_enemies(state)
    await send_edit_message(callback_query, f"{result_text}\n{msg_text.msg_pick_enemy}", reply_markup=buttons)


async def get_buttons_for_enemies(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
    character = data.get('character')
    enemies = character.whereami().get_enemies()

    if enemies:
        builder = InlineKeyboardBuilder()
        for idx, enemy in enumerate(enemies):
            builder.button(text=enemy.name,
                           callback_data=f'fight:{idx}')
        builder.button(text=msg_text.msg_back, callback_data='main_menu')
        builder.adjust(1)
        return builder.as_markup()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # await bot.delete_my_commands()  # temp
    # await bot.set_chat_menu_button()  # temp

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
