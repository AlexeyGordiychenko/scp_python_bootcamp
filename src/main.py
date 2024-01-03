from vk_test import VKTest
import os


def main():
    test = VKTest(os.path.join(
        os.path.dirname(__file__), 'questions.json'))
    if test.run():
        print(test.result())
    else:
        print("No questions found")


if __name__ == '__main__':
    main()
