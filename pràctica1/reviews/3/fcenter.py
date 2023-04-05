from dataclasses import dataclass
from typing import TextIO
from collections import deque
from enum import Enum
import curses
import time


TimeStamp = int

Identifier = int

class Direction(Enum):
    RIGHT = 1
    LEFT = -1

    def __int__(self):
        return self.value

@dataclass
class Package:
    identifier: Identifier
    arrival: TimeStamp
    source: int
    destination: int
    weight: int
    value: int


class Station: 
    packages: deque[Package]
    
    def __init__ (self) -> None:
        """Constructor of the station."""
        self.packages = deque()

    def receive_package(self, p: Package) -> None:
        """Adds a package p to the station."""
        self.packages.append(p)

    def load_package_wagon(self) -> None:
        """The station loads a package to the wagon (it deletes its first package)"""
        self.packages.popleft() 
        

class Wagon:
    pos: int
    packages: dict[Identifier, Package] 
    num_stations: int
    capacity: int
    current_load: int

    def __init__(self, num_stations: int, capacity: int) -> None: 
        """Constructor of the wagon with num_stations and capacity integrers."""
        self.num_stations, self.capacity = num_stations, capacity
        self.pos, self.current_load = 0, 0
        self.packages = dict()

    def move(self, direction: Direction) -> None:
        """Moves the wagon in the direction given."""
        self.pos = (self.pos + direction.value) % self.num_stations 

    def load_package(self, p: Package) -> None:
        """Loads a particular package p in the wagon."""
        self.packages[p.identifier] = p # adds package in the wagon
        self.current_load += p.weight   # updates the current weight

    def deliver(self, identifier: Identifier) -> int:
        """Delivers a package on a station and returns the benefit from the deliver."""
        p = self.packages[identifier]
        del self.packages[identifier]
        self.current_load -= p.weight  # updates the current weight

        return p.value


class FullfilmentCenter:

    counter_cash = 0
    _num_stations: int
    _wagon_capacity: int
    _wagon: Wagon
    stations: dict[int, Station] = dict()

    def __init__(self, num_stations: int, wagon_capacity: int) -> None: 
        """Constructor with num_stations and wagon_capacity integrers."""
        self._num_stations, self._wagon_capacity = num_stations, wagon_capacity

        for i in range(num_stations):
            self.stations[i] = Station()

        self._wagon = Wagon(num_stations, wagon_capacity) 

    def cash(self) -> int:
        """Returns the cash already earned by the FullfilmentCenter."""
        return self.counter_cash

    def wagon(self) -> Wagon: 
        """Returns the wagon of the FullfilmentCenter."""
        return self._wagon

    def num_stations(self) -> int: 
        """Returns the number of stations of the FullfilmentCenter."""
        return self._num_stations

    def station(self, idx: int) -> Station:
        """Returns the station number idx."""
        return self.stations[idx]

    def receive_package(self, p: Package) -> None: 
        """The FullfilmentCenter recieves a package in the corresponding station."""
        self.stations[p.source].receive_package(p)

    def deliver_package(self, identifier: Identifier) -> None: 
        """
        The wagon delivers a package in the corresponding station 
        of the FullfilmentCenter.
        """
        self.counter_cash = self.cash() + self.wagon().deliver(identifier) 
        # we sum the cash earned from the deliver while calling the wagon to do so.

    def current_station_package(self) -> Package | None: 
        """Returns the current station package if there's any."""

        current_pos = self.wagon().pos 

        if len(self.stations[current_pos].packages) > 0:
            return self.stations[current_pos].packages[0] 
        
        return None

    def load_current_station_package(self) -> None: 
        """Loads the current station package."""

        current_pos, p = self.wagon().pos, self.current_station_package()
        
        if p is not None and self.wagon().capacity >= (self.wagon().current_load + p.weight):
            self.wagon().load_package(p)  # we load the package to the wagon
            self.station(current_pos).load_package_wagon()  # we remove the package from the staation
            

    def write(self, stdscr: curses.window, caption: str = '') -> None:
        def package_color(p: Package) -> int:
            return curses.color_pair(1 + p.destination * 6 * 764351 % 250)

        factory_height = 8  # maximum number of rows to write
        wagon_height = 6 # maximum number of rows to write
        delay = 0.15  # delay after writing the state
        # start: clear screen
        stdscr.clear()
        # write caption
        stdscr.addstr(0, 0, caption)
        stdscr.addstr(1, 0, ' ' * caption.find('t:') + '$: ' + str(self.cash()))
        # write stations base
        for i in range(self.num_stations()):
            stdscr.addstr(factory_height + 3, 3*i, '-') 
            stdscr.addstr(factory_height + 3, 3*i + 1, f's{i}', package_color(Package(-1, -1, -1, i, -1, -1)))
        stdscr.addstr(factory_height + 3, 3*self.num_stations(), '-') 
        # write packages in stations
        for i in range(self.num_stations()):
            x, dy = 3*i + 1, 0
            for p in self.station(i).packages:
                dy += 1
                if dy > factory_height:
                    stdscr.addstr(factory_height + 3 - factory_height - 1, x, f'..')
                else:
                    stdscr.addstr(factory_height + 3 - dy, x, f'{p.identifier%100:02d}', package_color(p))
        # write wagon
        for i in range(wagon_height):
            stdscr.addstr(factory_height + 4 + wagon_height-1-i, 3*self.wagon().pos, '|')
            stdscr.addstr(factory_height + 4 + wagon_height-1-i, 3*self.wagon().pos + 3, '|')
        # write wagon packages
        ps = list(self.wagon().packages.values())
        for i in range(min(len(ps), wagon_height-1)):
            p = ps[i]
            stdscr.addstr(factory_height + 4 + wagon_height-1-i, 3*self.wagon().pos + 1, f'{p.identifier%100:02d}', package_color(p))
        if len(ps) >= wagon_height:
            stdscr.addstr(factory_height + 4, 3*self.wagon().pos + 1, '..')
        stdscr.addstr(factory_height + 4 + wagon_height, 3*self.wagon().pos, f'o--o')
        # done
        stdscr.refresh()
        time.sleep(delay)


class Logger:
    """Class to log fcenter actions to a file."""

    _file: TextIO

    def __init__(self, path: str, name: str, num_stations: int, wagon_capacity: int) -> None:
        self._file = open(path, 'w')
        print(0, 'START', name, num_stations, wagon_capacity, file=self._file)

    def load(self, t: TimeStamp, identifier: Identifier) -> None:
        print(t, 'LOAD', identifier, file=self._file)

    def deliver(self, t: TimeStamp, identifier: Identifier) -> None:
        print(t, 'DELIVER', identifier, file=self._file)

    def move(self, t: TimeStamp, direction: int) -> None:
        print(t, 'MOVE', direction, file=self._file)

    def add(self, t: TimeStamp, identifier: Identifier) -> None:
        print(t, 'ADD', identifier, file=self._file)


def read_packages(path: str) -> list[Package]:
    """Returns a list of packages read from a file at path."""

    with open(path, 'r') as file:
        packages: list[Package] = []
        for line in file:
            identifier, arrival, location, destination, weight, value = map(int, line.split())
            package = Package(identifier, arrival, location, destination, weight, value)
            packages.append(package)
        return packages


def check_and_show(packages_path: str, log_path: str, stdscr: curses.window | None = None) -> None:
    """
    Check that the actions stored in the log at log_path with the packages at packages_path are legal.
    Raise an exception if not.
    // In the case that stdscr is not None, the store is written after each action.
    """
    
    # get the data
    packages = read_packages(packages_path)
    packages_map = {p.identifier: p for p in packages}
    log = open(log_path, 'r')
    lines = log.readlines()

    # process first line
    tokens = lines[0].split()
    assert len(tokens) == 5
    assert tokens[0] == "0"
    assert tokens[1] == "START"
    name = tokens[2]
    num_stations = int(tokens[3])
    wagon_capacity = int(tokens[4])
    fcenter = FullfilmentCenter(num_stations, wagon_capacity)
    last_wagon_action = -1
    last_package_arrival = -1

    for line in lines[1:]:
        tokens = line.split()
        t: TimeStamp = int(tokens[0])
        what = tokens[1]
        assert t >= max(last_wagon_action, last_package_arrival)

        p: Package | None = None

        if what == "ADD":
            assert t > last_wagon_action
            identifier = int(tokens[2])
            assert identifier in packages_map.keys()
            p = packages_map[identifier]
            assert p.arrival == t
            fcenter.receive_package(p)
            last_package_arrival = t
        elif what == "DELIVER":
            identifier = int(tokens[2])
            matches = list(filter(lambda p: p.identifier == identifier, fcenter.wagon().packages.values()))
            assert len(matches) == 1
            p = matches[0]
            fcenter.deliver_package(identifier)
            last_wagon_action = t
        elif what == "MOVE":
            direction = Direction(int(tokens[2]))
            fcenter.wagon().move(direction)
            last_wagon_action = t
        elif what == "LOAD":
            identifier = int(tokens[2])
            p = fcenter.current_station_package()
            assert p is not None
            assert p.identifier == identifier
            fcenter.load_current_station_package()
            assert 0 <= sum(pkg.weight for pkg in fcenter.wagon().packages.values()) <= wagon_capacity
            last_wagon_action = t
        else:
            assert False

        if stdscr:
            fcenter.write(stdscr, f'{name} t: {line.strip()}')