"""
mazes.Algorithms.dff - the depth-first forest maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of a parallel depth-first search maze carver.
    The underlying algorithm is depth-first search:

        Push the start cell on the stack and mark it as visited
        Loop until the stack is empty:
            Consider the cell at the top of the stack;
            if the cell has an unvisited neighbor:
                carve a passage from the cell to the neighbor;
                mark the neighbor as visited
                push the neighbor onto the stack;
            otherwise:
                pop the cell from the stack

    But we have several search tasks running at the same time, so occasionally
    a cell will encounter a neighbor which has been visited but is not in
    the same component.  We can use an algorithm like Kruskal's algorithm to
    connect the components at the end.

    This is my implementation of an algorithm that Jamis Buck calls
    recursive backtracking with parallel seeds.  (see reference [2].)

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] Jamis Buck. "Maze Algorithms".  Web.  Accessed 28 September 2025.
            https://www.jamisbuck.org/mazes/

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
from mazes.Queues.stack import Stack

class Task(object):
    """keeps track of the queue associated with a single seed"""

    __slots__ = ("__taskID", "__q", "__maxlen", "__pushes", "__pops")

    def __init__(self, taskID:int, *args, QueueType:callable=Stack, **kwargs):
        """constructor"""
        self.__taskID = taskID
        self.__q = QueueType(*args, **kwargs)
        self.__maxlen = self.__pushes = self.__pops = 0

    @property
    def taskID(self):
        """returns the current task ID"""
        return self.__taskID

    @taskID.setter
    def taskID(self, taskID):
        """sets the current task ID"""
        self.__taskID = taskID

                # STACK OR QUEUE OPERATIONS

    def push(self, cell):
        """push the data onto the stack"""
        self.__q.enter(cell)
        if len(self.__q) > self.__maxlen:
            self.__maxlen += 1
        self.__pushes += 1

    def top(self):
        """return the top of the stack"""
        return self.__q.top()

    def jettison(self):
        """jettison the top of the stack"""
        self.__pops += 1
        self.__q.jettison()

    @property
    def isempty(self) -> bool:
        """condition for termination"""
        return self.__q.is_empty

    @property
    def stats(self) -> tuple:
        """returns counts of pushes and pops, and maximum stack length"""
        return self.__pushes, self.__pops, self.__maxlen

class DFF(Algorithm):
    """the depth-first forest maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Depth-first Forest (DFF)"

        __slots__ = ("__visited", "__visit", "__tasks", "__scheduler",
                     "__edges", "__seeds", "__task_iter", "__shuffle",
                     "__label")

                # INITIALIZATION

        def _seed_task(self, k, seed):
            """seed a task"""
            if not isinstance(seed, Cell):
                raise TypeError("seed must be a cell")
            if seed not in self.maze.grid:
                raise ValueError("seed is not a cell in the given grid")
            if seed in self.__visited:
                raise ValueError("duplicate seed")

            task = self.__tasks[k]
            if not task.isempty:
                raise ValueError("task already seeded")
            task.push(seed)
            self.__visited[seed] = task
            self.__seeds.append(seed.index)

        def parse_args(self, *tasks, seeds:tuple=(), shuffle:bool=True,
                       weights:list=None,
                       Scheduler:callable=Tournament,
                       label:bool=False):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

                *tasks - either a single integer or one or more task
                    objects.  If an integer is supplied, it denotes
                    the number of tasks to be scheduled.  If there
                    are no entries, then two tasks will be scheduled.

            KEYWORD ARGUMENTS

                seeds - an optional list or tuple of starting cells.

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)

                weights - a list of task weights.  If supplied, these
                    must be positive integers, and there must be one for
                    each task.

                Scheduler - the type of task scheduler (e.g. Tournament
                    or RoundRobin).

                label - label the snakes (for debugging)
            """
            super().parse_args()                # chain to parent

            self.__visited = dict()
            self.__shuffle = shuffle
            self.__visit = self.visit_random if shuffle else self.visit_first
            self.__seeds = list()
            self.__edges = set()
            self.__label = label

                # Set up the task scheduler
            self.__scheduler = Scheduler()
            n = len(tasks)
            if n == 0:
                tasks = (2, )
                n = 1
            if n == 1 and type(tasks[0]) == int:
                n = tasks[0]
                tasks = list()
                for i in range(n):
                    tasks.append(Task(n))
            self.__tasks = tuple(tasks)
            if not weights:
                weights = [1] * n
            for i in range(n):
                task = tasks[i]
                task.taskID = i
                weight = weights[i]
                if weight < 0:
                    weight = 1
                self.__scheduler[task] = weight

                # seed the tasks
            maze = self.maze
            grid = self.grid
            unvisited = list(grid)
            rng.shuffle(unvisited)
            
            if not seeds:
                seeds = tuple()
            if len(seeds) > n:
                raise ValueError("too many seeds")
            k = 0
            for seed in seeds:
                self._seed_task(k, seed)
                k += 1
            while k < n:
                seed = unvisited.pop()
                if seed in self.__visited:
                    continue            # one of the given seeds
                self._seed_task(k, seed)
                k += 1
            self.store_item("tasks", n)
            self.store_item("seeds", list(self.__seeds))

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.__tasks)) # the seed cells
            self.store_item("passages", 0)
            self.__task_iter = iter(self.__scheduler)

        def _link_components(self):
            """cleanup by linking the growing trees"""
                # KRUSKAL'S ALGORITHM
            n = len(self.__tasks)
            edges = list(self.__edges)      # edges between components
            if self.__shuffle:
                rng.shuffle(edges)
            self.store_item("border edges", len(edges))
            self.store_item("accept edges", 0)
            self.store_item("reject edges", 0)
            tasks = set()
            while len(tasks) < n and len(edges) > 0:
                edge = edges.pop()
                cell1, cell2 = edge
                task1, task2 = self.__visited[cell1], self.__visited[cell2]
                if task1 in tasks and task2 in tasks:
                        # reject the edge
                    self.increment_item("reject edges")
                else:
                    self.increment_item("accept edges")
                    tasks.add(task1)
                    tasks.add(task2)
                    self.link(cell1, cell2)

        def _task_stats(self):
            """collect the task statistics"""
            counts = {}
            for task in self.__tasks:
                label = f"task {task.taskID}"
                pushes, pops, maxlen = task.stats
                value = f"push({pushes}), pop({pops}), max({maxlen})"
                self.store_item(label, value)
                counts[task.taskID] = 0
            for cell in self.__visited:
                task = self.__visited[cell]
                counts[task.taskID] += 1
            label = "snake lengths"
            value = tuple(counts[i] for i in range(len(self.__tasks)))
            self.store_item(label, value)

            if self.__label:
                for cell in self.__visited:
                    task = self.__visited[cell]
                    cell.label = str(task.taskID)

        @property
        def more(self):
            """returns True if the stack is empty

            Overrides Algorithm.more.
            """
            if self.__scheduler.isempty:
                self._link_components()
                self._task_stats()
                return False
            return True

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def visit_first(self, task):
            """visit pass - unshuffled"""
            cell = task.top()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    self.link(cell, nbr)            # link to the first
                    self.__visited[nbr] = task
                    self.increment_item("cells")
                    task.push(nbr)
                    return                          # new top of stack
                if self.__visited[nbr] != task:
                    self.__edges.add(frozenset([cell, nbr]))

            task.jettison()                     # all done with this one

        def visit_random(self, task):
            """visit pass - shuffled

            We don't really shuffle... we choose at random
            """
            cell = task.top()
            nbrs = list()
            for nbr in cell.neighbors:
                if nbr in self.__visited:
                    if self.__visited[nbr] != task:
                        self.__edges.add(frozenset([cell, nbr]))
                else:
                    nbrs.append(nbr)

            if not nbrs:                        # done with this one
                task.jettison()
                return

            nbr = rng.choice(nbrs)              # random choice
            self.link(cell, nbr)                # link to it
            self.__visited[nbr] = task
            self.increment_item("cells")
            task.push(nbr)

        def visit(self):
            """wrapper for __visit"""
            task = next(self.__task_iter)
            if task.isempty:
                del self.__scheduler[task]
            else:
                self.__visit(task)

# end module mazes.Algorithms.dff
