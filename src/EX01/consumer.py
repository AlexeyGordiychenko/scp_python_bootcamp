import argparse
import json
import logging
import redis
import os


def comma_separated_int_list(s):
    return [int(item) for item in s.split(',')]


def process_data(data, account_numbers):
   # Check the structure
    if not data['metadata'] or not data['metadata']['from'] or not data['metadata']['to'] or not data['amount']:
        return
    # Swap sender and receiver if specified and amount is not negative
    if (data['metadata']['to'] in account_numbers and data['amount'] >= 0):
        data['metadata']['from'], data['metadata']['to'] = data['metadata']['to'], data['metadata']['from']


def run_consumer(account_numbers):

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('consumer')

    # Initialize Redis and pub/sub
    r = redis.Redis(host=os.getenv('S21_REDIS_HOST', 'localhost'), port=6379)
    p = r.pubsub()
    p.subscribe('transactions')

    # Process messages
    for message in p.listen():
        if message['type'] != 'message' or not message['data']:
            continue
        # Parse message data
        data = json.loads(message['data'])
        process_data(data, account_numbers)
        logger.info(json.dumps(data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', help='List of bad guys\' account numbers separated by comma', type=comma_separated_int_list)
    args = parser.parse_args()
    run_consumer(args.e)
