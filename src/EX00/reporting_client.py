import argparse
import grpc
from spaceship_pb2 import Coordinates
import spaceship_pb2_grpc
import json


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

        stub = spaceship_pb2_grpc.SpaceshipServiceStub(channel)
        for spaceship in stub.GetSpaceships(Coordinates(coordinate=coordinates)):
            message_dict = message_to_dict(spaceship)
            if 'officers' not in message_dict:
                message_dict['officers'] = []
            print(json.dumps(message_dict, indent=4))


def message_to_dict(message):
    # Convert a Protobuf message to a dict
    message_dict = {}
    for field, value in message.ListFields():
        if field.type == field.TYPE_ENUM:
            message_dict[field.name] = field.enum_type.values_by_number[value].name
        elif field.type == field.TYPE_MESSAGE:
            if field.label == field.LABEL_REPEATED:
                message_dict[field.name] = [message_to_dict(
                    sub_message) for sub_message in value]
            else:
                message_dict[field.name] = message_to_dict(value)
        else:
            message_dict[field.name] = value
    return message_dict


if __name__ == '__main__':
    run(parse_args())
