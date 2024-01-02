import argparse
import grpc
from proto.spaceship_pb2 import Coordinates
from proto.spaceship_pb2_grpc import SpaceshipServiceStub
import json
from google.protobuf.json_format import MessageToDict


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
            dict_msg = MessageToDict(
                spaceship, preserving_proto_field_name=True)
            if 'officers' not in dict_msg:
                dict_msg['officers'] = []
            print(json.dumps(dict_msg, indent=4))


if __name__ == '__main__':
    coords = parse_args()
    if not coords:
        print('No coordinates provided')
    else:
        run(coords)
