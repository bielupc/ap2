import sys
import curses

from fcenter import *


class Strategy:
    _center: FullfilmentCenter
    _time: int
    _logger: Logger    

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None:
        self._center = FullfilmentCenter(num_stations, wagon_capacity)
        self._time = 0
        self._logger = Logger(log_path, "simple", num_stations, wagon_capacity)
    
    def center(self) -> FullfilmentCenter:
        return self._center
    
    def logger(self) -> Logger:
        return self._logger
    
    def time(self) -> int:
        return self._time

    def cash(self) -> int: 
        return self.center().cash()

    def exec(self, packages: list[Package]) -> None:  
        finished = False
        center = self.center()
        logger = self.logger()

        while True:
            
            # We end when the last package arribes
            if len(packages) == 0: break
            
            # We first deliver the packages to the station
            if packages[0].arrival == self.time():
                p = packages.pop(0)
                center.receive_package(p)
                logger.add(self.time(), p.identifier)
            
            # We check for packages to deliver
            wagon_packages = center.wagon().packages
            for_delivery: list[int] = list()
            for identifier in wagon_packages.keys():
                if wagon_packages[identifier].destination == center.wagon().pos:
                    for_delivery.append(identifier)
                    print(identifier)
            
            for identifier in for_delivery:
                center.deliver_package(identifier)
                logger.deliver(self.time(), identifier)

                

            # We check for packages to load as long as it's not full
            # full = False
            # while not full:
            #     try:
            #         center.load_current_station_package()
            #         logger.load(self.time(), iden)

            #     except:
            #         full = True
           

            
            
            # After we're done, we move the wagon 1 unit
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
