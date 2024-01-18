import os
from sqlalchemy import Boolean, create_engine, Column, Integer, String, ForeignKey, Table, inspect, select, and_
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, foreign, remote, selectinload, LoaderCallableStatus
from random import randint

Base = declarative_base()
db_path = os.path.join(os.path.dirname(__file__), 'game.db')
engine = create_engine('sqlite:///'+db_path)
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
    location_id = Column(Integer, ForeignKey('locations.id'))

    location = relationship("Location", back_populates="npcs")
    dialogs = relationship("Dialog", back_populates="npc",
                           order_by="Dialog.stage_id")


class Enemy(Base):
    __tablename__ = 'enemies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location_id = Column(Integer, ForeignKey('locations.id'))
    level = Column(Integer)
    loot_id = Column(Integer, ForeignKey('items.id'), nullable=True)

    location = relationship("Location", back_populates="enemies")
    loot = relationship("Item")


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
    characters = relationship('Character', back_populates='location')

    def get_npcs(self):
        inspection = inspect(self)
        if inspection.attrs.npcs.loaded_value != LoaderCallableStatus.NO_VALUE:
            print('cache')
            return self.npcs
        else:
            with Session() as session:
                session.add(self)
                return self.npcs

    def get_enemies(self):
        inspection = inspect(self)
        if inspection.attrs.enemies.loaded_value != LoaderCallableStatus.NO_VALUE:
            return self.enemies
        else:
            with Session() as session:
                session.add(self)
                return self.enemies


class Dialog(Base):
    __tablename__ = 'dialogs'
    npc_id = Column(Integer, ForeignKey('npcs.id'), primary_key=True)
    stage_id = Column(Integer, nullable=False, index=True, primary_key=True)
    npc_text = Column(String, nullable=False)

    responses = relationship(
        "PlayerResponse",
        primaryjoin="and_(Dialog.npc_id==PlayerResponse.npc_id, Dialog.stage_id==foreign(PlayerResponse.stage_id))",
    )
    npc = relationship('NPC', back_populates='dialogs')


class PlayerResponse(Base):
    __tablename__ = 'player_responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    npc_id = Column(Integer, ForeignKey('npcs.id'))
    stage_id = Column(Integer)
    text = Column(String, nullable=False)
    next_stage_id = Column(Integer, nullable=True)

    dialog = relationship(
        "Dialog",
        primaryjoin="and_(foreign(PlayerResponse.npc_id) == remote(Dialog.npc_id), "
                    "foreign(PlayerResponse.stage_id) == remote(Dialog.stage_id))",
        back_populates="responses",
    )


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    hp = Column(Integer)
    level = Column(Integer)
    location_id = Column(Integer, ForeignKey('locations.id'))

    location = relationship('Location', back_populates='characters')
    inventory = relationship(
        'Inventory', back_populates='character')

    def __init__(self, id: int, name: str):
        self.id = id
        self.name: str = name
        self.hp: int = 10
        self.level = 1
        self.location_id = 1
        with Session() as session:
            default_location = session.execute(select(Location).where(
                Location.id == 1)).scalars().first()
        if default_location:
            self.location = default_location
        self.inventory = [Inventory(item_id=1, count=1),
                          Inventory(item_id=4, count=3)]

    def talk_to(self, npc: NPC):
        stage = 1
        with Session() as session:
            dialogs = session.execute(
                select(Dialog)
                .options(selectinload(Dialog.responses))
                .where(Dialog.npc_id == npc.id)
            ).scalars().all()

        while True:
            dialog = dialogs[stage-1]
            if not dialog:
                break
            stage = yield dialog

    def attack(self, enemy: Enemy):
        character_total = randint(1, 6) + int(self.level)
        enemy_total = randint(1, 6) + int(enemy.level)
        win = character_total >= enemy_total
        loot = None
        with Session() as session:
            session.add(self)
            if win:
                self.advance_level()
                if enemy.loot_id:
                    existing_item = next(
                        (item for item in self.inventory if item.item_id == enemy.loot_id), None)
                    if existing_item:
                        existing_item.count += 1
                    else:
                        self.inventory.append(
                            Inventory(item_id=enemy.loot_id, count=1))
                    loot = session.execute(select(Item).where(
                        Item.id == enemy.loot_id)).scalar_one_or_none()
            else:
                self.take_hit()
            session.commit()
            session.refresh(self, attribute_names=['location', 'inventory'])
            session.refresh(self.whereami(), attribute_names=['enemies'])
        return win, loot

    def take_hit(self, value: int = 1):
        self.hp -= value
        if self.hp <= 0:
            raise Exception("You died")

    def heal(self, value: int = 1):
        self.hp += value

    def advance_level(self, value: int = 1):
        self.level += value

    def go(self, location_id):
        with Session() as session:
            session.add(self)
            self.location_id = location_id
            session.commit()
            session.refresh(self, attribute_names=['location'])

    def whereami(self):
        return self.location


class Inventory(Base):
    __tablename__ = 'inventory'
    character_id = Column(Integer, ForeignKey(
        'characters.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    count = Column(Integer)

    character = relationship('Character', back_populates='inventory')
    item = relationship('Item', lazy='selectin')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    usable = Column(Boolean)
