import grpc
from proto.spaceship_pb2 import Spaceship
from proto.spaceship_pb2_grpc import SpaceshipServiceServicer, add_SpaceshipServiceServicer_to_server
import random
import time
import randomname
import names
from concurrent.futures import ThreadPoolExecutor

officer_ranks = [
    'Captain',
    'Ensign',
    'Lieutenant',
    'Chief Petty Officer',
    'Commander',
    'Officers',
    'First Officer',
    'Petty officer',
    'Admiral',
    'Bridge Officer',
    'Cadet',
    'Commodore',
    'Navigation officer',
    'Vice Admiral',
]


class SpaceshipServiceServicer(SpaceshipServiceServicer):
    def GetSpaceships(self, request, context):
        print(
            f'Scanning coordinates:{request.coordinate}')
        for _ in range(random.randint(1, 10)):
            yield generate_random_spaceship()


def get_random_spaceship_name(alignment):
    if alignment == Spaceship.Ally or alignment == Spaceship.Enemy and random.randint(0, 2):
        return randomname.generate('adj/speed,adj/shape,adj/size',
                                   'n/apex_predators,n/astronomy,n/military_navy,n/military_airforce',
                                   sep=' '
                                   ).title()
    else:
        return 'Unknown'


def get_random_officers():
    return [Spaceship.Officer(first_name=names.get_first_name(), last_name=names.get_last_name(
    ), rank=random.choice(officer_ranks)) for _ in range(random.randint(0, 10))]


def generate_random_spaceship():
    # Generate a random Spaceship
    alignment = random.choice(list(Spaceship.Alignment.values()))
    name = get_random_spaceship_name(alignment)
    class_ = random.choice(list(Spaceship.Class.values()))
    length = random.uniform(10, 30000.0)
    crew_size = random.randint(2, 800)
    armed = random.choice([True, False])
    officers = get_random_officers() if alignment == Spaceship.Ally else []

    return Spaceship(
        alignment=alignment,
        name=name,
        class_=class_,
        length=length,
        crew_size=crew_size,
        armed=armed,
        officers=officers
    )


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_SpaceshipServiceServicer_to_server(
        SpaceshipServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
