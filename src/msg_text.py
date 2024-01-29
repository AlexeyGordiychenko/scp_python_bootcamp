MAX_LINE_WIDTH = 200
SPEC_MSG_END = '&#x200D;'

msg_welcome_new = "Welcome! Please, create a character to start playing."
msg_welcome = "Welcome, {name}!"
msg_enter_name = "Enter your character name:"
msg_create_succ = "Character created."
msg_current_location = "Current location: {location}."
msg_stats = "Current level: {level}.\nCurrent health: {health}."
msg_current_inventory = "Current inventory:\n"
msg_choose_item_to_use = "Choose an item to use:"
msg_no_usable_items = "No usable items available."
msg_change_location_ask = "Where do you want to go?"
msg_change_location_succ = "You've moved to {location}.\nDescription: {desc}"
msg_pick_npc = "Which NPC do you want to interact with?"
msg_leave_npc = "You left."
msg_no_npcs_in_location = "There are no NPCs in this location."
msg_pick_enemy = "Which enemy do you want to fight:"
msg_no_enemies_in_location = "There are no enemies in this location."
msg_choose_action = "Choose an action:"
msg_fight_succ = "You've defeated the {enemy}!\nYour level is increased by 1.\nCurrent level is {level}.\nYou've looted 1 {loot}."
msg_fight_succ_no_loot = "You've defeated the {enemy}!\nYour level is increased by 1.\nCurrent level is {level}."
msg_fight_fail = "{enemy} has defeated you.\nYour health is reduced by 1.\nCurrent health is {hp}."
msg_fight_die = "{enemy} has defeated you. You've died.\nType /start to create a new character."
msg_npc_no_quest = "No quests available."
msg_no_quests = "You have no quests."
msg_current_quests = "Current quests:\n"
msg_quest = "{npc} at {location}: {task}"
msg_quest_complete_succ = "You've completed the quest."
msg_quest_complete_deny = "You don't have required items to complete this quest."
msg_no_character = "An error occured. Please, use /start to reload."

msg_gen_welcome = "This is a bot to generate names for various characters and items."
msg_gen_choose_type = "Choose a type:"
msg_gen_choose_category = "Choose a category:"

btn_menu = "Main Menu"
btn_back = "Back"
btn_dialog = "Dialogue"
btn_quest = "Quest"
btn_accept = "Accept"
btn_complete_quest = "Complete"
btn_quest_not_available = "Not available (required level {level})"


def format_string(input_string, line_length=MAX_LINE_WIDTH):
    return f"{input_string:<{line_length}}"+SPEC_MSG_END


def _apply_formatting():
    globals_to_format = {k: v for k,
                         v in globals().items() if isinstance(v, str) and k.startswith('msg_') and k != __name__}
    for name, value in globals_to_format.items():
        formatted_value = format_string(value)
        globals()[name] = formatted_value


_apply_formatting()
