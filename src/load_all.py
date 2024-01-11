import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import (Base, Location, NPC, Enemy,
                Dialog, PlayerResponse, LinkedLocations)

engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)


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
            id=dialog_entry['id'], stage=dialog_entry['stage'], npc_text=dialog_entry['npc'])
        session.add(dialog)
        session.flush()  # To ensure dialog has an ID

        for response in dialog_entry['player']:
            player_response = PlayerResponse(
                dialog_id=dialog.id,
                stage_id=dialog.stage,
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


if __name__ == "__main__":
    tables_to_drop = [Location.__table__, NPC.__table__, Enemy.__table__,
                      Dialog.__table__, PlayerResponse.__table__, LinkedLocations.__table__]
    Base.metadata.drop_all(bind=engine, tables=tables_to_drop)

    Base.metadata.create_all(engine)

    session = Session()
    load_npcs(session)
    load_enemies(session)
    load_dialogs(session)
    load_locations(session)
