from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)

linked_locations_association = Table('linked_locations', Base.metadata,
                                     Column('location_id', Integer, ForeignKey(
                                         'locations.id'), primary_key=True),
                                     Column('linked_location_id', Integer, ForeignKey(
                                         'locations.id'), primary_key=True)
                                     )


class LinkedLocations(Base):
    __tablename__ = 'linked_locations'


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
    location_id = Column(Integer, ForeignKey('locations.id'))
    level = Column(Integer)
    loot = Column(String)

    location = relationship("Location", back_populates="enemies")


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    linked_locations = relationship(
        "Location",
        secondary=linked_locations_association,
        primaryjoin=id == linked_locations_association.c.location_id,
        secondaryjoin=id == linked_locations_association.c.linked_location_id,
        backref="linked_to"
    )
    npcs = relationship('NPC', back_populates='location')
    enemies = relationship('Enemy', back_populates='location')


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
    hp = Column(Integer)
    level = Column(Integer)
    location_id = Column(Integer, ForeignKey('locations.id'))

    items = relationship('Inventory', back_populates='character')

    def __init__(self, id: int, name: str):
        self.id = id
        self.name: str = name
        self.hp: int = 10
        self.level = 1
        self.location_id = 1


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    item = Column(String)
    count = Column(Integer)

    character = relationship('Character', back_populates='items')
