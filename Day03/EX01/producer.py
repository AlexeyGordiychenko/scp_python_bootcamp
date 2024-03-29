import json
import logging
from time import sleep
import redis
from itertools import permutations
from random import randint, choice
import os


def get_transfer():
    first_account = 1111111111
    accounts = [first_account*i for i in range(1, 10)]
    account_pairs = list(permutations(accounts, 2))
    while True:
        yield *choice(account_pairs), randint(-10000, 10000)


def run_producer():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('producer')

    # Initialize Redis
    try:
        r = redis.Redis(host=os.getenv(
            'S21_REDIS_HOST', 'localhost'), port=6379)
        r.ping()
    except redis.ConnectionError:
        logger.error('Can\'t connect to redis')
        return

    # Generate messages and publish
    for from_account, to_account, amount in get_transfer():
        message = {
            "metadata": {
                "from": from_account,
                "to": to_account
            },
            "amount": amount
        }

        r.publish('transactions', json.dumps(message))
        logger.info(message)

        sleep(1)


if __name__ == "__main__":
    run_producer()
