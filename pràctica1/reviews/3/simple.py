# """
# Template file for simple.py module.
# """

import sys
import curses

from fcenter import *

stdscr = curses.initscr()


class Strategy:

    _num_stations: int
    _wagon_capacity: int
    _log_path: str
    _logger = Logger
    fcenter: FullfilmentCenter
    t: TimeStamp

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None:
        """
        Constructor with num_stations and wagon_capacity integrers and 
        log_path string.
        """
        self._num_stations, self._wagon_capacity = num_stations, wagon_capacity
        self._log_path = log_path
        self._logger = Logger(log_path, "Fullfilment_center", num_stations, wagon_capacity)
        self.fcenter = FullfilmentCenter(num_stations, wagon_capacity)
        self.t = 0  
        
    def cash(self) -> int:
        """ Returns the FullfilmentCenter's cash earned."""
        return self.fcenter.cash()
    
    def check_packages(self, packages: list[Package], i:int, log: Logger) -> int:
        """
        Checks if there are packages to be added (in a concrete time unit) and adds them. 
        Returns the index of the first package that should be added in the next call.
        """

        while i < len(packages) and packages[i].arrival == self.t:
            self.fcenter.receive_package(packages[i]) #add package in position i
            log.add(self.t, packages[i].identifier)
            i += 1

        return i
        
    def exec(self, packages: list[Package]) -> None:
        f = open("cash.txt", "w")

        # initial variables
        last = packages[-1].arrival
        i = 0  # index that will run the packages list to add them to the fcenter
        logger = self._logger

        # strategy

        while self.t < last:

            current_pos = self.fcenter.wagon().pos 

            if len(self.fcenter.wagon().packages) > 0:
                to_deliver: list[Package] = [] # auxiliar list of packages needed to be deliver
                for pack in self.fcenter.wagon().packages.values():
                    if pack.destination == current_pos:
                        to_deliver.append(pack)

                j, n = 0, len(to_deliver) #index that runs the list "to_deliver"

                while j < n and self.t < last:
                    self.fcenter.deliver_package(to_deliver[j].identifier)
                    logger.deliver(self.t, to_deliver[j].identifier)
                    self.t += 1
                    i = self.check_packages(packages, i, logger) # add packages to the fcenter and update the index
                    j += 1

            if self.fcenter.current_station_package() is not None and (self.fcenter.current_station_package().weight + self.fcenter.wagon().current_load) <= self.fcenter.wagon().capacity:
                # conditions that should be met for loading a package to the wagon

                logger.load(self.t, self.fcenter.current_station_package().identifier)
                self.fcenter.load_current_station_package()
                self.t += 1
                i = self.check_packages(packages, i, logger) # add packages to the fcenter and update the index
                
            else: 
                self.fcenter.wagon().move(Direction.RIGHT) 
                logger.move(self.t, int(Direction.RIGHT))
                self.t += 1
                i = self.check_packages(packages, i, logger) # add packages to the fcenter and update the index
        
        f.write(str(self.cash()))

def init_curses() -> None:
    """Initializes the curses library to get fancy colors and whatnots."""

    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, 255):
        curses.init_pair(i + 1, curses.COLOR_WHITE, i)


def execute_strategy(packages_path: str, log_path: str, num_stations: int, wagon_capacity: int) -> None:
    """Execute the strategy on an fcenter with num_stations stations reading packages from packages_path and logging to log_path."""

    packages = read_packages(packages_path)
    strategy = Strategy(num_stations, wagon_capacity, log_path)
    strategy.exec(packages)


def main(stdscr: curses.window) -> None:
    """main script"""

    init_curses()

    packages_path = sys.argv[1]
    log_path = sys.argv[2]
    num_stations = int(sys.argv[3])
    wagon_capacity = int(sys.argv[4])

    execute_strategy(packages_path, log_path, num_stations, wagon_capacity)
    check_and_show(packages_path, log_path, stdscr)


if __name__ == '__main__':
    curses.wrapper(main)