from vk_test import VKTest
import os


def main():
    """
    A function that serves as the entry point of the program.

    This function initializes a VKTest object with the path to a JSON file
    containing questions. It then runs the test and prints the result. If no
    questions are found in the JSON file, it prints a message indicating that no
    questions were found.
    """
    test = VKTest(os.path.join(
        os.path.dirname(__file__), 'questions.json'))
    if test.run():
        print(test.result())
    else:
        print("No questions found")


if __name__ == '__main__':
    main()
