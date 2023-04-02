from dataclasses import dataclass
from typing import TextIO
from collections import deque
from enum import Enum
import curses
import time


TimeStamp = int

Identifier = int


class Direction(Enum):
    """Enum that allows to represent a direction left (-1) or right (1)."""
    RIGHT = 1
    LEFT = -1

    def __int__(self):
        return self.value


@dataclass
class Package:
    """Structure to store package data."""
    identifier: Identifier
    arrival: TimeStamp
    source: int
    destination: int
    weight: int
    value: int


class Station:
    """Class to create a station where the packages are kept, collected and delivered."""
    packages: deque[Package]
    _station_idx: int

    def __init__(self, idx: int) -> None:
        """Constructor of the class Station indexed by the integer idx"""
        self.packages = deque()
        self._station_idx = idx
    
    def station_idx(self) -> int:
        """Returns the current station's index"""
        return self._station_idx
    
    def receive_package(self, p: Package) -> None:
        """
            Load onto the station a package awaiting to be picked up.
            The packages are stacked from the left and taken from the right.
        """
        self.packages.appendleft(p)

    def send_package(self) -> Package | None:
        """Sends out the highest priority package if possible."""
        return self.packages.pop() if len(self.packages) > 0 else None


class Wagon:
    """
        Class for the wagon and its attributes and methods to move and load.
    """
    pos: int
    packages: dict[Identifier, Package]
    num_stations: int
    capacity: int
    current_load: int

    def __init__(self, num_stations: int, capacity: int) -> None:
        """Initializes the wagon given two integers, capacity and station number."""
        self.capacity = capacity
        self.num_stations = num_stations
        self.pos = 0
        self.packages = dict()
        self.current_load = 0

    def move(self, direction: Direction) -> None: 
        """
            Method that moves a wagon a single unit in the given direction by the direction parameter of type Direction.
        """
        destination = self.pos + direction.value

        # Moves when no overflowing occurs
        if 0 <= destination <= self.num_stations - 1:
            self.pos = destination
        # First station case
        elif self.pos == 0:
            self.pos = self.num_stations - 1 if direction.value == -1 else destination
        # Last station case
        elif self.pos == self.num_stations - 1:
            self.pos = 0 if direction.value == 1 else destination
        
    def load_package(self, p: Package) -> None: 
        """Loads to the wagon the package p."""
        self.packages[p.identifier] = p
        self.current_load += p.weight
    
    def unload_package_id(self) -> Identifier | None:
        """
            Method that returns, if possible, the id of a deliverable package from the wagon.
        """
        if len(self.packages) == 0:
            return None
        else:
            for identifier in self.packages.keys():
                if self.packages[identifier].destination == self.pos:
                    return identifier
            return None
                    

class FullfilmentCenter:
    """Class that manages the fullfilment center."""
    _stations: list[Station]
    _num_stations: int
    _wagon: Wagon
    _cash: int

    def __init__(self, num_stations: int, wagon_capacity: int) -> None: 
        """Creates the center given two integers, the number of stations and wagon capacity."""
        self._num_stations = num_stations 
        self._stations = list()
        self._cash = 0

        #Create the list of stations
        for i in range(num_stations):
            self._stations.append(Station(i))

        #Create the wagon for the station
        self._wagon = Wagon(num_stations, wagon_capacity)

    def cash(self) -> int: 
        """Yields the corresponding integer of the invoiced money by the center so far."""
        return self._cash

    def wagon(self) -> Wagon: 
        """Returns the Wagon object that is being used by the fullfilment center."""
        return self._wagon 

    def num_stations(self) -> int:
        """Returns the integer of the number of stations of the center. """
        return self._num_stations

    def station(self, idx: int) -> Station:
        """
            Given an index as an integer, it returns the Station object corresponding to the selected station by the index if possible. 
        """
        assert 0 <= idx <= self.num_stations() - 1
        return self._stations[idx]

    def receive_package(self, p: Package) -> None: 
        """Given a package p, it gets loaded onto the desired station if valid."""
        assert self.station(p.source) 
        assert 0 <= p.destination <= self.num_stations() - 1

        source_station = self.station(p.source)
        source_station.receive_package(p)
         
    def deliver_package(self, identifier: Identifier) -> None:
        """Given an identifier, it tries to deliver the indexed package."""
        wagon = self.wagon()
        if wagon.pos == wagon.packages[identifier].destination:
            wagon.current_load -= wagon.packages[identifier].weight
            self._cash += wagon.packages[identifier].value
            del wagon.packages[identifier]

        elif wagon.pos != wagon.packages[identifier].destination:
             raise Exception("The package can't be delivered here!")
        else:
            raise Exception("The package has not been found!")

    def current_station_package(self) -> Package | None: 
        """Returns, if possible, a package from the current station."""
        wagon = self.wagon()
        packages = self.station(wagon.pos).packages
        return packages[-1] if len(packages) > 0 else None
    
    def load_current_station_package(self) -> None: 
        """Loads onto the wagon a current station package."""
        wagon = self.wagon()
        current_station = self.station(wagon.pos)
        package = current_station.send_package()

        # Check that the package has been successfully retracted
        assert package is not None
        # Check that the package doesn't overflow the wagon's capacity 
        assert wagon.current_load + package.weight <= wagon.capacity

        wagon.load_package(package)


    def write(self, stdscr: curses.window, caption: str = '') -> None:
        """Action that allows to visualize in the terminal the dynamics of the center."""
        def package_color(p: Package) -> int:
            return curses.color_pair(1 + p.destination * 6 * 764351 % 250)

        factory_height = 8  # maximum number of rows to write
        wagon_height = 6 # maximum number of rows to write
        delay = 0.15# delay after writing the state
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

    def move(self, t: TimeStamp, direction: Direction) -> None:
        print(t, 'MOVE', int(direction), file=self._file)

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