# """
# Template file for simple.py module.
# """

import sys
import curses
from fcenter import *


class Strategy:
    num_stations: int
    wagon_capacity: int
    center: FullfilmentCenter
    direction: Direction
    t: TimeStamp
    _log: Logger
    _cash: int

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None:
        """Initialize the variables"""
        self.num_stations = num_stations
        self.wagon_capacity = wagon_capacity
        self.center = FullfilmentCenter(num_stations, wagon_capacity)
        self.direction = Direction.RIGHT
        self.t = 0
        self._log = Logger(log_path, "center", num_stations, wagon_capacity)
        self._cash = self.center.cash()

    def cash(self) -> int: 
        """Return cash value"""
        return self.center.cash()

    def exec(self, packages: list[Package]) -> None:
        """Simple.py execution"""
        f = open("cash.txt", "w")
        log = self._log
        t = self.t
        paquet = packages[0]
        space = True

        while len(packages) > 0:
            f.write(" " + str(self.cash()))
            space = True
            self.center.wagon().move(self.direction)                    # We move the wagon a position forward
            log.move(t, self.direction)
            t += 1 
            if paquet.arrival == t:                                     # We check if a package arrives at one of the stations
                self.center.receive_package(paquet)
                log.add(t, paquet.identifier)     
                packages.remove(packages[0])                            # We remove the package from the initial package list
                if len(packages) > 0:
                    paquet = packages[0]

            if len(self.center.wagon().packages) != 0:                  # If the wagon is not empty
                paquets_carregats = self.center.wagon().packages        # We declare paquets_carregats as the dictionary of ID/Package of the wagon
                for caixa in list(paquets_carregats.values()):          # We visit all the packages in the wagon
                    if caixa.destination == self.center.wagon().pos:    # If the destination of one of the packages we have loaded == station where we are
                        self.center.wagon().deliver(caixa.identifier)   # We remain with the value of the delivered package
                        self.center.deliver_package(caixa.identifier)   # We deliver the package (we delete it from the list of packages of the wagon) and update the value of the money obtained
                        log.deliver(t, caixa.identifier)
                        t += 1
                        
                        if paquet.arrival == t:                         # We evaluate if we have delivered a package, another has arrived at any station
                            self.center.receive_package(paquet)         
                            log.add(t, paquet.identifier)
                            packages.remove(packages[0])
                            if len(packages) > 0:
                                paquet = packages[0]


            act_pack: Package | None = self.center.current_station_package()
            while act_pack is not None and space:                                                # If the station we encounter is not empty (it has packages, it can be more than one)
                weight = act_pack.weight
                if (self.center.wagon().current_load + weight) <= self.center.wagon().capacity:  # If when adding the weight of the first package of the station we do not exceed wagon capacity
                    self.center.load_current_station_package()                                   # We load the package in the wagon
                    log.load(t, act_pack.identifier)
                    t += 1
                    
                    if paquet.arrival == t:                                                      # We evaluate if we have delivered a package, another has arrived at any station
                            self.center.receive_package(paquet)                                  # We add the received package to its corresponding station
                            log.add(t, paquet.identifier)
                            packages.remove(packages[0])
                            if len(packages) > 0:
                                paquet = packages[0]

                    act_pack = self.center.current_station_package()                             # We scan to see if the station contains more packages to load

                else: space = False                                                              # If we don't have the capacity to load a package, we move on



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