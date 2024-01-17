MAX_LINE_WIDTH = 200

welcome_new = "Welcome! Please, create a character to start playing."
welcome = "Welcome, {name}!"
enter_name = "Enter your character name:"
create_succ = "Character created."
current_location = "Current location: {location}."
current_health = "Current health: {health}."
current_inventory = "Current inventory:\n"
change_location_ask = "Where do you want to go?"
change_location_succ = "You've moved to {location}.\nDescription: {desc}"
pick_npc = "Which NPC do you want to talk to:"
leave_npc = "You left."
no_npcs_in_location = "There are no NPCs in this location."
pick_enemy = "Which enemy do you want to fight:"
no_enemies_in_location = "There are no enemies in this location."
choose_action = "Choose an action:"
back = "Back"
fight_succ = "You've defeated the {enemy}!\nYour level is increased by 1.\nCurrent level is {level}.\nYou've looted 1 {loot}."
fight_fail = "{enemy} has defeated you.\nYour health is reduced by 1.\nCurrent health is {hp}."
fight_die = "You died."

gen_welcome = "This is a bot to generate names for various characters and items."
gen_choose_type = "Choose a type:"
gen_choose_category = "Choose a category:"


def format_string(input_string, line_length=MAX_LINE_WIDTH):
    return f"{input_string:<{line_length}}"+'&#x200D;'


def _apply_formatting():
    globals_to_format = {k: v for k,
                         v in globals().items() if isinstance(v, str) and v != back}
    for name, value in globals_to_format.items():
        formatted_value = format_string(value)
        globals()[name] = formatted_value


_apply_formatting()
