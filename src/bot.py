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
from sqlalchemy import select

load_dotenv()
TOKEN = getenv('TOKEN')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()
session = db.Session()


class MenuStates(StatesGroup):
    create_character = State()


@router.message(Command("start"))
async def start_command(message: Message):
    existing_character = session.execute(select(db.Character.name).where(
        db.Character.id == message.from_user.id)).scalars().first()

    if existing_character:
        await message.answer(msg_text.welcome.format(name=existing_character), reply_markup=kb.main_menu)
    else:
        await message.answer(msg_text.welcome_new, reply_markup=kb.create_character_menu)


@router.callback_query(F.data == "main_menu")
async def main_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(msg_text.choose_action, reply_markup=kb.main_menu)


@router.callback_query(F.data == "create_character")
async def input_character_name(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(MenuStates.create_character)
    await clbck.message.answer(msg_text.enter_name)


@router.callback_query(F.data == "get_location")
async def get_location(callback_query: CallbackQuery):
    current_location = session.execute(select(db.Location.name).join(db.Character).where(
        db.Character.id == callback_query.from_user.id)).scalars().first()

    if not current_location:
        current_location = 'Unknown'
    # await bot.send_message(callback_query.from_user.id, msg_text.current_location.format(location=current_location), reply_markup=kb.main_menu)
    await callback_query.message.edit_text(msg_text.current_location.format(location=current_location), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_hp")
async def get_hp(callback_query: CallbackQuery):
    current_health = session.execute(select(db.Character.hp).where(
        db.Character.id == callback_query.from_user.id)).scalars().first()
    if not current_health:
        current_health = 'Unknown'
    # await bot.send_message(callback_query.from_user.id, msg_text.current_health.format(health=current_health), reply_markup=kb.main_menu)
    await callback_query.message.edit_text(msg_text.current_health.format(health=current_health), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_inventory")
async def get_inventory(callback_query: CallbackQuery):
    current_character = session.execute(select(db.Character).where(
        db.Character.id == callback_query.from_user.id)).scalars().first()
    inventory_msg = '\n'.join(
        [f'{item.item}: {item.count}' for item in current_character.items])
    # await bot.send_message(callback_query.from_user.id, f'{msg_text.current_inventory}\n{inventory_msg}', reply_markup=kb.main_menu)
    await callback_query.message.edit_text(f'{msg_text.current_inventory}\n{inventory_msg}', reply_markup=kb.main_menu)


@router.callback_query(F.data == "change_location")
async def change_location(callback_query: CallbackQuery):
    current_location = session.execute(select(db.Location).join(db.Character).where(
        db.Character.id == callback_query.from_user.id)).scalars().first()
    builder = InlineKeyboardBuilder()
    for location in current_location.linked_locations:
        builder.button(text=location.name,
                       callback_data=f'set_location:{location.id}:{location.name}')
    builder.button(text=msg_text.back, callback_data='main_menu')
    builder.adjust(2)

    # await bot.send_message(callback_query.from_user.id, msg_text.change_location_ask, reply_markup=builder.as_markup())
    await callback_query.message.edit_text(msg_text.change_location_ask, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("set_location:"))
async def set_location(callback_query: CallbackQuery):
    _, location_id, location_name = callback_query.data.split(':')
    character = session.execute(select(db.Character).where(
        db.Character.id == callback_query.from_user.id)).scalars().first()
    if character:
        character.location_id = location_id
        session.commit()

    # await bot.send_message(callback_query.from_user.id, msg_text.change_location_succ.format(location=location_name), reply_markup=kb.main_menu)
    await callback_query.message.edit_text(msg_text.change_location_succ.format(location=location_name), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_npcs")
async def get_npcs(callback_query: CallbackQuery):
    current_location = session.execute(select(db.Location).join(db.Character).where(
        db.Character.id == callback_query.from_user.id)).scalars().first()
    npcs = current_location.npcs
    if npcs:
        builder = InlineKeyboardBuilder()
        for npc in npcs:
            builder.button(text=npc.name,
                           callback_data=f'talk_to_npc:{npc.id}:{npc.name}:{npc.dialog_id}:1')
        builder.button(text=msg_text.back, callback_data='main_menu')
        builder.adjust(1)

        # await bot.send_message(callback_query.from_user.id, msg_text.pick_npc, reply_markup=builder.as_markup())
        await callback_query.message.edit_text(msg_text.pick_npc, reply_markup=builder.as_markup())
    else:
        await callback_query.message.edit_text(msg_text.no_npcs_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("talk_to_npc:"))
async def talk_to_npc(callback_query: CallbackQuery):
    _, npc_id, npc_name, dialog_id, stage = callback_query.data.split(':')
    npc_text = session.execute(select(db.Dialog.npc_text).where(
        db.Dialog.id == dialog_id, db.Dialog.stage == stage)).scalars().first()
    responses = session.execute(select(db.PlayerResponse).where(
        db.PlayerResponse.dialog_id == dialog_id, db.PlayerResponse.stage_id == stage)).scalars().all()
    builder = InlineKeyboardBuilder()
    for response in responses:
        if response.next_stage_id:
            builder.button(text=response.text,
                           callback_data=f'talk_to_npc:{npc_id}:{npc_name}:{dialog_id}:{response.next_stage_id}')
        else:
            builder.button(text=response.text,
                           callback_data=f'leave_npc:{npc_name}')
    builder.adjust(1)

    # await bot.send_message(callback_query.from_user.id, npc_text, reply_markup=builder.as_markup())
    await callback_query.message.edit_text(npc_text, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("leave_npc:"))
async def leave_npc(callback_query: CallbackQuery):
    npc_name = callback_query.data.split(':')[1]
    # await bot.send_message(callback_query.from_user.id, msg_text.leave_npc.format(name=npc_name), reply_markup=kb.main_menu)
    await callback_query.message.edit_text(msg_text.leave_npc.format(name=npc_name), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_enemies")
async def get_enemies(callback_query: CallbackQuery):
    buttons = await get_buttons_for_enemies(callback_query.from_user.id)
    if buttons:
        await callback_query.message.edit_text(msg_text.pick_enemy, reply_markup=buttons)
    else:
        await callback_query.message.edit_text(msg_text.no_enemies_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("fight:"))
async def fight(callback_query: CallbackQuery):
    _, enemy_id, enemy_name, enemy_level = callback_query.data.split(':')
    character = session.execute(select(db.Character).where(
        db.Character.id == callback_query.from_user.id)).scalars().first()

    character_total = randint(1, 6) + int(character.level)
    enemy_total = randint(1, 6) + int(enemy_level)

    if character_total >= enemy_total:
        character.level += 1
        result_text = msg_text.fight_succ.format(
            enemy=enemy_name, level=character.level)
    else:
        character.hp -= 1
        result_text = msg_text.fight_fail.format(
            enemy=enemy_name, hp=character.hp)
    session.commit()
    buttons = await get_buttons_for_enemies(callback_query.from_user.id)
    await callback_query.message.edit_text(f"{result_text}\n{msg_text.pick_enemy}", reply_markup=buttons)


@router.message(MenuStates.create_character)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    new_character = db.Character(id=message.from_user.id, name=name)
    session.add(new_character)
    session.commit()
    await message.answer(msg_text.create_succ, reply_markup=kb.main_menu)
    # await message.edit_text(msg_text.create_succ, reply_markup=kb.main_menu)


async def get_buttons_for_enemies(user_id: int) -> InlineKeyboardMarkup:
    current_location = session.execute(select(db.Location).join(db.Character).where(
        db.Character.id == user_id)).scalars().first()
    enemies = current_location.enemies
    builder = InlineKeyboardBuilder()
    if enemies:
        for enemy in enemies:
            builder.button(text=enemy.name,
                           callback_data=f'fight:{enemy.id}:{enemy.name}:{enemy.level}')
        builder.button(text=msg_text.back, callback_data='main_menu')
        builder.adjust(1)

    return builder.as_markup()


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
