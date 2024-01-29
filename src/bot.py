import asyncio
import logging
from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv
import db
import kb
import msg_text
import html

load_dotenv()
TOKEN = getenv('TOKEN')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()


def check_character(func):
    async def wrapper(callback_query: CallbackQuery, state: FSMContext, character: db.Protagonist = None, **kwargs):
        data = await state.get_data()
        if character is None:
            character = data.get('character')
        msg_id = data.get('msg_id')
        if character is None or callback_query.message.message_id != msg_id:
            await send_edit_message(callback_query, msg_text.msg_no_character)
        else:
            return await func(callback_query=callback_query, state=state, character=character, **kwargs)
    return wrapper


class MenuStates(StatesGroup):
    create_character = State()


async def send_edit_message(callback_query: CallbackQuery, msg: str, reply_markup: types.InlineKeyboardMarkup = None):
    current_btns = [
        btn.text for row in reply_markup.inline_keyboard for btn in row] if reply_markup else []
    msg_btns = [
        btn.text for row in callback_query.message.reply_markup.inline_keyboard for btn in row]
    if html.unescape(msg) != html.unescape(callback_query.message.html_text) \
            or current_btns != msg_btns:
        await callback_query.message.edit_text(msg, reply_markup=reply_markup)


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    if msg_id:
        if not await bot.delete_message(message.chat.id, msg_id):
            return
    existing_character = await db.get_character(message.from_user.id)
    if existing_character:
        await state.update_data(character=existing_character)
        msg = await message.answer(msg_text.msg_welcome.format(name=existing_character.name), reply_markup=kb.main_menu)
        await state.update_data(msg_id=msg.message_id)
    else:
        await message.answer(msg_text.msg_welcome_new, reply_markup=kb.create_character_menu)


@router.callback_query(F.data == "main_menu")
async def main_menu(callback_query: CallbackQuery):
    await send_edit_message(callback_query, msg_text.msg_choose_action, reply_markup=kb.main_menu)


@router.callback_query(F.data == "create_character")
async def input_character_name(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(MenuStates.create_character)
    await send_edit_message(callback_query, msg_text.msg_enter_name)


@router.message(MenuStates.create_character)
async def create_character(message: Message, state: FSMContext):
    new_character = await db.create_character(message.from_user.id, message.text)
    await state.update_data(character=new_character)
    msg = await message.answer(msg_text.msg_create_succ, reply_markup=kb.main_menu)
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data == "get_location")
@check_character
async def get_location(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    location = await character.whereami()
    await send_edit_message(callback_query, msg_text.msg_current_location.format(location=location.name), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_stats")
@check_character
async def get_stats(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    await send_edit_message(callback_query, msg_text.msg_stats.format(health=character.hp, level=character.level), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_inventory")
@check_character
async def get_inventory(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    inventory_msg = '\n'.join(
        [f"{entry.get('item')}: {entry.get('count')}" for entry in await character.get_inventory()])
    await send_edit_message(callback_query, f'{msg_text.msg_current_inventory}{inventory_msg}', reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_usable_items")
@check_character
async def get_usable_items(callback_query: CallbackQuery,  character: db.Protagonist, effect: str = None, **kwargs):
    usable_items = await character.get_usable_inventory()
    if not usable_items:
        if effect:
            msg = effect
            reply_markup = kb.back_menu
        else:
            msg = msg_text.msg_no_usable_items
            reply_markup = kb.main_menu
    else:
        msg = effect if effect else msg_text.msg_choose_item_to_use
        builder = InlineKeyboardBuilder()
        for idx, item in enumerate(usable_items):
            builder.button(text=f'{item.item.name} ({item.count})',
                           callback_data=f'use_item:{idx}')
        builder.add(kb.back_to_menu_btn)
        builder.adjust(1)
        reply_markup = builder.as_markup()
    await send_edit_message(callback_query, msg, reply_markup=reply_markup)


@router.callback_query(F.data.startswith("use_item:"))
@check_character
async def use_item(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    _, item_idx = callback_query.data.split(':')
    effect = msg_text.format_string(await character.use_item(
        character.inventory_usable[int(item_idx)]))
    await get_usable_items(callback_query=callback_query, character=character, effect=effect, **kwargs)


@router.callback_query(F.data == "change_location")
@check_character
async def change_location(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    location = await character.whereami()
    directions = await location.get_directions()
    builder = InlineKeyboardBuilder()
    for direction in directions:
        builder.button(text=direction.name,
                       callback_data=f'set_location:{direction.id}')
    builder.add(kb.back_to_menu_btn)
    builder.adjust(2)

    await send_edit_message(callback_query, msg_text.msg_change_location_ask, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("set_location:"))
@check_character
async def set_location(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    _, location_id = callback_query.data.split(':')
    await character.go(location_id)
    location = await character.whereami()
    await send_edit_message(callback_query, msg_text.msg_change_location_succ.format(location=location.name, desc=location.description), reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_npcs")
@check_character
async def get_npcs(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    location = await character.whereami()
    npcs = await location.get_npcs()

    if npcs:
        builder = InlineKeyboardBuilder()
        for idx, npc in enumerate(npcs):
            builder.button(text=npc.name,
                           callback_data=f'interact_with_npc:{idx}')
        builder.add(kb.back_to_menu_btn)
        builder.adjust(1)

        await send_edit_message(callback_query, msg_text.msg_pick_npc, reply_markup=builder.as_markup())
    else:
        await send_edit_message(callback_query, msg_text.msg_no_npcs_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("interact_with_npc:"))
@check_character
async def interact_with_npc(callback_query: CallbackQuery,  msg: str = None, **kwargs):
    _, npc_idx = callback_query.data.split(':')
    builder = InlineKeyboardBuilder()
    builder.button(text=msg_text.btn_dialog,
                   callback_data=f"npc_dialog:{npc_idx}:1")
    builder.button(text=msg_text.btn_quest,
                   callback_data=f"npc_quest:{npc_idx}")
    builder.button(text=msg_text.btn_back, callback_data=f"get_npcs")
    builder.button(text=msg_text.btn_menu, callback_data=f"main_menu")
    builder.adjust(2)
    await send_edit_message(callback_query, msg if msg else msg_text.msg_choose_action, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("npc_dialog:"))
@check_character
async def npc_dialog(callback_query: CallbackQuery, state: FSMContext, character: db.Protagonist, **kwargs):
    _, npc_idx, stage_id = callback_query.data.split(':')
    stage_id = int(stage_id)
    if stage_id == 1:
        location = await character.whereami()
        npc = location.npcs[int(npc_idx)]
        dialogs = character.talk_to(npc)
        dialog = next(dialogs)
    else:
        data = await state.get_data()
        dialogs = data.get('current_conversation')
        dialog = dialogs.send(stage_id)

    await state.update_data(current_conversation=dialogs)
    builder = InlineKeyboardBuilder()
    for response in dialog.responses:
        if response.next_stage_id:
            builder.button(text=response.text,
                           callback_data=f"npc_dialog:{npc_idx}:{response.next_stage_id}")
        else:
            builder.button(text=response.text,
                           callback_data=f'interact_with_npc:{npc_idx}')
    builder.adjust(2)

    await send_edit_message(callback_query, msg_text.format_string(dialog.npc_text), reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("npc_quest:"))
@check_character
async def npc_quest(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    _, npc_idx = callback_query.data.split(':')
    location = await character.whereami()
    npc = location.npcs[int(npc_idx)]
    quest, journal_entry = await character.get_npc_quest(npc)
    if not quest or (journal_entry and journal_entry.completed):
        await send_edit_message(callback_query, msg_text.msg_npc_no_quest, reply_markup=callback_query.message.reply_markup)
    else:
        builder = InlineKeyboardBuilder()
        if journal_entry:
            builder.button(text=msg_text.btn_complete_quest,
                           callback_data=f'npc_quest_complete:{npc_idx}')
        elif quest.required_level > character.level:
            builder.button(text=msg_text.btn_quest_not_available.format(
                level=quest.required_level), callback_data='no_handling')
        else:
            builder.button(text=msg_text.btn_accept,
                           callback_data=f'npc_quest_accept:{npc_idx}')
        builder.button(text=msg_text.btn_back,
                       callback_data=f'interact_with_npc:{npc_idx}')
        await send_edit_message(callback_query, msg_text.format_string(quest.task), reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("npc_quest_accept:"))
@check_character
async def npc_quest_accept(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    _, npc_idx = callback_query.data.split(':')
    location = await character.whereami()
    npc = location.npcs[int(npc_idx)]
    await character.accept_npc_quest(npc)
    await interact_with_npc(callback_query=callback_query, character=character, **kwargs)


@router.callback_query(F.data.startswith("npc_quest_complete:"))
@check_character
async def npc_quest_complete(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    _, npc_idx = callback_query.data.split(':')
    location = await character.whereami()
    npc = location.npcs[int(npc_idx)]
    if await character.complete_npc_quest(npc):
        msg = msg_text.msg_quest_complete_succ
    else:
        msg = msg_text.msg_quest_complete_deny
    await interact_with_npc(callback_query=callback_query, character=character, msg=msg, **kwargs)


@router.callback_query(F.data == "get_quests")
@check_character
async def get_quests(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    quests = await character.get_active_quests()
    if quests:
        quests_msg = '\n'.join([msg_text.msg_quest.format(
            npc=quest.get('npc'), location=quest.get('location'), task=quest.get('task')) for quest in quests])
        msg = f'{msg_text.msg_current_quests}{quests_msg}'
    else:
        msg = msg_text.msg_no_quests
    await send_edit_message(callback_query, msg, reply_markup=kb.main_menu)


@router.callback_query(F.data == "get_enemies")
@check_character
async def get_enemies(callback_query: CallbackQuery,  character: db.Protagonist, msg: str = None, **kwargs):
    location = await character.whereami()
    enemies = await location.get_enemies()
    if enemies:
        builder = InlineKeyboardBuilder()
        for idx, enemy in enumerate(enemies):
            builder.button(text=f"{enemy.name} (lvl {enemy.level})",
                           callback_data=f'fight:{idx}')
        builder.add(kb.back_to_menu_btn)
        builder.adjust(1)
        await send_edit_message(callback_query, msg if msg else msg_text.msg_pick_enemy, reply_markup=builder.as_markup())
    else:
        await send_edit_message(callback_query, msg_text.msg_no_enemies_in_location, reply_markup=kb.main_menu)


@router.callback_query(F.data.startswith("fight:"))
@check_character
async def fight(callback_query: CallbackQuery,  character: db.Protagonist, **kwargs):
    _, enemy_idx = callback_query.data.split(':')
    location = await character.whereami()
    enemy = location.enemies[int(enemy_idx)]
    try:
        res, loot = await character.attack(enemy)
    except Exception as e:
        if str(e) == 'You died':
            msg = msg_text.msg_fight_die.format(enemy=enemy.name)
            await character.die()
            await send_edit_message(callback_query, msg)
            return

    if res and enemy.loot_id:
        result_text = msg_text.msg_fight_succ.format(
            enemy=enemy.name, level=character.level, loot=loot.name)
    elif res:
        result_text = msg_text.msg_fight_succ_no_loot.format(
            enemy=enemy.name, level=character.level)
    else:
        result_text = msg_text.msg_fight_fail.format(
            enemy=enemy.name, hp=character.hp)

    await get_enemies(callback_query=callback_query, character=character,
                      msg=f"{result_text}\n{msg_text.msg_pick_enemy}", **kwargs)


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
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    asyncio.run(main())
