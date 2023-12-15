import sys
import re


def mfinder():
    text = sys.stdin.read()
    if re.match(r'^.{5}\n.{5}\n.{5}\Z', text) is None:
        print('Error')
    else:
        text = text.replace('\n', '')
        if re.match(r'\*[^*]{3}\*\*{2}[^*]\*{2}\*[^*]\*[^*]\*', text) is None:
            print('False')
        else:
            print('True')


if __name__ == "__main__":
    try:
        mfinder()
    except (EOFError, ValueError):
        sys.exit()
