"""
mazes.Queues.median_queue - implementation of a median queue using generalized queues
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is class MedianQueue.

    A median queue consists of a stack and a double-ended queue.

    Arrivals:
        When a packet arrives, it is first placed at the end of the queue.
        If the queue more than one entry longer than the stack, the first
        entry in the queue is popped from the queue and onto the stack.

    Departures:
        A packet leaves from the start of the queue.  If the queue is then
        shorter than the stack, the last entry in the stack popped and pushed
        to the front of the queue.

    The length condition for arrivals insures that the queue never exceeds
    more than one more entry than the stack.  The length consdition on departures
    insures that the stack never has more entries than the queue:

            length(stack) <= length(queue) <= length(stack) + 1

    Note that this implies that if the queue is empty, then the stack must also
    be empty.  If the stack is empty, the queue can have at most one entry.

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
from collections import deque
from mazes.gqueue import GeneralizedQueue, JettisonError

class MedianQueue(GeneralizedQueue):
    """A middle in, first out queuing structure"""

    NAME = "Median Queue"

    __slots__ = ('__stack', '__deque', '__dirty')

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self):
        """constructor"""
        super().__init__()
        self.__stack = list()
        self.__deque = deque()
        self.__dirty = True            # used by top and jettison

            # MANAGE STATISTICS

    def __len__(self):
        """returns the length (override this!)"""
        return len(self.__stack) + len(self.__deque)

            # QUEUE OPERATIONS

    def _enter(self, *args):
        """place a packet in the queue"""
        packet = args[0] if len(args) == 1 else args
        self.__deque.append(packet)
        if len(self.__deque) > len(self.__stack) + 1:
            self.__stack.append(self.__deque.popleft())
        self.__dirty = True                 # changed

    def _leave(self) -> 'Packet':
        """remove and return a packet from the queue"""
        packet = self.__deque.popleft()
        if len(self.__stack) > len(self.__deque):
            self.__deque.appendleft(self.__stack.pop())
        self.__dirty = True                 # changed
        return packet

    def top(self) -> 'Packet':
        """return but do not remove a packet from the queue"""
        self.__dirty = False                # jettison is permitted
        return self.__deque[0]

    def jettison(self):
        """remove a packet provided the queue is clean"""
        if self.__dirty:
            super().jettison()
        self.leave()

# end module mazes.median_queue
