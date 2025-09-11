from functools import reduce

def input_room():
    name = input("Название комнаты: ")
    dlinna = float(input("Длина комнаты: "))
    shirina = float(input("Ширина комнаты: "))
    return {"name": name, "длина": dlinna, "ширина": shirina}

komnata = int(input("Количество комнат: "))
rooms = []

for i in range(komnata):
    print(f"\nКомната {i+1}:")
    rooms.append(input_room())

areas = list(map(lambda room: room["длина"] * room["ширина"], rooms))
total_area = reduce(lambda x, y: x + y, areas)

print("\nПлощади комнат:")
for i, room in enumerate(rooms):
    print(f"{room['name']}: {areas[i]} м²")

print(f"\nОбщая площадь квартиры: {total_area} м²")