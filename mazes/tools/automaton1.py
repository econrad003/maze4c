"""
mazes.tools.automataton1 - a simple cellular automaton for an oblong grid
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Our automaton assumes a Von Neuman neighborhood and uses two rules:

        Rule B: A dead cell is born if it has 1, 2 or 3 live neighbors.

        Rule D: A live cell dies if it has 0 or 4 live neighbors.

    Note that cells along the perimeter can be born but cannot die.

    Also note that we could simplify the rule set by simply saying that a cell
    will live if and only if it has 1, 2 or 3 live neighbors.  To allow play
    with other systems of neighborhoods, we won't make this simplification.

    Our program interprets these rules very literally.  If given a grid
    containing a live cell with five live neighbors, that cell will remain
    alive since 5 is not in {0, 4}.

    Changes of state happen synchronously.

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

from mazes import rng
from mazes.Grids.oblong import OblongGrid

def new_automaton(rows, cols, born=5) -> tuple:
    """create the automaton using an OblongGrid instance"""
    grid = OblongGrid(rows, cols)
    live_cells = set(rng.sample(list(grid), k=born))
        # label the initial live cells
    for cell in live_cells:
        cell.label = 1
    return grid, live_cells

def next_generation(grid, live_before) -> set:
    """apply the rules"""
    live_after = set()
    for cell in grid:
        live_nbrs = 0
        for nbr in cell.neighbors:
            if nbr in live_before:
                live_nbrs += 1
        if cell in live_before:
                    # rule D
            if live_nbrs not in {0, 4}:
                live_after.add(cell)
        else:
            if live_nbrs in {1, 2, 3}:
                live_after.add(cell)
    return live_after

def relabel(alive):
    """label the end state

    Under the relabelling, we have:
        1 - born in the initial state, now dead
        2 - dead initially, now alive
        3 - born in the initial state, now alive
    """
    for cell in alive:
        cell.label = 3 if cell.label == 1 else 2

def simulate(rows, cols, born_at_start=5, generations=10) -> tuple:
    """run a simulation using an OblongGrid instance"""
    grid, live_cells = new_automaton(rows, cols, born=born_at_start)
    for _ in range(generations):
        live_cells = next_generation(grid, live_cells)
    relabel(live_cells)
    return grid, live_cells

# end module mazes.tools.automaton1