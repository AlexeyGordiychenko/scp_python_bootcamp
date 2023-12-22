import random


def generate_traits(total=100, i=1, max=5):
    if i == max:
        yield total
        return
    number = random.randint(0, total)
    yield from generate_traits(total - number, i + 1, max)
    yield number


def turrets_generator():
    traits = ['neuroticism', 'openness',
              'conscientiousness', 'extraversion', 'agreeableness']
    methods = {
        'shoot': lambda: print("Shooting"),
        'search': lambda: print("Searching"),
        'talk': lambda: print("Talking")
    }
    while True:
        yield type('Turret', (object,), dict(zip(traits, generate_traits())) | methods)


def print_traits(turret):
    print(
        f'neuroticism: {turret.neuroticism}',
        f'openness: {turret.openness}',
        f'conscientiousness: {turret.conscientiousness}',
        f'extraversion: {turret.extraversion}',
        f'agreeableness: {turret.agreeableness}',
    )
    print('sum: {}'.format(turret.neuroticism + turret.openness +
          turret.conscientiousness + turret.extraversion + turret.agreeableness))


if __name__ == '__main__':
    turrets = turrets_generator()
    for _ in range(3):
        turret = next(turrets)
        print_traits(turret)
        turret.shoot()
        turret.search()
        turret.talk()
