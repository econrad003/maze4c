# Graphviz graphics interface

## Contents

* Introduction
* Section 1. Basic rectangular grid interface
* Section 2. A better rectangular grid interface

## Introduction

The examples in this document require the graphviz toolbox and the graphviz Python package.

Graphviz is a toolbox for displaying graphs, digraphs, and networks.  There are installation procedures for Windows, for Linux, and for Macintosh.

There is also a separate Python package called *graphviz* which uses the graphviz toolbox.  The graphviz toolbox must be installed before the Python package can be used.  The Python package can be installed using *pip* and *virtualenv*.  It may also be available as a package in some Linux repositories.  (It apparently requires Python version 3.9 or greater.)

Some documentation is available here:

* [https://graphviz.readthedocs.io/en/stable/manual.html](https://graphviz.readthedocs.io/en/stable/manual.html)

## Section 1. Basic rectangular grid interface

The basic graphviz driver is the module *mazes.Graphics.dot.oblong1*.  It handles rectangular grids with Von Neumann neighborhoods (N/S/E/W) or Moore neighborhoods (orthogonal and diagonal neighbors).

Grids (like the torus, the cylinder, the Moebius strip, the Klein bottle, or the projective plane) that support passages that fall outside the boundary of the rectangle will work poorly.

Weaving (overpasses and underpasses) is not supported.

In the next few examples, we will use the following small maze.  Image output may be found in the gallery.

```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.bfs import BFS
>>> maze = Maze(OblongGrid(3, 4))
>>> print(BFS.on(maze)); print(maze)
          Breadth-first Search (BFS) (statistics)
                            visits       12
                        start cell  (1, 2)
              maximum queue length        6
                             cells       12
                          passages       11
+---+---+---+---+
|               |
+---+---+   +---+
|               |
+   +   +   +   +
|   |   |   |   |
+---+---+---+---+
```

### Example 1.1: Default view

```
>>> from mazes.Graphics.dot.oblong1 import Plotter
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex1-1")
Output: gallery/graphviz-ex1-1 (svg)
```
The output image file is *gallery/graphviz-ex1-1.svg*.

To render the graph without calling up the viewer, the *render* method (*dot.render(filename)*) can be used.  Both the *view* and *render* methods have an additional argument, *cleanup* (default: *True*).  When *cleanup=False* is specified, the graphviz source is retained as *filename.gv*.

If scaled vector graphics (SVG) is not installed, a *CalledProcessError* exception is raised.  (See Example 1.2.)

The default viewer for *scalable vector graphics* (or *SVG*) was used to display the vector image file *gallery/graphviz-ex1-1.svg*.  The image consists of 12 squares, representing the cells, connected by thick lines.  Here is the graphviz source:
```
>>> print(dot.source)
// OblongGrid
graph {
	N0_0 [label="" pos="0,0!" shape=square]
	N0_1 [label="" pos="1,0!" shape=square]
	N0_2 [label="" pos="2,0!" shape=square]
	N0_3 [label="" pos="3,0!" shape=square]
	N1_0 [label="" pos="0,1!" shape=square]
	N1_1 [label="" pos="1,1!" shape=square]
	N1_2 [label="" pos="2,1!" shape=square]
	N1_3 [label="" pos="3,1!" shape=square]
	N2_0 [label="" pos="0,2!" shape=square]
	N2_1 [label="" pos="1,2!" shape=square]
	N2_2 [label="" pos="2,2!" shape=square]
	N2_3 [label="" pos="3,2!" shape=square]
	N1_2 -- N2_2 [penwidth=5]
	N0_0 -- N1_0 [penwidth=5]
	N1_3 -- N0_3 [penwidth=5]
	N2_3 -- N2_2 [penwidth=5]
	N2_0 -- N2_1 [penwidth=5]
	N1_2 -- N1_1 [penwidth=5]
	N2_2 -- N2_1 [penwidth=5]
	N1_1 -- N1_0 [penwidth=5]
	N1_2 -- N0_2 [penwidth=5]
	N1_1 -- N0_1 [penwidth=5]
	N1_3 -- N1_2 [penwidth=5]
}
```

The graphviz command *neato* can be used to render the source.  (Graphviz has several rendering engines including *neato*, *fdp*, *twopi*, *circo*, *patchwork*, *sfdp*, *osage*, and *dot*.  Each rendering engine has its own command to be used in a command shell like *cmd* on Windows or *bash* under Linux.)

### Example 1.2: A few options

The constructor for *Plotter* has some options:
```
>>>
Help on method __init__ in module mazes.Graphics.dot.oblong1:

__init__(maze: mazes.maze.Maze, comment: str = None, edgewidth: int = 5, format: str = 'svg', shape: str = 'square') method of mazes.Graphics.dot.oblong1.Plotter instance
    constructor
```

The *comment* option places a comment at the beginning of the graphviz source.  The default (*None*) is to use the class name as the comment.

The *edgewidth* option controls the width of the edge lines.  The *format* option controls the type of image output (*pdf*, *svg*, *png*, *jpg*, ...).  The *shape* option controls the shape of the cells ("triangle", "square", "pentagon", "hexagon", "circle", ...).

An *CalledProcessError* exception is raised if the format is not recognized.  (For example TIFF was not supported on my laptop.)  The exception message displays a list of recognized formats.

Only a few shapes are recognized -- and unrecognized shape name is rendered as a *box* (*i.e.* a small rectangle).

```
>>> dot = Plotter(maze, shape="circle", edgewidth=2, format="jpg")
>>> dot.view(filename="gallery/graphviz-ex1-2")
Output: gallery/graphviz-ex1-2 (jpg)
```
The output image file is *gallery/graphviz-ex1-2.jpg*.  Note that the nodes were drawn as circles and the edges were not as thick.

In general, SVG will produce the small file sizes, and for this sort of image, vector graphics (like SVG) works better than raster graphics (like PNG or JPG).

### Example 1.3: A few more options

WEBP is one of the newer raster formats that is available on my laptop.  So:
```
>>> dot = Plotter(maze, shape="pentagon", edgewidth=10, format="webp")
>>> dot.view(filename="gallery/graphviz-ex1-3")
Output: gallery/graphviz-ex1-3 (webp)
```
The output image (with its thick black edges and hexagonal cells) was saved as *gallery/graphviz-ex1-3.webp*.  (If you don't have an image viewer that supports WEBP, note that both Chrome and Firefox -- and web browsers that are based on one or the other -- can display WEBP files.)

### Example 1.4: A larger example (Von Neumann grid)

```
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(34, 55))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits      801
                             cells     1870
                          passages     1869
                 paths constructed      801
                     cells visited    16772
                          circuits     4789
                    markers placed    11182
                   markers removed     9313
                     starting cell  (0, 15)
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex1-4")
Output: gallery/graphviz-ex1-4 (svg)
```
The output (*gallery/graphviz-ex1-4.svg*) is too detailed for a typical laptop or desktop monitor (*e.g.* 1366×768 or 1920×1080).  But zooming in using an SVG viewer will improve the view.  Note that, after zooming in a bit, the cells and passages actually appear to be exactly the same as the cells and edges in the image in Example 1.1.

### Example 1.5: Another large example (Moore grid)

The format works well on the 8-connected (Moore neighborhood) rectangular grid.
```
>>> from mazes.Grids.oblong8 import MooreGrid
>>> maze = Maze(MooreGrid(34, 55))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits      866
                             cells     1870
                          passages     1869
                 paths constructed      866
                     cells visited     6014
                          circuits      975
                    markers placed     4173
                   markers removed     2304
                     starting cell  (2, 51)
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex1-5")
Output: gallery/graphviz-ex1-5 (svg)
```
Again, zoom in on the output (*gallery/graphviz-ex1-5.svg*) for a better view.

## Section 2. A better rectangular grid interface

The *graphviz* interface used in Section is both fast and adequate, but it does not allow very much in the way of customization.  It also won't give good results on grids like the toroidal grid or the Moebius grid which are based on a rectangular grid but have passages which leave the rectangle from one side and re-enter through another.

In this section, we examine an "improved" version of the previous plotter which addresses some (but by no means all) of the limitations.  It won't handle weaves, and its support for grids like the torus is very basic.  Using the default setup, it works exactly like the driver in the previous section.

For all of the examples in this section, the driver uses the following import:
```
>>> from mazes.Graphics.dot.oblong2 import Plotter
```
Our mazes are uniformly generated mazes carved using Wilson's alorithm:
```
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
```
The grids will vary, but we will use 8 rows and 13 columns for the grids and image output will be SVG.  (Most laptop displays should be able to accommodate the output without zooming.  You will, of course, need an SVG-enabled image viewer.  In addition, that size displays nicely as a text maze in a markdown file.)

### Von Neumann neighborhoods

#### Example 2.1.  Basic usage

With no options, it works like the very basic plotter, but with a few under-the-hood enhancements to accommodate more exotic grids.  For the usual Von Nemann rectangular grid, there is no difference at this level.

We start with the imports mentioned above:
```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
```

The example uses a Von Neumann grid (four compass neighbors):
```
>>> from mazes.Grids.oblong import OblongGrid
```

We need a maze:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       40
                             cells      104
                          passages      103
                 paths constructed       40
                     cells visited      637
                          circuits      190
                    markers placed      407
                   markers removed      304
                     starting cell  (1, 6)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |                               |
+---+---+   +   +---+   +---+---+---+---+---+---+   +
|   |       |           |                       |   |
+   +   +   +---+---+---+---+---+---+   +---+   +   +
|       |   |       |       |   |       |           |
+---+   +---+---+   +   +---+   +   +---+---+---+   +
|           |       |   |       |       |           |
+---+   +   +---+   +   +   +---+---+---+---+---+   +
|       |       |   |           |               |   |
+---+---+---+   +   +   +---+---+   +   +   +   +   +
|   |       |   |               |   |   |   |       |
+   +   +---+   +   +---+---+---+   +---+---+---+   +
|               |                           |       |
+   +---+   +---+   +---+   +   +---+---+   +   +   +
|       |       |   |       |           |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

We set up the plotter and view the graphic:
```
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex2-1")
Output: gallery/graphviz-ex2-1 (svg)
```
The graphic was saved in the gallery: *gallery/graphviz-ex2-1.svg*

In addition, we produced a PNG image:
```
>>> dot = Plotter(maze, format="png")
>>> dot.view(filename="gallery/graphviz-ex2-1")
Output: gallery/graphviz-ex2-1 (png)
```

#### Example 2.2.  Customizing the image

We will use the same maze, but we will customize certain cells as follows:

1. the cell in row 4 column 5 will be displayed as a red hexagon and labelled "A";
2. the neighbor to the south will be labelled "B";
3. the neighbor to the north will be filled with the color blue;
4. the neighbor to the east will be filled with a blue-red gradient;
5. the neighbor to the west will be filled with blue, white and red vertical stripes.

We need a dictionary to hold the cell customizations.
```
>>> cattr = dict()
```

The key is the cell object.  The value is a dictionary of name-value pairs.  Both the name and the value must be strings.  Here we create the customization.  We begin with the first two items.
```
>>> cell1 = maze.grid[4,5]
>>> cattr[cell1] = {"shape":"hexagon", "color":"red", "label":"A"}
>>> cattr[cell1.south] = {"label":"B"}
```

For the fills, we specify a style and the fill colors.  The style "filled" implies a solid color or a two-color horizontal gradient.  (Gradients are not supported in all image formats.) The style "striped" returns vertical stripes.  There is also a "gradientangle" attribute which changes the direction of a gradient.

```
>>> cattr[cell1.north] = {"style":"filled", "fillcolor":"blue"}
>>> cattr[cell1.east] = {"style":"filled", "fillcolor":"blue:red"}
>>> cattr[cell1.west] = {"style":"striped", "fillcolor":"blue:white:red"}
```
And just for fun, here are a couple of variants:
```
>>> cattr[cell1.east.east] = {"style":"filled", "fillcolor":"blue:red",
...                           "gradientangle":str(45)}
>>> cattr[cell1.west.west] = {"shape":"ellipse", "style":"wedged",
...                           "fillcolor":"blue:yellow:red"}
```
Note the the gradient angle was entered in degrees as a string (*str*) and not as an integer (*int* or *float*).

We can also customize the passages.  We'll just do one since the basic principles are the same.  Let's look at the cell in row 1 column 1 and its neighbor to the north.  We'll label those cells "C" and "D", respectively.
```
>>> cell2 = maze.grid[1,1]
>>> cattr[cell2] = {"label":"C"}
>>> cattr[cell2.north] = {"label":"D"}
```
We need to find the passage object (*i.e.* an edge or an arc):
```
>>> join = cell2.join_for(cell2.north)
>>> type(join)
<class 'mazes.edge.Edge'>
```
Of course it is undirected -- that makes the passage an edge.  But the order of the cells in an edge is not guaranteed, so let's make sure of how the cells happen to be ordered:
```
>>> cell3, cell4 = join
>>> cell3.index, cell4.index
((1, 1), (2, 1))
```
The dictionary order is first cell "C", and then cell "D".  The reason we wanted to know how the cells were ordered in the join is that we want the edge to change from red to yellow to blue as we proceed from "C" to "D".
```
>>> jattr = dict()
>>> jattr[join] = {"color":"red:yellow;0.25:blue"}
```

We have the customizations.  So let's initialize a plotter, and let it do its work:
```
>>> dot = Plotter(maze, cell_attrs=cattr, join_attrs=jattr)
>>> dot.view(filename="gallery/graphviz-ex2-2")
Output: gallery/graphviz-ex2-2 (svg)
```

And let's create a PNG image as well.
```
>>> dot = Plotter(maze, cell_attrs=cattr, join_attrs=jattr, format="png")
>>> dot.view(filename="gallery/graphviz-ex2-2")
Output: gallery/graphviz-ex2-2 (png)
```

#### Example 2.3.  Using cell labels

Now suppose you've worked hard at labelling the cells using the *Cell.label* setter.  For example:
```
>>> maze.grid[0,0].label = "SW"
>>> maze.grid[0,12].label = "SE"
>>> maze.grid[7,0].label = "NW"
>>> maze.grid[7,12].label = "NE"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| N                 |                             N |
+---+---+   +   +---+   +---+---+---+---+---+---+   +
|   |       |           |                       |   |
+   +   +   +---+---+---+---+---+---+   +---+   +   +
|       |   |       |       |   |       |           |
+---+   +---+---+   +   +---+   +   +---+---+---+   +
|           |       |   |       |       |           |
+---+   +   +---+   +   +   +---+---+---+---+---+   +
|       |       |   |           |               |   |
+---+---+---+   +   +   +---+---+   +   +   +   +   +
|   |       |   |               |   |   |   |       |
+   +   +---+   +   +---+---+---+   +---+---+---+   +
|               |                           |       |
+   +---+   +---+   +---+   +   +---+---+   +   +   +
| S     |       |   |       |           |   |   | S |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The console display only uses the first letter, of course.  Can we display those labels graphically?  Affirmative, Captain!  Just use the *labels* option:
```
>>> dot = Plotter(maze, labels=True)
>>> dot.view(filename="gallery/graphviz-ex2-3")
Output: gallery/graphviz-ex2-3 (svg)
```
We've also saved a PNG version (using *format="png"* in the constructor).

Now it's time to look at some other grids.

### Moore neighborhoods

#### Example 2.4.  The Moore grid

The Moore grid is supported, but as on the console, diagonally crossing edges are not weaved.
```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.oblong8 import MooreGrid   # <---
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(MooreGrid(8, 13))               # <---
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       50
                             cells      104
                          passages      103
                 paths constructed       50
                     cells visited      359
                          circuits       72
                    markers placed      237
                   markers removed      134
                     starting cell  (4, 5)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |           |               |
+---\   /   +   +   /---+   +---+---/   +---+---/   +
|   |   |   |       |   |   |   |   |   |   |   |   |
+   /---+---+   +---/---/   +---\   \---\   +   +   +
|       |   |   |   |   |   |   |   |   |   |   |   |
+---/   /---\   +   +   +---X   +   +---+---+---+---+
|   |       |       |   |   |   |       |   |   |   |
+---/---/---+---+---/---+   +---\---+---\   /   /   +
|   |   |   |   |   |           |       |   |   |   |
+   +   \   +   +---+---\---\---+   +---X---/   +---+
|   |   |   |       |       |   |   |   |   |   |   |
+   \---+   /---+   +---+   +---+---+---+---+---/---+
|   |   |   |   |   |   |   |       |           |   |
+---+   \---\---\---/---X---\---+   /---+---+   X---+
|       |   |           |   |           |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

#### Example 2.5.  The upsilon (Y-) grid

```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.upsilon import UpsilonGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(UpsilonGrid(8, 13))
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       45
                             cells      104
                          passages      103
                 paths constructed       45
                     cells visited      261
                          circuits       44
                    markers placed      172
                   markers removed       69
                     starting cell  (0, 4)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |       |       |   |       |   |   |
+   +   +---+---\   +   +---+---\   /---\---+   +   +
|   |   |   |   |   |   |   |   |   |           |   |
+---\---/---\   +---+   /---+   +   +---+   +---/---+
|   |   |   |               |           |   |   |   |
+   +   +   +   +---+---+---+---+---+---\---/---+   +
|       |   |   |                   |           |   |
+   \---+   \---/   +---+---+---/---+   +---\---+   +
|   |       |   |           |   |   |   |   |       |
+---+---+   +---+---+---+   +---+   /   +   +---+---+
|               |   |   |   |   |   |   |   |       |
+---\---+---+   +   +   +   +   +   +---/   \   +---+
|       |       |       |       |       |   |       |
+   +   +---+   \---/---\---+---+---/---+---/---\---+
|   |       |   |   |               |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Although sizing the octagons is tricky, we can easily place octagons where they are needed.  This is an even parity (*i.e.* *parity=False*) *Y*-maze, so the octagons belong where the sum of the coordinates is even.
```
>>> cattr = dict()
>>> for i in range(maze.grid.m):
...     for j in range(maze.grid.n):
...         if (i+j)%2 == 0:             # even parity  <---
...             cell = maze.grid[i, j]
...             cattr[cell] = {"shape":"octagon"}
...
>>> dot = Plotter(maze, cell_attrs=cattr)
>>> dot.view(filename="gallery/graphviz-ex2-5-Upsilon")
Output: gallery/graphviz-ex2-5-Upsilon (svg)
```
For an odd parity *Y*-maze, just specify *parity=True* in the grid constructor and replace the indicated line in the nested *if* with:
```python
       if (i+j)%2 == 1:             # odd parity  <---
```
Ideally we'd like those octagons to be bigger and more regular and those squares to be smaller.  It's probably possible with *graphviz*, but we'll leave that as an exercise for another day.

### Exotica

In the rest of the examples in this section (Section 2), we look at the more exotic grids based on an ordinary rectangle by identifying opposite sides.  The simplest example is the cylinder.

#### Example 2.6.  The cylindrical grid

```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.cylinder import CylinderGrid    # <---
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(CylinderGrid(8, 13))                 # <---
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       42
                             cells      104
                          passages      103
                 paths constructed       42
                     cells visited      554
                          circuits      148
                    markers placed      364
                   markers removed      261
                     starting cell  (2, 4)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
            |   |           |       |   |   |   |
+   +   +---+   +---+---+   +   +---+   +   +   +---+
    |   |                   |
+   +---+---+   +---+---+   +   +---+   +---+---+   +
|           |   |   |   |   |   |   |   |       |   |
+---+   +---+   +   +   +   +---+   +   +   +---+   +
    |   |       |   |               |   |   |
+   +   +   +---+   +---+---+   +---+   +   +---+---+
|   |                   |           |       |       |
+---+---+---+---+   +   +---+   +---+---+   +---+   +
                    |   |           |       |   |
+   +   +---+---+---+---+---+---+   +   +---+   +   +
|   |           |                   |   |       |   |
+---+   +   +---+---+   +---+---+   +---+   +   +---+
        |           |           |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
If we proceed one step west from a cell in the leftmost column which shows a westbound passage, we end up in the rightmost cell in the same columns.  Tabs might be helpful in making the step more clear:
```
>>> from mazes.console_tools import unicode_str
>>> print(unicode_str(maze, e="NR", w="N"))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  7             ┃   ┃           ┃       ┃   ┃   ┃   ┃     7
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━┫
  6     ┃   ┃                   ┃                         6
    ┣   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  5 ┃           ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃ 5
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ┫
  4     ┃   ┃       ┃   ┃               ┃   ┃   ┃         4
    ┣   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━┫
  3 ┃   ┃                   ┃           ┃       ┃       ┃ 3
    ┣━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ┫
  2                     ┃   ┃           ┃       ┃   ┃     2
    ┣   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ┫
  1 ┃   ┃           ┃                   ┃   ┃       ┃   ┃ 1
    ┣━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━┫
  0         ┃           ┃           ┃       ┃   ┃         0
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Let's see how our more advanced plotter deals with this maze.
```
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex2-6-cylinder")
Output: gallery/graphviz-ex2-6-cylinder (svg)
```
We are also saving this as a PNG image:
```
>>> dot = Plotter(maze, format="png")
>>> dot.view(filename="gallery/graphviz-ex2-6-cylinder")
Output: gallery/graphviz-ex2-6-cylinder (png)
```

#### Example 2.7.  The Moebius strip grid

```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.moebius import MoebiusGrid       # <---
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(MoebiusGrid(8, 13))                   # <---
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       48
                             cells      104
                          passages      103
                 paths constructed       48
                     cells visited      453
                          circuits      110
                    markers placed      295
                   markers removed      192
                     starting cell  (2, 0)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
            |                       |
+---+---+---+   +   +---+---+   +   +   +---+---+---+
            |   |   |   |   |   |   |
+   +---+   +   +---+   +   +---+---+---+   +   +---+
|   |                       |   |   |       |       |
+---+---+---+---+   +---+   +   +   +---+   +---+   +
|                       |       |       |       |   |
+---+   +---+   +   +   +   +---+   +   +---+---+---+
|       |   |   |   |   |   |       |       |       |
+---+   +   +---+---+---+   +   +   +---+   +   +---+
|       |   |   |       |       |       |           |
+---+   +   +   +---+   +   +---+---+---+---+   +---+
                |   |       |   |               |
+---+---+   +---+   +   +   +   +   +   +   +   +---+
        |   |           |   |       |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Here we tape the east and west ends after giving the strip a half twist.  To the west of the first cell in the row just below the top row is the last cell in the row just above the bottom row.  Again, this might be more clear with tabs:
```
>>> from mazes.console_tools import unicode_str
>>> print(unicode_str(maze, e="NR", w="N"))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  7             ┃                       ┃                 0
    ┣━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━┫
  6             ┃   ┃   ┃   ┃   ┃   ┃   ┃                 1
    ┣   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
  5 ┃   ┃                       ┃   ┃   ┃       ┃       ┃ 2
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ┫
  4 ┃                       ┃       ┃       ┃       ┃   ┃ 3
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━┫
  3 ┃       ┃   ┃   ┃   ┃   ┃   ┃       ┃       ┃       ┃ 4
    ┣━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━┫
  2 ┃       ┃   ┃   ┃       ┃       ┃       ┃           ┃ 5
    ┣━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━┫
  1                 ┃   ┃       ┃   ┃               ┃     6
    ┣━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━┫
  0         ┃   ┃           ┃   ┃       ┃   ┃   ┃         7
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
The plotter for this section supplies the tabs.
```
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex2-7-Moebius_strip")
Output: gallery/graphviz-ex2-7-Moebius_strip (svg)
```

#### Example 2.8.  The toroidal grid

The the torus, we have horizontal and vertical connections
```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.torus import TorusGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(TorusGrid(8, 13))
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       42
                             cells      104
                          passages      103
                 paths constructed       42
                     cells visited      479
                          circuits      117
                    markers placed      320
                   markers removed      217
                     starting cell  (4, 2)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏━━━┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳━━━┳━━━┳━━━┳   ┳   ┓
  7         ┃           ┃                       ┃   ┃     7
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ┫
  6     ┃               ┃   ┃   ┃   ┃       ┃       ┃     6
    ┣━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
  5     ┃       ┃   ┃           ┃           ┃       ┃     5
    ┣   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ┫
  4 ┃       ┃                       ┃   ┃           ┃   ┃ 4
    ┣━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━┫
  3 ┃   ┃               ┃       ┃               ┃   ┃   ┃ 3
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ┫
  2         ┃   ┃           ┃       ┃           ┃         2
    ┣━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ┫
  1     ┃       ┃   ┃   ┃   ┃   ┃       ┃   ┃       ┃     1
    ┣   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━┫
  0 ┃       ┃       ┃       ┃       ┃       ┃   ┃   ┃   ┃ 0
    ┗━━━┻━━━┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻━━━┻━━━┻   ┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex2-8-torus")
Output: gallery/graphviz-ex2-8-torus (svg)
```
There is also a PNG image...

#### Example 2.9.  The Klein bottle grid

A torus with a Moebius twist in one direction...
```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.klein import KleinGrid             # <---
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(KleinGrid(8, 13))                       # <---
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       41
                             cells      104
                          passages      103
                 paths constructed       41
                     cells visited      264
                          circuits       53
                    markers placed      170
                   markers removed       67
                     starting cell  (6, 0)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┳   ┳   ┳━━━┳━━━┳   ┓
  7 ┃       ┃               ┃                             0
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
  6 ┃       ┃   ┃                   ┃           ┃   ┃   ┃ 1
    ┣   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━┫
  5     ┃   ┃   ┃               ┃                   ┃   ┃ 2
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ┫
  4     ┃       ┃           ┃   ┃       ┃       ┃       ┃ 3
    ┣━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
  3 ┃                           ┃           ┃   ┃   ┃     4
    ┣━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━┫
  2 ┃       ┃   ┃       ┃                   ┃   ┃         5
    ┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ┫
  1 ┃       ┃           ┃       ┃       ┃           ┃   ┃ 6
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
  0     ┃           ┃           ┃   ┃   ┃   ┃           ┃ 7
    ┗   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┻   ┻   ┻━━━┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex2-9-klein")
Output: gallery/graphviz-ex2-9-klein (svg)
```
There is also a PNG image...

#### Example 2.10.  The projective grid

Half-twists in both directions make this the strangest of the grids (so far) in the rectangular grid menagerie...  This grid requires very special handling because diagonally opposite corners represent a single cell.  In the console display below, note that the northwest and southeast corners a both adjacent to tabs M and 7, while the southwest and northeast corners are both adjacent to tabs A and 0.  In the graphic, the top two corners of the rectangle are not displayed.  To avoid tab conflicts, there are special rules for placement of tabs.  (See Example 2.11 for more details.)
```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.projective import ProjectiveGrid    # <---
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(ProjectiveGrid(8, 13))                   # <---
>>> print(Wilson.on(maze)); print(maze)
                            visits       49
                             cells      102
                          passages      101
                 paths constructed       49
                     cells visited      294
                          circuits       59
                    markers placed      186
                   markers removed       85
                     starting cell  (1, 9)
      M   L   K   J   I   H   G   F   E   D   C   B   A
    ┏━━━┳━━━┳━━━┳   ┳   ┳   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳━━━┓
  7     ┃   ┃       ┃   ┃       ┃   ┃           ┃   ┃     0
    ┣━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ┫
  6     ┃       ┃   ┃           ┃           ┃   ┃   ┃   ┃ 1
    ┣   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ┫
  5         ┃           ┃   ┃                   ┃   ┃   ┃ 2
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ┫
  4                 ┃       ┃   ┃   ┃   ┃       ┃   ┃     3
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━┫
  3     ┃   ┃               ┃       ┃   ┃   ┃   ┃   ┃     4
    ┣   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ┫
  2 ┃       ┃       ┃           ┃   ┃   ┃                 5
    ┣   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━┫
  1 ┃   ┃       ┃       ┃   ┃               ┃   ┃   ┃     6
    ┣━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
  0 ┃       ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃           ┃ 7
    ┗   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┻   ┻   ┻━━━┻━━━┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
>>> dot = Plotter(maze)
>>> dot.view(filename="gallery/graphviz-ex2-10-projective")
Output: gallery/graphviz-ex2-10-projective (svg)
```

#### Example 2.11.  Tabs in the projective grid

We use a 4-row 4-column 14-cell projective grid as an example.
```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.projective import ProjectiveGrid
>>> from mazes.maze import Maze
>>> maze = Maze(ProjectiveGrid(4, 4))
```

First we label the bottom corners for the graphic:
```
>>> SW = maze.grid[0,0]; SW.label = "SW"
>>> SE = maze.grid[0,3]; SE.label = "SE"
```

Next we (a) connect both cells to their four neighbors, and (b) label those neighbors:
```
>>> for way in ("south", "east", "north", "west"):
...     maze.link(SW, SW[way])
...     maze.link(SE, SE[way])
...     SW[way].label = way[0].upper()
...     SE[way].label = way[0]
...
```

Finally, we complete the set of connections which leave and re-enter the rectangle:
```
>>> maze.link(SW.east, SW.east.south)
>>> maze.link(SE.west, SE.west.south)
>>> maze.link(SW.north, SW.north.west)
>>> maze.link(SE.north, SE.north.east)
```

Next we display the maze on the console:
```
>>> print(maze)
      D   C   B   A
    ┏   ┳   ┳   ┳   ┓
  3   S   e ┃ W   S   0
    ┣   ╋━━━╋━━━╋   ┫
  2   s ┃   ┃   ┃ S   1
    ┣━━━╋━━━╋━━━╋━━━┫
  1   N ┃   ┃   ┃ n   2
    ┣   ╋━━━╋━━━╋   ┫
  0   S   E ┃ w   S   3
    ┗   ┻   ┻   ┻   ┛
      A   B   C   D
```
Let's edit that to make it more readable.  On the left, we label the four corners of the rectangle.  On the right, we discard the top two corners since
they are the same cell as their diagonal opposites:

```
      D   C   B   A                        D   C   B   A
    ┏   ┳   ┳   ┳   ┓                        ┏   ┳   ┓
  3   NW  e ┃ W   NE  0                3       e ┃ W       0
    ┣   ╋━━━╋━━━╋   ┫                    ┏   ╋━━━╋━━━╋   ┓
  2   s ┃   ┃   ┃ S   1                2   s ┃   ┃   ┃ S   1
    ┣━━━╋━━━╋━━━╋━━━┫                    ┣━━━╋━━━╋━━━╋━━━┫
  1   N ┃   ┃   ┃ n   2                1   N ┃   ┃   ┃ n   2
    ┣   ╋━━━╋━━━╋   ┫                    ┣   ╋━━━╋━━━╋   ┫
  0   SW  E ┃ w   SE  3                0   SW  E ┃ w   SE  3
    ┗   ┻   ┻   ┻   ┛                    ┗   ┻   ┻   ┻   ┛
      A   B   C   D                        A   B   C   D

   Figure 2.11.1. Corners labelled       Figure 2.11.2.  Duplicated
                                            cells removed
```
Now let's use the display on the right to label the four neighbors of the southwest corner *(below left)* and the four neighbors of the southeast corner *(below right)*:
```
      D   C   B   A                        D   C   B   A
        ┏   ┳   ┓                            ┏   ┳   ┓
  3         ┃ W       0                3       E ┃         0
    ┏   ╋━━━╋━━━╋   ┓                    ┏   ╋━━━╋━━━╋   ┓
  2     ┃   ┃   ┃ S   1                2   S ┃   ┃   ┃     1
    ┣━━━╋━━━╋━━━╋━━━┫                    ┣━━━╋━━━╋━━━╋━━━┫
  1   N ┃   ┃   ┃     2                1     ┃   ┃   ┃ N   2
    ┣   ╋━━━╋━━━╋   ┫                    ┣   ╋━━━╋━━━╋   ┫
  0   X   E ┃         3                0         ┃ W   X   3
    ┗   ┻   ┻   ┻   ┛                    ┗   ┻   ┻   ┻   ┛
      A   B   C   D                        A   B   C   D

   Figure 2.11.3.  Neighbors of         Figure 2.11.4. Neighbors of
      the southwest corner (X)             the southeast corner (X)
```
Now let's look at the graphic:
```
>>> dot = Plotter(maze, labels=True)
>>> dot.view(filename="gallery/graphviz-ex2-11-projective-tabs")
Output: gallery/graphviz-ex2-11-projective-tabs (svg)
```
Using the gallery image, let's tabulate the tabs:

| tab | source cell | direction | target cell | notes         |
| --: | :---------: | :-------: | :---------: | :------------ |
|   0 | (0, 0)      | south     | (3, 2)      | SW == S       |
|   1 | (0, 3)      | south     | (2, 0)      | SE == s       |
|   2 | (1, 0)      | west      | (2, 3)      | N == S        |
|   3 | (2, 0)      | west      | (1, 3)      | s == n        |
|   4 | (0, 2)      | south     | (3, 1)      | w == e        |
|   5 | (0, 3)      | east      | (3, 1)      | SE == e       |
|   6 | (0, 1)      | south     | (3, 2)      | E == W        |
|   7 | (0, 0)      | west      | (3, 2)      | SW == W       |

Note that at the top, the first tab (#5) is displayed to the northwest instead of the west to avoid colliding with tab #1.  The last tab on the right (#7) is similarly displayed to the northeast instead of east to avoid colliding with tab #0.

### Additional information

For additional information on graphviz attributes (as used in Example 2.2), see the graphviz "Attributes" documentation:

* [https://graphviz.org/doc/info/attrs.html](https://graphviz.org/doc/info/attrs.html)

#### Example 2.12.  Reducing the size of tabsize.

The *tabsize* constructor option may be used to create smaller tabs on the exotic grids:
```
$ python
Python 3.10.12 (main, Nov  4 2025, 08:48:33) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.torus import TorusGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(TorusGrid(8, 13))
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       43
                             cells      104
                          passages      103
                 paths constructed       43
                     cells visited      396
                          circuits       85
                    markers placed      268
                   markers removed      165
                     starting cell  (4, 0)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏━━━┳   ┳   ┳   ┳━━━┳   ┳   ┳   ┳   ┳   ┳━━━┳━━━┳━━━┓
  7     ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃                 7
    ┣   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
  6     ┃       ┃               ┃               ┃         6
    ┣   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
  5 ┃   ┃   ┃           ┃       ┃                       ┃ 5
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ┫
  4 ┃       ┃       ┃   ┃           ┃   ┃   ┃   ┃       ┃ 4
    ┣   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━┫
  3 ┃   ┃       ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ 3
    ┣   ╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋   ┫
  2 ┃       ┃       ┃   ┃   ┃       ┃       ┃           ┃ 2
    ┣   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━┫
  1         ┃   ┃       ┃           ┃       ┃             1
    ┣   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
  0 ┃       ┃       ┃       ┃       ┃   ┃   ┃           ┃ 0
    ┗━━━┻   ┻   ┻   ┻━━━┻   ┻   ┻   ┻   ┻   ┻━━━┻━━━┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
>>> dot = Plotter(maze, tabsize=0.3)
>>> dot.view("gallery/graphviz-ex2-12-smalltabs")
Output: gallery/graphviz-ex2-12-smalltabs (svg)
```

#### Example 2.13.  Saving and using the graphviz source

For this example, we save the source to a file and then use a shell command to create the and view the image.  First, of course, we need some imports, and then we need a maze.  Easy enough!
```
$ python
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(4, 4))
>>> print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits        8
                             cells       16
                          passages       15
                 paths constructed        8
                     cells visited       31
                          circuits        4
                    markers placed       19
                   markers removed        4
                     starting cell  (2, 1)
+---+---+---+---+
|           |   |
+---+   +---+   +
|   |   |   |   |
+   +   +   +   +
|   |   |       |
+   +   +   +   +
|           |   |
+---+---+---+---+
```
Now we need a *Plotter* object to create and save the source:
```
>>> dot = Plotter(maze)
>>> dot.save("gallery/graphviz-ex2-13-savefile")
Source: gallery/graphviz-ex2-13-savefile.gv (engine: neato)
```
The filename is optional -- the default is "output".  The extension ".gv" is automatically added.

Now let's run some shell commands...  (I am using Linux.  If you are using a Macintosh or running Unix, the commands are similar.  With Windows, there will be some differences.)  First, the last two lines of the source file contain some very basic instructions:
```
$ tail -n 2 gallery/graphviz-ex2-13-savefile.gv
// Use the neato engine, for example:
//    neato -Tsvg -O gallery/graphviz-ex2-13-savefile.gv
```
Let's run *neato*.
```
neato -Tsvg -O gallery/graphviz-ex2-13-savefile.gv
```
It immediately returned to the shell -- that's a good sign.  In the gallery we find an SVG file:

* gallery/graphviz-ex2-13-savefile.gv.svg

Note that the ".gv" stays -- the *-O* option tells us to simply append the image extension, in this case ".svg".  (The Windows version of graphviz might do something different.  Or maybe not.  I don't have access to a WIndows machine with graphviz installed.)  At this point, we can call our SVG image viewer.  For me:
```
$ xviewer gallery/graphviz-ex2-13-savefile.gv.svg
```