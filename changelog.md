# Change Log

## Release 0.3 - 3 December 2024

There is quite a bit here, so this summary may be imcomplete.  Documentation is not up to date.

### New module folders

* *mazes.Queues* - for queuing classes (includes modules defining classes *Stack*, *Queue*, *RandomQueue* and *PriorityQueue*)
* *mazes.AGT* - for arc-based growing tree algorithms (4 new modules)
* *mazes.VGT* - for vertex-based growing tree algorithms (4 new modules)

### New modules

* *mazes.gqueue* - generalized queue virtual class (*GeneralizedQueue*)
* *mazes.Graphics.oblong2* (class *SpiderWeb*) - a linewise graphics driver for oblong grids that inherits from class *Spider* in the *matplotlib* driver
* *mazes.Algorithms.growing\_tree1* (class *VertexGrowingTree*) - a growing tree family of algorithms using queuing classes.  This algorithm generalizes DFS (aka: recursive backtracker" -- using a stack), BFS (using a queue), "simplified Prim" (using a random queue) and "vertex Prim" (using a priority queue). This version of growing tree places cells (vertices) on the queuing structure.
* *mazes.Algorithms.growing\_tree2* (class *ArcGrowingTree*) - a growing tree family of algorithms using queuing classes.  This algorithm generalizes Prim's algorithm.  It places grid arcs (ordered pairs of neighboring cells on the queuing structure.

### Enhancements

* *mazes.Graphics.matplot\_driver* - added method *draw_arrow* to the *Spider* class

### Corrections

* *cell*/*edge*/*arc*/*maze* in *mazes* folder - corrected the unlink sequence

### Cosmetic corrections

* corrected docstrings and formatting in a number of places

## Release 0.2 - 30 November 2024

### New modules

#### depth-first search

* *mazes.Algorithms.dfs_better* - a more elegant (and efficient) depth-first search (as described in the Jamis Buck book (Reference 1 in README)
* *demos.dfs_better* - demonstration program for the more elegant depth-first search

#### breadth-first search

* *mazes.Algorithms.bfs* - breadth-first search
* *demos.bfs* - demonstration program for breadth-first search

#### simplified Prim

* *mazes.Algorithms.simplified\_Prim* - a basic growing tree algorithm
* *demos.simplified\_Prim* - demonstration program for simplified Prim

### Gallery

* 2 images for the improved DFS (*better\_dfs*)
* 2 images for BFS
* 2 images for simplified Prim

### Updated modules

#### Minor Corrections

* *mazes.Algorithms.dfs*
    1. the maximum length of the stack
    2. corrected some docstrings
    3. corrected the cell counter

#### Cosmetic Changes

* all in *mazes.Algorithms* - corrected the module docstring

* all in ^demos* - corrected the tail comment
* *demos.dfs* - corrected the module docstring and the tail comment

## Release 0.1 - November 29, 2024

### New modules

* *mazes.Algorithms.dfs* - depth-first search
* *demos.dfs* - demonstration program for depth-first search

### Gallery

* 4 images for DFS

### Updated modules

#### Cosmetic corrections

* *demos.simple\_binary\_tree* - add docstring for *make\_binary\_tree*

## November 28, 2024

**Initial upload.**

The base folder contains a *README.md* file and a *LICENSE* file (GPL v3).  The subfolders contain *README.md* files which very briefly summarize their purpose in the repository.

* package: *mazes*

    + modules subfolder: *Algorithms*
        - *simple_binary_tree.py* - the heads=north/tails=east binary tree algorithm
        - *sidewinder.py* - the heads=carve north from run/tails=continue run to east sidewinder algorithm
        - *inwinder.py* - the inwinder algorithm, a variant of sidewinder that uses concentric rings instead of rows or columns

    + modules subfolder: *Graphics*
        - *matplot_driver.py* - a base for *matplotlib* graphics drivers
        - *oblong1.py* - a very simple *matplotlib* driver for oblong mazes

    + modules subfolder: *Grids*
        - *oblong.py* - the N/S/E/W oblong (or rectangular) grid
        - *oblong_rings.py* - tools for accessing oblong grids using concentric rectangular rings

    + *\_\_init.py\_\_* - package initialization
    + *\_\_main.py\_\_* - package main (stub)
    + *algorithm.py* - base class for maze algorithms
    + *arc.py* - base class for directed (or one-way) passages
    + *cell.py* - base class for cells
    + *edge.py* - base class for undirected (or bidirectional) passages
    + *grid.py* - base class for grids
    + *maze.py* - base class for mazes

* folder: *demos* - demonstration modules
    + *simple_binary_tree.py*
    + *sidewinder.py*
    + *inwinder.py*

* folder: *tests* - test modules
    + *oblong_rings.py*
    + *sidewinder.py*
    + *simple_binary_tree.py*

* folder: *gallery* - sample images
    + 5 sample images
