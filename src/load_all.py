import json
from db import (Base, Item, Location, NPC, Enemy,
                Dialog, PlayerResponse, Direction, Quest, engine, Session)


def get_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def load_npcs(session):
    for npc_data in get_json_data('npcs.json'):
        session.add(NPC(**npc_data))
    session.commit()


def load_enemies(session):
    for enemy_data in get_json_data('enemies.json'):
        session.add(Enemy(**enemy_data))
    session.commit()


def load_dialogs(session):
    for dialog in get_json_data('dialogs.json'):
        session.add(Dialog(
            npc_id=dialog['npc_id'], stage_id=dialog['stage_id'], npc_text=dialog['npc_text']))

        for response in dialog['responses']:
            session.add(PlayerResponse(
                **response, npc_id=dialog['npc_id'], stage_id=dialog['stage_id']))

    session.commit()


def load_locations(session):
    locations = get_json_data('locations.json')
    for location in locations:
        session.add(Location(
            id=location['id'], name=location['name'], description=location['description']))

    for location in locations:
        for direction in location['directions']:
            session.add(
                Direction(location_from_id=location['id'], location_to_id=direction))
    session.commit()


def load_items(session):
    for item_data in get_json_data('items.json'):
        session.add(Item(**item_data))
    session.commit()


def load_quests(session):
    for quest_data in get_json_data('quests.json'):
        session.add(Quest(**quest_data))
    session.commit()


if __name__ == "__main__":
    tables_to_drop = [Location.__table__, NPC.__table__, Enemy.__table__,
                      Dialog.__table__, PlayerResponse.__table__, Direction.__table__, Item.__table__, Quest.__table__]
    Base.metadata.drop_all(bind=engine, tables=tables_to_drop)

    Base.metadata.create_all(engine)

    session = Session()
    load_items(session)
    load_npcs(session)
    load_enemies(session)
    load_dialogs(session)
    load_quests(session)
    load_locations(session)
