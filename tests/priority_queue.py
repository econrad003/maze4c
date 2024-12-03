"""
tests.queue - test the Queue class
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The Stack class is the simplest queuing structure based on virtual
    base class GeneralizedQueue defined in mazes.gqueue.

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
import mazes
from mazes import rng
from mazes.Queues.priority_queue import PriorityQueue, JettisonError
cls = PriorityQueue

class Incomparable(object):
    """an incomparable widget"""

    def __init__(self, n):
        """constructor"""
        self.n = n

    def __repr__(self):
        """representation"""
        return f"w{self.n}"

def test1():
    """ten pushes and pops"""
    print("  1) ten enters followed by ten leaves")
    pr = lambda n: n
    q = PriorityQueue(priority=pr)
    data = list(range(10))
    rng.shuffle(data)
    print(f"     {data=}")
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.leave())
    assert exits == 10
    expected = sorted(data)
    print(f"    {output=}")
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test2():
    """ten pushes, then ten top-jettison pairs"""
    print("  2) ten enters followed by ten top-jettison pairs")
    q = PriorityQueue()
    data = list(range(10))
    rng.shuffle(data)
    print(f"     {data=}")
    for datum in data:
        q.enter(datum, priority=datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.top())
        q.jettison()
    assert exits == 10
    expected = sorted(data)
    print(f"    {output=}")
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test3():
    """ten pushes and pops"""
    print("  3) ten enters followed by ten leaves with pr=-n")
    pr = lambda n: -n
    q = PriorityQueue(priority=pr)
    data = list(range(10))
    rng.shuffle(data)
    print(f"     {data=}")
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.leave())
    assert exits == 10
    expected = list(sorted(data, reverse=True))
    print(f"    {output=}")
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test4():
    """ten pushes and pops"""
    print("  4) ten enters followed by ten leaves")
    d1 = {0:"zero", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five",
          6:"six", 7:"seven", 8:"eight", 9:"nine", 10:"ten",
          11:"eleven", 12:"twelve", 13:"thirteen", 14:"fourteen"}
    priorities = dict()
    data = list()
    expected = list()
    for n in d1:
        priorities[d1[n]] = n
        data.append(d1[n])
        expected.append(d1[n])
    data = sorted(data)
    print(f"    {priorities=}")
    print(f"    {data=}")
    print(f"    {expected=}")
    pr = lambda x: priorities[x]
    q = PriorityQueue(priority=pr)
    for datum in data:
        q.enter(datum)
    assert len(q) == 15
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 16, "Too many exits"
        output.append(q.leave())
    assert exits == 15
    print(f"    {output=}")
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 7.5
    print(q)

        # add test definitions above

def test5():
    """ten pushes and pops"""
    print("  5) ten entering widgets followed by ten leaving")
    pr = lambda widget: widget.n
    q = PriorityQueue(priority=pr)
    data = list(Incomparable(n) for n in range(10))
    expected = list(data)
    assert data is not expected
    rng.shuffle(data)
    print(f"     {data=}")
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.leave())
    assert exits == 10
    print(f"    {output=}")
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test6():
    """ten pushes and pops"""
    print("  6) stable queue")
    pr = lambda widget: 1
    q = PriorityQueue(priority=pr, action="stable")
    data = list(Incomparable(n) for n in range(10))
    expected = list(data)
    assert data is not expected
    print(f"     {data=}")
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.leave())
    assert exits == 10
    print(f"    {output=}")
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test7():
    """ten pushes and pops"""
    print("  7) antistable queue")
    pr = lambda widget: 1
    q = PriorityQueue(priority=pr, action="antistable")
    data = list(Incomparable(n) for n in range(10))
    expected = list(reversed(data))
    assert data is not expected
    print(f"     {data=}")
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.leave())
    assert exits == 10
    print(f"    {output=}")
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test8():
    """ten pushes and pops"""
    print("  8) unstable queue")
    pr = lambda widget: 1
    q = PriorityQueue(priority=pr, action="unstable")
    data = list(Incomparable(n) for n in range(10))
    expected = list(data)
    assert data is not expected
    print(f"     {data=}")
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.leave())
    assert exits == 10
    print(f"    {output=}")
    print("    This probably isn't in order.  That's normal!")
    print("    If it is in order, repeat the experiment!")
    print("    Theoretical probability of in order: 1 in 3,628,800.")
    assert set(output) == set(expected), f"{expected=}, {output=} (random order)"
    assert q.mean == 5
    print(q)

def test9():
    """test cache"""
    print("  9) cache")
    q = PriorityQueue()
    data = list(n for n in range(5))
    data = data + data
    print(f"     {data=}")
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    assert len(q.cache) == 5
    exits = 0
    output = list()
    while not q.is_empty:
        q1 = q.leave()
        q2 = q.leave()
        output += [q1, q2]
        assert q1 == q2
        exits += 2
    print(f"    {output=}")
    print(q)
    assert exits == 10
    assert q.mean == 5

def main():
    """run all the tests"""
    print(f"Test the {cls.__name__} class...")
            # place tests here
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
            # end of tests
    print("SUCCESS!")

if __name__ == "__main__":
    main()

# end module tests.priority_queue