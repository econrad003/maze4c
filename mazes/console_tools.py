"""
print_tools.py - console display tools
Eric Conrad
Copyright ©2020 by Eric Conrad

DESCRIPTION

    This module provides some tools to facilitate working with mazes
    without using graphics tools such as the python turtle or a plotter
    library like "matplotlib".

TOOLS

    method "uncode_str"
        creates a string representation of an undirected rectangular maze.
        The maze may contain undirected passages with exits in any of the
        eight compass directions.  There is optional support for boundary
        labels.

LICENSE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Gnu
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

HISTORY

    22 Aug 2025 - Initial version
"""

from mazes.grid import Grid
from mazes.maze import Maze

S, E, N, W = ("south", "east", "north", "west")
SE, NE, NW, SW = ("southeast", "northeast", "northwest", "southwest")

posts = dict()
posts[NW], posts[N], posts[NE] = "\u250f", "\u2533", "\u2513"
posts[W], posts[0], posts[E] = "\u2523", "\u254b", "\u252b"
posts[SW], posts[S], posts[SE] = "\u2517", "\u253b", "\u251b"

links = dict()
links[N], links[W] = "\u2503", "\u2501"

def unicode_str(maze:(Maze, Grid), **kwargs):
    """produce a string representation of a rectangular maze

    POSITIONAL ARGUMENTS

        grid - a rectangular maze or grid instance

    KEYWORD ARGUMENTS

        s, e, n, w, h, v - boundary label arguments (default: None)
            The choices are:
                "A" - alphabetic labels
                "N" - numeric digit labels
                "RA" - reverse alphabetic labels
                "RN" - reverse numeric digit labels
            "RA" can be abbreviated to "R".

            Numeric digit labels run from "0" to "9".  If more than
            ten rows or columns are to receive a label, labelling
            continues with characters that follow "9".

            Alphabetic digit labels run from "A" to "Z".  If more than
            twenty-six rows or columns are to receive a label,
            labelling continues with characters that follow "Z".

            The default value (None) indicates that no labels are to
            be supplied in the indicated direction.  The lower case
            compass directions (s, e, n, w) indicate which boundaries
            are to be labelled.  The directional options h and v (for
            horizontal and vertical) can be used in lieu of pairs of
            compass directions -- h for e and w, or v for n and s.

            Labels normally run from left to right (i.e. west to east)
            and from bottom to top (south to north).

            The label options are all a single lower case letter.  The
            horizontal and the vertical options, when set, override
            any compass direction settings.

    EXAMPLES

            For a normal rectangular grid, labels are not needed:

                print(unicode_str(maze))

            For a cylindrical grid, where the east and west edges meet
            with no twist, we might label the joined edges from the
            south row upward numerically as follows:

                print(unicode_str(maze, v="N"))

            or from the north row downward:

                print(unicode_str(maze, v="NR"))

            If there are more than 10 rows, alphabetic labels might be
            preferable: 

                print(unicode_str(maze, v="A"))

            For a Moebius strip, where the east and west edges meet with
            a half twist, we would prefer labels to go in the opposite
            directions, for example:

                print(unicode_str(maze, w="NR", e="N"))
    """
    def make_labels(n:int, option:str) -> str:
        """make a row or column of labels"""
        if not option:
            return None
        first = '0' if option[0] == 'N' else 'A'
        labels = [first]
        for i in range(1, n):
            labels.append(chr(ord(labels[-1])+1))
        if option[-1] == "R":
            labels.reverse()
        return labels

    def label_line(row, col) -> str:
        """make a north or south label row"""
        if not row:
            return ""
        line = "    " if col else ""
        for label in row:
            line += f"  {label} "
        line = line[:-1] + "\n"
        return line

    grid = maze.grid if isinstance(maze, Maze) else maze

    SL, NL = kwargs.get("s"), kwargs.get("n")
    if "v" in kwargs:
        SL = NL = kwargs["v"]
    SL = make_labels(grid.n, SL)
    NL = make_labels(grid.n, NL)

    EL, WL = kwargs.get("e"), kwargs.get("w")
    if "h" in kwargs:
        EL = WL = kwargs["h"]
    EL = make_labels(grid.m, EL)
    WL = make_labels(grid.m, WL)
#    print(f"{S=}"); print(f"{E=}"); print(f"{N=}"); print(f"{W=}")

    lines = label_line(NL, bool(WL))    # top label row, if applicable
    ######################### MAZE STARTS HERE ########################
        # north fence
    line = list()
    if bool(WL):
        line.append("    ")
    line.append(posts[NW])
    corner = posts[N]
    for j in range(grid.n):
        cell = grid[grid.m-1, j]
        if cell:
            if cell[NW] and cell.is_linked(cell[NW]):
                if line[-1] == "/":
                    line[-1] = "X"          # crossing diagonal links
                else:
                    line[-1] = "\\"         # one diagonal link
            if cell[N] and cell.is_linked(cell[N]):
                line.append(f"   ")
            else:
                line.append(links[W] * 3)
            if cell[NE] and cell.is_linked(cell[NE]):
                line.append("/")
            else:
                line.append(posts[N])
        else:
            line += [links[W] * 3, posts[N]]
    if line[-1] == posts[N]:
        line.pop()
        line.append(posts[NE])
    line = "".join(line)
    lines += line + "\n"

        # all rows
    for i in range(grid.m-1, -1, -1):
            # west-to-east row
        line = list()
        if bool(WL):
            line.append(f"  {WL[i]} ")
        cell = grid[i, 0]
        if cell and cell[W] and cell.is_linked(cell[W]):
            line.append(" ")
        else:
            line.append(links[N])
        for j in range(grid.n):
            cell = grid[i, j]
            if cell:
                line.append(f" {cell.char} ")
            else:
                line.append("   ")
            if cell[E] and cell.is_linked(cell[E]):
                line.append(" ")
            else:
                line.append(links[N])
        line = "".join(line)
        if bool(EL):
            line += " " + EL[i]
        line += "\n"
        lines += line
            # south fence for row
        line = list()
        if bool(WL):
            line.append("    ")
        line.append(posts[SW] if i==0 else posts[W])
        for j in range(grid.n):
            cell = grid[i, j]
            if cell:
                if cell[SW] and cell.is_linked(cell[SW]):
                    if line[-1] == "\\":
                        line[-1] = "X"      # crossed diagonals
                    else:
                        line[-1] = "/"      # one diagonal
                if cell[S] and cell.is_linked(cell[S]):
                    line.append("   ")
                else:
                    line.append(links[W] * 3)
                if cell[SE] and cell.is_linked(cell[SE]):
                    line.append("\\")
                else:
                    line.append(posts[S] if i==0 else posts[0])
            else:
                line.append(links[W] * 3)
                line.append(posts[S] if i==0 else posts[0])
        if line[-1] == posts[0]:
            line[-1] = posts[E]
        elif line[-1] == posts[S]:
            line[-1] = posts[SE]
        line = "".join(line)
        line += "\n"
        lines += line
    ########################## MAZE ENDS HERE #########################
    lines += label_line(SL, bool(WL))   # bottom label row, if applicable
    lines = lines[:-1]              # throw away trailing newline
    return lines

# end console_tools.py
