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
from mazes.Queues.random_queue import RandomQueue, JettisonError
cls = RandomQueue

def test1():
    """ten pushes and pops"""
    print("  1) ten enters followed by ten leaves")
    q = RandomQueue()
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
    print(f"    {output=}")
    assert sorted(output) == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

def test2():
    """ten pushes, then ten top-jettison pairs"""
    print("  2) ten enters followed by ten top-jettison pairs")
    q = RandomQueue()
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
    print(f"    {output=}")
    assert sorted(output) == expected, f"{expected=}, {output=}"
    assert q.mean == 5
    print(q)

        # add test definitions above

def main():
    """run all the tests"""
    print(f"Test the {cls.__name__} class...")
            # place tests here
    test1()
    test2()
            # end of tests
    print("SUCCESS!")

if __name__ == "__main__":
    main()

# end module tests.random_queue