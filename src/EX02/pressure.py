import random
from time import sleep


def emit_gel(step):
    pressure = 50
    while True:
        step = yield pressure
        pressure += random.randint(min(0, step), max(0, step))
        pressure = max(0, min(100, pressure))


def valve():
    step = 18
    generator = emit_gel(step)
    pressure = next(generator)
    while 10 <= pressure <= 90:
        if pressure > 80 and step > 0 or pressure < 20 and step < 0:
            step = -step
        print(f"Pressure: {pressure}; Step: {step:>3}")
        pressure = generator.send(step)
        sleep(0.1)
    generator.close()
    print(f"Emergency break at {pressure}")


if __name__ == "__main__":
    valve()
