class Room:
    def __init__(
        self,
        room_number: int,
        is_booked: bool,
        persons: int,
        floor: int,
        price: int
    ) -> None:
        self.room_number = room_number
        self.is_booked = is_booked
        self.persons = persons
        self.floor = floor
        self.price = price


room_1 = Room(
    room_number=1,
    is_booked=False,
    persons=2,
    floor=1,
    price=100,
)

room_2 = Room(
    room_number=2,
    is_booked=False,
    persons=4,
    floor=1,
    price=200,
)
print(f"Комната №{room_1.room_number} на {room_1.floor} этаже стоит {room_1.price}$.")
print(f"Комната №{room_2.room_number} вмещает {room_2.persons} человек(а).")

from enum import IntEnum

class BathSize(IntEnum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Room:
    def __init__(
        self,
        room_number: int,
        is_booked: bool,
        persons: int,
        floor: int,
        price: int
    ) -> None:
        self.room_number = room_number
        self.is_booked = is_booked
        self.persons = persons
        self.floor = floor
        self.price = price

class LuxuryRoom(Room):
    def __init__(
        self,
        room_number: int,
        is_booked: bool,
        persons: int,
        floor: int,
        price: int | float,
        bath_size: BathSize,
    ) -> None:
        super().__init__(room_number, is_booked, persons, floor, price)
        self.bath_size = bath_size

room_1 = Room(room_number=1, is_booked=False, persons=2, floor=1, price=100)
room_2 = Room(room_number=2, is_booked=False, persons=4, floor=1, price=200)

room_3 = LuxuryRoom(
    room_number=3,
    is_booked=False,
    persons=1,
    floor=2,
    price=500.0,
    bath_size=BathSize.LARGE,
)

room_4 = LuxuryRoom(
    room_number=4,
    is_booked=False,
    persons=1,
    floor=2,
    price=450,
    bath_size=BathSize.MEDIUM,
)

# Проверка работы
print(f"Объект room_3: Комната №{room_3.room_number}, Ванна: {room_3.bath_size.name} (код {room_3.bath_size.value})")
print(f"Объект room_4: Комната №{room_4.room_number}, Ванна: {room_4.bath_size.name} (код {room_4.bath_size.value})")