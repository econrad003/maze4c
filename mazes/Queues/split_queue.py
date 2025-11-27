"""
mazes.Queues.split_queue - implementation of a split queue using generalized queues
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is class SplitQueue.

    A split queue consists of a stack, a double-ended queue and a target
    length.

    Arrivals:
        When a packet arrives, it is placed at the end of the queue.  If the
        stack is then shorter than the target length, then the first entry in
        the queue is popped from the queue and onto the stack.

    Departures:
        A packet leaves from the end of the stack.  If the queue is not
        empty, then the first entry in the queue is popped from the queue
        and onto the stack.

    The length conditions insure that, the stack has exactly the target
    length whenever the queue is not empty.

    Note that the length conditions for SplitStack and SplitQueue differ!

EXAMPLES

    In each example, we push the numbers 1 through 12 onto the queue.  If
    the number most recently pushed is a member of the "pop at" set, we then
    pop an entry. After all pushes are complete, we pop entries until the
    queue is empty.  For comparison, we display ordinary stack and queue
    behavior as well.

        Pop at {}, target length=1
          Split queue: 1 2 3 4 5 6 7 8 9 10 11 12       same as queue
                Stack: 12 11 10 9 8 7 6 5 4 3 2 1
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {1, 5, 9}, target length=1
          Split queue: 1 2 3 4 5 6 7 8 9 10 11 12       same as queue
                Stack: 1 5 9 12 11 10 8 7 6 4 3 2
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {}, target length=2
          Split queue: 2 3 4 5 6 7 8 9 10 11 12 1       second in, first out
                Stack: 12 11 10 9 8 7 6 5 4 3 2 1
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {1, 5, 9}, target length=2
          Split queue: 1 3 4 5 6 7 8 9 10 11 12 2
                Stack: 1 5 9 12 11 10 8 7 6 4 3 2
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {}, target length=5
          Split queue: 5 6 7 8 9 10 11 12 4 3 2 1       fifth in first out
                Stack: 12 11 10 9 8 7 6 5 4 3 2 1
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {1, 5, 9}, target length=5
          Split queue: 1 5 7 8 9 10 11 12 6 4 3 2
                Stack: 1 5 9 12 11 10 8 7 6 4 3 2
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {}, target length=12 (maximum length=12)
          Split queue: 12 11 10 9 8 7 6 5 4 3 2 1       twelth in first out
                Stack: 12 11 10 9 8 7 6 5 4 3 2 1       (same results)
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {1, 5, 9}, target length=12 (maximum length=9)
          Split queue: 1 5 9 12 11 10 8 7 6 4 3 2
                Stack: 1 5 9 12 11 10 8 7 6 4 3 2       (same results)
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

SPECIAL CASES

    If the target length is 1, the split queue behaves like an ordinary
    queue.

    If the target length is greater than or equal to the number of cells
    in the maze, the split queue behaves like a stack.

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

class SplitQueue(GeneralizedQueue):
    """A end of the first line in, first out queuing structure"""

    NAME = "Split Queue"

    __slots__ = ('__stack', '__deque', '__target', '__dirty')

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, target_length:int=10):
        """constructor"""
        super().__init__()
        assert target_length >= 1
        self.__stack = list()
        self.__deque = deque()
        self.__target = target_length
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
        if len(self.__stack) < self.__target:
            self.__stack.append(self.__deque.popleft())
        self.__dirty = True                 # changed

    def _leave(self) -> 'Packet':
        """remove and return a packet from the queue"""
        packet = self.__stack.pop()
        if len(self.__deque) > 0:
            self.__stack.append(self.__deque.popleft())
        self.__dirty = True                 # changed
        return packet

    def top(self) -> 'Packet':
        """return but do not remove a packet from the queue"""
        self.__dirty = False                # jettison is permitted
        return self.__stack[-1]

    def jettison(self):
        """remove a packet provided the queue is clean"""
        if self.__dirty:
            super().jettison()
        self.leave()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="split queue demo")
    parser.add_argument("target", type=int, help="target length")
    parser.add_argument("-p", "--pop_at", type=int, nargs="*", help="pops", default=[])
    args = parser.parse_args()

    popat = set(args.pop_at)
    print(f"        Pop at {popat}, target length={args.target}")
    print("          Split queue: ", end="")
    q = SplitQueue(args.target)
    for n in range(1, 13):
        q.enter(n)
        if n in popat:
            print(f"{q.leave()} ", end="")
    while len(q)>0:
        print(f"{q.leave()} ", end="")
    print()
    print("                Stack: ", end="")
    q = list()
    for n in range(1, 13):
        q.append(n)
        if n in popat:
            print(f"{q.pop()} ", end="")
    while len(q)>0:
        print(f"{q.pop()} ", end="")
    print()
    print("                Queue: ", end="")
    q = list()
    for n in range(1, 13):
        q.append(n)
        if n in popat:
            print(f"{q.pop(0)} ", end="")
    while len(q)>0:
        print(f"{q.pop(0)} ", end="")
    print()

# end module mazes.split_queue
