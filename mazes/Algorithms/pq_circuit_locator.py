"""
mazes.Algorithms.pq_circuit_locator - a best-first search maze circuit locator
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module is a wrapper for module qs_circuit_locator.  It uses a priority
    queue for searching.

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
from numbers import Real
from functools import lru_cache

import mazes
from mazes import Algorithm, rng
import mazes.Algorithms.qs_circuit_locator as QS
from mazes.Queues.priority_queue import PriorityQueue            

class QSPriority(object):
    """methods that determine the appropriate priority"""

    __slots__ = ("__map_pr", "__pr0", "__pr1", "__missed", "__misses")

    def __init__(self, priority:(callable, dict), cached=True,
                 missed:tuple=(rng.random, tuple(), dict())):
        """constructor

        REQUIRED ARGUMENTS

            priority - either a function which takes one or two arguments
                or a dictionary.  If a function is supplied, it must take
                the correct number of arguments:

                    *   one argument for either a vertex (cell) priority
                        or an edge (passage or join) priority
                    *   two arguments for an arc priority -- the cell
                        first, and then the passage

                For a dictionary. the key is either the cell (vertex-based),
                the join (edge-based), or a (cell, join)-ordered pair.

            cache (default: True) - missed priorities are cached if True

            missed (default: (random, (), {})) - a (pseudo-)random number generator 
        """
        if not callable(priority):
            if not isinstance(priority, dict):
                raise TypeError("the priority map must be a function or a dictionary")
        self.__map_pr = priority
        is_dict = isinstance(priority, dict)
        self.__pr0 = self.__dict_pr if is_dict else self.__map_pr
        self.__pr1 = self.cached_pr if cached else self.uncached_pr
        if not isinstance(missed, tuple):
            raise TypeError("'missed' must be an ordered triple (type)")
        if len(missed) != 3:
            raise ValueError("'missed' must be an ordered triple (length)")
        if not callable(missed[0]):
            raise TypeError("'missed[0]' must be random number generator")
        if not isinstance(missed[1], tuple):
            raise TypeError("'missed[1]' must be a list of arguments to the PRNG")
        if not isinstance(missed[2], dict):
            raise TypeError("'missed[2]' must be a keyword argument list for the PRNG")
        self.__missed = missed
        self.__misses = 0

    def __dict_pr(self, *args):
        """used to obtain a raw priority from the dictionary"""
        return self.__map_pr.get(args)

    def __missing(self):
        """generate a random priority"""
        f, args, kwargs = self.__missed
        self.__misses += 1
        return f(*args, **kwargs)

    @lru_cache()
    def cached_pr(self, *args):
        """cache the priority"""
        pr = self.__pr0(*args)
        if isinstance(pr, Real):
            return pr
        pr = self.__missing()
        if not isinstance(pr, Real):
            raise RuntimeError("random number generator error")
        return pr

    def uncached_pr(self, *args):
        """cache the priority"""
        pr = self.__pr0(*args)
        if isinstance(pr, Real):
            return pr
        pr = self.__missing()
        if not isinstance(pr, Real):
            raise RuntimeError("random number generator error")
        return pr

    def vertex_pr(self, packet:QS._QueueEntry):
        """vertex based priority"""
        cell = packet.cell
        return self.__pr1(cell)    

    def edge_pr(self, packet:QS._QueueEntry):
        """vertex based priority"""
        arc = packet.arc                # a join, typically bidirectional (i.e. edge)
        return self.__pr1(arc)    

    def arc_pr(self, packet:QS._QueueEntry):
        """vertex based priority"""
        cell = packet.cell              # determines the direction (away from cell)
        arc = packet.arc                # edge or arc
        return self.__pr1(cell, arc)

    @property
    def misses(self):
        """returns the number of missing priorities"""
        return self.__misses

class CircuitFinder(Algorithm):
    """a depth-first search circuit-locator algorithm

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

        __slots__ = ("__qs_priorities", "__prtype")

        NAME = "Priority Queue Circuit Locator"

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True,
                       pr:(callable, dict)=dict(), prtype:str="edge",
                       qtype:str="unstable", cached:bool=True, **kwargs):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)  The default is True.

                pr - a priority function or dictionary.

                prtype - one of "vertex", "edge", or "arc". If 'prtype' is
                    "arc", then the priorty takes two arguments, namely a
                    cell and a passage in that order.  The vertex and edge
                    priorities both take one argument, a cell or a passage,
                    respectively. (default: edge)

                qtype - one of "stable", "unstable" or "antistable".  This
                    determines how equal priorities are handled. (default:
                    unstable)

                cached - determines whether priorities are cached or calculated
                    anew each time.  If the priority map is complete and free
                    of side effects (i.e. a pure function), then caching is
                    unnecessary but might improve performance.  If the priority
                    map is incomplete or suffers from side effects, caching
                    guarantees a pure priority function.  There is a performance
                    tradeoff as caching requires additional space roughly
                    proportional to the number of distinct keys. (default: True)

                _prng - a random number generator function. (default: rng.random)

                _prng_args - arguments for the random number generator.
                    (default: ())

                _prng_kwargs - keyword arguments for the random number generator.
                    (default: {})
            """
            missed = (kwargs.get("_prng", rng.random),
                      kwargs.get("_prng_args", tuple()),
                      kwargs.get("_prng_kwargs", dict()))
            self.__qs_priorities = QSPriority(pr, cached=cached, missed=missed)
            self.__prtype = prtype
            wpr = self.prmap()
            qargs=tuple()
            qkwargs = {"priority":wpr, "action":"unstable", "cache":False}
            super().parse_args(start_cell=start_cell, shuffle=shuffle, \
                QueueType=PriorityQueue, qargs=qargs, qkwargs=qkwargs)

        def prmap(self):
            """returns the priority map function"""
            prtype = str(self.__prtype)
            prmapper = self.__qs_priorities
            if prtype == "vertex":
                return prmapper.vertex_pr
            if prtype == "edge":
                return prmapper.edge_pr
            if prtype == "arc":
                return prmapper.arc_pr
            raise NotImplementedError(f"{prtype=} is unknown")

        def __str__(self):
            """string representation"""
            prtype = str(self.__prtype)
            prmapper = self.__qs_priorities
            indent = ' ' * self.format("indent2")
            s = super().__str__()
            s += "\n" + indent + "%30s  %-10s" % ("priority type", prtype)
            s += "\n" + indent + "%30s  %7d" % ("unmapped priorities", prmapper.misses)
            return s

# end module mazes.Algorithms.pq_circuit_locator
