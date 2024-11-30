"""
mazes.active_list - base class implementation for active lists
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An active list is an array in which arbitrary members can be quickly
    removed at random.  In [1], this sort of structure is implied in
    the discussion SimplifiedPrims and GrowingTree.

    The price we pay is that deletions from anywhere but the end reorder the
    entries in the array.

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

from mazes import rng

class ActiveList(object):
    """Directed passages in a maze (arcs in a directed graph)"""

    __slots__ = ("__array")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self):
        """constructor"""
        self.__array = list()

    def __len__(self):
        """returns the length - O(1)"""
        return len(self.__array)

    def __iter__(self):
        """generates the entries in the the active list -- O(n)"""
        for x in self.__array:
            yield x

    def __getitem__(self, index):
        """returns the requested item -- O(1)"""
        return self.__array[index]

    def __setitem__(self, index, value):
        """replaces the requested item -- O(1)"""
        self.__array[index] = value

    def __delitem__(self, index):
        """delete the requested item -- O(1)

        Deleting any item involves setting the value to the value of the
        last item and then popping the last item.  Note that this may change
        the order of the remaining items.
        """
        self.__array[index] = self.__array[-1]      # move
        self.__array.pop()                          # pop

    def push(self, value):
        """append a value to the list -- O(1)"""
        self.__array.append(value)

    def append(self, value):
        """append a value to the list (same as push) -- O(1)"""
        self.__array.append(value)

# end module mazes.active_list
