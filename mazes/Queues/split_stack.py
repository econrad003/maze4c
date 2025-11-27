"""
mazes.Queues.split_stack - implementation of a split stack using generalized queues
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is class SplitStack.

    A split stack consists of two stacks and a target length.

    Arrivals:
        When a packet arrives, it is placed at the end of the second stack.
        If the total length is then shorter than the target length, then the
        last entry in the second stack is popped from the second stack and
        pushed into the first.

    Departures:
        A packet is popped from the first stack.  If the second stack is not
        empty, then the last entry in the second stack is popped and pushed
        into the first.

    The length conditions insure that, the first stack has exactly the target
    length whenever the second stack is not empty.

    Note that the length conditions for SplitStack and SplitQueue differ!

EXAMPLE

    In each example, we push the numbers 1 through 12 onto the queue.  If
    the number most recently pushed is a member of the "pop at" set, we then
    pop an entry. After all pushes are complete, we pop entries until the
    queue is empty.  For comparison, we display ordinary stack and queue
    behavior as well.

        Pop at {}, target length=1
          Split stack: 1 12 11 10 9 8 7 6 5 4 3 2   rotated LIFO
                Stack: 12 11 10 9 8 7 6 5 4 3 2 1   last in, first out
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {1, 5, 9}, target length=1
          Split stack: 1 2 5 9 12 11 10 8 7 6 4 3
                Stack: 1 5 9 12 11 10 8 7 6 4 3 2
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

    Sort of stack-like, but with a delay.

        Pop at {}, target length=2
          Split stack: 1 2 12 11 10 9 8 7 6 5 4 3
                Stack: 12 11 10 9 8 7 6 5 4 3 2 1
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {1, 5, 9}, target length=2
          Split stack: 1 2 3 5 9 12 11 10 8 7 6 4
                Stack: 1 5 9 12 11 10 8 7 6 4 3 2
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

    Starts off as a queue, but becomes stack-like.

        Pop at set(), target length=12 (maximum length=12)
          Split stack: 1 2 3 4 5 6 7 8 9 10 11 12   (behaves like queue)
                Stack: 12 11 10 9 8 7 6 5 4 3 2 1
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

        Pop at {1, 5, 9}, target length=12 (maximum length=9)
          Split stack: 1 2 3 4 5 6 7 8 9 10 11 12   (behaves like queue)
                Stack: 1 5 9 12 11 10 8 7 6 4 3 2
                Queue: 1 2 3 4 5 6 7 8 9 10 11 12

SPECIAL CASES

    If the target length is greater than or equal to the number of cells in
    the maze, the split stack behaves like a queue.

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

class SplitStack(GeneralizedQueue):
    """A beginning of the second line in, first out queuing structure"""

    NAME = "Split Queue"

    __slots__ = ('__deque', '__stack', '__target', '__dirty')

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, target_length:int=10):
        """constructor"""
        super().__init__()
        assert target_length >= 1
        self.__deque = deque()
        self.__stack = list()
        self.__target = target_length
        self.__dirty = True            # used by top and jettison

            # MANAGE STATISTICS

    def __len__(self):
        """returns the length (override this!)"""
        return len(self.__deque) + len(self.__stack)

            # QUEUE OPERATIONS

    def _enter(self, *args):
        """place a packet in the split stack"""
        packet = args[0] if len(args) == 1 else args
        self.__stack.append(packet)
        if len(self.__deque) < self.__target:
            self.__deque.append(self.__stack.pop())
        self.__dirty = True                 # changed

    def _leave(self) -> 'Packet':
        """remove and return a packet from the split stack"""
        packet = self.__deque.popleft()
        if len(self.__stack) > 0:
            self.__deque.append(self.__stack.pop())
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="split stack demo")
    parser.add_argument("target", type=int, help="target length")
    parser.add_argument("-p", "--pop_at", type=int, nargs="*", help="pops", default=[])
    args = parser.parse_args()

    popat = {1, 2, 3, 5, 8}
    popat = set(args.pop_at)
    print(f"        Pop at {popat}, target length={args.target}")
    print("          Split stack: ", end="")
    q = SplitStack(args.target)
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

# end module mazes.split_stack
