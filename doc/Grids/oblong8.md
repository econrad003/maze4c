# The 8-connected rectangular grid

The usual rectangular or oblong grid uses a Von Neumann or 4-neighborhood of a cell.  The interior cells have neighbors to the south, east, north and west.  if we add in the nearest cells on the diagonals, we have Moore or 8-neighborhoods of each interior cell.  Instead of treating the cells as square, we think of them as regular octagons even though the plane cannot actually be tiled by regular octagons.

The implementation is class *MooreGrid* in module *oblong8.py* located in the *mazes/Grids* folder.  We may variously refer to this class of grids as Moore grids, rectangular Moore grids, 8-grids, rectangular 8-grids, and 8-connected rectangular grids.

The constructor takes the numbers of rows and columns, and an optional keyword argument *configure* which we use to create several subgrid classes.

## CONTENTS

1. Algorithms (with examples)
2. Paradoxes
3. Demonstration module
4. Graphics

## 1 - Algorithms

   Any method that is designed for a Von Neumann rectangular grid can be used to carve a maze on a Moore grid, but, if our desire is to produce perfect mazes (*i.e.* spanning trees), there is not much point in that. The more general algorithms can, of course, be used.  We will consider the uniform maze algorithms (Aldous/Broder and Wilson), depth-first search, and Kruskal's algorithm.

## Example 1.1 - Aldous/Broder

Aldous/Broder generally performs reasonably on the 4-grid small enough to fit on an 80x25 console display -- roughly the same on the 8-grid.  The additional grid connections don't make it much harder to complete the random walk.

We start, of course, by importing a few things:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong8 import MooreGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
```

Next we create the maze and run Aldous/Broder:
```
>>> maze = Maze(MooreGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     3087
                             cells      150
                          passages      149
                     starting cell  (4, 8)
```

Here is the resulting maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |   |   |       |       |       |   |   |   |
+---/---X---+---/---+   +   +---/---+---\---\---+---X   +   +
|   |       |   |   |       |   |   |   |       |   |       |
+---/---+---/   +---X   +---+---\---X---+---/---/---/---+   +
|           |       |   |       |       |       |   |   |   |
+---+---/   +---/   \---+   +   +---+---+---\---+   /---+---+
|   |   |   |   |   |   |   |       |       |   |   |       |
+---X---\---+---+---+---+---\---+   /---+---+---/   \---/   +
|   |   |       |   |   |       |   |       |   |   |   |   |
+   /---+---+---\---X---\---/   \---/---/---\---+---\---\---+
|       |       |   |   |   |   |   |   |   |   |       |   |
+---+---+---/---+   +   /---/---+---+---/---/---\---\---+---+
|       |   |   |   |   |           |   |   |   |   |       |
+---/   \   /---\---\---+---\---+   +---X   X---+---\   +   +
|   |   |       |   |       |   |   |   |   |   |   |   |   |
+---+---+---/   \---\   +---+---+---/---+---/   \---\---+---+
|   |   |   |   |   |   |       |       |   |   |           |
+   \   X---+---+---/---/---/---/---+---+---/   +---\---+---+
|   |   |   |           |   |           |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The slashes and backslashes represent northeastward and northwestward passages, respectfully.  If both are present from a cell, the passage crossing is represented by a capital X.  (This particular run produced 8 passage crossings.)

### Example 1.2 - Wilson's algorithm

Wilson's algorithm offers no unpleasant surprises on the 8-grid.  We start with an import:
```
>>> from mazes.Algorithms.wilson import Wilson
```

Next we create the grid and run Wilson:
```
>>> maze = Maze(MooreGrid(10, 15))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       77
                             cells      150
                          passages      149
                 paths constructed       77
                     cells visited      637
                          circuits      133
                    markers placed      427
                   markers removed      278
                     starting cell  (5, 11)
```
This run was uneventful.  Here is the maze:

```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |   |   |   |   |   |           |   |
+---+   +---+   +---+---\---X---/---\---X---+---X---+---/---+
|                       |       |   |   |   |   |       |   |
+---+---\---+   \---+---\---\---+---X---+---X---+---+---\   +
|   |   |   |   |   |       |   |   |       |   |   |   |   |
+---\   +---+   +---+   \---+   +---+---+---+   /---/   +   +
|           |   |   |   |       |       |   |   |   |   |   |
+   +---+---\---/---+---/---\---+---/---+   /---+---+   /---+
|       |   |       |   |   |   |   |           |   |   |   |
+---+---+---\   +   /---/---/---\---\---+---X---/---/---+   +
|   |       |   |       |   |   |   |       |               |
+   +   +---+---+   +   +---\---\---\---+---+---/   \---+---+
|   |       |   |   |   |   |   |       |       |   |   |   |
+---\   \---/---+---+   +---\---+---+---/---/---+---\---+   +
|   |   |   |       |   |           |   |   |       |   |   |
+   /   +---+---\---\---\---+---+   /---\---\---+---\---\   +
|   |           |   |   |   |       |   |   |   |   |   |   |
+---+---/---\---+---/   X---\   +   /---+---+---\   X---+---+
|           |       |   |   |   |               |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Again there were 8 crossing diagonal passages...

### Example 1.3 - Depth-first search

Because there are more connections than in the 4-grid, we would expect to go deeper before we are blocked.

```
>>> from mazes.Algorithms.dfs_better import DFS
>>> maze = Maze(MooreGrid(10, 15))
>>> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits      299
                        start cell  (3, 1)
               maximum stack depth       93
                             cells      150
                          passages      149
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |       |   |       |               |   |   |
+   +---+---/---X---+---X   +---\---X---+---/---+---\---X   +
|   |       |       |   |   |   |   |   |   |       |   |   |
+   \---\---+---+---+   +---/---\---+---+---\   +---\---+   +
|   |   |   |   |       |   |   |           |   |       |   |
+   +---X---/---/---+---+   /---\---+---+   +   +   +---+---+
|   |   |   |       |   |   |   |   |   |   |   |   |       |
+   +   +   +---+   +   \---/---+   +   \   +   +---\---X---+
|   |   |       |   |   |   |       |   |   |   |   |   |   |
+---+   +---/---+   +   +---/---+---+   +---+---/---\---X---+
|       |       |   |   |   |       |       |       |   |   |
+---\---+   +   /---+---\---X---+   \---+   +---+   +---/---+
|   |   |   |   |   |   |   |       |   |   |   |   |   |   |
+   +---+---\---+   X---\---+---+---+---X---/   /---+---X---+
|           |   |   |   |               |   |   |   |   |   |
+---+---\---+   +   +---\---+---+---+---+---+---/---X---X---+
|       |   |   |   |   |   |   |   |       |   |   |   |   |
+---\---X---+---X---X---\---X   +   /   +---+---X---+---/   +
|       |       |   |   |   |   |   |           |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Here we have 17 diagonal passage crossings.  The maximum stack depth tells us that the longest path has 93 cells and 92 passages giving us a diameter of 92.  

### Example 1.4 - Kruskal's algorithm

We start in the usual way:
```
>>> from mazes.Algorithms.kruskal import Kruskal
>>> maze = Maze(MooreGrid(10, 15))
>>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      277
                 components (init)      150
               queue length (init)      527
                             cells      150
                          passages      149
                components (final)        1
              queue length (final)      250
```
Nothing alarming in these statistics... And here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |       |           |   |       |       |   |
+---+---+   /   +---+   X---+   +---/---+---\---\---/---\   +
|   |   |   |       |   |   |   |   |       |   |   |   |   |
+---X---/   +---+   +---+---\---+---\---/   /---+   X---+   +
|   |   |       |   |   |           |   |       |   |   |   |
+   /---+---\---+---+---\   +---/---+---\---+---+---+---+---+
|   |   |   |           |   |       |       |       |       |
+---+   +---\   +---X---\---+   +---X---X---X---+---/---+   +
|       |       |   |   |   |   |   |   |   |       |   |   |
+---/---\---/   +---+---+   \---/---+---+---\---\---+---X---+
|   |       |   |       |   |       |   |   |   |   |   |   |
+---+---+   +---+---+   /---+---+---/---\   /---+   \---/   +
|   |   |           |   |   |   |   |           |   |   |   |
+---\   \   +---/---+---\---X---+---+---+---/---\---+---+---+
|       |   |       |   |   |                   |   |   |   |
+---/---\---+---X---\   +---+---+   +   \---+---/   /---X---+
|   |   |   |   |   |   |   |       |   |   |   |   |       |
+---+   +---/---X---+   +   \---+---+   \---\---+---+   +---+
|           |   |   |       |   |       |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## 2 - Paradoxes (or how grids break reality)

### Example 2.1 - Moore grid - a simple circuit with a leak

A simple circuit in a Moore grid does not necessarily disconnect the grid.  (A  circuit in the plane does disconnect the plane.)  In the illustration below, our circuit consists of the cells labelled "C" and the indicated passages.  The hashed cell in the physical center of the circuit has four neighboring cells which are physically outside the circuit.  Thus, in the sense of Moore neighborhoods, the pictured circuit doesn't actually have an inside.

```
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   | C |   |   |
+---+---/---\---+---+
|   | C | # | C |   |
+---+---\---/---+---+
|   |   | C |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
```
This particular example does not apply in the Von Neumann grid as the four cells labelled "C" do not form a circuit.  (They are not adjacent.)

Note that the issue here arises because of crossing diagonal edges.  If we eliminate either the descending diagonals (slope -1) or the ascending diagonals (slope 1), the paradox disappears.

### Example 2.2 - Von Neumann grid - a simple circuit with two insides

The Von Neumann neighborhood system creates a different paradox.  Pictured below left is a simple circuit in a Von Neumann 4-grid.  The two hashed cells are indeed inside the circuit and the unlabelled cells form a connected outside.

The paradox is that the inside is not connected -- with a single simple circuit, we created not one, but two holes.

This example does not apply in the Moore grid because, although the indicated walk is a circuit, it is not a simple circuit.  The figure on the right shows a diagonal passage between two cells in the circuit that separates the two cells.
```
+---+---+---+---+---+---+    +---+---+---+---+---+---+
|   |   |   |   |   |   |    |   |   |   |   |   |   |
+---+---+---+---+---+---+    +---+---+---+---+---+---+
|   |   | C - C - C |   |    |   |   | C - C - C |   |
+---+---+-|-+---+-|-+---+    +---+---+-|-+---+-|-+---+
|   | C - C | # | C |   |    |   | C - C |   | C |   |
+---+-|-+---+---+-|-+---+    +---+-|-+---\---+-|-+---+
|   | C | # | C - C |   |    |   | C |   | C - C |   |
+---+-|-+---+-|-+---+---+    +---+-|-+---+-|-+---+---+
|   | C - C - C |   |   |    |   | C - C - C |   |   |
+---+---+---+---+---+---+    +---+---+---+---+---+---+
|   |   |   |   |   |   |    |   |   |   |   |   |   |
+---+---+---+---+---+---+    +---+---+---+---+---+---+
```

## 3 - Demonstration module

There is a demonstration module which can produce sample Moore Grid mazes (console and/or graphics) using Wilson's algorithm, Kruskal's algorithm, DFS, or BFS.  The module is *demos.moore\_maze*.  A sample PNG file may be found in the *gallery* folder as *gallery/Moore\_grid\_Wilson.png*. This is a weave maze...

(A weave maze is a maze in which passages may go under cells or other passages.  With Moore neighborhoods, diagonal passages may cross.  The convention used in the graphics program is that northeast-bound passages go under northwest-bound passages. In the console display, crossing passages are displayed as a capital "X".)

Here is the console display version of the gallery maze *Moore\_grid\_Wilson*:

```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |   |   |   |       |   |       |   |   |
+   \---/---+   +   \   +   \---X---+---X---+---\   +
|   |   |       |   |       |   |       |   |   |   |
+---\---+   +   +   +---+---+---\---+---/---/   X---+
|   |       |       |   |       |   |   |   |   |   |
+---\---+   +---/   +   +---/---+---/   +---+   +---+
|       |   |   |   |   |           |   |   |   |   |
+---\---+---+   \---+   /---+---+---\---+   /   +   +
|           |   |   |   |       |   |       |   |   |
+   +---+---+---/---+---/---+   /---\---+   +---/---+
|           |   |   |   |       |   |   |       |   |
+---\---+   /---/   /   \---+---+---\---+   +---X   +
|   |   |   |   |   |   |           |   |   |   |   |
+   \---/---\---X---+---/   +---/---/---X---+---+   +
|   |       |   |   |   |   |   |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Note the crossing passages northeast and northwest, respectively, from the fourth and fifth cells in the bottom row.  The passage northeast from the fourth cell tunnels under the passage northeast from the fifth cell.

Now let's look at how to use the demo...

### Example 3.1 - Help

To get printed help, use the help option:

```
$ python -m demos.moore_maze -h
usage: moore_maze.py [-h] [-d ROWS COLS] [-a ALGORITHM] [-c] [--coff] [-p PEN]
                     [-o OUTPUT] [-t TITLE] [--goff] [-v]

Moore grid maze demonstration

options:
  -h, --help            show this help message and exit
  -d ROWS COLS, --dim ROWS COLS
                        the numbers of rows and columns in the maze. (Default:
                        (8, 13).)

maze options:
  -a ALGORITHM, --algorithm ALGORITHM
                        The algorithm used to carve the maze. The choices are
                        w-Wilson (default), k-kruskal, d-dfs, b-bfs.

display options:
  -c, --console         display to console even if the maze is larger than
                        10x19.
  --coff                omit display to console for mazes no larger than
                        10x19.

graphics options:
  -p PEN, --pen PEN     The pen color. (Default: black.)
  -o OUTPUT, --output OUTPUT
                        An image file for the output, e.g. foo.png. (Default:
                        None.)
  -t TITLE, --title TITLE
                        A title for the maze.
  --goff                Don't display the graphics. The graphics are drawn
                        regardless. A warning will be displayed if this
                        optionis set and not output is requested.

control options:
  -v, --verbose         display the arguments and the output from argparse.
```

The Python module option (*-m*) is required here and comes before the module name.

The *-h* or *--help* option displays the help message and exits.

If the maze has more than 10 rows or more than 19 columns, it is normally not displayed on the console.  To suppress the display of smaller mazes, use the *--coff* option.  To force the console display even if the maze is too large, use the *-c* or the *--console* option.

The verbose option (*-v* or *--verbose*) displays the command line options and the parsed options, for example:
```
$ python -m demos.moore_maze -v --coff --goff
command line input:
    argv=['-v', '--coff', '--goff']
argparse output:
    args=Namespace(dim=(8, 13), algorithm='w', console=False, coff=True, pen='black', output=None, title='Moore neighborhood maze', goff=True, verbose=True)
```
The *--coff* and *--goff* options turned of the console and GUI displays, but they didn't stop maze creation.  Here is the rest of the console output:
```
WARNING: Algorithm class set to default (Wilson's algorithm).
WARNING: No gui and no output!
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       51
                             cells      104
                          passages      103
                 paths constructed       51
                     cells visited      376
                          circuits       71
                    markers placed      254
                   markers removed      151
                     starting cell  (2, 4)
```

### Example 3.2 - Running the demo

We will create an 11x18 maze with console and GUI, and we will save the output to the gallery.  We will use depth-first search...

```
$ python -m demos.moore_maze -d 11 18 -c \
>     -a d -o gallery/Moore_maze_DFS.png \
>     -t "Moore neighborhood maze (DFS)"
```

The *-d 11 18* option tells us 11 rows and 18 columns.  The *-c* option is short for *--console* and tells us that we want to display the maze on the console.  (It has more than 10 rows, so we need this option to force the display.)  The *-a d* option tells us to use DFS instead of Wilson's algorithm.  The *-o* option tells us to save the graphics image to a PNG file.  (We can also do this from the *matplotlib* panel.)  Finally, the *-t* option replaces the default title.

Here is the console output:
```
          Depth-first Search (DFS) (statistics)
                            visits      395
                        start cell  (5, 2)
               maximum stack depth      140
                             cells      198
                          passages      197
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |   |       |           |   |   |               |       |
+---\---\---X---/---+---\---\---+---\---+   X---+   +---+---/---+---X---+
|   |   |   |   |   |       |   |   |       |   |   |   |   |       |   |
+   X---+---+---/---X---+---+---X---\---+---+---X---/   +---\---+---X---+
|   |   |       |   |   |       |   |   |   |   |   |   |   |   |   |   |
+---/---+   +---+   +   \---\---/---/---+   X---/---/---/---\   +   +---+
|   |       |       |   |   |   |   |   |   |   |   |   |   |   |       |
+---X---+---+   +---+   +---+---+   +   \---+---/---+---\---\---+---X---+
|   |   |   |   |   |               |   |   |   |   |       |       |   |
+---X---/---\---\---\---+---+---+---/---+---+   /---\---\---+   +---+   +
|   |   |   |   |   |           |           |   |       |   |       |   |
+   +---/---+---\---\---+---+   +   +---+   +---/---+---+   +   +   +---+
|   |   |   |       |       |   |   |   |       |   |       |   |       |
+   +---X---\   +---+---/---/---X---+   +---+---+---X---+---+---\---+   +
|       |   |   |       |   |       |   |       |   |   |       |   |   |
+   +---+   +---/---+---/---+---+---+---X---+   /---/---+---X---\---+   +
|   |   |       |   |       |           |   |   |   |   |   |   |       |
+---X---\---+---/---X---+---X---+---+---+---\---+---X---X---+   +---+   +
|   |   |       |   |   |   |   |       |       |   |   |   |   |   |   |
+   \---\---+---+   +   /---/---/---+   /---+   /---+   +   /---/---X---+
|   |       |       |   |       |       |       |       |   |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
Saving to gallery/Moore_maze_DFS.png
```
The PNG image of the graphical output may be found in the gallery.  We will go through the programming steps in the next section.

## 4 - Graphics

Now let's look at the steps.  We start with the python interpreter and some imports:
```
$ python
Python 3.10.12 (main, Aug 15 2025, 14:32:43) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mazes.Grids.oblong8 import MooreGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.dff import DFF
>>> from mazes.Graphics.moore import Huntsman
```
The first import is the grid class (*MooreGrid*), and we follow that with the usual *Maze* class.  The third import is the *depth-first forest* algorithm, or depth-first search with parallel seeds.  The last import is the *matplotlib* spider graphics module.  It produces a simple weave maze (with northeastly passages tunneling under northwesterly crossing passages).

(The huntsman spider is a large household spider native to Australia.  Generally harmless and usually welcomed as a pet, it helps clear the household of annoying insects.)

The first step is to create the maze.  We will use four seeds.
```
>>> maze = Maze(MooreGrid(10, 18))
>>> print(DFF.on(maze, 4))
          Depth-first Forest (DFF) (statistics)
                            visits      360
                             tasks        4
                             seeds  [(4, 11), (4, 0), (5, 12), (9, 15)]
                             cells      180
                          passages      179
                      border edges      225
                      accept edges        3
                      reject edges        2
                            task 0  push(52), pop(52), max(31)
                            task 1  push(45), pop(45), max(37)
                            task 2  push(46), pop(46), max(34)
                            task 3  push(37), pop(37), max(26)
                     snake lengths  (52, 45, 46, 37)
```

Here is the console display of the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |               |           |       |   |   |               |   |
+   \   \---+---+---+   +---/---+---X---+---/---X---\   +---+---+   +   +
|   |   |   |       |   |   |   |       |   |   |   |   |       |       |
+---\---+---X---+   +---X---/---\---+---/---+   /---+---/---+   +---+   +
|   |   |   |   |   |   |   |   |   |       |   |       |       |       |
+   \---X---\---\---\---\---/---X---+---/---+---/---+---/---+---/---+---+
|   |   |   |   |       |   |   |   |   |       |       |   |           |
+   +---+---\---\---+---+---/   +---X---/---+   +---\---+---X---+---/---+
|   |   |       |       |   |   |   |   |       |   |       |   |       |
+---/   /---+---+---+   +---X---+   +---+---\---+---\---+---+   \---+   +
|   |   |   |       |   |   |       |       |   |   |   |       |       |
+---+---/---/---X---\   +---\---+---+---X---+---+---X---+   +---+---+---+
|   |       |   |   |       |   |   |   |   |       |   |   |   |       |
+   +   +---+   +---\---+---/---+   \   +   +   +---/---+   /---\---\---+
|   |   |       |   |   |       |   |   |   |   |   |       |   |   |   |
+   +---+---\---+   X---/---+---+   +---+---X---+   X---+---/   +---X---+
|   |       |   |   |   |       |       |   |   |   |   |   |   |   |   |
+   +   +   X---+---+---\---\---\---+   +---X---\---+---+   +   /---+   +
|       |   |           |       |       |       |           |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Now for the graphics...

We must create a huntsman spider object.  If we want a pen color other than black, we need to run setup.  If we want a title, we need tu run the title method:
```
>>> huntsman = Huntsman(maze)
>>> huntsman.setup('blue')
>>> huntsman.title('A Depth-First Forest on a Moore Grid (4 Seeds)')
```

Now we can draw the maze -- this takes a moment:
```
>>> huntsman.draw_maze()
```
This draws the maze virtually -- it doesn't display anything.  There is some extra space in the drawing.  We can reduce that using some *matplotlib* magic (which also takes a moment):
```
>>> huntsman.fig.tight_layout()
```

If we want to save a copy to an image file, we can.  For example, PNG, JPEG and TIFF are all supported:
```
>>> huntsman.save_image("Moore_DFF4.jpg")
>>> huntsman.save_image("Moore_DFF4.png")
>>> huntsman.save_image("Moore_DFF4.tiff")
```
(All three have been placed in the gallery.  For this sort of non-photographic drawing, PNG is usually more efficient than either JPEG or TIFF.)

Finally, we probably want to display the graphics:
```
>>> huntsman.show()
```
We could save the figure to a file from the display panel -- look for the floppy disk icon on the lower right.  When done, click on the close screen (X) on the upper right.  After closing the screen, we can exit from the Python interpreter.