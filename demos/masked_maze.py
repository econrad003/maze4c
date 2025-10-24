"""
demos.masked_maze - demonstrate masking
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module demonstrates masking.

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
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson

from mazes.tools.image_to_mask import image_open, image_threshold_mask

if __name__ == "__main__":
        # open the image file
    img = image_open("demos/mask1.png", debug=True)

        # create a 0/1 threshold mask
    start = (3, 3)
    step = (10, 10)
    minvalues = (50, 0, 0)
    mask = image_threshold_mask(img, start, step, minvalues, debug=True)

        # create the grid and maze objects
    rows = len(mask)
    cols = len(mask[0])
    grid = OblongGrid(rows, cols)
    maze = Maze(grid)
    for i in range(rows):
        for j in range(cols):
            if mask[rows-i-1][j] == 0:
                grid[i,j].label = "X"           # label the masked cells
                grid[i,j].hide()                # hide the masked cells

        # print a note of explanation (this is a demo!)
    print("The hidden cells are labelled 'X'.  The carving algorithm avoids")
    print("the hidden cells.  (CAUTION: Wilson's algorithm will fail if the")
    print("revealed cells do not form a connected set.)")

        # carve the maze using only the revealed cells
    print(Wilson.on(maze))

        # display the result
    print(maze)

# end module demos.masked_maze
