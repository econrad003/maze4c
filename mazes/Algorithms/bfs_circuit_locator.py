"""
mazes.Algorithms.bfs_circuit_locator - a breadth-first search maze circuit locator
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module is a wrapper for module qs_circuit_locator.

REFERENCES

    [1] "Cycle (graph theory)" in Wikipedia. 13 Nov 2025. Web
        Accessed: 17 Nov 2025.
            URL: https://en.wikipedia.org/wiki/Cycle_(graph_theory) 

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
from mazes import Algorithm
import mazes.Algorithms.qs_circuit_locator as QS
from mazes.Queues.queue import Queue

class CircuitFinder(Algorithm):
    """a breadth-first search circuit-locator algorithm

    USAGE

        The status must be queried to determine the result:

            status = CircuitFinder,on(maze)
            print(status)
            if status.result:
                cell, join, nbr = status.result
                print("cell in circuit:", cell)
                print("the edge or arc in the circuit", join)
                print("the other endpoint:", nbr)
            else:
                print("No circuits")

        If you want to break the circuit:
            maze.unlink(join)

        There is not generally enough information in the queue to reconstruct
        the circuit.
    """

    class Status(QS.CircuitFinder.Status):
        """the bulk of the work is in the parent"""

        NAME = "BFS Circuit Locator"

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)  The default is True.
            """
            super().parse_args(start_cell=start_cell, shuffle=shuffle, \
                QueueType=Queue, qargs=tuple(), qkwargs=dict())     # chain to parent

# end module mazes.Algorithms.bfs_circuit_locator
