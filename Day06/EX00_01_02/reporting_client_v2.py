import argparse
import grpc
from proto.spaceship_pb2 import Coordinates
from proto.spaceship_pb2_grpc import SpaceshipServiceStub
from typing import ClassVar, Optional
from pydantic import BaseModel, ValidationError, model_validator
from google.protobuf.json_format import MessageToJson


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


# def is_valid_spaceship(data):
def validate_spaceship(spaceship):
    try:
        print(SpaceshipValidator.model_validate_json(MessageToJson(
            spaceship, preserving_proto_field_name=True)).model_dump_json(indent=4))
    except ValidationError as ve:
        # for error in ve.errors():
        #     print(error.get('msg', ''))
        #     print(error.get('input', ''))
        pass


def parse_args():
    parser = argparse.ArgumentParser(
        description='Spaceship scanner')
    parser.add_argument(
        "coordinates",
        type=float,
        nargs="*",
        help="Set of coordinates to scan."
    )
    return parser.parse_args().coordinates


def run(coordinates):
    with grpc.insecure_channel('localhost:50051') as channel:
        # Check if the server is running
        try:
            grpc.channel_ready_future(channel).result(timeout=2)
        except grpc.FutureTimeoutError:
            print('Error: Server is not running.')
            return

        stub = SpaceshipServiceStub(channel)
        for spaceship in stub.GetSpaceships(Coordinates(coordinate=coordinates)):
            validate_spaceship(spaceship)


if __name__ == '__main__':
    coords = parse_args()
    if not coords:
        print('No coordinates provided')
    else:
        run(coords)
