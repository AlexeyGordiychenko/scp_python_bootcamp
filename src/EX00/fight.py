import asyncio

from enum import Enum, auto
from random import choice, uniform
import argparse


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', nargs='?', help='Number of agents', type=int)
    return parser.parse_args().n


def get_counteraction(action):
    if action == Action.HIGHKICK:
        return Action.HIGHBLOCK, 0
    elif action == Action.LOWKICK:
        return Action.LOWBLOCK, 0
    elif action == Action.HIGHBLOCK:
        return Action.LOWKICK, 1
    elif action == Action.LOWBLOCK:
        return Action.HIGHKICK, 1


async def battle(agent, agent_number='', format=0):
    async for action in agent:
        if agent.health <= 0:
            return True
        counteraction, damage = get_counteraction(action)
        agent.health -= damage
        print(
            f'Agent{agent_number:>{format}}: {action:<16} Neo: {counteraction:<16} Agent Health: {agent.health}')
        await asyncio.sleep(uniform(0.001, 0.002))
    return False


async def fight():
    await asyncio.gather(battle(Agent()))


async def fightmany(n):
    agents = [Agent() for _ in range(n)]
    format = len(str(n))+1
    results = await asyncio.gather(*(battle(agent, i, format) for i, agent in enumerate(agents, 1)))
    if all(results):
        print("Neo wins!")


if __name__ == "__main__":
    n = parse_args()
    if n and n > 0:
        asyncio.run(fightmany(n))
    else:
        asyncio.run(fight())
