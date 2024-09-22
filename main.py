import time
from itertools import zip_longest
from queue import Queue
from random import randint
from threading import Thread
from time import sleep


class Table:
    def __init__(self, number, guest=None) -> None:
        self.number = number
        self.guest = guest

    def set_guest(self, guest):
        self.guest = guest


class Guest(Thread):
    def __init__(self, str_name) -> None:
        super().__init__()
        self.name = str_name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue_table = Queue()
        self.quere_guests = Queue()
        self.list_service = []
        [self.queue_table.put(t) for t in tables]

    def guest_arrival(self, *guests):
        for guest in guests:
            if not self.queue_table.empty():
                tmp = self.queue_table.get()
                tmp.set_guest(guest)
                print(f'{guest.name} сел(-а) за стол номер {tmp.number}')
                self.list_service.append(tmp)
            else:
                self.quere_guests.put(guest)
                print((f'{guest.name} в очереди'))

    def __used_tables(self) -> bool:
        count = 0
        for table in self.list_service:
            if table.guest != None:
                count += 1
        return True if count != 0 else False

    def discuss_guests(self):
        [table.guest.start() for table in self.list_service if table.guest != None]
        while not self.quere_guests.empty() and self.__used_tables():
            for table in self.list_service:
                if not table.guest.is_alive() and not self.quere_guests.empty():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    tmp_guest = self.quere_guests.get()
                    table.guest = tmp_guest
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    table.guest.start()
                else:
                    table.guest == None
            sleep(1)


tables = [Table(number) for number in range(1, 6)]
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
guests = [Guest(name) for name in guests_names]

cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()
