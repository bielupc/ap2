# """
# Template file for expert.py module.
# """

import sys
import curses

from fcenter import *

class Strategy:
    _num_stations: int
    _wagon_capacity: int
    fcenter: FullfilmentCenter
    direction: Direction
    t: TimeStamp
    _log_path: str
    _logger = Logger

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None:
        """
        Constructor with num_stations and wagon_capacity integrers and 
        log_path string.cd
        """
        self._num_stations, self._wagon_capacity = num_stations, wagon_capacity
        self._log_path = log_path
        self._logger = Logger(log_path, "Centre_distribucio", num_stations, wagon_capacity)
        self.fcenter = FullfilmentCenter(num_stations, wagon_capacity)
        self.t = 0
        self.direction = Direction.RIGHT
        
    def cash(self) -> int:
        """ Returns the cash earned."""
        return self.fcenter.cash()
    
    def check_convenient_direction(self, half: int, current: int) -> None:
        """
        Changes the actual direction to the most convenient one, comparing the value and the weight of the
        packages that can be delivered in the stations[0:half] and in the stations[half:num_stations].
        """

        points_esq, points_dre = 0, 0

        # strategy: we consider that it is equally important to maximize the money earned while emptying
        # the wagon as much as we can. That's why the points reside on pack.weight*pack.value.

        if len(self.fcenter.wagon().packages) > 0:
            for pack in self.fcenter.wagon().packages.values():
                if pack.destination < half: # the destination is in the stations[0:half]
                    points_esq += pack.value*pack.weight 

                else: # the destination is in the stations[half:num_stations]
                    points_dre += pack.value*pack.weight

            if points_esq > points_dre: # we want to go to the left part (stations[0:half])
                if current == 0: self.direction = Direction.RIGHT
                else: self.direction = Direction.LEFT

            else: # we want to go to the right part (stations[half:num_stations])
                if current == 0: self.direction = Direction.LEFT
                else: self.direction = Direction.RIGHT


    def check_packages(self, packages: list[Package], i:int, log: Logger) -> int:
        """Checks if there are packages to be added and adds them."""

        while i < len(packages) and packages[i].arrival == self.t:
            self.fcenter.receive_package(packages[i])
            log.add(self.t, packages[i].identifier)
            i += 1

        return i
        
    def exec(self, packages: list[Package]) -> None:
        f = open("cash.txt", "w")

        # initial variables
        last = packages[-1].arrival
        i = 0  #index used for checking the packages that need to be added at every time unit
        half = self.fcenter.num_stations() // 2 # half of the num_stations 
        logger = self._logger

        # strategy starts: similar to the simple strategy but we add this extra function 
        # that checks the convenient direction when we are in the pos = 0 or the pos = half

        while self.t < last:

            current = self.fcenter.wagon().pos
            if current % half == 0:
                self.check_convenient_direction(half, current)

            if len(self.fcenter.wagon().packages) > 0:
                to_deliver: list[Package] = []
                for pack in self.fcenter.wagon().packages.values():
                    if pack.destination == current:
                        to_deliver.append(pack)

                j, n = 0, len(to_deliver)

                while j < n and self.t < last:
                    self.fcenter.deliver_package(to_deliver[j].identifier)
                    logger.deliver(self.t, to_deliver[j].identifier)
                    self.t += 1
                    i = self.check_packages(packages, i, logger)
                    j += 1

            if self.fcenter.current_station_package() is not None and (self.fcenter.current_station_package().weight + self.fcenter.wagon().current_load) <= self.fcenter.wagon().capacity:
                logger.load(self.t, self.fcenter.current_station_package().identifier)
                self.fcenter.load_current_station_package()
                self.t += 1
                i = self.check_packages(packages, i, logger)
                
            else:
                self.fcenter.wagon().move(self.direction) 
                logger.move(self.t, int(self.direction)) 
                self.t += 1
                i = self.check_packages(packages, i, logger)
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