class Room:
    def __init__(
        self,
        room_number: int,
        is_booked: bool,
        persons: int,
        floor: int,
        price: int | float,  # Цена может быть как целой так и нет
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