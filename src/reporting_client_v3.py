import argparse
import json
import grpc
from proto.spaceship_pb2 import Coordinates
from proto.spaceship_pb2_grpc import SpaceshipServiceStub
from typing import ClassVar, Optional
from pydantic import BaseModel, ValidationError, model_validator
from google.protobuf.json_format import MessageToJson
from sqlalchemy import UniqueConstraint, and_, create_engine, Column, Integer, String, Float, Boolean, ForeignKey, distinct, exists, func, select
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


class OfficerValidator(BaseModel):
    first_name: str
    last_name: str
    rank: str


class SpaceshipValidator(BaseModel):
    alignment: str
    name: str
    class_: str
    length: float
    crew_size: int
    armed: bool
    officers: Optional[list[OfficerValidator]] = []

    checks: ClassVar = {
        # class_: (length_range, crew_size_range, can_be_armed, can_be_hostile)
        'Corvette': [(80, 250), (4, 10), True, True],
        'Frigate': [(300, 600), (10, 15), True, False],
        'Cruiser': [(500, 1000), (15, 30), True, True],
        'Destroyer': [(800, 2000), (50, 80), True, False],
        'Carrier': [(1000, 4000), (120, 250), False, True],
        'Dreadnought': [(5000, 20000), (300, 500), True, True]
    }

    @model_validator(mode='after')
    def check_spaceship(self):
        limitations = self.checks[self.class_]
        if not limitations:
            raise ValueError(f'Invalid class {self.class_}')

        length_range, crew_size_range, can_be_armed, can_be_hostile = limitations

        if not (length_range[0] <= self.length <= length_range[1]):
            raise ValueError(f'Incorrect length for {self.class_}')
        elif not (crew_size_range[0] <= self.crew_size <= crew_size_range[1]):
            raise ValueError(f'Incorrect crew size for {self.class_}')
        elif (not can_be_armed and self.armed):
            raise ValueError(f'{self.class_} can not be armed')
        elif (not can_be_hostile and self.alignment == 'Enemy'):
            raise ValueError(f'{self.class_} can not be hostile')
        elif (self.name == 'Unknown' and self.alignment == 'Ally'):
            raise ValueError(f'Name \'Unknown\' can be only for enemy ships')

        return self


Base = declarative_base()


class Spaceship(Base):
    __tablename__ = 'spaceships'

    id = Column(Integer, primary_key=True)
    alignment = Column(String)
    name = Column(String)
    class_ = Column(String)
    length = Column(Float)
    crew_size = Column(Integer)
    armed = Column(Boolean)
    officers = relationship('Officer', backref='spaceship')
    officers_hash = Column(String)
    # speed = Column(Float)


class Officer(Base):
    __tablename__ = 'officers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    rank = Column(String)
    spaceship_id = Column(Integer, ForeignKey('spaceships.id'))


engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}")
try:
    Base.metadata.create_all(engine)
except Exception:
    print('Error: Cannot connect to the database.')
    exit(1)
Session = sessionmaker(bind=engine)


def validate_spaceship(spaceship):
    try:
        model = SpaceshipValidator.model_validate_json(MessageToJson(
            spaceship, preserving_proto_field_name=True))
        print(model.model_dump_json(indent=4))
        spaceship_dict = model.model_dump()
        officers = [Officer(**officer_dict)
                    for officer_dict in spaceship_dict.pop('officers', [])]
        spaceship_model = Spaceship(**spaceship_dict)
        spaceship_model.officers = officers
        spaceship_model.officers_hash = get_officers_hash(
            spaceship_model.officers)
        return spaceship_model
    except ValidationError as ve:
        # for error in ve.errors():
        #     print(error.get('msg', ''))
        #     print(error.get('input', ''))
        pass


def get_officers_hash(officers):
    return ''.join(sorted(officer.first_name + officer.last_name + officer.rank for officer in officers))


def spaceship_exists(session, name, officers_hash):
    return session.query(exists().where(and_(Spaceship.name == name, Spaceship.officers_hash == officers_hash))).scalar()


def print_traitors():
    with Session() as session:
        officers_with_both_alignments = select(Officer.first_name, Officer.last_name, Officer.rank)\
            .join(Spaceship, Officer.spaceship_id == Spaceship.id)\
            .group_by(Officer.first_name, Officer.last_name, Officer.rank)\
            .having(func.count(distinct(Spaceship.alignment)) > 1)
        result = session.execute(officers_with_both_alignments)
    for row in result:
        print(row._asdict())


def parse_args():
    parser = argparse.ArgumentParser(
        description='Spaceship scanner')
    parser.add_argument(
        "command",
        type=str,
        choices=['scan', 'list_traitors'],
        help="The command to execute: scan - scan spaceships, list_traitors - display traitors."
    )
    parser.add_argument(
        "coordinates",
        type=float,
        nargs="*",
        help="Set of coordinates to scan."
    )
    args = parser.parse_args()
    return args.command, args.coordinates


def run(coordinates):
    with grpc.insecure_channel('localhost:50051') as channel:
        # Check if the server is running
        try:
            grpc.channel_ready_future(channel).result(timeout=2)
        except grpc.FutureTimeoutError:
            print('Error: Server is not running.')
            return

        stub = SpaceshipServiceStub(channel)
        with Session() as session:
            for spaceship in stub.GetSpaceships(Coordinates(coordinate=coordinates)):
                validated_spaceship = validate_spaceship(spaceship)
                if validated_spaceship and not spaceship_exists(session, validated_spaceship.name, validated_spaceship.officers_hash):
                    session.add(validated_spaceship)
            session.commit()


if __name__ == '__main__':
    command, coords = parse_args()
    if command == 'scan':
        if not coords:
            print('No coordinates provided')
        else:
            run(coords)
    elif command == 'list_traitors':
        print_traitors()
