"""
mazes.Queues.random_queue - implementation of a random queue using
    generalized queues and active lists
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is class RandomQueue.

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
from mazes.active_list import ActiveList
from mazes.gqueue import GeneralizedQueue, JettisonError

class RandomQueue(GeneralizedQueue):
    """A random in, first out queuing structure"""

    NAME = "Random In, First Out Queue"

    __slots__ = ('__array', '__key')

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self):
        """constructor"""
        super().__init__()
        self.__array = ActiveList()
        self.__key = None             		# used by top and jettison

            # MANAGE STATISTICS

    def __len__(self):
        """returns the length (override this!)"""
        return len(self.__array)

            # QUEUE OPERATIONS

    def _enter(self, *args):
        """place a packet in the queue"""
        packet = args[0] if len(args) == 1 else args
        self.__array.push(packet)
        self.__key = None                 	# changed

    def _leave(self, key=None) -> 'Packet':
        """remove and return a packet from the queue"""
        if key == None:
        	key = rng.randrange(len(self.__array))
        packet = self.__array[key]
        del self.__array[key]
        self.__key = None                 	# changed
        return packet

    def top(self, key=None) -> 'Packet':
        """return but do not remove a packet from the queue"""
        if key == None:
        	key = rng.randrange(len(self.__array))
        self.__key = key                	# jettison is permitted
        return self.__array[key]

    def jettison(self):
        """remove a packet provided the queue is clean"""
        if not isinstance(self.__key, int):
            super().jettison()
        self.leave(key=self.__key)

# end module mazes.random_queue