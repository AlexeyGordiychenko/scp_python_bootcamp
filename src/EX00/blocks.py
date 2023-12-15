import argparse
import sys


def read_input(argv):
    for _ in range(argv.n):
        line = sys.stdin.readline().rstrip()
        if len(line) == 32 and line[:5] == '00000' and line[5] != '0':
            print(line.rstrip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('n', help='Number of lines to parse', type=int)
    args = parser.parse_args()
    try:
        read_input(args)
    except (EOFError, ValueError):
        sys.exit(1)
