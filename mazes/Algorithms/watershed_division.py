"""
mazes.Algorithms.watershed_division - a more general recursive division algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of recursive division using the Watershed class.
    It is implemented here as a passage carver.  The only precondition is that
    the starting set of cells (or subgrid) must be connected.

    Here we implement the algorithm on a rectangular grid as a passage
    carver.  The following pseucode encapsulates the essentials:

        def divide(bbox, params):
            if bbox is larger than 1 cell:
                bbox1, params1, bbox2, params2 = subdivide(bbox, params)
                divide(bbox1, params1)
                divide(bbox2, params2)
                link the two subdivisions

IMPLEMENTATION

    The class RecursiveDivision is built on the Algorithm class in the usual
    way.  Run the implementation as:
        status = RecursiveDivision.on(maze)
    See method parse_args() in RecursiveDivision.Status for optional arguments.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 55-60, 249.

LICENSE
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

MODIFICATIONS

    1 Sep 2025 - detect disconnected auxiliary mazes.   
        (a) change the default floodgate carver to Kruskal
        (b) add an option to fix the maze
    8 Sep 2025 - add code to place extra pumps, when needed, and,
        optionally to save a trace of the basins formed when these
        extra pumps are placed.
"""
import mazes
from mazes.grid import Grid
from mazes.maze import Maze
from mazes.watershed import Watershed
from mazes import rng, Algorithm
from mazes.Algorithms.kruskal import Kruskal    # 1 Sep 2025 - change default

ROOM_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    # UTILITY ROUTINES
    #       These are for any connected grid or for any connected subset
    #       of the cells in a grid.

error_info = dict()

class Reservoir(object):       # duck-typed replacement for Subgrid
    """subgrid"""

    def __init__(self, maze:Maze, cells:set=None):
        """initialization"""
        self.maze = maze
        self.grid = cells if cells else set(maze.grid)

    def __str__(self):
        """representation"""
        return "Reservoir(" + str(self.cells) + " cells)"

    @property
    def cells(self):
        """returns the number of cells in the reservoir"""
        return len(self.grid)

    def carve_room(self):
        """link all the neighborhoods in the reservoir

        returns the number of links created
        """
        links = 0
        to_be_joined = set()
        for cell in self.grid:
            for nbr in cell.neighbors:
                if nbr in self.grid:
                    to_be_joined.add(frozenset([cell, nbr]))
        for join in to_be_joined:
            cell, nbr = join
            self.maze.link(cell, nbr)
            links += 1
        return links

    def divide(self, mincells:int, pumps:int, *args, debug:bool=False,
               FloodgateCarver:object=Kruskal,          # 1 Sep 2025
               WatershedType:object=Watershed, **kwargs):
        """partition a reservoir, if possible

        REQUIRED ARGUMENTS

            mincells - if there are fewer cells, the reservoir will not
                be divided (must be at least 2)

            pumps - the number of pumps to use (must be at least 2)

        KEYWORD ARGUMENTS

            debug (default: False)
                display some comments for debugging purposes

            FloodgateCarver (default: Kruskal)
                the algorithm for determining where floodgates are needed.
                This only determines which pairs of reservoirs will be
                joined by a passage (or floodgate).  Within those constraints,
                the actual choice is random.

                Kruskal's algorithm is admits disconnected grids and returns
                the number of components in the grid.

            WatershedType (default: Watershed)
                The type to be used.  Unparsed arguments will be passed as
                additional arguments to the constructor.

        RETURN VALUE

            ((subgrid1, subgrid2), links) where:
                subgrid1 and subgrid2 are the subdivisions;
                links is the number of doors carved (links=1)

            If no further subdivision is possible, then the return value
            is ((), 0).
        """
        mincells = max(mincells, 2)
        pumps = min(max(pumps, 2), self.cells)  # at most 1 per cell
        if self.cells < mincells:
            if debug:
                print(f"{self}: below threshold")
            return (tuple(), 0, None)           # too small

        seeds = rng.choices(list(self.grid), k=pumps)
        watershed = WatershedType(self.grid, seeds, *args, **kwargs)

        passes = 1
        while watershed.round_robin():
            passes += 1
        if debug:
            print(f"{self}: {passes} passes, {pumps} pumps")

        auxiliary_maze = watershed.initialize_maze()
        status = FloodgateCarver.on(auxiliary_maze)

        if debug:
            print(status)

        gates = watershed.doors(auxiliary_maze)
        if debug:
            print(f"{self}: {gates} floodgates")
        for gate in gates:
            assert isinstance(gate, set)
            cell1, cell2 = gate
            self.maze.link(cell1, cell2)

            # set up the return value
        reservoirs = tuple(watershed.watersheds.values())
        return reservoirs, len(gates), auxiliary_maze

class WatershedDivision(Algorithm):
    """a generalized recursive division algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Watershed Recursive Division"

        __slots__ = ("__Reservoir", "__stack", "__min_cells", "__pumps",
                     "__label_rooms", "__room_carver", "__room_id",
                     "__debug", "__args", "__kwargs",
                     "__error_action",                  # 1 Sep 2025
                     "__eptracer", "__eptrace")         # 8 Sep 2025

        @property
        def debug(self) -> bool:
            """for debugging"""
            return self.__debug

        @property
        def min_cells(self) -> int:
            """the smallest number of cells"""
            return self.__min_cells

        def label(self, reservoir):
            """label a room"""
            theLabel = ROOM_LABELS[self.__room_id]
            self.__room_id = (self.__room_id + 1) % len(ROOM_LABELS)
            for cell in reservoir:
                cell.label = theLabel

        def pump_more(self, cells:set, basins:tuple, links:int, aux_maze:'Maze'):
            """are there cells that haven't been filled?'"""
            filled = sum(len(basin) for basin in basins)
            if filled >= len(cells):
                return basins, links, aux_maze          # full!

                    # more work to do...
            basins = list(basins)
            aux_grid = aux_maze.grid
            visited = set()
            for basin in basins:
                visited.update(set(basin))
            unvisited = cells - visited
            # end for

                    ##### THE BIG LOOP #####
            while unvisited:
                self.increment_item("extra pumps")
                pump = rng.choice(list(unvisited))  # the pump
                new_basin = set()
                stack = [pump]
                edges = list()
                while stack:
                    cell = stack.pop()
                    new_basin.add(cell)
                    for nbr in cell.neighbors:
                        if nbr not in cells:
                            continue                # not part of the reservoir
                        if nbr in new_basin:
                            continue                # already part of the new basin
                        if nbr in visited:
                            arc = (cell, nbr)       # in another basin
                            edges.append(arc)
                            continue
                        stack.append(nbr)       # to be added
                    # end for
                # end while stack

                    # update the reservoir -- we have a new filled basin
                i = len(basins)                 # get the basin number
                basins.append(new_basin)
                visited.update(new_basin)
                unvisited.difference_update(new_basin)
                    # pick an edge to create a floodgate
                arc = rng.choice(edges)
                cell, nbr = arc
                self.maze.link(cell, nbr)
                links += 1
                    # update the auxiliary maze
                aux_grid[i] = aux_grid.newcell(i)
                for j in range(len(basins)):
                    if nbr in basins[j]:
                        aux_maze.link(aux_grid[i], aux_grid[j])
                        break
                # end for
            # end while unvisited

            if self.__eptrace:
                self.__eptracer.append(basins)
            return tuple(basins), links, aux_maze

        def divide(self):
            """divide the current subdivision

            This is an iterative formulation using a stack.  Don't call this
            if the stack is empty
            """
            reservoir = self.pop()
            pumps = self.__pumps(reservoir.cells)
            basins, links, aux_maze = reservoir.divide(self.min_cells, pumps, \
                *self.__args, **self.__kwargs)
            if len(basins) > 0:
#                print(len(basins), links, len(aux_maze.grid), len(aux_maze))
                assert len(basins) == len(aux_maze.grid)
                assert links == len(aux_maze)

                    # have all cells been flooded?  -- 8 Sep 2025
                basins, links, aux_maze = self.pump_more(reservoir.grid, \
                    basins, links, aux_maze)

            # print(type(basins), links)
            self.increment_item("links", links)
            self.increment_item("doors", links)
            if len(basins) == 0:
                if self.__room_carver:
                    links = reservoir.carve_room()
                    self.increment_item("rooms", 1)
                    self.increment_item("room links", links)
                    self.increment_item("links", links)
                return

                # Added 1 Sep 2025 - detect disconnected auxiliary mazes
            if len(basins) > links + 1:
                if self.fetch_item("watershed errors") == 0:
                    print("*** Warning:",
                          "A disconnected watershed has been detected.",
                          "***")
                                ### DEBUGGING INFORMATION
                    if self.__error_action == 'debug':
                        n = 0
                        for basin in basins:
                            for cell in basin:
                                cell.label = chr(n + ord('0'))
                            n += 1
                        error_info[0] = self
                        error_info[1] = reservoir
                        print("Auxiliary maze:")
                        for cell in aux_maze.grid:
                            for nbr in cell.neighbors:
                                if cell.is_linked(nbr):
                                    print(cell.index, "--", nbr.index)
                        assert False, "Watershed error detected"
                self.increment_item("watershed errors")

            for basin in basins:
                reservoir = self.__Reservoir(self.maze, basin)
                self.push(reservoir)
                if self.__label_rooms:
                    self.label(basin)

        def parse_args(self, min_cells:int, pumps:(int, callable), *args,
                       ReservoirType:object=Reservoir,
                       error_action:('ignore', 'fix')='ignore',     # 1 Sep 2025
                       carve_rooms:bool=False, label_rooms:bool=False,
                       extra_pumps_trace:bool=False,                # 8 Sep 2025
                       **kwargs):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.
                min_cells   the minimum number of cells in a subdividable
                        basin.  This value must be at least 2.
                pumps       this can either be a fixed integer or a function
                        of the number of cells, as with fewer cells, we might
                        want fewer pumps.

                    For example, consider the following pump function:
                        def pumps(cells:int):
                            return 4 if cells > 100 else 2
                    If there are more than 100 cells in a given basin,
                    the number of pumps will be set at 4, yield smaller
                    subdivisions than if two pumps are used.  This will
                    tend to result in fewer levels of recursion.
                args    additional positional arguments

            KEYWORD ARGUMENTS
             *  debug (default=False)
                    set to True for detailed stack analysis
                ReservoirType (default=Reservoir defined above)
                    can be modified to change the way the algorithm
                    recursively subdivides the grid.
                WatershedType (default=Watershed defined in mazes.watershed)
                    the watershed object type.
             *  FloodgateCarver (default=Kruskal)
                    a passage carving algorithm to be used to carve the
                    floodgates (doors).

                    Kruskal's algorithm is preferred since it can accept
                    a disconnected grid and reports the number of components.
                    Use of an algorithm that forbids disconnected grids
                    (like Aldous/Broder) may result in unpredictable
                    failures.
                error_action (default='ignore')
                    the possible values are 'ignore' or 'fix'.
                        'ignore' - if there are disconnected basins, a
                            message will be printed but no action will
                            be taken at the end to connect the maze.
                        'fix' - if there are disconnected basins, a
                            message will be printed, and Kruskal's
                            algorithm will be used at the end to connect
                            the maze.  This option is not available if
                            the cell minimum is larger than two unless
                            rooms are carved.
                extra_pumps_trace (default=False)
                    set to True to get basin information for extra pumps.
                    See the documentation for more details.
             *  QueueType (default=maze.Queues.Queue)
                    a queuing type.
             *  qargs (default={})
                    queuing arguments (e.g. for type PriorityQueue)
                carve_rooms (default=False)
                    if True, rooms will be carved when the subgrid is
                    too small to subdivide.  This will make no difference
                    if min_cells is equal to 2.
                label_rooms (default=False)
                    if true, the cells in the basin will be labelled.  The
                    labels will only be displayed in console displays, so
                    they are of no use for grids that can only be displayed
                    as graphic objects.
                kwargs
                    unparsed keyword arguments to pass to the ReservoirType
                    object

            Except for "debug", the starred arguments are carried in "kwargs"
            and passed along for parsing in the Reservoir and Watershed
            initializations.  The "debug" option is both parsed and passed
            along.
            """
            super().parse_args()                # chain to parent
            self.__min_cells = max(min_cells, 2)
            if isinstance(pumps, int):
                self.__pumps = lambda cells: pumps
            else:
                self.__pumps = pumps
            if error_action not in ('ignore', 'fix', 'debug'):  # 1 Sep 2025
                raise ValueError("'error_action' must be 'ignore' or 'fix'")
            if error_action == 'fix':                   # 1 Sep 2025
                if bool(carve_rooms) or self.__min_cells <= 2:
                    pass
                else:
                    msg = "'error_action=fix' is incompatible with" \
                        + " 'min_cells'>2 when 'carve_rooms' is False"
                    raise ValueError(msg)
            self.__error_action = error_action          # 1 Sep 2025
            self.__Reservoir = ReservoirType
            self.__label_rooms = bool(label_rooms)
            self.__room_id = 0
            self.__room_carver = bool(carve_rooms)
            self.__debug = kwargs.get("debug", False)
            self.__args = args
            self.__kwargs = kwargs
            self.__eptrace = extra_pumps_trace
            self.__eptracer = list()
            self.__stack = []

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.maze.grid))
            self.store_item("passages", 0)
            self.store_item("links", 0)
            self.store_item("unlinks", 0)
            self.store_item("doors", 0)
            self.store_item("max stack", 0)
            if self.__room_carver:
                self.store_item("rooms", 0)
                self.store_item("room links", 0)
            self.store_item("extra pumps", 0)
            self.store_item("watershed errors", 0)
            reservoir = self.__Reservoir(self.maze)
            self.__stack.append(reservoir)

        def push(self, subgrid):
            """push data onto the stack"""
            if self.__debug:
                print("PUSH:", subgrid)
            self.__stack.append(subgrid)
            if len(self.__stack) > self.fetch_item("max stack"):
                self.store_item("max stack", len(self.__stack))

        def pop(self):
            """push data onto the stack"""
            result = self.__stack.pop()
            if self.__debug:
                print("POP:", result)
            return result

        def top(self):
            """push data onto the stack"""
            return self.__stack[-1]

        @property
        def extra_pumps_trace(self) -> list:
            """returns the extra pumps trace, if any"""
            return self.__eptracer

        @property
        def more(self):                 # changed: 1 Sep 2025
            """returns True if there are stack entries

            Overrides Algorithm.more.
            """
            if len(self.__stack) > 0:
                return True

                # this check was added
            if self.fetch_item("watershed errors") > 0:
                if self.__error_action == 'fix':
                    status = Kruskal.on(self.__maze)
                    if self.__debug:
                        print(status)
                    self['action'] = 'fixed, Kruskal'
                    self['missing floodgates'] = status['components (init)'] - 1
                    self['components'] = status.components
                    self['passages in fix'] = status['passages']
                else:
                    self['action'] = 'errors ignored'

            return False

        def visit(self):
            """a single pass -- wrapper for _visit"""
            self.divide()

# end module mazes.Algorithms.watershed_division
