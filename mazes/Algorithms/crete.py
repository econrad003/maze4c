"""
mazes.Algorithms.crete - a depth-first forest maze carving algorithm
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a variation on the depth-first forest algorithm.  It starts
    with a cross (called a gammadion) and proceeds.  The mazes that
    result are somewhat reminiscent of unicursal Cretan (or Trojan)
    mazes, but only somewhat.

    The gammadion algorithm that is supplied here assumes a Von Neumann
    rectangular grid with at least six rows and six columns.

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
from mazes import rng, Cell
from mazes.maze import Maze
from mazes.round_robin import RoundRobin
from mazes.Algorithms.dff import DFF

def gammadion_Von_Neumann(maze:Maze, **kwargs) -> tuple:
    """carve a gammadion on an ordinary rectangular grid

    DESCRIPTION

        This routine carves the gammadion and hides its cells.  It
        assumes a Von Neumann (i.e. NSEW) rectangular grid with a
        minimum of six rows and six columns.

    RETURNS

        An ordered triple consisting of (1) a list of cells in the
        gammadion, (2) a list of cells to be used as seeds by the
        depth-first-forest (DFF) passage carver, and (3) the number
        of passages carved.  The cells in the first list are hidden
        from DFF and revealed after DFF is complete.

        The number of this particular gammadion has eight passages 
    """
    from mazes.Grids.oblong import OblongGrid

    cells = list()
    queue = list()
    result = [cells, queue, 0]

    def update(cell1, cell2, cell3):
        """build the gammadion"""
        cells.append(cell1)             # a corner
        queue.append(cell2)             # its first free neighbor
        maze.link(cell1, cell2)
        queue.append(cell3)             # its second free neighbor
        maze.link(cell1, cell3)
        cell1.hide()
        result[2] += 2                  # two more passages

    grid = maze.grid
    if not isinstance(grid, OblongGrid):
        raise TypeError("gammadion_Von_Neumann: OblongGrid is required")
    if grid.m < 6 or grid.n < 6:
        raise ValueError("gammadion_Von_Neumann: 6x6 or larger is required")
    n = rng.randrange((grid.m-6) * (grid.n-6))
    i = n // (grid.n-6) + 2
    j = n % (grid.n-6) + 2
    cell = grid[i,j]                   # SW cell of the cross
    update(cell, cell.west, cell.south)
    cell = grid[i,j+1]                 # SE cell of the cross
    update(cell, cell.south, cell.east)
    cell = grid[i+1,j+1]               # NE cell of the cross
    update(cell, cell.east, cell.north)
    cell = grid[i+1,j]                 # NW cell of the cross
    update(cell, cell.north, cell.west)
    return tuple(result)

def reveal(cells:set):
    """take cells out of hiding"""
    for cell in cells:
        cell.reveal()

class Crete(DFF):
    """an algorithm for producing mazes reminiscent of Cretan labyrinths"""

    class Status(DFF.Status):
        """the workhorse"""

        NAME = "Cretan/DFF algorithm"

        __slots__ = ("__gammadion", )

        def parse_args(self, *tasks, seeds:tuple=(), shuffle:bool=True,
                       gammadion:callable=gammadion_Von_Neumann,
                       gkwargs:dict=dict(),
                       weights:list=None,
                       Scheduler:callable=RoundRobin,
                       label:bool=False):
            """parse arguments

            REQUIRED ARGUMENTS

                maze - a maze object

            OPTIONAL ARGUMENTS

                gammadion - a function or method which carves a starting
                    pattern in the maze.  It takes a maze as its required
                    argument and may take additional optional arguments
                    (supplied by gkwargs).

                    The default is the function gammadion_Von_Neumann
                    which takes a maze as its only argument.  (Arguments
                    supplied in gkwargs are accepted but ignored.)
                    This function requires a rectangular grid with at
                    least six rows and six columns.  The gammadion is
                    carved in a random part of the grid.

                    User-degined gammadion methods should return two
                    lists.  The first is a list of cells that are hidden
                    from the DFF carver.  (These cells and their
                    incident passages form the gammadion.)  After DFF is
                    complete, these cells will be unmasked using the
                    Cell.reveal method.

                    The second list returned by the gammadion method
                    are the cells to be used as seeds for DFF.  The
                    default method returns the cells that are incident
                    to passages that lead outward from the default
                    gammadion.

                gkwargs - a dictionary (empty by default) which supplies
                    optional arguments to the gammadion carver.
            """
                ### carve the gammadion
            self.__gammadion = gammadion(maze, **gkwargs)
            assert len(self.__gammadion) == 3
            cells, queue, passages = self.__gammadion
            tasks = len(queue)
            self["gammadion"] = len(cells)
            self["passages (gammadion)"] = passages
            super().parse_args(tasks, seeds=queue, shuffle=shuffle, \
                weights=weights, Scheduler=Scheduler, label=label)

        @property
        def gammadion(self) -> set:
            """returns the gammadion cells"""
            return set(self.__gammadion[0])

        @property
        def seed_cells(self) -> set:
            """returns the seed cells"""
            return set(self.__gammadion[1])

        @property
        def gammadion_passages(self) -> int:
            """returns the number gammadion passages"""
            return self.__gammadion[2]

        @property
        def more(self):
            """returns True if the stack is empty

            The gammadion cells are unmasked here.
            """
            result = super().more
            if not result:
                reveal(self.gammadion)
                self["passages"] += self.gammadion_passages
            return result

# END mazes.Algorithms.crete.py
