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
        price: int,
    ) -> None:
        self.room_number = room_number
        self.is_booked = is_booked
        self.persons = persons
        self.floor = floor
        self.price = price

    @property
    def is_available(self) -> bool:
        return not self.is_booked

    def book(self) -> None:
        if self.is_booked:
            print(f"Ошибка: Комната №{self.room_number} уже забронирована.")
        else:
            self.is_booked = True
            print(f"Успех: Комната №{self.room_number} успешно забронирована.")

    def cancel_booking(self) -> None:
        if not self.is_booked:
            print(f"Ошибка: Комната №{self.room_number} и так свободна.")
        else:
            self.is_booked = False
            print(
                f"Успех: Бронирование комнаты №{self.room_number} отменено."
            )


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


class Hotel:

    def __init__(self) -> None:
        self.rooms: list[Room] = []

    def add_rooms(self, rooms: list[Room]) -> None:
        self.rooms.extend(rooms)
        print(f"В отель добавлено комнат: {len(rooms)}.")

    def get_room(self, room_number: int) -> Room | None:
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        print(f"Комната №{room_number} не найдена в отеле.")
        return None

    def show_available_rooms(self) -> None:
        available_rooms = [room for room in self.rooms if room.is_available]

        if not available_rooms:
            print("Свободных комнат нет!")
            return

        print(" Свободные номера ")
        for room in available_rooms:
            info = f"Номер {room.room_number} (Мест: {room.persons}, Этаж: {room.floor}) — {room.price}$"
            if isinstance(room, LuxuryRoom):
                info += f" [Люкс, Ванна: {room.bath_size.name}]"
            print(info)

if __name__ == "__main__":
    #  Создаем отель
    hotel = Hotel()

    #  Создаем комнаты
    room_1 = Room(
        room_number=1, is_booked=False, persons=2, floor=1, price=100
    )
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
        is_booked=True,  # Эта комната изначально занята
        persons=1,
        floor=2,
        price=450,
        bath_size=BathSize.MEDIUM,
    )

    #  Добавляем комнаты в отель
    hotel.add_rooms([room_1, room_2, room_3, room_4])

    hotel.show_available_rooms()

    target_room = hotel.get_room(3)
    if target_room:
        print(f"До бронирования: свободен? {target_room.is_available}")
        target_room.book()
        print(f"После бронирования: свободен? {target_room.is_available}")

    hotel.show_available_rooms()

    room_4_obj = hotel.get_room(4)
    if room_4_obj:
        room_4_obj.cancel_booking()

    hotel.show_available_rooms()