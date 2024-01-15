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
from sqlalchemy.orm import selectinload

load_dotenv()
TOKEN = getenv('TOKEN')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()


class MenuStates(StatesGroup):
    create_character = State()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    with db.Session() as session:
        existing_character = session.execute(
            select(db.Character)
            .options(selectinload(db.Character.location), selectinload(db.Character.items))
            .where(db.Character.id == message.from_user.id)
        ).scalar_one_or_none()
    if existing_character:
        await state.update_data(character=existing_character)
        await message.answer(msg_text.welcome.format(name=existing_character.name), reply_markup=kb.main_menu)
    else:
        await message.answer(msg_text.welcome_new, reply_markup=kb.create_character_menu)


@router.callback_query(F.data == "main_menu")
async def main_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(msg_text.choose_action, reply_markup=kb.main_menu)


@router.callback_query(F.data == "create_character")
async def input_character_name(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(MenuStates.create_character)
    await clbck.message.answer(msg_text.enter_name)


@router.message(MenuStates.create_character)
async def create_character(message: Message, state: FSMContext):
    name = message.text
    new_character = db.Character(id=message.from_user.id, name=name)
    with db.Session() as session:
        session.add(new_character)
        session.commit()
        session.refresh(new_character, attribute_names=['location', 'items'])
        await state.update_data(character=new_character)
    await message.answer(msg_text.create_succ, reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_location")
async def get_location(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    await callback_query.message.edit_text(msg_text.current_location.format(location=character.whereami().name), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_hp")
async def get_hp(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    await callback_query.message.edit_text(msg_text.current_health.format(health=character.hp), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_inventory")
async def get_inventory(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    inventory_msg = '\n'.join(
        [f'{item.item}: {item.count}' for item in character.items])
    await callback_query.message.edit_text(f'{msg_text.current_inventory}{inventory_msg}', reply_markup=kb.main_menu)


@router.callback_query(F.data == "change_location")
async def change_location(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    with db.Session() as session:
        session.add(character)
        linked_locations = character.whereami().linked_locations
    builder = InlineKeyboardBuilder()
    for location in linked_locations:
        builder.button(text=location.name,
                       callback_data=f'set_location:{location.id}')
    builder.button(text=msg_text.back, callback_data='main_menu')
    builder.adjust(2)

    await callback_query.message.edit_text(msg_text.change_location_ask, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("set_location:"))
async def set_location(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')
    _, location_id = callback_query.data.split(':')
    character.go(location_id)
    await state.update_data(character=character)
    await callback_query.message.edit_text(msg_text.change_location_succ.format(location=character.whereami().name, desc=character.whereami().description), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_npcs")
async def get_npcs(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')

    with db.Session() as session:
        session.add(character)
        npcs = character.whereami().npcs
    if npcs:
        builder = InlineKeyboardBuilder()
        for npc in npcs:
            builder.button(text=npc.name,
                           callback_data=f'talk_to_npc:{npc.id}:1')
        builder.button(text=msg_text.back, callback_data='main_menu')
        builder.adjust(1)

        await callback_query.message.edit_text(msg_text.pick_npc, reply_markup=builder.as_markup())
    else:
        await callback_query.message.edit_text(msg_text.no_npcs_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("talk_to_npc:"))
async def talk_to_npc(callback_query: CallbackQuery, state: FSMContext):
    _, npc_id, stage_id = callback_query.data.split(':')
    stage_id = int(stage_id)
    data = await state.get_data()
    if stage_id == 1:
        character = data.get('character')
        dialogs = character.talk_to(npc_id)
        dialog = next(dialogs)
    else:
        dialogs = data.get('current_conversation')
        dialog = dialogs.send(stage_id)

    await state.update_data(current_conversation=dialogs)
    builder = InlineKeyboardBuilder()
    for response in dialog.get('responses', []):
        if response.get('next_stage_id'):
            builder.button(text=response.get('text'),
                           callback_data=f"talk_to_npc:{npc_id}:{response.get('next_stage_id')}")
        else:
            builder.button(text=response.get('text', 'Leave'),
                           callback_data='leave_npc')
    builder.adjust(1)

    await callback_query.message.edit_text(dialog.get('npc_text'), reply_markup=builder.as_markup())


@router.callback_query(F.data == "leave_npc")
async def leave_npc(callback_query: CallbackQuery):
    await callback_query.message.edit_text(msg_text.leave_npc, reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_enemies")
async def get_enemies(callback_query: CallbackQuery, state: FSMContext):
    buttons = await get_buttons_for_enemies(state)
    if buttons:
        await callback_query.message.edit_text(msg_text.pick_enemy, reply_markup=buttons)
    else:
        await callback_query.message.edit_text(msg_text.no_enemies_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("fight:"))
async def fight(callback_query: CallbackQuery, state: FSMContext):
    _, enemy_id, enemy_name, enemy_level, enemy_loot = callback_query.data.split(
        ':')
    data = await state.get_data()
    character = data.get('character')

    character_total = randint(1, 6) + int(character.level)
    enemy_total = randint(1, 6) + int(enemy_level)
    with db.Session() as session:
        session.add(character)
        if character_total >= enemy_total:
            character.advance_level()
            if enemy_loot:
                existing_item = next(
                    (item for item in character.items if item.item == enemy_loot), None)
                if existing_item:
                    existing_item.count += 1
                else:
                    new_item = db.Inventory(
                        character_id=character.id, item=enemy_loot, count=1)
                    character.items.append(new_item)
            result_text = msg_text.fight_succ.format(
                enemy=enemy_name, level=character.level, loot=enemy_loot)
        else:
            character.take_hit()
            result_text = msg_text.fight_fail.format(
                enemy=enemy_name, hp=character.hp)
        session.commit()
        session.refresh(character, attribute_names=[
                        'items'] if enemy_loot else None)
        await state.update_data(character=character)
    buttons = await get_buttons_for_enemies(state)
    await callback_query.message.edit_text(f"{result_text}\n{msg_text.pick_enemy}", reply_markup=buttons)


async def get_buttons_for_enemies(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
    character = data.get('character')

    with db.Session() as session:
        session.add(character)
        enemies = character.whereami().enemies

    if enemies:
        builder = InlineKeyboardBuilder()
        for enemy in enemies:
            builder.button(text=enemy.name,
                           callback_data=f'fight:{enemy.id}:{enemy.name}:{enemy.level}:{enemy.loot}')
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
