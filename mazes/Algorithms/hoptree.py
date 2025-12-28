"""
mazes.Algorithms.hoptree - the hop search maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

BACKGROUND

    This algorithm was inspired by a problem in Chapter 11 of [1].  The
    problem deals with cell selection for a growing tree:

        "Most distant -- always choose the cell furthest from the cell
        that was selected previously."  -- page 188

    Now I am fairly certain that furthest is based on grid distance.  So
    furthest depends on a grid metric such as the Pythagorean distance,
    the taxicab metric, or perhaps even the knight's move metric.

    But as we grow a maze, more cells become reachable.  What if we pick
    the frontier cell that is furthest away using maze distance (or the
    number of hops in the _maze_)?  Well one thing that becomes apparent
    is that distance needs to be updated with each new link -- and this
    update is essentially a O(n) operation, where n is the number of
    cell in the grid.  (We should probably say O(n log n) since there is
    some dictionary access overhead.)  Since we need to add n-1 edges,
    this leads to a rougly Ω(n²) estimated lower bound.  Not good!  So
    this probably won't be a good algorithm for preparing large mazes.
    But for small to medium-sized mazes, it might be worth investigating.

DESCRIPTION

    This algorithm works directly in the frontier.  One pass is
    essentially as follows:

        Select a grid edge e={u,v} the frontier,
            where u is visited and v is in the frontier;
        Add e to the maze;
        Compute distances from v to each visited cell;
        Remove v from the frontier;
        Mark v as visited;
        Add each unvisited neighbor of v to the frontier.

    The key question that arises is how we select the edge from the
    frontier.

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
from mazes import rng, Cell, Algorithm
from mazes.Metrics.hops import Metric

class HopTree(Algorithm):
    """the hop search maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Hop Search"

        __slots__ = ("__metric", "__previous", "__select")

                # INITIALIZATION

        def parse_args(self, *args, start_cell:'Cell'=None,
                       HopClass=Metric, action:str="furthest",
                       **kwargs):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

                args - positional arguments (other than maze) for HopClass

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                HopClass - the class to use as a metric.  The default is
                    class Metric in module mazes.Metrics.hops

                action
                    "furthest" - the furthest frontier cell from the
                        previous selection wins
                    "closest" - the closest frontier cell from the
                        previous selection wins

                kwargs - keyword arguments (other than maze) for HopClass
            """
            super().parse_args()                # chain to parent
                # create the metric
            self.__metric = HopClass(self.maze, *args, **kwargs)
                # initialize the unvisited set and the stack
            if start_cell == None and len(self.maze) == 0:
                start_cell = rng.choice(list(self.maze.grid))
            if start_cell != None:
                self.__metric.start_cell(start_cell)
                self["start cell"] = start_cell.index
            self.__previous = None
            self.set_action(action)

        def set_action(self, action:str):
            """set the selection"""
            self["action"] = str(action)
            if action in {"furthest", "farthest", "far"}:
                self.__select = self.select_furthest
            elif action in {"closest", "nearest", "close", "near"}:
                self.__select = self.select_closest
            elif action == "random":
                self.__select = self.select_first_cell
            else:
                raise NotImplementedError(f"action = {str(action)}")

        def set_select(self, select:callable):
            """set the selection action"""
            self.__select = select

        def configure(self):
            """configuration"""
                # set up the statistics
            self["selection passes"] = 0
            self["cells"] = self.__metric.number_visited
            self["passages (start)"] = len(self.maze)
            self["passages"] = len(self.maze)

        @property
        def more(self):
            """returns True if the frontier is empty

            Overrides Algorithm.more.
            """
            return not self.__metric.empty_frontier

        @property
        def metric(self):
            """the metric object"""
            return self.__metric

        def link(self, cell, nbr, dist:float=1):
            """carve a passage"""
            self.__metric.link(cell, nbr, dist)
            self["passages"] += 1
            self["cells"] += 1

        def select_first_cell(self):
            """this selects a starting cell"""
            cell = rng.choice(list(self.__metric.frontier))
            candidates = list()
            for nbr in cell.neighbors:
                if self.__metric.is_visited(nbr):
                    vector = (nbr, cell)
                    candidates.append(vector)
            return candidates

        def select_furthest(self):
            """this selects the cell furthest from the predecessor"""
            candidates = list()
            max_d = - float('inf')
            for cell in self.__metric:      # search in the frontier
                self["selection passes"] += 1
                d, via = self.__metric.trial_d(self.__previous, cell)
                if via == None:
                    continue
                if d < max_d:
                    continue
                if d > max_d:
                    candidates = list()
                    max_d = d
                vector = (via, cell)
                candidates.append(vector)
            return candidates

        def select_closest(self):
            """this selects the cell closest to the predecessor"""
            candidates = list()
            min_d = float('inf')
            for cell in self.__metric:      # search in the frontier
                self["selection passes"] += 1
                d, via = self.__metric.trial_d(self.__previous, cell)
                if via == None:
                    continue
                if d > min_d:
                    continue
                if d < min_d:
                    candidates = list()
                    min_d = d
                vector = (via, cell)
                candidates.append(vector)
            return candidates

        def visit(self):
            """visit pass"""
                    # Select a grid edge e={u,v} the frontier,
                    #   where u is visited and v is in the frontier;
            candidates = self.select_first_cell() if self.__previous == None \
                else self.__select()
            via, cell = rng.choice(candidates)

                    # Add e to the maze;
                    # Compute distances from v to each visited cell;
                    # Remove v from the frontier;
                    # Mark v as visited;
                    # Add each unvisited neighbor of v to the frontier.
            self.link(via, cell)
            self.__previous = via

# end module mazes.Algorithms.hoptree
