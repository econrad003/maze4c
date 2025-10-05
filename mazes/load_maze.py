"""
mazes.load_maze - load a maze from a file
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION
    The maze must be initialized and configured.  The method can give
    give a hint (if maze is set to None) or it can create the edges
    and arcs. 

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
import csv
from ast import literal_eval
from mazes.maze import Maze

def load_from(filename:str, maze:Maze=None, evaluate:callable=literal_eval):
    """save a maze to a file

    If maze is None, a hint for maze creation will be displayed.

    If the cell indices are strings instead of integers or tuples,
    set evaluate to str.  The default is literal_eval:
        literal_eval('1') == 1              (int)
        literal_eval('(1)') == 1            (int)
        literal_eval('(1,)') == (1,)        (tuple)
        literal_eval('(1,2)') == (1,2)      (tuple)
    """
    assert isinstance(filename, str)
    if not isinstance(maze, Maze):
        if maze == None:
            print(f"maze = Maze({hint_from(filename)})")
            return
        raise TypeError("Maze instance or None is required")
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        cells = dict()
        for row in reader:
            if row[0] == "cell":
                i = int(row[1])
                index = evaluate(row[2])
                # print(f"cell {i}:{type(i)} {index=}:{type(index)})")
                cells[i] = maze.grid[index]
                # print(cells[i])
            elif row[0] == "edge":
                cell1 = cells[int(row[1])]
                cell2 = cells[int(row[2])]
                try:
                    w = int(row[3])
                except ValueError:
                    w = float(row[3])
                maze.link(cell1, cell2, weight=w)
            elif row[0] == "arc":
                cell1 = cells[int(row[1])]
                cell2 = cells[int(row[2])]
                try:
                    w = int(row[3])
                except ValueError:
                    w = float(row[3])
                maze.link(cell1, cell2, weight=w, directed=True)
                
    # end method savemaze

def hint_from(filename:str):
    """display instructions for creating the maze"""
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        Gridtype = "UnknownType"
        args = list()
        kwargs = dict()
        for row in reader:
            if row[0] == "cls":
                Gridtype = row[1]
            elif row[0] == "arg":
                args.append(row[1])
            elif row[0] == "kwarg":
                kwargs[row[1]] = row[2]
        s = Gridtype + "("
        for arg in args:
            s += arg + ", "
        for kw in kwargs:
            s += kw + "=" + kwargs[kw] + ", "
        if s[-1] != "(":
            s = s[:-2]
        s += ")"
        return s

# end module mazes.load_maze
