"""
tests.stack - test the Stack class
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
from mazes.Queues.stack import Stack, JettisonError
cls = Stack

def test1():
    """10 pushes and pops"""
    print("  1) ten pushes followed by ten pops")
    stack = Stack()
    data = list(range(10))
    for datum in data:
        stack.enter(datum)
    assert len(stack) == 10
    output = list()
    pops = 0
    while not stack.is_empty:
        pops += 1
        assert pops < 11, "Too many pops"
        output.append(stack.leave())
    assert pops == 10
    expected = list(reversed(data))
    assert output == expected, f"{expected=}, {output=}"
    assert stack.mean == 5
    print(stack)

def test2():
    """ten pushes, then ten top-jettison pairs"""
    print("  2) ten pushes followed by ten top-jettison pairs")
    stack = Stack()
    data = list(range(10))
    for datum in data:
        stack.enter(datum)
    assert len(stack) == 10
    output = list()
    pops = 0
    while not stack.is_empty:
        pops += 1
        assert pops < 11, "Too many pops"
        output.append(stack.top())
        stack.jettison()
    assert pops == 10
    expected = list(reversed(data))
    assert output == expected, f"{expected=}, {output=}"
    assert stack.mean == 5
    print(stack)

def test3():
    """exception handling for jettison"""
    print("  3) test exception handling for jettison")
    stack = Stack()
    data = list(range(10))
    for datum in data:
        stack.enter(datum)
    assert len(stack) == 10
    assert stack.top() == 9
    assert len(stack) == 10
    stack.jettison()
    assert len(stack) == 9
    assert stack.top() == 8
    assert stack.leave() == 8
    assert len(stack) == 8
    try:
        stack.jettison()
        assert False, "JettisonError was not raised after pop (leave)"
    except JettisonError:
        pass
    assert len(stack) == 8
    assert stack.top() == 7
    stack.enter(8)
    try:
        stack.jettison()
        assert False, "JettisonError was not raised after push (enter)"
    except JettisonError:
        pass
    assert len(stack) == 9
    assert stack.top() == 8
    stack.jettison()
    assert len(stack) == 8
    try:
        stack.jettison()
        assert False, "JettisonError was not raised after jettison"
    except JettisonError:
        pass
    assert len(stack) == 8
    assert stack.top() == 7
    pops = 0
    while not stack.is_empty:
        pops += 1
        assert pops < 9, "Too many pops"
        stack.top()
        stack.jettison()
    assert pops == 8
    print(stack)

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

# end module tests.stack