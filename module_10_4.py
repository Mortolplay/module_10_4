from random import randint
import time
from threading import Thread
from time import sleep
from queue import Queue

class Table():
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))

class Cafe:
    l = 0
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        guests1 = list(guests)
        for guest in guests1:
            for t in self.tables:
                if t.guest is None:
                    t.guest = guest
                    t.guest.start()
                    self.l += 1
                    print(f"{guest.name} сел(-а) за стол номер {t.number}")
                    break
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or self.l > 0:
            for d in self.tables:
                if d.guest is not None and d.guest.is_alive():
                    print(f"{d.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {d.number} свободен")
                    d.guest = None
                    self.l -= 1
                if not self.queue.empty() and d.guest is None:
                    d.guest = self.queue.get()
                    print(f"{d.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {d.number}")
                    self.l += 1
                    d.guest.start()


tables = [Table(number) for number in range(1, 6)]

guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

guests = [Guest(name) for name in guests_names]

cafe = Cafe(*tables)

cafe.guest_arrival(*guests)

cafe.discuss_guests()