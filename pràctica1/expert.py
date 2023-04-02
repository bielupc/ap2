import sys
import curses

from fcenter import *


class Strategy:
    """Class that holds the methods for the logistics of the strategy."""
    _center: FullfilmentCenter
    _logger: Logger    

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None:
        """Constructor that builds up the loger and the fcenter objects."""
        self._center = FullfilmentCenter(num_stations, wagon_capacity)
        self._logger = Logger(log_path, "expert", num_stations, wagon_capacity)
    
    def center(self) -> FullfilmentCenter:
        """Returns the fullfullment center object being used for the strategy."""
        return self._center
    
    def logger(self) -> Logger:
        """Returns the logger object being used by for the strategy."""
        return self._logger

    def cash(self) -> int: 
        """Yields the corresponding integer of the invoiced money by the center so far."""
        return self.center().cash()
    
    def optimal_direction(self, target: int) -> tuple[int, int]:
        """
            Returns a tuple (distance, direction) to indicate the shortest distance from wagon position to target and the direction it should move.
        """

        wagon_pos = self.center().wagon().pos

        inner_distance = (wagon_pos - target) % self.center().num_stations()
        outer_distance = (target - wagon_pos) % self.center().num_stations()
        distance = min(inner_distance, outer_distance)

        if target < wagon_pos:
            direction = 1 if outer_distance >= inner_distance else -1
        else:
            direction = 1 if outer_distance <= inner_distance else -1
        
        return distance, direction
  
    def highest_delivery_station(self) -> int:
        """
            Returns the direction to take in order to deliver the most amount of valuable packages in one full circular motion.
        """

        left = 0
        right = 0
        
        wagon_pos = self.center().wagon().pos
        for package in self.center().wagon().packages.values():
            if check_if_deliverable(1, wagon_pos, package.destination, wagon_pos):
                right += 1
            elif check_if_deliverable(-1, wagon_pos, package.destination, wagon_pos):
                left += 1
        return 1 if right >= left else -1
    
    def highest_value_station(self) -> int:
        """
            Returns the index of the most valuable station based on package value, proximity and unload values.

            Score(Si) = 0.5*VAL + 0.1*(STATIONS - DIST) + 0.1*UNLOADS - 0.3*WEIGHTS
        """

        scores = {idx: 0 for idx in range(self.center().num_stations())}
        
        for target in range(self.center().num_stations()):
            value = 0
            weight = 0
            unloads= 0

            distance, direction = self.optimal_direction(target)

            # Accumulated value and weight penaty.
            for p in self.center().station(target).packages:
                value += p.value
                weight += p.weight

            # Possible unloads
            wagon_pos = self.center().wagon().pos
            for package in self.center().wagon().packages.values():
                if check_if_deliverable(direction, wagon_pos, package.destination, target):
                    unloads += 1

            scores[target] = 0.5*value + 0.1*(self.center().num_stations() - distance) + 0.1*unloads - 0.3*(weight)

        return max(scores, key=scores.get)
        
    def exec(self, packages: list[Package]) -> None:  
        """
            Given a list of packages it executes the strategy that tries to deliver them all.
        """

        #Shortcuts
        center = self.center()
        logger = self.logger()

        fixed = False
        deliver_mode = False
        load_mode = True
        target = 1

        for t in range(packages[-1].arrival):
            # Checks for new arrivals 
            if packages[0].arrival == t:
                p = packages.pop(0)
                center.receive_package(p)
                logger.add(t, p.identifier)
            
            # Check for delivery
            identifier = center.wagon().unload_package_id()
            if identifier is not None:
                center.deliver_package(identifier)
                logger.deliver(t, identifier)
                continue # It jumps to the next timestamp

            # Check if we arrived at goal station
            if center.wagon().pos == target: fixed = False

            if not fixed:
                # Set deliver mode
                if self.center().wagon().current_load > 0:
                    deliver_mode = True
                    load_mode = False
                    direction = self.highest_delivery_station()
                    fixed = True
                    target = center.wagon().pos
                # Set load mode
                else:
                    deliver_mode = False
                    load_mode = True
                    target = self.highest_value_station()
                    fixed = True
                    distance, direction = self.optimal_direction(target)
                    
            # Check for packages to load in both modes 
            if load_mode:
                p = center.current_station_package()

                # The package exist, and fits in
                if p is not None and p.weight + center.wagon().current_load <= center.wagon().capacity: 
                    # Lots of capacity left scenario
                    if center.wagon().current_load <= 0.8*center.wagon().capacity:
                        center.load_current_station_package()
                        logger.load(t, p.identifier)
                        continue 
                    # Deliverable on the way to target scenario
                    elif check_if_deliverable(direction, center.wagon().pos, p.destination, target):
                        center.load_current_station_package()
                        logger.load(t, p.identifier)
                        continue 
                    # Very valuable package scenario
                    elif p.value >= center.station(target).packages[-1].value:
                        center.load_current_station_package()
                        logger.load(t, p.identifier)
                        continue 

            elif deliver_mode:
                p = center.current_station_package()
                if (p is not None and p.weight + center.wagon().current_load <= center.wagon().capacity) and center.wagon().current_load <= 0.8*center.wagon().capacity:
                    center.load_current_station_package()
                    logger.load(t, p.identifier)
                    continue 
                elif (p is not None and p.weight + center.wagon().current_load <= center.wagon().capacity) and (check_if_deliverable(direction, center.wagon().pos, p.destination, target)): 
                    center.load_current_station_package()
                    logger.load(t, p.identifier)
                    continue 

            # If it hasn't skiped the iteration, it moves.
            center.wagon().move(Direction(direction))
            logger.move(t, direction)


def check_if_deliverable(direction: int, wagon_pos: int, destination: int, target: int) -> bool:
    """
        Given a direction, wagon pos, target and package destination, it returns weather the package
        will be deliverable on the way to the target station.
    """

    if direction == 1 and ((wagon_pos <= destination <= target) or
    (destination <= target < wagon_pos) or 
    (target < wagon_pos < destination)):
       return True

    elif direction == -1 and ((target <= destination <= wagon_pos) or 
    (destination >= wagon_pos > target) or 
    (wagon_pos > target > destination)):
        return True 
    
    else: return False
    

def init_curses() -> None:
    """Initializes the curses library to get fancy colors and whatnots."""

    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS - 1):
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
