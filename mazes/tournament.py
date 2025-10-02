"""
mazes.tournament - a simple task handler
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a simple task controller that yields control to a set of
    tasks based on priority,

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

MODIFICATIONS

    28 Sep 2025 - E Conrad
        1) refactor to facilitate derivation of class RoundRobin.
        2) correction: add "else" clause after "yield None"
"""

from mazes import rng

class Tournament(object):

    __slots__ = ("__table", "__tasks", "__cum_wgts", "__clean")

    def __init__(self):
        """constructor"""
        self.__table = {}           # task -> weight
        self.__tasks = tuple()      # task vector
        self.__cum_wgts = tuple()   # cumulative weights vector
        self.__clean = True

    def update_choices(self):
        """update the vectors"""
        if self.__clean:
            return                  # nothing to do
        self.__tasks = tuple(self.__table.keys())
        cum_wgt = 0
        cum_wgts = list()
        for task in self.__tasks:
            cum_wgt += self.__table[task]
            cum_wgts.append(cum_wgt)
        self.__cum_wgts = tuple(cum_wgts)
        self.__clean = True

    @property
    def isempty(self):
        """return True if there are no tasks"""
        return len(self.__table) == 0

    @staticmethod
    def check_weight(weight):
        """"""
        if type(weight) != int:
            raise TypeError("weights must be positive integers")
        if weight < 1:
            raise ValueError("weights must be positive integers")

    @classmethod
    def validate_add_task(cls, task, weight):
        """validate the operands"""
        if task == None:
            raise ValueError("None is not a valid task")
        cls.check_weight(weight)

    def add_task(self, task, weight:int=1):
        """add a task to the tournament"""
        self.validate_add_task(task, weight)
        self.__table[task] = weight
        self.__clean = False

    def remove_task(self, task):
        """remove a task from the tournament"""
        del self.__table[task]
        self.__clean = False

    def __getitem__(self, task) -> int:
        """return the task weight"""
        return self.__table[task]

    def __setitem__(self, task, weight):
        """update the tournament"""
        if weight == None:
            self.remove_task(task)
        else:
            self.add_task(task, weight)

    def __delitem__(self, task):
        """remove a task from the tournament"""
        self.remove_task(task)

    def choose_next(self):
        """choose the task that is to be next"""
        self.update_choices()
        return rng.choices(self.__tasks, cum_weights=self.__cum_wgts)[0]

    def __iter__(self):
        """determine the next active task"""
        while True:
            yield None if self.isempty else self.choose_next()

