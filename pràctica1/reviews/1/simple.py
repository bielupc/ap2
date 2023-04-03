# """
# Template file for simple.py module.
# """

import sys
import curses

from fcenter import *

class Strategy:

    _num_stations: int
    _wagon_capacity : int
    _log_path : str
    _direction: Direction
    _fullfilmentCenter : FullfilmentCenter
    _logger : Logger
    _time : TimeStamp
    _cash : int
    

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None: 
        """This is for initializing the object created"""
        
        self._num_stations = num_stations
        self._wagon_capacity = wagon_capacity
        self._log_path = log_path
        self._direction = Direction.RIGHT
        self._fullfilmentCenter = FullfilmentCenter(num_stations,wagon_capacity)
        self._logger = Logger(log_path, "simple", self._num_stations, self._wagon_capacity)
        self._time = 0
        self._cash = 0 
    
    def cash(self) -> int:
        """This function returns the amount of cash collected""" 
        
        return self._cash
   
    def list_packages_delivery(self)-> list[Package]:
        """This function gives a list of packages that can be delivered at the station"""
        list_to_deliver : list[Package] 
        list_to_deliver = []

        for possible_delivered_package in self._fullfilmentCenter.wagon().packages.values():
            if possible_delivered_package.destination == self._fullfilmentCenter.wagon().pos:
                list_to_deliver.append(possible_delivered_package)
        
        return list_to_deliver
    
    def package_to_source_station(self, packages:list[Package])->None:
        """This function checks if any package has to be delivered at that time"""

        if self._time == packages[0].arrival and len(packages) > 0:
            self._fullfilmentCenter.receive_package(packages[0])
            self._logger.add(self._time,packages[0].identifier)
            packages.remove(packages[0])
        

    def exec(self, packages: list[Package]) -> None: 
        """ This function executes the strategy by using the fcenter and new functions"""
        f = open("cash.txt", "w")
        while len(packages) > 0 and self._time <= packages[-1].arrival:

            f.write(" " + str(self._fullfilmentCenter.cash()))
            
            #packages to go to their station source
            self.package_to_source_station(packages)
            _first_package_in_station = self._fullfilmentCenter.current_station_package()
            
            #delivering packages on the list created to know which ones have to be delivered
            while len(self.list_packages_delivery()) > 0:
                package_needed:Package
                package_needed = self.list_packages_delivery()[0]
                self._logger.deliver(self._time, package_needed.identifier)
                self._fullfilmentCenter.deliver_package(package_needed.identifier)
                self._time += 1
                if len(packages) == 0 or self._time == packages[-1].arrival: break
                self.package_to_source_station(packages) #we will look every time we add a second if some package can be delivered

            #packages the wagon can pick up from the station
            while _first_package_in_station is not None and (_first_package_in_station.weight + self._fullfilmentCenter.wagon().current_load < self._fullfilmentCenter.wagon().capacity):
                
                self._logger.load(self._time, _first_package_in_station.identifier)
                self._fullfilmentCenter.load_current_station_package()
                self._time += 1
                if len(packages) == 0 or self._time == packages[-1].arrival: break
                self.package_to_source_station(packages)
                _first_package_in_station = self._fullfilmentCenter.current_station_package() #as the first package in the station changes, we have to pick a new package
            
            #moving one position to the right and starting all over again if demanded
            self._fullfilmentCenter.wagon().move(Direction(1))
            self._logger.move(self._time, Direction(1))
            self._time += 1
        



def init_curses() -> None:
    """Initializes the curses library to get fancy colors and whatnots."""

    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
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