import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, event
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)

association_table = Table('linked_locations', Base.metadata,
                          Column('location_id', Integer, ForeignKey(
                              'locations.id'), primary_key=True),
                          Column('linked_location_id', Integer, ForeignKey(
                              'locations.id'), primary_key=True)
                          )


class NPC(Base):
    __tablename__ = 'npcs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    location_id = Column(Integer, ForeignKey('locations.id'))
    dialog_id = Column(Integer, ForeignKey('dialogs.id'))

    location = relationship("Location", back_populates="npcs")
    dialog = relationship("Dialog", back_populates="npc")


class Enemy(Base):
    __tablename__ = 'enemies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    level = Column(Integer)
    loot = Column(String)


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    linked_locations = relationship(
        "Location",
        secondary=association_table,
        primaryjoin=id == association_table.c.location_id,
        secondaryjoin=id == association_table.c.linked_location_id,
        backref="linked_to"
    )
    npcs = relationship('NPC', back_populates='location')


class Dialog(Base):
    __tablename__ = 'dialogs'
    id = Column(Integer, primary_key=True)
    stage = Column(Integer, nullable=False, index=True, primary_key=True)
    npc_text = Column(String, nullable=False)
    # Relationship to player responses
    player_responses = relationship("PlayerResponse", back_populates="dialog")
    npc = relationship('NPC', back_populates='dialog')


class PlayerResponse(Base):
    __tablename__ = 'player_responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dialog_id = Column(Integer, ForeignKey('dialogs.id'))
    stage_id = Column(Integer)
    text = Column(String, nullable=False)
    next_stage_id = Column(Integer, nullable=True)
    # Relationship to dialog
    dialog = relationship("Dialog", foreign_keys=[
                          dialog_id, stage_id], back_populates="player_responses")
    # Relationship to next stage dialog
    next_stage = relationship("Dialog", foreign_keys=[
                              dialog_id, next_stage_id], overlaps="dialog,player_responses")


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


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


Base.metadata.create_all(engine)

session = Session()
load_npcs(session)
load_enemies(session)
load_dialogs(session)
load_locations(session)
