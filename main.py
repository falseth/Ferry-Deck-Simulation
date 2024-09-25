from enum import Enum
import random


class Vehicle:
    def __init__(self, vehicle_type, length):
        self.type = vehicle_type
        self.length = int(length*10)/10.0

    def __str__(self):
        return self.type + ', ' + str(self.length) + 'm'


class LoadingProcedure(Enum):
    ONE_COL_FIRST = 0
    SEPARATE_LOOSE = 1
    SEPARATE_STRICT = 2
    RANDOM = 3


class FerryDeck:
    def __init__(self, loading_proceduce=LoadingProcedure.RANDOM):
        self.length = 32.0
        self.columns = 2
        self.deck = [[], []]
        self.space_remaining = [self.length] * self.columns
        self.vehicle_count = 0
        self.vehicle_count_by_type = [0, 0, 0]
        self.loading_proceduce = loading_proceduce

    def load_vehicle(self, vehicle):
        if self.loading_proceduce == LoadingProcedure.ONE_COL_FIRST:
            return self.__load_one_deck_first(vehicle)
        elif self.loading_proceduce == LoadingProcedure.SEPARATE_LOOSE:
            return self.__load_separately_loose(vehicle)
        elif self.loading_proceduce == LoadingProcedure.SEPARATE_STRICT:
            return self.__load_separately_strict(vehicle)
        else:
            return self.__load_randomly(vehicle)

    def __load_one_deck_first(self, vehicle):
        for i in range(self.columns):
            if self.__load_vehicle_in_column(vehicle, i):
                return 1
        return 0

    def __load_separately_loose(self, vehicle):
        if vehicle.type == 'Lorry':
            if self.__load_vehicle_in_column(vehicle, 1):
                return 1
            elif self.__load_vehicle_in_column(vehicle, 0):
                return 1
            else:
                return 0
        else:
            if self.__load_vehicle_in_column(vehicle, 0):
                return 1
            elif self.__load_vehicle_in_column(vehicle, 1):
                return 1
            else:
                return 0

    def __load_separately_strict(self, vehicle):
        if vehicle.type == 'Lorry':
            return self.__load_vehicle_in_column(vehicle, 1)
        else:
            return self.__load_vehicle_in_column(vehicle, 0)

    def __load_randomly(self, vehicle):
        random_col = list(range(self.columns))
        random.shuffle(random_col)

        for i in random_col:
            if self.__load_vehicle_in_column(vehicle, i):
                return 1
        return 0
    
    def __load_vehicle_in_column(self, vehicle, i):
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
        string += f'Total wasted space: {sum(self.space_remaining)}m\n'
        string += f'Total vehicles carried: {self.vehicle_count}\n'
        string += f'Total cars carried: {self.vehicle_count_by_type[0]}\n'
        string += f'Total lorries carried: {self.vehicle_count_by_type[1]}\n'
        string\
            += f'Total motorcycles carried: {self.vehicle_count_by_type[2]}\n'
        return string


def random_vehicle():
    r = random.randint(1, 100)
    if r <= 40:
        length = random.uniform(3.5, 5.5)
        return Vehicle('Car', length)
    elif r <= 95:
        length = random.uniform(8.0, 10.0)
        return Vehicle('Lorry', length)
    else:
        length = random.uniform(1.8, 2.2)
        return Vehicle('Motorcycle', length)


def simulate(total_sim, algorithm=1):
    total_wasted_space = 0
    total_vehicles_carried = 0
    total_cars_carried = 0
    total_lorries_carried = 0
    total_motorcycles_carried = 0

    for i in range(total_sim):
        ferry_deck = FerryDeck(algorithm)
        while ferry_deck.load_vehicle(random_vehicle()):
            pass

        total_wasted_space += sum(ferry_deck.space_remaining)
        total_vehicles_carried += ferry_deck.vehicle_count
        total_cars_carried += ferry_deck.vehicle_count_by_type[0]
        total_lorries_carried += ferry_deck.vehicle_count_by_type[1]
        total_motorcycles_carried += ferry_deck.vehicle_count_by_type[2]

    avg_wasted_space = round((total_wasted_space*100) / (total_sim*64), 2)
    avg_vehicles_carried = total_vehicles_carried / total_sim
    avg_cars_carried\
        = round((total_cars_carried*100)
                / (total_sim*avg_vehicles_carried), 2)
    avg_lorries_carried\
        = round((total_lorries_carried*100)
                / (total_sim*avg_vehicles_carried), 2)
    avg_motorcycles_carried\
        = round((total_motorcycles_carried*100)
                / (total_sim*avg_vehicles_carried), 2)

    string = ''
    string += f'Total simulation: {total_sim}\n'
    string += f'Algorithm: {algorithm}\n'
    string += f'Average wasted space: {avg_wasted_space}%\n'
    string += f'Average vehicles carried: {avg_vehicles_carried}\n'
    string += f'Average cars carried: {avg_cars_carried}%\n'
    string += f'Average lorries carried: {avg_lorries_carried}%\n'
    string +=\
        f'Average motorcycles carried: {avg_motorcycles_carried}%\n'
    print(string)


def main():
    simulate(100000, LoadingProcedure.ONE_COL_FIRST)
    simulate(100000, LoadingProcedure.SEPARATE_LOOSE)
    simulate(100000, LoadingProcedure.SEPARATE_STRICT)
    simulate(100000, LoadingProcedure.RANDOM)


if __name__ == '__main__':
    main()
