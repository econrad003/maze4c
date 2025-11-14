"""
mazes.tools.dead_ends - dead end management tools
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Dead ends in a maze (graph, network) are the cells (vertices, nodes)
    which have exactly one neighbor, i.e. the degree 1 cells.  This module
    provides methods which collect and sample the dead ends, and methods
    which can be used to eliminate them.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

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

"""
import mazes
from mazes import rng

class DeadEnds(object):
    """managing the dead ends in a maze"""

    __slots__ = ("__maze", "__dead_ends", "__sampled")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, maze:'Maze', *args, **kwargs):
        """constructor

        DESCRIPTION

            Don't override this constructor.  Instead, override _parse_args,
            _initialize, or _configure.

        REQUIRED ARGUMENTS

            maze - a maze object

                Results are not guaranteed for mazes which contain one-way
                passages (arcs).
        """
        self.__maze = maze
        self._parse_args(*args, **kwargs)       # parse remaining arguments
        self._initialize()
        self.configure()

    def _parse_args(self):
        """argument parser for Cell class (stub)

        A TypeError exception is raised if there are any unprocessed arguments.
        """
        pass

    def _initialize(self):
        """initialization (stub)"""
        pass

    def _configure(self):
        """first time configuration

        if this is overridden, make sure that method configure() (no undercsore)
        is called.
        """
        self.configure()        # gets the dead ends

    def configure(self, quiet:bool=True):
        """configuration

        Determines which cells are dead ends...  This may be called as needed
        to refresh the dead end set.  The sampled flag is reset by this method
        """
        dead_ends = set()
        for cell in self.grid:
            if len(list(cell.passages)) == 1:
                dead_ends.add(cell)
        self.__sampled = False
        self.dead_ends = dead_ends
        if not quiet:
            print(f"method {self.__class__.__name__}.configure:",
                  f"{len(self)} dead ends")

            # PROPERTIES AND SETTERS

    @property
    def dead_ends(self) -> set:
        """returns the dead ends set"""
        return self.__dead_ends

    @dead_ends.setter
    def dead_ends(self, other:set):
        """reconfigures the dead ends set

        Does not modify the sampled flag.
        """
        self.__dead_ends = set(other)

    @property
    def maze(self):
        """returns the maze"""
        return self.__maze

    @property
    def grid(self):
        """return the underlying grid"""
        return self.__maze.grid

    @property
    def sampled(self) -> bool:
        """returns True if the dead end set is a sample and False otherwise"""
        return self.__sampled

            # DUNDER MAGIC METHODS

    def __len__(self):
        """returns the number of cells in the dead end set"""
        return len(self.dead_ends)

    def __iter__(self):
        """generator for the dead end set"""
        for cell in self.dead_ends:
            yield cell

        # DEAD ENDS SAMPLING

    def discard_on_head(self, bias:float=0.5, quiet:bool=False):
        """samples cells from the dead end set

        Sampling is done using a coin toss.  If a cell receives a head, then
        it is removed from the sample.

        The sampled flag is set to True by this method.

        OPTIONAL ARGUMENTS

            bias (default 0.5) - the expected proportion of heads in the coin
                toss.

            quiet (default False) - if False, displays a message indicating
                how many cells are in the sample
        """
        dead_ends = set()
        for cell in self.dead_ends:
            if rng.random() >= bias:
                dead_ends.add(cell)
        if not quiet:
            n = len(self)
            q = len(dead_ends)
            p = n - q
            print(f"method {self.__class__.__name__}.discard_on_head:",
                  f"{p} cells removed,",
                  f"{q} cells remain in the sample")
        self.__sampled = True
        self.dead_ends = dead_ends

    def sample(self, q:int, quiet:bool=False):
        """samples cells from the dead end set

        Sampling is done by extracting a specific number of cells.

        The sampled flag is set to True by this method.

        REQUIRED ARGUMENTS

            q - the number of dead ends to remain in the sample

        OPTIONAL ARGUMENTS

            quiet (default False) - if False, displays a message indicating
                how many cells are in the sample
        """
        dead_ends = set(rng.sample(list(self.dead_ends), q))
        if not quiet:
            n = len(self)
            p = n - q
            print(f"method {self.__class__.__name__}.sample:",
                  f"{p} cells removed,",
                  f"{q} cells remain in the sample")
        self.__sampled = True
        self.dead_ends = dead_ends

            # DEAD END REMOVAL

    def _make_action(self, action:str="all", q:int=0,
                     bias:float=0.5, quiet:bool=False):
        """parse the preparatory action

        sets the sampled flag to True
        """
        action = action[0].lower()
        if action == 'a':
            self.configure(quiet=quiet)
        elif action in {'f', 't'}:
            self.configure()
            self.discard_on_head(bias=bias, quiet=quiet)
        elif action == 's':
            self.configure()
            self.sample(q if q else round(len(self)/2), quiet=quiet)
        elif action in {'c', 'u'}:
            if not quiet:
                print("User sample:", f"{len(self)} cells")
        else:
            raise ValueError("undefined action")
        self.__sampled = True

    def _get_neighbors(self, cell:'Cell') -> "two sets or nothing":
        """get neighbor sets"""
        if cell not in self.dead_ends:
            return
        if len(list(cell.passages)) != 1:
            print("ERROR:",
                  f"Cell[{cell.index}] is not a dead end.",
                  "(ignored)")
            return
        nbrs = set()
        dead_nbrs = set()
        for nbr in cell.neighbors:
            if not cell.is_linked(nbr):
                nbrs.add(nbr)
                if len(list(nbr.passages)) == 1:
                    dead_nbrs.add(nbr)
        if len(nbrs) < 1:
            print("WARNING:",
                  f"Dead End Cell[{cell.index}] has no unlinked neighbors.",
                  "(ignored)")
            return None
        return nbrs, dead_nbrs

    def remove_by_linking(self, action:str="all", q:int=0,
                          bias:float=0.5, quiet:bool=False):
        """remove dead ends

        Remove some or all of the dead ends by linking them with a random
        neighbor.

        OPTIONAL ARGUMENTS

            action (default: all) - which dead ends will be removed?

                Possible values are:

                    all - all the dead ends in the maze (except any with
                        just one grid connection)

                    flip, toss - extract a sample using a series of coin
                       tosses (option: bias)

                    sample - extract a fixed size sample (option: n)

                    use_me, custom - use whatever cells happen to be in the
                        set 'dead_end'

                Only the first letter ('a', 'f', 't', 's', 'c' or 'u') is
                significant.

            q - (default: half the sample) number to sample.

            bias - proportion of heads (discards).

            quiet (default: False) if False, displays status messages.
        """
        links = 0
        self._make_action(action, q, bias, quiet)
        cells = list(self.dead_ends)
        rng.shuffle(cells)
        v0 = len(self)
        for cell in cells:
            result = self._get_neighbors(cell)
            if not result:
                continue
            nbrs = list(result[0])
            nbr = rng.choice(nbrs)
            self.maze.link(cell, nbr)
            links += 1
            self.dead_ends -= {cell, nbr}
        v1 = len(self)
        if not quiet:
            print(f"method {self.__class__.__name__}.remove_by_linking",
                  f"before: {v0} samples,",
                  f"new passages: {links},",
                  f"after: {v1} samples")

    def link_pairs(self, action:str="all", q:int=0,
                   bias:float=0.5, quiet:bool=False):
        """remove dead ends by linking them in pairs

        Remove some or all of the dead ends by linking them in pairs.

        OPTIONAL ARGUMENTS

            action (default: all) - which dead ends will be removed?

                Possible values are:

                    all - all the dead ends in the maze (except any with
                        just one grid connection)

                    flip, toss - extract a sample using a series of coin
                       tosses (option: bias)

                    sample - extract a fixed size sample (option: n)

                    use_me, custom - use whatever cells happen to be in the
                        set 'dead_end'

                Only the first letter ('a', 'f', 't', 's', 'c' or 'u') is
                significant.

            q - (default: half the sample) number to sample.

            bias - proportion of heads (discards).

            quiet (default: False) if False, displays status messages.
        """
        links = 0
        self._make_action(action, q, bias, quiet)
        cells = list(self.dead_ends)
        rng.shuffle(cells)
        v0 = len(self)
        for cell in cells:
            result = self._get_neighbors(cell)
            if not result:
                continue
            nbrs = list(result[1])
            if len(nbrs) == 0:
                continue            # no neighbors are dead ends
            nbr = rng.choice(nbrs)
            self.maze.link(cell, nbr)
            links += 1
            self.dead_ends -= {cell, nbr}
        v1 = len(self)
        if not quiet:
            print(f"method {self.__class__.__name__}.link_pairs",
                  f"before: {v0} samples,",
                  f"new passages: {links},",
                  f"after: {v1} samples")

# end module mazes.tools.dead_ends
