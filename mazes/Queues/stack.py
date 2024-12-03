"""
mazes.Queues.stack - implementation of a stack using generalized queues
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is class Stack.

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

from mazes.gqueue import GeneralizedQueue, JettisonError

class Stack(GeneralizedQueue):
    """A last in, first out queuing structure"""

    NAME = "Stack"

    __slots__ = ('__array', '__dirty')

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self):
        """constructor"""
        super().__init__()
        self.__array = list()
        self.__dirty = True            # used by top and jettison

            # MANAGE STATISTICS

    def __len__(self):
        """returns the length (override this!)"""
        return len(self.__array)

            # QUEUE OPERATIONS

    def _enter(self, *args):
        """place a packet in the queue"""
        packet = args[0] if len(args) == 1 else args
        self.__array.append(packet)
        self.__dirty = True                 # stack has changed

    def _leave(self) -> 'Packet':
        """remove and return a packet from the queue"""
        packet = self.__array.pop()
        self.__dirty = True                 # stack has changed
        return packet

    def top(self) -> 'Packet':
        """return but do not remove a packet from the queue"""
        self.__dirty = False                # jettison is permitted
        return self.__array[-1]

    def jettison(self):
        """remove a packet provided the stack is clean"""
        if self.__dirty:
            super().jettison()
        self.leave()

# end module mazes.gqueue
