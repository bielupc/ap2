# """
# Template file for expert.py module.
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
    box: bool

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None:
        """Initialize the variables"""
        self.num_stations = num_stations
        self.wagon_capacity = wagon_capacity
        self.center = FullfilmentCenter(num_stations, wagon_capacity)
        self.direction_r = Direction.RIGHT
        self.direction_l = Direction.LEFT
        self.t = 0
        self._log = Logger(log_path, "center", num_stations, wagon_capacity)
        self._cash = self.center.cash()
        self.box = True

    def cash(self) -> int: 
        """Return cash value"""
        return self.center.cash()
    
    def dir_LEFT(self, w: Wagon, number_stations:int) -> int: 
            """
            Returns the minimum number of moves we have to do 
            to deliver one of the packages we have loaded if we 
            go to the left.
            """
            assert len(w.packages) != 0
            min_ = number_stations
            mov: int
            pack: Package

            for paquet in w.packages:
                pack = w.packages[paquet]
                if pack.destination < w.pos:
                    mov = abs(pack.destination - w.pos)
                else:
                    mov = (w.pos - pack.destination) + number_stations

                if mov < min_:
                    min_ = mov
                
            return min_
    
    def dir_RIGHT(self, w: Wagon, number_stations: int) -> int:
            """
            Returns the minimum number of moves we have to do 
            to deliver one of the packages we have loaded if we 
            go to the right.
            """
            assert len(w.packages) != 0
            min_ = number_stations
            mov: int
            pack: Package

            for paquet in w.packages:
                pack = w.packages[paquet]
                if pack.destination < w.pos:
                    mov = (pack.destination - w.pos) + number_stations
                else:
                    mov = pack.destination - w.pos

                if mov < min_:
                    min_ = mov
            
            return min_
    

    def stat(self, w: Wagon, number_stations:int) -> int:
            """
            Returns the index of the nearest station that 
            contains packets to pick up (is not empty)
            """
            idx = 0
            mov = 0
            min_mov = number_stations
            min_idx = 0

            for station in self.center.stations:
                if len(station.packages) != 0:
                    left = w.pos - station.idx 
                    if left < 0:
                        left += number_stations
                    right = station.idx - w.pos
                    if right < 0:
                        right += number_stations

                    mov = min(left, right)
                    if mov < min_mov:
                        min_mov = mov 
                        min_idx = idx

                idx += 1

            return min_idx
    
    def r_or_l(self, w: Wagon, stations: int) -> bool:
            """
            Returns true if it takes less time to go to the 
            nearest packet station going right and false if it 
            takes less time going left. If it takes the same, 
            it goes right by default.
            """

            left = (w.pos - self.stat(w, stations))
            if left < 0:
                left += stations
            right = (self.stat(w, stations) - w.pos)
            if right < 0:
                right += stations

            return left >= right
    
    def exec(self, packages: list[Package]) -> None: 
        log = self._log
        t = self.t
        paquet = packages[0]
        space = True
        f = open("cash.txt", "w")

        while len(packages) > 0:                                            # The loop will last as long as there are packets to arrive at one of the stations
            f.write(" " + str(self.cash()))

            while self.box:
                # MOVE WAGON
                self.center.wagon().move(self.direction_r)                  # We move the wagon a position forward
                log.move(t, self.direction_r)
                t += 1 

                # ADD PACKAGE
                if paquet.arrival == t:                                     # We check if a package arrives at one of the stations
                    self.center.receive_package(paquet)
                    log.add(t, paquet.identifier)     
                    packages.remove(packages[0])                            # We remove the package from the initial package list
                    if len(packages) > 0:
                        paquet = packages[0]
                    self.box = False


            # The first package has just arrived at one of the stations
            # We move, then, in the direction that allows us to pick it up before as long as our wagon is empty
            # (If the distance to pick up the package is the same for both the right and the left, by default, we advance to the right)


            if len(self.center.wagon().packages) == 0:                      # If our wagon is empty
                space = True

                # MOVE WAGON
                if self.r_or_l(self.center.wagon(), self.num_stations):
                    self.center.wagon().move(self.direction_r)
                    log.move(t, self.direction_r)
                else:
                    self.center.wagon().move(self.direction_l)
                    log.move(t, self.direction_l)
                t += 1

                # ADD PACKAGE
                if paquet.arrival == t:                                     # We check if a package arrives at one of the stations
                    self.center.receive_package(paquet)
                    log.add(t, paquet.identifier)     
                    packages.remove(packages[0])                            # We remove the package from the initial package list
                    if len(packages) > 0:
                        paquet = packages[0]
                

                # LOAD PACKAGE
                act_pack: Package | None = self.center.current_station_package()                     # act_pack will be the first package of the station in which we are (if it's not empty)
                while act_pack is not None and space:                                                # If the station we encounter is not empty (it has packages, it can be more than one)
                    weight = act_pack.weight
                    if (self.center.wagon().current_load + weight) <= self.center.wagon().capacity:  # If when adding the weight of the first package of the station we do not exceed wagon capacity
                        self.center.load_current_station_package()                                   # We load the package in the wagon
                        log.load(t, act_pack.identifier)
                        t += 1
                        
                        # ADD PACKAGE
                        if paquet.arrival == t:
                            self.center.receive_package(paquet)                                      # We evaluate if we have loaded one package, another has arrived at any station
                            log.add(t, paquet.identifier)
                            packages.remove(packages[0])                                             # We remove the package from the initial package list
                            if len(packages) > 0:
                                paquet = packages[0]

                        act_pack = self.center.current_station_package()                             # We scan to see if the station contains more packages to load

                    else: space = False                                                              # If we don't have the capacity to load a package, we move on


            # Now that the wagon has a package (or more) we move in a direction that allows us to deliver the package (or one of them) as soon as possible, minimizing the number of movements
            # If the shortest distance to deliver a packet is the same for both left and right, by default it moves to the right

            elif len(self.center.wagon().packages) != 0:
                
                # MOVE WAGON 
                space = True
                if self.dir_LEFT(self.center.wagon(), self.num_stations) >= self.dir_RIGHT(self.center.wagon(), self.num_stations):
                    self.center.wagon().move(self.direction_r)
                    log.move(t, self.direction_r)
                else:
                    self.center.wagon().move(self.direction_l)
                    log.move(t, self.direction_l)
                t += 1

                # ADD PACKAGE
                if paquet.arrival == t:                                     # We evaluate if we have loaded one package, another has arrived at any station
                    self.center.receive_package(paquet)                                  
                    log.add(t, paquet.identifier)
                    packages.remove(packages[0])                            # We remove the package from the initial package list
                    if len(packages) > 0:
                        paquet = packages[0]


                # DELIVER PACKAGE
                paquets_carregats = self.center.wagon().packages        # We declare paquets_carregats as the dictionary of ID/Package of the wagon
                for caixa in list(paquets_carregats.values()):          # We visit all the packages in the wagon
                    if caixa.destination == self.center.wagon().pos:    # If the destination of one of the packages we have loaded == station where we are
                        self.center.wagon().deliver(caixa.identifier)   # We remain with the value of the delivered package
                        self.center.deliver_package(caixa.identifier)   # We deliver the package (we delete it from the list of packages of the wagon) and update the value of the money obtained
                        log.deliver(t, caixa.identifier)
                        t += 1
                        
                        # ADD PACKAGE
                        if paquet.arrival == t:
                            self.center.receive_package(paquet)         # We evaluate if we have delivered a package, another has arrived at any station
                            log.add(t, paquet.identifier)
                            packages.remove(packages[0])                # # We remove the package from the initial package list
                            if len(packages) > 0:
                                paquet = packages[0]


                # LOAD PACKAGE
                act_pack: Package | None = self.center.current_station_package()                     # act_pack will be the first package of the station in which we are (if it's not empty)
                while act_pack is not None and space:                                                # If the station we encounter is not empty (it has packages, it can be more than one)
                    weight = act_pack.weight
                    if (self.center.wagon().current_load + weight) <= self.center.wagon().capacity:  # If when adding the weight of the first package of the station we do not exceed wagon capacity
                        self.center.load_current_station_package()                                   # We load the package in the wagon
                        log.load(t, act_pack.identifier)
                        t += 1
                        
                        # ADD PACKAGE
                        if paquet.arrival == t:                                                      # We evaluate if we have loaded one package, another has arrived at any station
                                self.center.receive_package(paquet)                                  
                                log.add(t, paquet.identifier)
                                packages.remove(packages[0])                                         # We remove the package from the initial package list
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