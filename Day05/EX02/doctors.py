import threading
from time import sleep


class Screwdriver:
    def __init__(self, index):
        self.index = index
        self.lock = threading.Lock()


class Doctor():
    def __init__(self, index, left_screwdriver, right_screwdriver):
        self.index = index
        self.left_screwdriver = left_screwdriver
        self.right_screwdriver = right_screwdriver

    def blast(self):
        with self.left_screwdriver.lock:
            with self.right_screwdriver.lock:
                sleep(0.5)
                print(f'Doctor {self.index:2}: BLAST!')


screwdrivers = [Screwdriver(i) for i in range(5)]
doctors = [Doctor(i+9, screwdrivers[i], screwdrivers[(i+1) % 5])
           for i in range(5)]

threads = []
for doctor in doctors:
    thread = threading.Thread(target=doctor.blast)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
