from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

back_to_menu_btn = InlineKeyboardButton(text="Back", callback_data='main_menu')

create_character_button = [
    [InlineKeyboardButton(text="Create", callback_data="create_character")],
]
create_character_menu = InlineKeyboardMarkup(
    inline_keyboard=create_character_button)

main_menu_buttons = [
    [InlineKeyboardButton(text="Location", callback_data="get_location"),
     InlineKeyboardButton(text="Go to", callback_data="change_location")],
    [InlineKeyboardButton(text="Inventory", callback_data="get_inventory"),
     InlineKeyboardButton(text="NPC", callback_data="get_npcs")],
    [InlineKeyboardButton(text="Stats", callback_data="get_stats"),
     InlineKeyboardButton(text="Enemies", callback_data="get_enemies")],
]
main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)
