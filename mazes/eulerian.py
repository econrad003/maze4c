"""
mazes.eulerian - tools for verifying Eulerian mazes
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module defines two exceptions:

        DisconnectedMaze

        NonEulerian

    This module provides three methods:

        is_eulerian:

            * raises a DisconnectedMaze exception if the maze is
              disconnected;

            * returns True if the maze is Eulerian;

            * returns False otherwise.

        is_path_eulerian:

            * raises a DisconnectedMaze exception if the maze is
              disconnected;

            * returns the two odd vertices if the maze is path-Eulerian;

            * returns False otherwise.

        not_maximally_eulerian:

            * raises a DisconnectedMaze exception if the maze is
              disconnected;

            * raises a NonEulerian exception if the maze is not Eulerian;

            * returns a set of unused edges that can be added to produce
              a larger Eulerian maze;

            * returns None if the the maze is maximally Eulerian.

DEFINITIONS

    A graph G=(V,E) is Eulerian if and only if there is a closed walk in
    the graph in which every edge occurs exactly once.  Any such closed
    walk is called an Eulerian cycle (or an Eulerian circuit).

    A graph G=(V,E) is path-Eulerian if and only if there is an open walk
    in the graph in which every edge occurs exactly once.  Any such open
    walk is called an Eulerian trail (or an Eulerian path).

    The graph does not need to be simple -- it may contain loops and
    parallel edges.  The only difference between the two is that an Eulerian
    cycle is closed, i.e. the source and the sink vertex are one and the
    same, while an Eulerian trail is open, i.e., the source and the sink are
    distinct vertices.

THEOREM (EULER-HIERHOLZER)

    A) A graph is Eulerian if and only if:
            a) it is connected; and
            b) every vertex is of even degree.

    B) A graph is path-Eulerian if and only if:
            a) it is connected; and
            b) it has exactly two vertices of odd degree.
       Moreover, every Eulerian trail starts in one odd vertex and ends in
       the other.

REMARKS

    The results (in a different but equivalent form) were conjectured by
    Euler.  Euler that every vertex in an Eulerian graph is of even degree.
    He also showed that (B) follows almost immediately from (A).

    The proof was completed by Hierholzer (who showed that every connected
    graphs whose vertices are all even is an Eulerian graph) and published
    posthumously.

    Note than in determining the degree of a vertex, loops (edges that are
    incident to exactly one vertex) must be counted twice in the degree of
    the vertex.

EXAMPLE

            1 --- 2 --- 3       There are two edges between 4 and 5.
            |           |       The vertices are all even:
            4 === 5 --- 6           degree 2: 1, 2, 3, 6, 7, 8
            |     |                 degree 4: 4, 5
            7 --- 8             Eulerian circuit:
                                                           T  B
                                    1--2--3--6--5--8--7--4--5--4--1

                                For the parallel edges
                                    T=top edge, B=bottom edge

    Note that we adding loops does not change the property.  Any time we
    encounter vertex with a loop, we may follow the loop before proceeding
    along an edge to another vertex.

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
from collections import defaultdict

from mazes import rng
from mazes.grid import Grid
from mazes.maze import Maze

        #################### EXCEPTIONS #################

class DisconnectedMaze(Exception):
    """disconnected maze exception"""
    pass

class NonEulerian(Exception):
    """non-Eulerian maze exception"""
    pass

        ##################### SUPPORT ########################################
        # These are usable, though not mentioned above i the documentation   #
        # They are intended mainly for use by the functions that are         #
        # mentioned above.                                                   #
        ######################################################################

class Statistics(object):
    """a namespace for collecting data about the various methods"""

    def __init__(self):
        """initialize the data to a pristine state"""
        self.max_stack = 0
        self.grid_size = 0
        self.cells_reached = 0

    def __str__(self):
        """statistics"""
        s = "Statistics"
        stat = "\n\t%30s\t%10d"
        s += stat % ("maximum stack", self.max_stack)
        s += stat % ("cells", self.grid_size)
        s += stat % ("reached", self.cells_reached)
        return s

connectivity = Statistics()         # connectivity statistics

def is_connected(maze:Maze) -> bool:
    """returns True if the Maze is connected and False otherwise"""
    stack = list()

    not_reached = list(maze.grid)
    connectivity.grid_size = len(not_reached)

    start = rng.choice(not_reached)
    reached = set(not_reached)
    stack.append(start)
    not_reached.remove(start)
    connectivity.max_stack = 1
    connectivity.cells_reached = 1

    while stack:
        cell = stack.pop()
        for nbr in cell.passages:
            if nbr not in not_reached:
                continue
            stack.append(nbr)
            not_reached.remove(nbr)
            connectivity.cells_reached += 1
        connectivity.max_stack = max(len(stack), connectivity.max_stack)

    return len(not_reached) == 0

        ################# STANDARD FUNCTIONS ###############

def is_Eulerian(maze:Maze, check_connectivity=True) -> bool:
    """checks whether the maze is Eulerian

    If check_connectivity is False, the connectivity check is skipped.
    Otherwise a DisconnectedMaze exception is raised if the maze is
    not connected.

    If connectivity is not checked, only the vertex degrees are checked.
    If a maze has a single vertex, then it is automatically Eulerian.

    If it has more than one vertex, then we check that each vertex
    has even positive degree.  (This insures that if the graph has
    isolated vertices, it will fail the test when the connectivity
    check is bypassed.  Note that if the connectivity check is bypassed,
    the vertex degree check is a necessary but not a sufficient condition.)

    In computing the degree of a vertex, we omit loops as they do not
    affect parity, but a vertex with loops can be isolated.
    """
    if len(maze.grid) == 1:
        return True         # trivially Eulerian

    if check_connectivity:
        if not is_connected(maze):
            raise DisconnectedMaze("The maze is disconnected")

    for cell in maze.grid:
        degree = 0
        for join in cell.joins:
            if cell.cell_for(join) == cell:
                continue            # ignore loops (normally counted twice)
            degree += 1
        if degree % 2 == 1 or degree == 0:
            return False

    return True     # if connectivity was checked, this is sufficient

def is_path_Eulerian(maze:Maze, check_connectivity=True) -> (list, bool):
    """checks whether the maze is path-Eulerian

    If check_connectivity is False, the connectivity check is skipped.
    Otherwise a DisconnectedMaze exception is raised if the maze is
    not connected.

    If connectivity is not checked, only the vertex degrees are checked.
    If a maze has a single vertex, then it is automatically Eulerian
    and not path-Eulerian.

    If it has more than one vertex, then we check that each vertex
    has even positive degree.  (This insures that if the graph has
    isolated vertices, it will fail the test when the connectivity
    check is bypassed.  Note that if the connectivity check is bypassed,
    the vertex degree check is a necessary but not a sufficient condition.)

    In computing the degree of a vertex, we omit loops as they do not
    affect parity, but a vertex with loops can be isolated.

    If the graph is path-Eulerian, then a list containing the two odd cells
    is returned.
    """
    if len(maze.grid) == 1:
        return False         # trivially Eulerian, not path-Eulerian

    if check_connectivity:
        if not is_connected(maze):
            raise DisconnectedMaze("The maze is disconnected")

    odds = list()
    for cell in maze.grid:
        degree = 0
        for join in cell.joins:
            if cell.cell_for(join) == cell:
                continue            # ignore loops (normally counted twice)
            degree += 1
        if degree == 0:
            return False            # isolate (possibly with some loops)
        if degree % 2 == 1:
            odds.append(cell)
            if len(odds) > 2:
                return False        # too many odd vertices

    if len(odds) != 2:
        return False                # necessary if connectivity checked
    return odds                     # sufficient if connectivity checked

maximality = Statistics()

def not_maximally_Eulerian(maze:Maze, check_connectivity=True,
                           check_Eulerian=True,
                           check_path_Eulerian=False,
                           shuffle=False) -> (type(None), list):
    """checks whether the graph is maximally Eulerian in the grid

    DESCRIPTION

        To be maximally Eulerian:

            a) it must be connected;
            b) it must be Eulerian;
            c) there is no circuit in the grid consisting entirely of
               unused grid edges.

        Condition (c) is checked using depth-first search.

    RETURN VALUE

        The cells in a missing circuit, if the maze is not maximal; or None
        if no such circuit was found.
    """
    if check_Eulerian:
        if check_path_Eulerian:
            if not is_path_Eulerian(maze, check_connectivity=check_connectivity):
                raise NonEulerian("The maze is not path-Eulerian")
        else:
            if not is_Eulerian(maze, check_connectivity=check_connectivity):
                raise NonEulerian("The maze is not Eulerian")
    elif check_connectivity:
        if not is_connected(maze):
            raise DisconnectedMaze("The maze is disconnected")

            ### CHECK FOR condition (c)
    grid = maze.grid
                # the complementary maze
    complement = defaultdict(list)
    for cell in grid:
        for nbr in cell.neighbors:
            if not cell.is_linked(nbr):
                complement[cell].append(nbr)

                # DFS setup
    unvisited = list(complement.keys())
    if shuffle:
        for cell in unvisited:
            rng.shuffle(complement[cell])
    maximality.grid_size = len(unvisited)
    stack = list()
    maximality.max_stack = 1                        # will be added momentarily
    maximality.cells_reached = 0
                # DFS implementation
    while unvisited:
        cell = rng.choice(unvisited)
        packet = (None, cell)
        stack.append(packet)                        # random starting point
        unvisited = set(unvisited)
        visited = set()
        while stack:
            prev, cell = stack[-1]
            if cell in visited:
                stack.pop()
                continue
            visited.add(cell)
            unvisited.remove(cell)
            maximality.cells_reached += 1
            added = False
            for nbr in complement[cell]:
                if nbr == prev:
                    continue
                if nbr not in visited:
                    packet = (cell, nbr)
                    stack.append(packet)
                    added = True
                    continue
                circuit = [nbr, cell]
                curr = prev
                stack.pop()
                while True:
                    prev, cell = stack.pop()
                    if cell == curr:
                        circuit.append(cell)
                        if cell == nbr:
                            return circuit
                        curr = prev
            if added:
                maximality.max_stack = max(len(stack), maximality.max_stack)
            else:
                stack.pop()
        unvisited = list(unvisited)

    return None     # no circuit found

# END eulerian.py
