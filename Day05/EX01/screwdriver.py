import os
import requests
import argparse

SERVER_URL = 'http://localhost:8888'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Screwdriver - a CLI program to upload audio files to the server.')
    parser.add_argument(
        "command",
        type=str,
        choices=['upload', 'list'],
        help="The command to execute: upload - upload a file to the server, list - list all files on the server."
    )
    parser.add_argument(
        "file",
        type=str,
        nargs="?",
        help="A file to upload to the server."
    )
    args = parser.parse_args()
    return args.command, args.file


def upload_file(filename):
    if not os.path.exists(filename):
        print('File does not exist')
        return
    with open(filename, 'rb') as f:
        try:
            r = requests.post(SERVER_URL, files={'file': f}, headers={
                'Accept': 'application/json'})
            r.raise_for_status()
            print(r.json().get('message'))
        except Exception as e:
            print(f'A server error occured:\n{e}')


def list_files():
    try:
        r = requests.get(SERVER_URL, headers={'Accept': 'application/json'})
        r.raise_for_status()
        [print(file) for file in r.json().get('files')]
    except Exception as e:
        print(f'A server error occured:\n{e}')


if __name__ == '__main__':
    command, file = parse_args()
    if command == 'upload':
        if file is None:
            print('Please specify a file to upload')
        else:
            upload_file(file)
    elif command == 'list':
        list_files()
