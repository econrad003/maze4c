"""
mazes.algorithm - base class implementation for maze generation algorithms
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A maze is an undirected graph which defines passages between cells.

IMPLEMENTATION

    Two classes are implemented here:

        Algorithm - contains a single class method 'on'.  In most cases
            this should be adequate for maze generation.

        Algorithm.Status - in most cases, subclassing this is all that is
            required.  The following methods should be overridden as needed:
                parse_args
                initialize
                configure
                visit
            To force a visit, include the following in method 'initialize':
                self.more = True
            Method 'visit' should include logic to decide when no further
            visits are required.  To stop further visits:
                self.more = False
            Statistics are name value pairs. The name should be a string and
            the value should be an int, a float, or a string.  The title
            in the first line can be changed using the 'name' option.  A
            default value can be set as a class constant NAME.

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

class Algorithm(object):
    """maze generation algorithm (stub)"""

    class Status(object):
        """this is where most of the work is done"""

        NAME = "maze algorithm"

        __slots__ = ("__maze", "__grid", "__statistics", "__name", "__more",
                     "__fmt")

        def __init__(self, maze:'Maze', *args, name:str=None, **kwargs):
            """constructor"""
            self.__maze = maze
            self.__grid = maze.grid
            self.__statistics = dict()
            self.store_item("visits", 0)
            self.__fmt = dict()
            self.set_format("indent1", 10)
            self.set_format("indent2", 4)
            self.__name = name if name else self.NAME
            self.__more = False             # set this to True in configure!
            self.parse_args(*args, **kwargs)
            self.initialize()
            self.configure()

        def parse_args(self):
            """parse constructor arguments (stub)"""
            pass

        def initialize(self):
            """initialize structures (stub)"""
            pass

        def configure(self):
            """configure structures (stub)"""
            pass

        @property
        def name(self):
            """name getter"""
            return self.__name

        @name.setter
        def name(self, new_name:str):
            """name setter"""
            self.__name = new_name

        @property
        def maze(self):
            """returns the maze to be carved"""
            return self.__maze

        @property
        def grid(self):
            """returns the underlying grid"""
            return self.__grid

        @property
        def more(self):
            """return False if no additional visits are required"""
            return self.__more

        @more.setter
        def more(self, more_to_do:bool):
            """set to True to continue or False if done"""
            self.__more = bool(more_to_do)
            return bool(more_to_do)

        def store_item(self, item:str, new_value):
            """initialize a statistic"""
            self.__statistics[item] = new_value

        def fetch_item(self, item:str):
            """retrieve a statistic"""
            return self.__statistics[item]

        def increment_item(self, item:str, increment:int=1):
            """update a statistic"""
            self.__statistics[item] += increment

        def decrement_item(self, item:str, decrement:int=1):
            """update a statistic"""
            self.__statistics[item] -= decrement

        def visit(self):
            """visit or basic pass (stub)"""
            pass

        def format(self, name):
            """return print formatting, if supported"""
            return self.__fmt.get(name, 0)

        def set_format(self, name, value):
            """set print formatting, if supported"""
            self.__fmt[name] = value

        def __str__(self) -> str:
            """returns the statistics in printable format"""
            indent1 = ' ' * self.format("indent1")
            indent2 = ' ' * self.format("indent2")
            s = indent1 + str(self.__name) + " (statistics)"
            for stat, value in self.__statistics.items():
                s += "\n" + indent2
                if isinstance(value, int):
                    fmt = "%30s  %7d"
                elif isinstance(value, float):
                    fmt = "%30s  %12.4f"
                else:
                    fmt = "%30s  %-10s"
                s += fmt % (stat, value)
            return s

                # Added 1 September 2025:
                #   dunder methods: __contains__, __getitem__, __setitem__

        def __contains__(self, name:str):
            """check for the existence of a statistic"""
            return name in self.__statistics

        def __getitem__(self, name:str):
            """return the value of a statistic, or return None

            Like Status.fetch_item, but no error if the item does not exist.
            """
            return self.__statistics.get(name)

        def __setitem__(self, name:str, value:any):
            """set the value of a statistic

            Same as Status.store_item.
            """
            self.__statistics[name] = value

        # RUN

    @classmethod
    def on(cls, maze:'Maze', *args, status=None, **kwargs):
        """algorithm execution"""
        if status == None:
            status = cls.Status(maze, *args, **kwargs)

        while status.more:
            status.increment_item("visits")
            status.visit()

        return status

# end module mazes.algorithm
