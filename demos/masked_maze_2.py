"""
demos.masked_maze_2 - a fancier demonstration of masking
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
from PIL import Image

import mazes
from mazes.Grids.oblong import OblongGrid
from mazes.Grids.oblong8 import MooreGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson

        # maze carving

def make_grid(GridType, rows, cols, *args, **kwargs):
    """make a Von Neumann grid"""
    print(f"Maze({GridType.__name__}{(rows,cols,'*')}")
    return Maze(GridType(rows, cols, *args, **kwargs))

def mask_grid(grid:'Grid', mask:list):
    """hide cells"""
    masked = 0                  # number of masked cells
    errors = 0                  # inaccessibles
    cells = len(maze.grid)      # number of cells
    max_row = len(mask) - 1
    if cells < 1:
        raise ValueError("no cells in grid!")
    i = 0                       # row number
    for row in mask:
        j = 0                       # column number
        for ch in row:
            cell = grid[max_row-i, j]
            if cell:
                if ch in {'X', 'x'}:
                    cell.hide()
                    masked += 1
            else:
                errors += 1
                if errors == 1:
                    print(f"WARNING: first mask error at grid[{(i,j)}]")
            j += 1
        i += 1
    print(f"{cells} cells: {masked} hidden, {cells-masked} revealed")
    if errors > 0:
        print(f"WARNING: The mask is larger than the grid.  ({errors} errors)")
    if masked < 1:
        raise ValueError("no cells were hidden.")
    if masked >= cells:
        raise ValueError("all cells were hidden.")

def grid_is_connected(grid:'Grid') -> int:
    """returns True if the grid is connected"""
    unvisited = list(grid)
    stack = list()                  # DFS
    stack.append(unvisited[-1])
    unvisited = set(unvisited)
    while stack:
        cell = stack.pop()
        if cell in unvisited:
            for nbr in cell.neighbors:
                if nbr in unvisited:
                    stack.append(nbr)
            unvisited.remove(cell)
    return len(unvisited) == 0

def carve_maze(Algorithm:'Algorithm', maze:Maze, *args, **kwargs):
    """carve the result"""
    print(Algorithm.on(maze, *args, **kwargs))

        # masking
from mazes.tools.image_to_mask import image_open, image_threshold_mask, image_mask

def open_image(filename:str) -> Image:
    """returns a PIL image object"""
    return image_open(filename, debug=True)

def threshold_mask(filename:str, start:tuple, step:tuple,
                   minvalues:tuple, AND:bool) -> (int, int, tuple):
    """create a 0/1 threshold mask

    Returns rows, cols, mask
    """
    img = open_image(filename)
    mask = image_threshold_mask(img, start, step, minvalues, AND=AND, debug=True)
    rows = len(mask)
    cols = len(mask[0])
    return rows, cols, mask    

def text_mask(filename:str, start:tuple, step:tuple,
              minvalues:tuple, AND:bool) -> (int, int, str):
    """returns rows and columns and a text mask (spaces or 'X')"""
    img = open_image(filename)
    return image_mask(img, start, step, minvalues, AND=AND, debug=True)

def read_mask(filename:str) -> str:
    mask = list()
    fp = open(filename, "r")
    content = fp.read()
    fp.close()
    return content

def is_mask_file(filename:str) -> bool:
    """returns true if the indicated file is a text mask

    The file is assumed to be a text mask if the extension is '.txt',
    '.msk', or '.mask'.
    """
    x4 = filename[-4:]
    x5 = filename[-5:]
    return x4 in ('.txt', '.msk') or x5 in ('.mask', )

def parse_args(argv):
    """main entry point for the demo"""
    import sys
    import argparse
    print(argv)

    DESC = "a fancier masked maze demo"
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("-s", "--start", type=int, nargs=2, \
        default=(3, 3), metavar=("X0", "Y0"), \
        help="start coordinates (default: 3, 3).  Ignored if a text mask" \
        + " is provided as input.")
    parser.add_argument("-t", "--step", type=int, nargs=2, \
        default=(5, 5), metavar=("H", "K"), \
        help="step offsets (default: 5, 5).  Ignored if a text mask" \
        + " is provided as input.")
    parser.add_argument("-r", "--red", type=int, default=50, \
        help="minimum red value for revealed cells (default: 50). To" \
        + " change the direction of the comparison, use a negative" \
        + " integer.")
    parser.add_argument("-g", "--green", type=int, default=0, \
        help="minimum green value for revealed cells (default: 0). To" \
        + " change the direction of the comparison, use a negative" \
        + " integer.")
    parser.add_argument("-b", "--blue", type=int, default=0, \
        help="minimum blue value for revealed cells (default: 0). To" \
        + " change the direction of the comparison, use a negative" \
        + " integer.")
    parser.add_argument("--OR", action="store_true", \
        help="The default is to accept a pixel if all three conditions" \
        + " are met.  Set this option to accept if at least one condition" \
        + " is satisfied.  If this option is set and a value for -r, -g," \
        + " -b is 0, that value will be changed to 256 to force that" \
        + " comparison to fail.")
    parser.add_argument("input", type=str, \
        help="image or text file input (required). If the file is a text" \
        + " file, the first row will determine the number of columns and" \
        + " the file should consist of one or more rows of spaces and 'X'" \
        + " characters.  If the file is an image file, the mask will be" \
        + " produced using the start, stop, and minvalues specifications." \
        + "  Text files must have one of the following extensions: '.txt'," \
        + " '.mask' or '.msk'.")
    parser.add_argument("output", type=str, nargs="?", \
        help="an optional text file (optional).  If provided, this will be" \
        + " a text mask.")
    mazegrp = parser.add_argument_group("Maze Arguments", \
        description="These arguments are used to create a maze from the" \
        + "image or the mask that was supplied as input.  They are ignored" \
        + " if an output mask is specified.")
    mazegrp.add_argument("-M", "--Moore", action="store_true", \
        help="if set, a Moore grid (8 compass neighbors) will be used.  If" \
        + " it is not set (default), the usual Von Neumann neighborhood (4" \
        + " compass neighbors) will be used.")
    mazegrp.add_argument("-A", "--Algorithm", type=str, default="w", \
        help="carving algorithm.  Permissible entries are 'w' (Wilson's" \
        + " algorithm), 'd' (DFS), 'b' (BFS), and 'k' (Kruskal's algorithm)." \
        + "  Wilson's algorithm cannot be used if the revealed part of the" \
        + " grid is not connected.")
    mazegrp.add_argument("-o", "--graphics", type=str, default=None, \
        help="optional filename for graphics output, e.g. 'foo.png'")
    plotgrp = parser.add_argument_group("Plot Arguments", \
        description="These arguments are change the plot configuration.")
    plotgrp.add_argument("--figure", type=float, nargs=3, default=None, \
        metavar=("W", "H", "DPI"), help="sizing hints")
    plotgrp.add_argument("--title", type=str, default=None, \
        help="plot title")
    args = parser.parse_args(argv)
    print(args)
    from_text_mask = is_mask_file(args.input)
    to_text_mask = bool(args.output) and is_mask_file(args.output)
    if args.output:
        assert not from_text_mask, "image input expected"
        assert to_text_mask, "mask output expected"
    if args.OR:
        if args.red == 0:
            args.red = 256
            print("WARNING: changed '-r 0' to '-r 256'. (with '--OR')")
        if args.green == 0:
            args.green = 256
            print("WARNING: changed '-g 0' to '-g 256'. (with '--OR')")
        if args.blue == 0:
            args.blue = 256
            print("WARNING: changed '-b 0' to '-b 256'. (with '--OR')")
    minvalues = (args.red, args.green, args.blue)
    op = "OR" if args.OR else "AND"
    op2 = "ANY" if args.OR else "ALL"
    compR = f"R ≥ {args.red}" if args.red >= 0 else f"R ≤ {abs(args.red)}"
    compG = f"G ≥ {args.green}" if args.green >= 0 else f"G ≤ {abs(args.green)}"
    compB = f"R ≥ {args.blue}" if args.blue >= 0 else f"R ≤ {abs(args.blue)}"
    print(f"threshold mask: {op2}{minvalues}")
    print(f"\t{compR} {op} {compG} {op} {compB}")
    print(f"{from_text_mask=}, {to_text_mask=}")
    if from_text_mask:
        mask = read_mask(args.input)
        mask = mask.splitlines()
        rows = len(mask)
        cols = len(mask[0])
    else:
        rows, cols, mask = text_mask(args.input, args.start, args.step,
                                     minvalues, not args.OR)
        mask = mask.splitlines()
    if to_text_mask:
        with open(args.output, "w") as fp:
            for line in mask:
                fp.write(f"{line}\n")
        print(f"wrote mask: {args.output} ({rows} rows, {cols} columns)")
        sys.exit()              # that's all, folks!
    return args, rows, cols, mask

if __name__ == "__main__":
    import sys
    args, rows, cols, mask = parse_args(sys.argv[1:])
    GridType = MooreGrid if args.Moore else OblongGrid
    title = "Moore (8 neighbors)" if args.Moore else "Von Neumann (4 neighbors)"
    title += " / "
    maze = make_grid(GridType, rows, cols)
    mask_grid(maze.grid, mask)
    Algorithm = args.Algorithm[0].lower()
    if grid_is_connected(maze.grid):
        print('The revealed cells form a connected set.  (Good!)')
    else:
        print("The revealed cells do not form a connected set.  (Not good!)")
        if Algorithm == 'w':
            raise ValueError("Wilson's algorithm not valid for disconnected grid.")
    if Algorithm == 'w':
        from mazes.Algorithms.wilson import Wilson
        carve_maze(Wilson, maze)
        title += "Wilson"
    elif Algorithm == 'd':
        from mazes.Algorithms.dfs_better import DFS
        carve_maze(DFS, maze)
        title += "DFS"
    elif Algorithm == 'b':
        from mazes.Algorithms.bfs import BFS
        carve_maze(BFS, maze)
        title += "BFS"
    else:       # Algorithm == 'k':
        from mazes.Algorithms.kruskal import Kruskal
        carve_maze(Kruskal, maze)
        title += "Kruskal"
    # print(maze)
    if GridType == MooreGrid:
        from mazes.Graphics.moore import Huntsman as Arachnid
    else:
        from mazes.Graphics.oblong1 import Pholcidae as Arachnid
    print("Rendering graphics...")
    spider = Arachnid(maze)
    colorings = dict()
    for cell in maze.grid._cells:
        if cell.hidden:
            cell.reveal()
            colorings[cell] = (0.75, 0, 0)
    spider.setup(fillcolors=colorings)
    spider.title(args.title if args.title else title)
    if args.figure:
        width, height, dpi = args.figure
        dpi = int(dpi)
        if width > 1 and height > 1:
            spider.fig.set_size_inches(width, height)
        if dpi > 70:
            spider.fig.set_dpi(dpi)
    spider.draw_maze()
    spider.fig.tight_layout()
    if args.graphics:
        print(f"Saving to {args.graphics}")
        spider.save_image(args.graphics)
    spider.show()

# end module demos.masked_maze
