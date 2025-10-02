"""
mazes.round_robin - another simple task handler
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a simple task controller that yields control to a set of
    tasks by taking turns.

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
from mazes.tournament import Tournament

class RoundRobin(Tournament):

    __slots__ = ("__table", "__tasks", "__index")

    def __init__(self):
        """constructor"""
        super().__init__()          # set parent data to defaults
        self.__table = dict()
        self.__tasks = list()       # task vector
        self.__index = 0

    @property
    def isempty(self):
        """return True if there are no tasks"""
        return len(self.__table) == 0

    def add_task(self, task, weight:int=1):
        """add a task to the tournament

        The weight argument is ignored
        """
        if task in self.__tasks:
            pass
        else:
            location = len(self.__tasks)
            self.validate_add_task(task, 1)
            self.__table[task] = location
            self.__tasks.append(task)

    def remove_task(self, task):
        """remove a task from the tournament"""
        location = self[task]
        # print(f"del {task} at {location}")
        # print(self.__tasks)
        del self.__table[task]
        self.__tasks = self.__tasks[:location] + self.__tasks[location+1:]
        for i in range(location, len(self.__tasks)):
            task2 = self.__tasks[i]
            self.__table[task2] = i
        # print(self.__table)
        # print(self.__tasks)
        if self.__index > location:
            self.__index -= 1           # correct the next task pointer

    def __getitem__(self, task) -> int:
        """return the task weight"""
        return self.__table[task]

    def choose_next(self):
        """choose the task that is to be next"""
        if self.__index < len(self.__tasks):
            choice = self.__tasks[self.__index]
            self.__index += 1
            return(choice)
        self.__index = 1
        return self.__tasks[0]

