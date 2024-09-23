import random


class Vehicle:
    def __init__(self, vehicle_type, length):
        self.type = vehicle_type
        self.length = int(length*10)/10.0

    def __str__(self):
        return self.type + ', ' + str(self.length) + 'm'


class FerryDeck:
    def __init__(self):
        self.length = 32.0
        self.columns = 2
        self.deck = [[], []]
        self.space_remaining = [self.length] * self.columns
        self.vehicle_count = 0
        self.vehicle_count_by_type = [0, 0, 0]

    def load_vehicle(self, vehicle):
        for i in range(self.columns):
            if self.space_remaining[i] >= vehicle.length:
                self.deck[i].append(vehicle)
                self.space_remaining[i] -= vehicle.length
                self.vehicle_count += 1
                if vehicle.type == 'Car':
                    self.vehicle_count_by_type[0] += 1
                elif vehicle.type == 'Lorry':
                    self.vehicle_count_by_type[1] += 1
                else:
                    self.vehicle_count_by_type[2] += 1
                return 1
        return 0

    def __str__(self):
        string = ''
        for i in range(self.columns):
            string += f'Column {i}\n'
            for vehicle in self.deck[i]:
                string += vehicle.__str__()
                string += '; '
            string += f'\nWasted space: {self.space_remaining[i]}m\n\n'
        string += f'Total vehicles carried: {self.vehicle_count}\n'
        string += f'Total cars carried: {self.vehicle_count_by_type[0]}\n'
        string += f'Total lorries carried: {self.vehicle_count_by_type[1]}\n'
        string\
            += f'Total motorcycles carried: {self.vehicle_count_by_type[2]}\n'
        return string


def main():
    ferry_deck = FerryDeck()

    for i in range(100):
        r = random.randint(1, 100)
        if r <= 40:
            length = random.uniform(3.5, 5.5)
            vehicle = Vehicle('Car', length)
        elif r <= 95:
            length = random.uniform(8.0, 10.0)
            vehicle = Vehicle('Lorry', length)
        else:
            length = random.uniform(2.0, 3.0)
            vehicle = Vehicle('Motorcycle', length)

        ferry_deck.load_vehicle(vehicle)

    print(ferry_deck)


if __name__ == '__main__':
    main()
