import argparse


def decypher(text):
    """
    Decypher the text
    """
    return ''.join(word[0] for word in text.split() if word).lower()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('s', help='String to decypher', type=str)
    args = parser.parse_args()
    print(decypher(args.s))
