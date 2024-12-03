"""
mazes.Queues.priority_queue - implementation of a priority queue using
    generalized queues
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is class PriorityQueue.

IMPLEMENTATION NOTES

    Here we use Python module 'heapq' to implement our priority queue.  There
    is a major drawback to heapq as it does not work with data that
    is not comparable.  We accordingly use a tuple to represent the priority.
    There are three options:
        "stable" - (priority, index)
            index is simply an integer which increases by 1 each time a
            packet is placed on the queue.  The effect is to create a stable
            queue as equal priority items are ordered in order of entry.
        "antistable" - (priority, -index)
            Here we decrease the index by 1 with each entry, so that equal
            priority packets are ordered in reverse entry order.
        "unstable" - (priority, random, index)
            Here equal priority items are ordered randomly.  To guard against
            problems with random number generation, we throw in a unique
            index.
    The option is specified using the keyword 'action' and the action can
    be abbreviated as 's', 'a', 'u'.

    The priority lookup function is specified using the 'priority' keyword.
    If the lookup returns the value None, then a value created and cached
    in a dictionary.  (This will fail if the packet is not hashable.)  The
    option 'cache=False' can be used to suppress caching.

    As an alternative, a priority can also be supplied when a packet is
    entered.  This is more suitable for algorithms (such as discrete event
    simulations) where priorities are created on the fly.

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
import heapq

import mazes
from mazes import rng
from mazes.gqueue import GeneralizedQueue, JettisonError

class PriorityQueue(GeneralizedQueue):
    """A last in, first out queuing structure"""

    NAME = "PriorityQueue"

    __slots__ = ('__array', '__dirty', '__priority', '__action', '__cache',
                 '__index')

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, priority:callable=None, action="unstable", cache=True):
        """constructor"""
        if not callable(priority) and priority != None:
            raise TypeError("The priority function must be callable or None")
        if not isinstance(action, str):
            msg = "The action must be 'stable', 'antistable' or 'unstable'"
            raise TypeError(msg)
        if not isinstance(cache, bool):
            raise TypeError("The cache option must be True or False")

        super().__init__()
        self.__array = []
        self.__dirty = True            # used by top and jettison
        self.__priority = priority
        action = action[0].lower()
        if action not in {'s', 'a', 'u'}:
            msg = "The action must be 'stable', 'antistable' or 'unstable'"
            raise ValueError(msg)
        self.__action = action
        self.__cache = dict() if cache else None
        self.__index = 0

            # MANAGE STATISTICS

    def __len__(self):
        """returns the length (override this!)"""
        return len(self.__array)

            # QUEUE OPERATIONS

    def _encode(self, pr) -> tuple:
        """encodes the priority as described in the preamble"""
        if self.__action == 's':        # stable
            result = (pr, self.__index)
        elif self.__action == 'a':      # antistable
            result = (pr, -self.__index)
        else:                           # unstable
            result = (pr, rng.random(), self.__index)
        self.__index += 1
        return result

    def _lookup(self, packet):
        """look up the priority of a packet"""
        pr = None if self.__priority == None else self.__priority(packet)
        if pr == None:                  # not found
            if self.__cache == None:    # not cacheable
                raise ValueError("priority lookup failed")
            else:                       # is it cached?
                pr = self.__cache.get(packet, None)
        if pr == None:                  # not cached, so cache it
            pr = rng.random()
            self.__cache[packet] = pr
        return pr

    def _enter(self, *args, priority:'Number'=None):
        """place a packet in the queue"""
        packet = args[0] if len(args) == 1 else args
        if priority == None:
            priority = self._lookup(packet)
        pr = self._encode(priority)
        prioritized = (pr, packet)
        heapq.heappush(self.__array, prioritized)
        self.__dirty = True                 # changed

    def _leave(self) -> 'Packet':
        """remove and return a packet from the queue"""
        pr, packet = heapq.heappop(self.__array)
        self.__dirty = True                 # changed
        return packet

    def top(self) -> 'Packet':
        """return but do not remove a packet from the queue"""
        self.__dirty = False                # jettison is permitted
        pr, packet = self.__array[0]
        return packet

    def jettison(self):
        """remove a packet provided the queue is clean"""
        if self.__dirty:
            super().jettison()
        self.leave()

    @property
    def cache(self):
        """return the cache (for debugging)"""
        return self.__cache

# end module mazes.priority_queue