"""
mazes.save_maze - save a maze to a file
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

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
from mazes.maze import Maze
from mazes.edge import Edge
from mazes.arc import Arc

def save_to(maze:Maze, filename:str, overwrite:bool=False):
    """save a maze to a file"""
    assert isinstance(maze, Maze)
    grid = maze.grid
    print(f"Saving maze to : {filename}")
    Gridtype = grid._cons["cls"]
    gridargs = grid._cons["args"]
    gridkwargs = grid._cons["kwargs"]
    print(f"Grid type: {Gridtype}")
    print("positional arguments:", f"{gridargs}")
    print("keyword arguments:", f"{gridkwargs}")
    print("gathering information:")
    print("\tcells...", end='')
    cells = dict()
    indices = dict()
    refs = set()
    n = 0
    for cell in grid:
        cells[cell] = n
        indices[n] = cell
        n += 1
    print(f" {n} cells")
    print("\tjoins...", end='')
    edges = dict()
    arcs = dict()
    weights = dict()
    e = 0
    for join in maze:
        cell1, cell2 = join
        if isinstance(join, Edge):
            edges[e] = (cell1, cell2)
        elif isinstance(join, Arc):
            arcs[e] = (cell1, cell2)
        else:
            raise TypeError("join must be Edge or Arc")
        refs.add(cell1)
        refs.add(cell2)
        weights[e] = join.weight
        e += 1
    print(f" {e} joins ({len(edges)} edges, {len(arcs)} arcs)")
    print("Saving...")
    opentype = "w" if overwrite else "x"
    with open(filename, opentype, newline='') as csvfile:
        fieldnames = ["op", "A", "B", "C"]
        writer = csv.DictWriter(csvfile, delimiter="|", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"op":"cls", "A":Gridtype})
        for arg in gridargs:                # positional arguments
            writer.writerow({"op":"arg", "A":arg})
        for kw in gridkwargs:               # keyword arguments
            writer.writerow({"op":"kwarg", "A":kw, "B":gridkwargs[kw]})
        for i in range(n):
            cell = indices[i]
            if cell not in refs:
                continue
            writer.writerow({"op":"cell", "A":i, "B":cell.index})
        for edge in edges:
            cell1, cell2 = edges[edge]
            j1, j2 = cells[cell1], cells[cell2]
            w = weights[edge]
            writer.writerow({"op":"edge", "A":j1, "B":j2, "C":w})
        for arc in arcs:
            cell1, cell2 = arcs[arc]
            j1, j2 = cells[cell1], cells[cell2]
            w = weights[arc]
            writer.writerow({"op":"arc", "A":j1, "B":j2, "C":w})
    # end method save_to

# end module mazes.save_maze
