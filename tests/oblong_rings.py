"""
tests.oblong_rings - test the oblong rings module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This tests the hell out of mazes.Grids.oblong_rings.

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

from mazes.Grids.oblong import OblongGrid
from mazes.Grids.oblong_rings import ConcentricOblongs

    # some simple consistency checks

def test2x2():
    """2x2 test"""
    grid = OblongGrid(2, 2)
    rings = ConcentricOblongs(grid)
    # print(rings.bounding_boxes)
    assert rings.bounding_boxes == ((0, 0, 1, 1),)
    bbox = rings.bounding_boxes[0]
    for cell in grid:
        assert rings.is_on(cell, bbox)
        assert not rings.is_inside(cell, bbox)
        assert not rings.is_outside(cell, bbox)
        assert rings.tier_for(cell) == 0

def test3x3():
    """3x3 test"""
    grid = OblongGrid(3, 3)
    rings = ConcentricOblongs(grid)
    # print(rings.bounding_boxes)
    assert rings.bounding_boxes == ((0, 0, 2, 2), (1, 1, 1, 1))
    bbox0 = rings.bounding_boxes[0]
    bbox1 = rings.bounding_boxes[1]
    for cell in grid:
        msg = f"{cell.index} (%d, %d, %d, %d)"
        if cell == grid[1,1]:
            assert not rings.is_on(cell, bbox0), msg % bbox0
            assert rings.is_on(cell, bbox1), msg % bbox1
            assert rings.is_inside(cell, bbox0), msg % bbox0
            assert not rings.is_inside(cell, bbox1), msg % bbox1
            assert not rings.is_outside(cell, bbox0), msg % bbox0
            assert not rings.is_outside(cell, bbox1), msg % bbox1
            assert rings.tier_for(cell) == 1
        else:
            assert rings.is_on(cell, bbox0), msg % bbox0
            assert not rings.is_on(cell, bbox1), msg % bbox1
            assert not rings.is_inside(cell, bbox0), msg % bbox0
            assert not rings.is_inside(cell, bbox1), msg % bbox1
            assert not rings.is_outside(cell, bbox0), msg % bbox0
            assert rings.is_outside(cell, bbox1), msg % bbox1
            assert rings.tier_for(cell) == 0

def test3x4():
    """3x4 test"""
    grid = OblongGrid(3, 4)
    rings = ConcentricOblongs(grid)
    # print(rings.bounding_boxes)
    assert rings.bounding_boxes == ((0, 0, 2, 3), (1, 1, 1, 2))
    bbox0 = rings.bounding_boxes[0]
    bbox1 = rings.bounding_boxes[1]
    for cell in grid:
        msg = f"{cell.index} (%d, %d, %d, %d)"
        if cell in {grid[1,1], grid[1,2]}:
            assert not rings.is_on(cell, bbox0), msg % bbox0
            assert rings.is_on(cell, bbox1), msg % bbox1
            assert rings.is_inside(cell, bbox0), msg % bbox0
            assert not rings.is_inside(cell, bbox1), msg % bbox1
            assert not rings.is_outside(cell, bbox0), msg % bbox0
            assert not rings.is_outside(cell, bbox1), msg % bbox1
            assert rings.tier_for(cell) == 1
        else:
            assert rings.is_on(cell, bbox0), msg % bbox0
            assert not rings.is_on(cell, bbox1), msg % bbox1
            assert not rings.is_inside(cell, bbox0), msg % bbox0
            assert not rings.is_inside(cell, bbox1), msg % bbox1
            assert not rings.is_outside(cell, bbox0), msg % bbox0
            assert rings.is_outside(cell, bbox1), msg % bbox1
            assert rings.tier_for(cell) == 0
                # outer ring
        assert rings.site_for(grid[0,0]) == {"south", "west"}
        assert rings.site_for(grid[1,0]) == {"west"}
        assert rings.site_for(grid[2,0]) == {"north", "west"}
        assert rings.site_for(grid[2,1]) == {"north"}
        assert rings.site_for(grid[2,2]) == {"north"}
        assert rings.site_for(grid[2,3]) == {"north", "east"}
        assert rings.site_for(grid[1,3]) == {"east"}
        assert rings.site_for(grid[0,3]) == {"south", "east"}
        assert rings.site_for(grid[0,2]) == {"south"}
        assert rings.site_for(grid[0,1]) == {"south"}
                # inner ring
        assert rings.site_for(grid[1,1]) == {"north", "west", "south"}
        assert rings.site_for(grid[1,2]) == {"north", "east", "south"}

def test4x3():
    """4x3 test"""
    grid = OblongGrid(4, 3)
    rings = ConcentricOblongs(grid)
    # print(rings.bounding_boxes)
    assert rings.bounding_boxes == ((0, 0, 3, 2), (1, 1, 2, 1))
    bbox0 = rings.bounding_boxes[0]
    bbox1 = rings.bounding_boxes[1]
    for cell in grid:
        msg = f"{cell.index} (%d, %d, %d, %d)"
        if cell in {grid[1,1], grid[2,1]}:
            assert not rings.is_on(cell, bbox0), msg % bbox0
            assert rings.is_on(cell, bbox1), msg % bbox1
            assert rings.is_inside(cell, bbox0), msg % bbox0
            assert not rings.is_inside(cell, bbox1), msg % bbox1
            assert not rings.is_outside(cell, bbox0), msg % bbox0
            assert not rings.is_outside(cell, bbox1), msg % bbox1
            assert rings.tier_for(cell) == 1
        else:
            assert rings.is_on(cell, bbox0), msg % bbox0
            assert not rings.is_on(cell, bbox1), msg % bbox1
            assert not rings.is_inside(cell, bbox0), msg % bbox0
            assert not rings.is_inside(cell, bbox1), msg % bbox1
            assert not rings.is_outside(cell, bbox0), msg % bbox0
            assert rings.is_outside(cell, bbox1), msg % bbox1
            assert rings.tier_for(cell) == 0

print("Test oblong iteration:")
print("  simple consistency tests... ", end="", flush=True)
test2x2()
test3x3()
test3x4()
test4x3()
print("pass!")

def test1():
    """test iteration"""
    print("  testing 'tier_for' [test1]... ", end="", flush=True)
    grid = OblongGrid(6,10)         # even/Even
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |' == foo[11]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |' == foo[9]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 0 |' == foo[7]

    grid = OblongGrid(10,6)         # Even/even
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 |' == foo[19]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 0 |' == foo[17]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 1 | 0 |' == foo[7] == foo[9]
    assert foo[9] == foo[11] == foo[13] == foo[15]

    grid = OblongGrid(7,10)         # odd/Even
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |' == foo[13]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |' == foo[11]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 0 |' == foo[9]
    assert foo[7] == '| 0 | 1 | 2 | 3 | 3 | 3 | 3 | 2 | 1 | 0 |'

    grid = OblongGrid(10,7)         # Even/odd
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 | 0 |' == foo[19]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 1 | 0 |' == foo[17]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 2 | 1 | 0 |' == foo[15]
    assert foo[7] == '| 0 | 1 | 2 | 3 | 2 | 1 | 0 |' == foo[13]
    assert foo[9] == foo[11] == foo[13] == foo[7]

    grid = OblongGrid(7,9)          # odd/Odd
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |' == foo[13]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |' == foo[11]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 0 |' == foo[9]
    assert foo[7] == '| 0 | 1 | 2 | 3 | 3 | 3 | 2 | 1 | 0 |'

    grid = OblongGrid(9,7)          # Odd/odd
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 | 0 |' == foo[17]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 1 | 0 |' == foo[15]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 2 | 1 | 0 |' == foo[13]
    assert foo[7] == '| 0 | 1 | 2 | 3 | 2 | 1 | 0 |' == foo[9] == foo[11]

    grid = OblongGrid(10,10)        # Even-square
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |' == foo[19]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |' == foo[17]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 0 |' == foo[15]
    assert foo[7] == '| 0 | 1 | 2 | 3 | 3 | 3 | 3 | 2 | 1 | 0 |' == foo[13]
    assert foo[9] == '| 0 | 1 | 2 | 3 | 4 | 4 | 3 | 2 | 1 | 0 |' == foo[11]

    grid = OblongGrid(9,9)          # Odd-square
    rings = ConcentricOblongs(grid)
    for cell in grid:
        cell.label = rings.tier_for(cell)
    foo = str(grid).split('\n')
    assert foo[1] == '| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |' == foo[17]
    assert foo[3] == '| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |' == foo[15]
    assert foo[5] == '| 0 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 0 |' == foo[13]
    assert foo[7] == '| 0 | 1 | 2 | 3 | 3 | 3 | 2 | 1 | 0 |' == foo[11]
    assert foo[9] == '| 0 | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 0 |'

    print("pass!")

test1()

def test2(rows, cols, tier, note, expected, at):
    """test the path maker"""
    print(f"  test pathmaker [test2({rows},{cols},{tier},{note})]... ",
           end="", flush=True)
    grid = OblongGrid(rows, cols)
    rings = ConcentricOblongs(grid)
    path = rings.pathmaker(tier)
    if path[-1] == None:
        path.pop()
    if expected == '':
        print(path)
    for n in range(len(path)):
        index = path[n]
        cell = grid[index]
        cell.label = chr(n + ord('0'))
    got = str(grid).split('\n')[at]
    if expected == '':
        print(grid)
        print(got)
    if expected != '':
        assert got == expected, f"{expected=} at {at}, {got=}"
    print("pass!")

expected = '| 4 | 5 | 6 | 7 | 8 |'
test2(5, 5, 0, "outer", expected, 1)
expected = '|   | 2 | 3 | 4 |   |'
test2(5, 5, 1, "in 1", expected, 3)
expected = '|   |   | 0 |   |   |'
test2(5, 5, 2, "inner", expected, 5)

expected = '| 5 | 6 | 7 | 8 | 9 | : |'
test2(6, 6, 0, "outer", expected, 1)
expected = '|   | 3 | 4 | 5 | 6 |   |'
test2(6, 6, 1, "in 1", expected, 3)
expected = '|   |   | 1 | 2 |   |   |'
test2(6, 6, 2, "inner", expected, 5)

expected = '| 5 | 6 | 7 | 8 | 9 |'
test2(6, 5, 0, "outer", expected, 1)
expected = '|   | 3 | 4 | 5 |   |'
test2(6, 5, 1, "in 1", expected, 3)
expected = '|   |   | 1 |   |   |'
test2(6, 5, 2, "inner", expected, 5)

expected = '| 4 | 5 | 6 | 7 | 8 | 9 |'
test2(5, 6, 0, "outer", expected, 1)
expected = '|   | 2 | 3 | 4 | 5 |   |'
test2(5, 6, 1, "in 1", expected, 3)
expected = '|   |   | 0 | 1 |   |   |'
test2(5, 6, 2, "inner", expected, 5)

def test3(rows, cols, tier, note, expected, at):
    """can we correctly identify vertices in a path?"""
    print(f"  test vertices [test3({rows},{cols},{tier},{note})]... ",
           end="", flush=True)
    grid = OblongGrid(rows, cols)
    rings = ConcentricOblongs(grid)
    path = rings.pathmaker(tier)
    for i in range(len(path)):
        index = path[i]
        if index == None:                   # careful!
            continue
        vertex = rings.is_vertex(path, i)
        cell = grid[index]
        cell.label = "*" if vertex else "."
    if expected == []:
        print(path)
        print(grid)
    else:
        foo = str(grid).split("\n")
        for i in range(len(at)):
            exp = expected[i]
            for j in at[i]:
                got = foo[j]
                assert exp==got, f"{j}: {exp=} but {got=}"
    print("pass!")

expected = ['| * | . | . | . | * |', '| . |   |   |   | . |']
test3(5, 5, 0, "outer", expected, [[1, 9], [3, 5, 7]])
expected = ['|   | * | . | * |   |', '|   | . |   | . |   |']
test3(5, 5, 1, "in 1", expected, [[3, 7], [5]])
expected = ['|   |   | * |   |   |', '|   |   |   |   |   |']
test3(5, 5, 2, "inner", expected, [[5], [1, 3, 7, 9]])

expected = ['| * | . | . | . | . | * |', '| . |   |   |   |   | . |']
test3(6, 6, 0, "outer", expected, [[1, 11], [3, 5, 7, 9]])
expected = ['|   | * | . | . | * |   |', '|   | . |   |   | . |   |']
test3(6, 6, 1, "in 1", expected, [[3, 9], [5, 7]])
expected = ['|   |   | * | * |   |   |']
test3(6, 6, 2, "inner", expected, [[5, 7]])

expected = ['| * | . | . | . | * |', '| . |   |   |   | . |']
test3(6, 5, 0, "outer", expected, [[1, 11], [3, 5, 7, 9]])
expected = ['|   | * | . | * |   |', '|   | . |   | . |   |']
test3(6, 5, 1, "in 1", expected, [[3, 9], [5, 7]])
expected = ['|   |   | * |   |   |']
test3(6, 5, 2, "inner", expected, [[5, 7]])

expected = ['| * | . | . | . | . | * |', '| . |   |   |   |   | . |']
test3(5, 6, 0, "outer", expected, [[1, 9], [3, 5, 7]])
expected = ['|   | * | . | . | * |   |', '|   | . |   |   | . |   |']
test3(5, 6, 1, "in 1", expected, [[3, 7], [5]])
expected = ['|   |   |   |   |   |   |', '|   |   | * | * |   |   |']
test3(5, 6, 2, "inner", expected, [[1, 3, 7, 9], [5]])

def test4(rows, cols, tier, reverse, rotate, expected, at, corners=True):
    """can we correctly transform a path?"""
    print(f"  test vertices [test4({rows},{cols},{tier},{reverse=}, {rotate=})]... ",
           end="", flush=True)
    grid = OblongGrid(rows, cols)
    rings = ConcentricOblongs(grid)
    path = rings.pathmaker(tier)
    path = rings.transform(path, reverse=reverse, rotate=rotate)
    for i in range(len(path)):
        index = path[i]
        if index == None:                   # careful!
            continue
        vertex = corners and rings.is_vertex(path, i)
        cell = grid[index]
        cell.label = "*" if vertex else chr(i + ord('0'))
    if expected == []:
        print(path)
        print(grid)
    else:
        foo = str(grid).split("\n")
        for i in range(len(at)):
            exp = expected[i]
            for j in at[i]:
                got = foo[j]
                assert exp==got, f"{j}: {exp=} but {got=}"
    print("pass!")

    # First we try various combinations of rotate and reverse...
print("\tpath transforms -- (a) rotations/reversals")
expected = ['| * | 5 | 6 | 7 | * |', '| * | ? | > | = | * |']
test4(5, 5, 0, False, 0, expected, [[1], [9]])          # identity
expected = ['| * | : | 9 | 8 | * |', '| * | 0 | 1 | 2 | * |']
test4(5, 5, 0, True, 0, expected, [[1], [9]])           # reverse
expected = ['| * | 4 | 5 | 6 | * |', '| 0 |   |   |   | : |',
            '| * | > | = | < | * |']
test4(5, 5, 0, False, 1, expected, [[1], [7], [9]])     # rotate
expected = ['| * | 3 | 4 | 5 | * |', '| 0 |   |   |   | 8 |',
            '| * | = | < | ; | * |']
test4(5, 5, 0, False, 2, expected, [[1], [5], [9]])     # rotate 2
expected = ['| * | ; | : | 9 | * |', '| * | 1 | 2 | 3 | * |']
test4(5, 5, 0, True, 1, expected, [[1], [9]])           # rotate, then reverse

    # next we verify that folding a degenerate path doesn't happen
print("\tpath transforms -- (b) degenerate path handling")
expected = ['|   |   | * | 1 | 2 | 3 | 4 | 5 | * |   |   |']
test4(5, 11, 2, False, 0, expected, [[5]])              # identity
test4(5, 11, 2, False, 2, expected, [[5]])              # rotate igored
expected = ["".join(reversed(expected[0]))]
test4(5, 11, 2, True, 0, expected, [[5]])               # reversal

    # now we just check a few cases
print("\tpath transforms -- (c) miscellany")
expected = ['|   | * | 2 | * |   |', '|   | 0 |   | 4 |   |',
            '|   | * | 6 | * |   |']
test4(5, 5, 1, False, 1, expected, [[3], [5], [7]])     # tier 1
expected = ['|   |   | * |   |   |']
test4(5, 5, 2, True, 1, expected, [[5]])

expected = ['| * | 1 | 2 | 3 | 4 | * |']
test4(6, 6, 0, True, 1, expected, [[11]])
expected = ['|   | * | 1 | 2 | * |   |']
test4(6, 6, 1, True, 1, expected, [[9]])
expected = ['|   |   | 0 | 1 |   |   |']
test4(6, 6, 2, True, 1, expected, [[7]], corners=False)

expected = ['| * | 1 | 2 | 3 | * |']
test4(6, 5, 0, True, 1, expected, [[11]])
expected = ['|   | * | 1 | * |   |']
test4(6, 5, 1, True, 1, expected, [[9]])
expected = ['|   |   | 1 |   |   |']
test4(6, 5, 2, True, 1, expected, [[7]], corners=False)

expected = ['| * | 1 | 2 | 3 | 4 | * |']
test4(5, 6, 0, True, 1, expected, [[9]])
expected = ['|   | * | 1 | 2 | * |   |']
test4(5, 6, 1, True, 1, expected, [[7]])
expected = ['|   |   | 1 | 0 |   |   |']
test4(5, 6, 2, True, 1, expected, [[5]], corners=False)

def test5(rows, cols, cells, expected, at):
    """can we correctly classify neighborhoods?"""
    print(f"  test neighborhoods [test5({rows},{cols}]... ",
           end="", flush=True)
    grid = OblongGrid(rows, cols)
    rings = ConcentricOblongs(grid)
    classified = {-1:'o', 0:'p', 1:'i'}
    for i in range(len(cells)):
        index = cells[i]
        cell = grid[index]
        cell.label = i
        classify = rings.classify(cell)
        for nbr in classify:
            nbr.label = classified[classify[nbr]]
    if expected:
        foo = str(grid).split('\n')
        for i in range(len(expected)):
            exp = expected[i]
            j = at[i]
            got = foo[j]
            assert exp==got, f"at {j}: {exp=}, {got=}"
    else:
        print()
        print(grid)
    print("pass!")

expected = ['| 3 | p |   | p | 2 |', '| p |   | o |   | p |',
            '|   | o | 4 | o |   |', '| p |   | o |   | p |',
            '| 0 | p |   | p | 1 |']
test5(5, 5, [(0,0), (0,4), (4,4), (4,0), (2,2)], expected, [1, 3, 5, 7, 9])
expected = ['| p | 3 | p |   | p |', '| p | i |   | i | 4 |',
            '| 2 | i |   | p | p |', '| p | i | p | 1 | o |',
            '| p | 0 | p | o |   |']
test5(5, 5, [(0,1), (1,3), (2,0), (4,1), (3,4)], expected, [1, 3, 5, 7, 9])
expected = ['| p | p | 6 | p | o |   |', '| 3 | i | i | p | 2 | o |',
            '| p |   | p |   | p | p |', '|   | o | 4 | p | i | 5 |',
            '| p |   | o |   | i | p |', '| 0 | p |   | p | 1 | p |']
test5(6, 6, [(0,0), (0,4), (4,4), (4,0), (2,2), (2,5), (5,2)], expected,
      [1, 3, 5, 7, 9, 11])
expected = []
expected = []
expected = []
expected = []
expected = []
expected = []
expected = []
expected = []
expected = []
print('SUCCESS!')

# end module tests.oblong_rings
