"""
mazes.tetris.tetris - a bag of Tetris tiles
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    To weight shapes equally, ignoring rotations:
        from mazes.tetris.tetris import shapes, create_tile

    To weight each configuration equally:
        from mazes.tetris.tetris import configs, create_tile

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

from mazes.tetris.tile import Tile
    
n = 4                           # each tile has four cells

    # directions on the 4-connected rectangular grid
N, S, E, W = "north", "south", "east", "west"

        # configurations
        #   these are oriented so that the southeastmost cell is
        #   cell number 0.  When southmost and eastmost conflict,
        #   southmost is given preference.
        #
        # bounding box
        #   The configuration matrix has the following form:
        #       (shape_descriptor, (width, height, zero))
        #   where zero locates the 0 cell in the bottom row.

            #   3 2     1 2      2 3      3|2
            #  ---                ---
            #   0 1     0|3      0 1      0 1
            #            
            #   The O cells are distinguished by the location of
            #   the missing edge.  Here we marrk this with a bar.
O1 = (((0, E, 1), (1, N, 2), (2, W, 3)),    (2, 2, 0))
O2 = (((0, N, 1), (1, E, 2), (2, S, 3)),    (2, 2, 0))
O3 = (((0, E, 1), (0, N, 2), (2, E, 3)),    (2, 2, 0))
O4 = (((0, E, 1), (1, N, 2), (0, N, 3)),    (2, 2, 0))
    # ----------descriptor-------------     ---bbox---

            #   3       2      213      2
            #  012     31       0       13
            #           0               0
T1 = (((0, W, 1), (1, W, 2), (1, N, 3)),    (3, 2, 0))
T2 = (((0, N, 1), (1, N, 2), (1, W, 3)),    (2, 3, 1))
T3 = (((0, N, 1), (1, W, 2), (1, E, 3)),    (3, 2, 1))
T4 = (((0, N, 1), (1, N, 2), (1, E, 3)),    (2, 3, 0))
    # ----------descriptor-------------     ---bbox---

            #     3    32       123     3
            #   012     1       0       2
            #           0               01
L1 = (((0, E, 1), (1, E, 2), (2, N, 3)),    (3, 2, 0))
L2 = (((0, N, 1), (1, N, 2), (2, E, 3)),    (2, 3, 1))
L3 = (((0, N, 1), (1, E, 2), (2, E, 3)),    (3, 2, 0))
L4 = (((0, E, 1), (0, N, 2), (2, N, 3)),    (2, 3, 0))
    # ----------descriptor-------------     ---bbox---

            #   3       2     321       23
            #   012     1       0       1
            #          30               0
M1 = (((0, E, 1), (1, E, 2), (0, N, 3)),    (3, 2, 0))
M2 = (((0, N, 1), (1, N, 2), (0, W, 3)),    (2, 3, 1))
M3 = (((0, N, 1), (1, W, 2), (2, W, 3)),    (3, 2, 2))
M4 = (((0, N, 1), (1, N, 2), (2, E, 3)),    (2, 3, 0))
    # ----------descriptor-------------     ---bbox---


            # horizontal or vertical chain
I1 = (((0, E, 1), (1, E, 2), (2, E, 3)),    (4, 1, 0))
I2 = (((0, N, 1), (1, N, 2), (2, N, 3)),    (1, 4, 0))
    # ----------descriptor-------------     ---bbox---

            #   32       3
            #    01     12
            #           0
Z1 = (((0, E, 1), (0, N, 2), (2, W, 3)),    (3, 2, 1))
Z2 = (((0, N, 1), (1, E, 2), (2, N, 3)),    (2, 3, 0))
    # ----------descriptor-------------     ---bbox---

            #     23   3
            #    01    21
            #           0
S1 = (((0, E, 1), (1, N, 2), (2, E, 3)),    (3, 2, 0))
S2 = (((0, N, 1), (1, W, 2), (2, N, 3)),    (2, 3, 1))
    # ----------descriptor-------------     ---bbox---


        # shapes

O = [O1, O2, O3, O4]
T = [T1, T2, T3, T4]
L = [L1, L2, L3, L4]
M = [M1, M2, M3, M4]
I = [I1, I2]
Z = [Z1, Z2]
S = [S1, S2]

shapes = tuple(tuple(x) for x in [O, T, L, M, I, Z, S])
configs = tuple(O + T + L + M + I + Z + S)

def create_tile(descriptor, N=n):
    """create tile from a shape descriptor/bbox pair"""
    shape, box = descriptor                 # unpack
    width, height, zero_locator = box               # unpack
    bbox = (width, height)                  # repack
    return Tile(N, shape, bbox=bbox, zero=zero_locator)
