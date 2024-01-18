import json
from db import (Base, Item, Location, NPC, Enemy,
                Dialog, PlayerResponse, LinkedLocations, engine, Session)


def get_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def load_npcs(session):
    for npc_data in get_json_data('npcs.json'):
        npc = NPC(**npc_data)
        session.add(npc)
    session.commit()


def load_enemies(session):
    for enemy_data in get_json_data('enemies.json'):
        enemy = Enemy(**enemy_data)
        session.add(enemy)
    session.commit()


def load_dialogs(session):
    for dialog_entry in get_json_data('dialogs.json'):
        dialog = Dialog(
            npc_id=dialog_entry['npc_id'], stage_id=dialog_entry['stage_id'], npc_text=dialog_entry['npc_text'])
        session.add(dialog)
        session.flush()  # To ensure dialog has an ID

        for response in dialog_entry['player']:
            player_response = PlayerResponse(
                npc_id=dialog.npc_id,
                stage_id=dialog.stage_id,
                text=response['text'],
                next_stage_id=response.get('next_stage')
            )
            session.add(player_response)

    session.commit()


def load_locations(session):
    locations_data = get_json_data('locations.json')
    location_instances = {}
    for location in locations_data:
        location_instance = Location(
            id=location['id'], name=location['name'], description=location['description'])
        session.add(location_instance)
        session.flush()  # To ensure each location instance has an ID
        location_instances[location['id']] = location_instance

    for location in locations_data:
        current_location = location_instances[location['id']]
        for linked_location_id in location['linked_locations']:
            linked_location = location_instances[linked_location_id]
            current_location.linked_locations.append(linked_location)

    session.commit()


def load_items(session):
    for item_data in get_json_data('items.json'):
        item = Item(**item_data)
        session.add(item)
    session.commit()


if __name__ == "__main__":
    tables_to_drop = [Location.__table__, NPC.__table__, Enemy.__table__,
                      Dialog.__table__, PlayerResponse.__table__, LinkedLocations.__table__, Item.__table__]
    Base.metadata.drop_all(bind=engine, tables=tables_to_drop)

    Base.metadata.create_all(engine)

    session = Session()
    load_items(session)
    load_npcs(session)
    load_enemies(session)
    load_dialogs(session)
    load_locations(session)
