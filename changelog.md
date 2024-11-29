# Change Log

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