import sys
import curses

from fcenter import *


class Strategy:
    """Class that holds the methods for the logistics of the strategy."""
    _center: FullfilmentCenter
    _time: int
    _logger: Logger    

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None:
        """Constructor that builds up the loger and the fcenter objects."""
        self._center = FullfilmentCenter(num_stations, wagon_capacity)
        self._time = 0
        self._logger = Logger(log_path, "simple", num_stations, wagon_capacity)
    
    def center(self) -> FullfilmentCenter:
        """Returns the fullfullment center object being used for the strategy."""
        return self._center
    
    def logger(self) -> Logger:
        """Returns the logger object being used by for the strategy."""
        return self._logger
    
    def time(self) -> int:
        """Returns the current time."""
        return self._time

    def cash(self) -> int: 
        """Yields the corresponding integer of the invoiced money by the center so far."""
        return self.center().cash()

    def exec(self, packages: list[Package]) -> None:  
        """
            Given a list of packages it executes the strategy that tries to deliver them all.
        """
        #Shortcuts
        center = self.center()
        logger = self.logger()

        while True:
            # It ends when the last package arrives
            if len(packages) == 0: break
            
            # Checks for new arrivals 
            if packages[0].arrival == self.time():
                p = packages.pop(0)
                center.receive_package(p)
                logger.add(self.time(), p.identifier)
            
            # Lists the deliverable packages
            wagon_packages = center.wagon().packages
            for_delivery: list[int] = list()
            for identifier in wagon_packages.keys():
                if wagon_packages[identifier].destination == center.wagon().pos:
                    for_delivery.append(identifier)
                    print(identifier)
            
            # It delivers the packages after iterating the dictionary
            for identifier in for_delivery:
                center.deliver_package(identifier)
                logger.deliver(self.time(), identifier)

            # Loads the packages
            full = False
            while not full:
                try:
                    # The assertions are coded inside the module
                    p = center.current_station_package()
                    center.load_current_station_package()
                    logger.load(self.time(), p.identifier)
                except:
                    full = True

            # When it's done, it moves the wagon 1 unit
            center.wagon().move(Direction(1))
            logger.move(self.time(), 1)

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
