from typing import Dict


def squeak_decorator(func):
    def wrapper(*args, **kwargs):
        print('SQUEAK')
        return func(*args, **kwargs)
    return wrapper


@squeak_decorator
def add_ingot(purse: Dict[str, int]):
    return {'gold_ingots': purse.get('gold_ingots', 0) + 1}


@squeak_decorator
def get_ingot(purse: Dict[str, int]):
    amount = max(0, purse.get('gold_ingots', 0) - 1)
    return {} if amount == 0 else {'gold_ingots': amount}


@squeak_decorator
def empty(purse: Dict[str, int]):
    return {}


if __name__ == "__main__":
    purse = {'gold_ingots': 6}
    empty(purse)
    add_ingot(purse)
    get_ingot(purse)
