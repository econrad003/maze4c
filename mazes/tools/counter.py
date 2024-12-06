"""
mazes.tools.counter - methods that run through a range of states
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A state switching method that runs through a number of states

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

class Counter(object):
    """values that run through a range"""

    __slots__ = ("__state", "__values")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, *values):
        """constructor"""
        self.__values = values
        self.reset()

    def reset(self, initialstate:int=-1):
        """reset

        If initialstate is -1 (default), the value sequence is:
            0, 1, 2, 3, ..., 0, 1, 2, 3
        """
        self.__state = int(initialstate) % len(self.__values)

    def value(self, *args, **kwargs):
        """returns the value regardless of the input"""
        self.__state = (self.__state + 1) % len(self.__values)
        return self.__values[self.__state]

# end module mazes.tools.counter
