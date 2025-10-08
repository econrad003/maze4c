"""
mazes.Algorithms.mt_random_walk - the first entrance random multi-thread random walk algorithm
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of a first entrance random walk maze carver
    with multiple threads,  It is a generalization of the Aldous/Broder
    first entrance random walk algorithm.  With a single thread, the
    algorithm reduces to Aldous/Broder. The underlying algorithm is
    as follows:

        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;
            the starting cell is now the current cell.

        Loop until every cell has been visited:
            choose a random neighbor of the current cell;
            if this neighbor has not been visited:
                (this is a first entrance!)
                remove the neighbor from the unvisited set
                carve a passage from the current cell to the neighbor;
            now the neighbor is the current cell.

    For the multi-threaded version, in addition to the overall visited
    set, for each thread, there is a "claimed set", the set of cells
    claimed by that thread.

        Preparation:
            get a list of cells to be visited.
            for each thread:
                choose a starting cell and remove it from the unvisited set;
                add it to the thread's claimed set;
                it is now the current cell for the thread.

        Loop until all cells are visited and all but one thread have closed:
            choose a thread (called thread A) to be active;
            choose a random neighbor of the current cell;
            if this neighbor has been claimed by another thread (called thread I):
                carve a passage from the current cell to the neighbor;
                add all cells claimed by thread A to the claimed set for I;
                thread A's claimed set is now empty;
                if all cells have been visited:
                    close thread A
                else:
                    choose a starting cell and remove it from the unvisited set;
                    add it to thread A's claimed set;
                    it is now the current cell for thread A;
            else:
                (this neighbor is either claimed by thread A or unclaimed)
                if this neighbor has not been visited:
                    (this is a first entrance!)
                    remove the neighbor from the unvisited set
                    carve a passage from the current cell to the neighbor;
                    add the neighbor to thread A's claimed set
                now the neighbor is the current cell

    As with Aldous/Broder, there is an assumption here.  With a bad random
    sequence, the algorithm will never finish.

    For all but one thread to close, it is necessary that the grid be
    connected.

QUESTIONS

    I doubt that the algorithm produces uniform spanning trees except in
    trivial case (with 1 thread).  But I don't have a proof, and I don't
    have any suspicions about the biases.  So the questions are:

        1) Is the algorithm unbiased?

        2) If the algorithm is biased, then is there a characterization
           of the bias?

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 55-60, 249.  (For Aldous/Broder.)

    I haven't seen this particular spanning tree algorithm described
    elsewhere.  If someone has a reference, or even a reference to a
    another threaded first-entrance random walk algorithm, please share.

    You can post a reference as an issue on github at
        https://github.com/econrad003/maze4c

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
from mazes import rng, Cell, Algorithm
from mazes.tournament import Tournament

class MTRandomWalk(Algorithm):
    """the first entrance random walk maze carving algorithm"""

    class Thread(object):
        """keeps track of a particular thread"""

        __slots__ = ("__claimed", "__open", "__cells", "__current")

        def __init__(self, start_cell:Cell, cells:dict):
            """constructor

            The dictionary "cells" is shared by all the threads.
            See method claimed for more information.
            """
            # print("Thread", id(self), "starting at", start_cell.index)
            self.__open = True
            self.__cells = cells            # shared
            self.__claimed = set()
            self.claim(start_cell)
            self.__current = start_cell

        @property
        def is_open(self) -> bool:
            """returns True if the thread is open"""
            return self.__open

        @property
        def claimed(self) -> set:
            """returns the thread's set of claimed cells"""
            return self.__claimed

        @property
        def current(self) -> Cell:
            """returns the current cell

            A ValueError exception is raised if the thread is not open.
            """
            if self.__open:
                return self.__current
            raise ValueError("A closed thread has no current cell.")

        @current.setter
        def current(self, cell:Cell):
            """set the current cell

            A ValueError exception is raised if the thread is not open.
            """
            if not self.__open:
                raise ValueError("Cannot set current cell for a closed thread.")
            self.__current = cell

        def close(self, other:"Thread"):
            """closes a thread

            The thread's current claims are passed to the 'other' thread's
            claims.
            """
            # print("Thread", id(self), "closed to", id(other))
            for cell in self.__claimed:
                other.claim(cell)
            self.__claimed = set()
            self.__open = False

        def restart(self, other:"Thread", start_cell:Cell):
            """restarts the thread by claiming the start cell

            The thread's current claims are passed to the 'other' thread's
            claims.
            """
            # print("Thread", id(self), "closing to", id(other), "...")
            # print("        ", "restarting at", start_cell.index)
            for cell in self.__claimed:
                other.claim(cell)
            self.__claimed = set()
            self.claim(start_cell)
            self.__current = start_cell

        def claim(self, cell:Cell):
            """claim a cell for the thread

            The cell is marked here as claimed by entering the claiming
            thread's id in the "cells" dictionary.

            A closed thread cannot claim cells -- a ValueError exception
            is raised in this case.
            """
            if not self.__open:
                raise ValueError("A closed thread cannot claim cells.")
            self.__cells[cell] = self
            self.__claimed.add(cell)
            # print("Thread", id(self), "claiming", cell.index)

        def claimed_by(self, cell:Cell) -> "ID | None":
            """determine who if anyone owns a cell"""
            if not self.__open:
                raise ValueError("A closed thread cannot verify claims.")
            return self.__cells.get(cell)

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Multi-Threaded First Entrance Random Walk"

        __slots__ = ("__unvisited", "__threads", "__scheduler", "__cells",
                     "__task_iter")

        def parse_args(self, n, scheduler:Tournament=None,
                       task_args:list=None, task_kwargs:list=None):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

                n - the number of threads

            KEYWORD ARGUMENTS

                scheduler - the scheduler (default: Tournament()).

                task_args - additional positional arguments to be
                    passed to the scheduler's add_task method.   If
                    this is not set to None (default), there must be
                    n tuples in the list, one tuple per thread.

                task_kwargs - additional keyword arguments to be
                    passed to the scheduler's add_task method.   If
                    this is not set to None (default), there must be
                    n dictionaries in the list.
            """
            super().parse_args()                # chain to parent
            self.__threads = (n, task_args, task_kwargs)    # pack!
            if scheduler == None:
                scheduler = Tournament()
            if len(scheduler) != 0:
                print(f"{len(scheduler)=}")
                raise ValueError("scheduler must be empty")
            self.__scheduler = scheduler
            self.__cells = dict()

        @property
        def Thread(self) -> "Thread":
            """returns the thread class"""
            return MTRandomWalk.Thread

        def create_threads(self):
            n, targs, tkwargs = self.__threads      # unpack
            self.store_item("threads", n)
            self.store_item("runners", 0)
            if type(n) == int:
                if n < 1:
                    raise ValueError("Parameter n must be at least 1.")
            else:
                raise TypeError("Parameter n must be a positive integer")

            self.__threads = list()
            unvisited = list(self.__unvisited)
            rng.shuffle(unvisited)
            i = 0
                    # PREPARATION
            while unvisited and i < n:
                args = targs[i] if targs else tuple()
                kwargs = tkwargs[i] if tkwargs else dict()
                        # get starting cell
                start_cell = unvisited.pop()
                        # remove it from the unvisited set
                self.__unvisited.remove(start_cell)
                        # claim it for the thread and make it current
                thread = self.Thread(start_cell, self.__cells)
                self.__scheduler.add_task(thread, *args, **kwargs)
                self.increment_item("runners")
                i += 1

        def initialize(self):
            """initialization"""
            self.__unvisited = set(self.maze.grid)

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.__unvisited))
            self.store_item("passages", 0)
            self.create_threads()
            self.__task_iter = iter(self.__scheduler)

        @property
        def more(self):
            """returns True if there are unvisited cells

            Overrides Algorithm.more.
            """
            return len(self.__unvisited) > 0 or len(self.__scheduler) > 1

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def visit(self):
            """a single pass"""
            thread = next(self.__task_iter)
            if thread == None:
                raise RuntimeError("The scheduler returned None.")
            if not thread.is_open:
                raise RuntimeError("The scheduler returned a closed thread")

            cell = thread.current
            nbr = rng.choice(list(cell.neighbors))
            thread2 = thread.claimed_by(nbr)
            if thread2 == None:
                    # the neighbor is unclaimed
                self.__unvisited.remove(nbr)
                self.link(cell, nbr)
                thread.claim(nbr)
                thread.current = nbr
            elif thread2 == thread:
                    # the neighbor belongs to the active thread
                thread.current = nbr
            else:
                    # the neighbor belongs to another thread
                self.link(cell, nbr)
                if len(self.__unvisited) == 0:
                        # there are no more cells to claim
                    thread.close(thread2)
                    self.__scheduler.remove_task(thread)
                else:
                        # there are more unclaimed cells
                    start_cell = rng.choice(list(self.__unvisited))
                    self.__unvisited.remove(start_cell)
                    thread.restart(thread2, start_cell)
                    self.increment_item("runners")

# end module mazes.Algorithms.mt_random_walk
