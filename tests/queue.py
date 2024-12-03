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
from mazes.Queues.queue import Queue, JettisonError
cls = Queue

def test1():
    """10 pushes and pops"""
    print("  1) ten enters followed by ten leaves")
    q = Queue()
    data = list(range(10))
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
    expected = data
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test2():
    """ten pushes, then ten top-jettison pairs"""
    print("  2) ten enters followed by ten top-jettison pairs")
    q = Queue()
    data = list(range(10))
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    output = list()
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 11, "Too many exits"
        output.append(q.top())
        q.jettison()
    assert exits == 10
    expected = data
    assert output == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test3():
    """exception handling for jettison"""
    print("  3) test exception handling for jettison")
    q = Queue()
    data = list(range(10))
    for datum in data:
        q.enter(datum)
    assert len(q) == 10
    assert q.top() == 0
    assert len(q) == 10
    q.jettison()
    assert len(q) == 9
    assert q.top() == 1
    assert q.leave() == 1
    assert len(q) == 8
    try:
        q.jettison()
        assert False, "JettisonError was not raised after leave"
    except JettisonError:
        pass
    assert len(q) == 8
    assert q.top() == 2
    q.enter(10)
    try:
        q.jettison()
        assert False, "JettisonError was not raised after enter"
    except JettisonError:
        pass
    assert len(q) == 9
    assert q.top() == 2
    q.jettison()
    assert len(q) == 8
    try:
        q.jettison()
        assert False, "JettisonError was not raised after jettison"
    except JettisonError:
        pass
    assert len(q) == 8
    assert q.top() == 3
    exits = 0
    while not q.is_empty:
        exits += 1
        assert exits < 9, "Too many pops"
        q.top()
        q.jettison()
    assert exits == 8
    print(q)

        # add test definitions above

def main():
    """run all the tests"""
    print(f"Test the {cls.__name__} class...")
            # place tests here
    test1()
    test2()
    test3()
            # end of tests
    print("SUCCESS!")

if __name__ == "__main__":
    main()

# end module tests.queue