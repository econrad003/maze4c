# Maze-building using Tetris tiles

## Contents

1. What is a Tetris tile?
2. The Tetris maze carving algorithm
3. The *Tile* object
4. Simplified Tetris
5. Simulated tiles
6. Creating a maze with simulated tiles

## For the reader

Section 1 is a very short introduction into Tetris.  If you want to know more, check the *Wikipedia* article or play the game online or perhaps on your cellphone.

In Section 2, I carve a maze using the algorithm.  If all you want to do is produce these mazes using my code and Tetris tiles, you can stop reading after Section 2.

Section 3 is a long section dealing with the *Tile* class.  If you plan to program using my code, you will probably need to skim this section.

Section 4 is a rough sketch of the algorithm's internal.  But note that the *Tetris* algorithm implemented in Section 1 does drops from north to south instead of south to north.  (It simplifies the programming.)

Section 5 deals with creating tiles.  If you want to create dominops, trominos, pentominos, hexominos, octominos, or other ominos, you should read this section.

Enjoy

## 1. What is a Tetris tile?

"Tetris is a video game created by Soviet engineer Alexey Pajitnov in the 1980s.  The game is played is played in a rectagonal grid with unlabelled *tetrominos* -- a tetronimo is a domino-like object consisting of four connected square cells of the same size.  With one exception, a tetromino can be synthesized by gluing together two dominos.  The exception is the T tetronimo:
```
                    ┏━━━┳━━━┳━━━┓
                    ┃   ┃   ┃   ┃
                    ┗━━━╋━━━╋━━━┛
                        ┃   ┃
                        ┗━━━┛
```
There are six other shapes.

The tiles are randomly chosen and dropped from above the grid.  The player can rotate them and move them sideways while they are falling.  The object is to leave as few gaps in the grid as possible.

## 2. The Tetris maze carving algorithm

Without going into much detail, we'll create a maze using Tetris tiles, or more accurately, tetrominos.  (*tetromino* -- an *omino* with four square cells, *i.e.* a 4-omino.  A *domino* is a 2-omino.)

The *Tetris* passage carving algorithm is defined in the following module:

> mazes.Algorithms.tetris

It uses modules defined in the *mazes.tetris* folder.  (Those are described in Sections 3, 4 and 5 of this HOWTO.)

We create a maze in two steps.  We start by carving a partial maze using the *Tetris* algorithm.  We finish the maze by running Kruskal's algorithm -- we could instead finish using a growing tree algorithm such as BFS, DFS, or a variant of Prim's algorithm.

We start with three imports:
```
    >>> from mazes.Grids.oblong import OblongGrid
    >>> from mazes.maze import Maze
    >>> from mazes.Algorithms.tetris import Tetris
        # for unicode block characters
    >>> from mazes.console_tools import unicode_str as U
```

We create an *OblongGrid* and a *Maze* object and drop Tetris tiles into it.
```
    >>> maze = Maze(OblongGrid(8, 13))
    >>> print(Tetris.on(maze))
          Tetris tile carver (statistics)
                            visits      386
                             cells      104
                          passages       60
                        tile types       22
                             tiles       42
                             drops      321
                        placements       20
    >>> print(U(maze))              # unicode block characters
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃   ┃           ┃   ┃   ┃   ┃           ┃   ┃   ┃   ┃
    ┣   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃   ┃   ┃   ┃   ┃       ┃       ┃   ┃   ┃   ┃       ┃
    ┣   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
    ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ┫
    ┃   ┃       ┃       ┃   ┃   ┃   ┃       ┃   ┃       ┃
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
    ┃   ┃   ┃       ┃   ┃   ┃       ┃   ┃       ┃   ┃   ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃       ┃       ┃       ┃   ┃           ┃           ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
    ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
    ┣━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━┫
    ┃   ┃   ┃       ┃   ┃   ┃           ┃           ┃   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Note that we need a minimum of 119 passages for a connected maze.  (119 passages is a necessary condition for a perfect maze.  To connect all the cells, we need at least that.)  Note that some passages have been carved -- these passages connect cells in each tetronimo -- exactly 3 passages for each 4-omino.

To complete the maze, we will use Kruskal's algorithm:
```
    >>> from mazes.Algorithms.kruskal import Kruskal
    >>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits       73
                 components (init)       44
               queue length (init)      125
                             cells      104
                          passages       43
                components (final)        1
              queue length (final)       52
    >>> print(U(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃   ┃           ┃           ┃                       ┃
    ┣   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃   ┃       ┃   ┃       ┃           ┃   ┃   ┃       ┃
    ┣   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━┫
    ┃           ┃   ┃   ┃   ┃           ┃       ┃   ┃   ┃
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
    ┃   ┃       ┃       ┃   ┃   ┃           ┃           ┃
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
    ┃   ┃   ┃       ┃   ┃   ┃       ┃           ┃   ┃   ┃
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━┫
    ┃               ┃       ┃               ┃           ┃
    ┣   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ┫
    ┃   ┃       ┃       ┃       ┃       ┃   ┃   ┃   ┃   ┃
    ┣   ╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ┫
    ┃   ┃   ┃       ┃       ┃                       ┃   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

We can verify that the maze is perfect as it is connected and has exactly 103 passages, one passage fewer than the number of cells:
```
    >>> print("Number of passages = ", len(maze))
    Number of passages =  103
```
60 of these were from tile drops leaving 44 components, and the remaining 43 were carved by Kruskal's algorithm to connect the components.

This sequence is package as a demonstration module `demos.tetris` with several options.
```
    usage: tetris.py [-h] [-d DIM DIM] [-T] [-D] [-N]

    create a maze using the Tetris tile drop algorithm

    options:
          -h, --help            show this help message and exit
          -d ROW COL, --dim ROW COL
                                maze dimensions (default: 8,13)
          -T, --tetris_only     set this option to suppress the run
                            of Kruskal's algorithm
          -D, --debug           set this option to display state
                            messages
          -N, --no_display      set this suppress printing
```
The `-N` option might be useful in scripts.

## 3. The *Tile* object

Class *Tile* is defined in module *mazes.tetris.tile*.  The interface is as follows:
```
class Tile(builtins.object)
 |  Tile(*args, **kwargs)
 |      a tile, such as one used in Tetris
 |  PROTECTED DATA
 |      dropped (boolean) -- a flag indicates whether the tile has
 |          found its place in the maze.  A dropped tile is locked in
 |          place.
 |      n (positive integer) -- the number of cells in the tile.  Cells
 |          are numbered from 0 through n-1.
 |      shape (set of 3-tuples) -- the shape description of the tile.
 |          It is a set consisting of exactly n-1 3-tuples.  Each
 |          3-tuples has the following form:
 |                  (C1, D12, C2)
 |          where C1 and C2 are the numbers of two cells in the tile and
 |          D12 is the grid direction in the tile from cell C1 to C2.
 |          In each 3-tuple C1<C2, so C2 cannot be 0 and C1 cannot be
 |          be n-1.  In addition, each C2 is unique, guaranteeing that
 |          the tile is a small perfect maze.  (It is internally
 |          represented as a tuple instead of a set.)
 |      cells (set of cells) - the cells in the maze that were covered
 |          by the tile.  This is only defined for dropped tiles.
 |      bbox - bounding box coordinates for the tile (optional)
 |      zero - location of the zero in the bounding box (optional)
 |  SHAPE EXAMPLE
 |     Consider the following Tetris tile:
 |                                  +---+
 |                                  | 3 |
 |                              +---+---+---+
 |                              | 0 | 1 | 2 |
 |                              +---+---+---+
 |      For a 4-connected grid, the tile's shape description is essentially
 |      unique:
 |          {(0, "east", 1), (1, "east", 2), (1, "north", 3)}
 |      For an 8-connected grid, the tile's shape description may vary:
 |          {(0, "east", 1), (1, "east", 2), (1, "north", 3)}
 |          {(0, "east", 1), (0, "northeast", 3), (1, "east", 2)}
 |          {(0, "east", 1), (1, "east", 2), (2, "northwest", 3)}
 |  ----------------------------------------------------------------------
 |  Methods defined here:
 |  __init__(self, *args, **kwargs)
 |      constructor
 |  parse_args(self, n: int, shape: set, bbox=None, zero=None)
 |      parse the tile description (base)
 |  configure(self)
 |      configuration (stub)
 |  initialize(self)
 |      initialization (stub)
 |  drop(self, places: list, occupied: set) -> bool
 |      attempt to drop a tile into a grid
 |      ARGUMENTS
 |          places -- the cells to try as cell number 0; the
 |              first successful placement wins.  The list is
 |              processed as a stack, last in, first out.
 |              (This is a destructive operation!)  The cells
 |              in this list may not be occupied.
 |          occupied -- cells that are already occupied - if the
 |              placement is successful, this will be updated
 |      RETURN VALUE
 |          True if the placement is successful, False otherwise.
 |  carve(self, maze: mazes.maze.Maze) -> int
 |      carve the tile in the maze - once only!
 |      Returns the number of carved links. 
 |  ----------------------------------------------------------------------
 |  Readonly properties defined here:
 |  bbox
 |      bounding box, if defined
 |  cells
 |      returns the cells covered by the tile
 |  dropped
 |      returns True if the tile has been placed, and False otherwise
 |  n
 |      returns the number of cells in the tile
 |  shape
 |      returns the shape vector as a set
 |  zero
 |      zero location, if defined
```
To see how it works, let's look at the some edited output from program *tests.tetris1*:
```
placements:
    WHERE   ------------- SHAPE DESCRIPTOR ------------    TYPE
    (0,0)   ((0,'east',1), (1,'north',2), (0,'north'3))     O
    (4,1)   ((0,'north',1), (1,'west',2), (1,'east',3))     T
    (0,5)   ((0,'north',1), (1,'east',2), (2,'east',3))     L
    (4,4)   ((0,'north',1), (1,'north',2), (2,'east',3))    M
    (0,8)   ((0,'east',1), (1,'east',2), (2,'east',3))      I
    (4,8)   ((0,'north',1), (1,'east',2), (2,'north',3))    Z
    (0,13)  ((0,'north',1), (1,'west',2), (2,'north',3))    S
    (0,13)  ((0,'east',1), (1,'east',2), (0,'north',3))     random
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃   ┃   ┃   ┃   ┃ M   M ┃   ┃   ┃   ┃ Z ┃   ┃   ┃   ┃   ┃   ┃   ┃
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃ T   T   T ┃   ┃ M ┃   ┃   ┃   ┃ Z   Z ┃   ┃   ┃ ? ┃   ┃   ┃   ┃
    ┣━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━┫
    ┃   ┃ T ┃   ┃   ┃ M ┃   ┃   ┃   ┃ Z ┃   ┃   ┃   ┃ ?   ?   ? ┃   ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ S ┃   ┃   ┃   ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━┫
    ┃ O ┃ O ┃   ┃   ┃   ┃ L   L   L ┃   ┃   ┃   ┃   ┃ S   S ┃   ┃   ┃
    ┣   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
    ┃ O   O ┃   ┃   ┃   ┃ L ┃   ┃   ┃ I   I   I   I ┃   ┃ S ┃   ┃   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Test program *tetris1* creates an imperfect 8 by 16 rectangular maze which contains an example of each type of Tetris tile.

In the lower left corner we have the square (or O tile).  Notice that three of the four edges have been carved.  Since tiles can be rotated, there are actually four configurations for the square even though in actual Tetris play, there is only one configuration. 

In the upper left, we have the T tile.  To the right of the O tile is an L tile that has been rotated counterclockwise through a right angle.  To its right is an I tile rotated through a right angle, as if it had fallen on the floor.  In the upper right, a tile has been randomly selected and rotated.

Let's look at the shape descriptor for that rotated I tile:
```
    ((0,'east',1), (1,'east',2), (2,'east',3))
```
Basically it says the tile looks like this:
```
    ┏━━━┳━━━┳━━━┳━━━┓
    ┃ 0   1   2   3 ┃
    ┗━━━┻━━━┻━━━┻━━━┛
```
The row in the placement table says:
```
    WHERE                    SHAPE                        TYPE
    (0,8)   ((0,'east',1), (1,'east',2), (2,'east',3))      I
```
The column "WHERE" gives the location of the 0 cell in the maze.  The "TYPE" column names the kind of tile.  (There are two distinct configurations for the I tile.)

Now let's look at a few key sections of the test program.  We start with the imports -- we focus on the last two:
```python
    from mazes import rng
    from mazes.maze import Maze
    from mazes.console_tools import unicode_str
    from mazes.Grids.oblong import OblongGrid
    from mazes.tetris.tile import Tile
    from mazes.tetris.tetris import shapes, configs, create_tile
```

Class *Tile* is the class of interest.  The objects *shapes* and *configs* are collections of tile descriptors.  These collections are just tuples which contain the same descriptors in the same order, but they are arranged in different ways to serve different purposes.  Method *create_tile* turns a shape descriptor into a working tile.

Except for the tile labelled with the question marks, we used the *shapes* collection.  If we want to choose a particular shape and then rotate it at random, we can select the shape using its index, and then randomly choose the rotated form.  For example, the M shape is the fourth shape (*i.e.* index 3):
```python
    from mazes import rng
    from mazes.tetris.tetris import shapes, create_tile
    shape = shapes[3]
    config = rng.choice(shape)
    tile = create_tile(config)
```
Now let's inspect the tile using *Tile* properties:
```
    >>> tile.shape
    {(2, 'east', 3), (1, 'north', 2), (0, 'north', 1)}
    >>> tile.bbox
    (2, 3)
    >>> tile.zero
    0
```
These data describe the following tile:
```
    ┏━━━┳━━━┓
    ┃ 2   3 ┃           bbox: two columns wide,
    ┣   ╋━━━┫                 three rows high.
    ┃ 1 ┃   ┃           zero: column offset for cell 0 in the
    ┣   ╋━━━┫                 bottom row.
    ┃ 0 ┃   ┃
    ┗━━━┻━━━┛
```
(The M shape is a reflected L shape.)  If we only wanted to select random M tiles, we could instead proceed as follows:
```python
    from mazes import rng
    from mazes.tetris.tetris import M as M_shape
    from mazes.tetris.tetris import create_tile
    config = rng.choice(M_shape)
    tile = create_tile(config)
```
Now let's inspect the tile:
```
    >>> tile.shape
    {(1, 'east', 2), (0, 'east', 1), (0, 'north', 3)}
    >>> tile.bbox
    (3, 2)
    >>> tile.zero
    0
```
These data describe the following tile:
```
    ┏━━━┳━━━┳━━━┓
    ┃ 3 ┃   ┃   ┃           bbox: three columns wide,
    ┣━━━╋━━━╋━━━┫                 two rows high.
    ┃ 0 ┃ 1 ┃ 2 ┃           zero: column offset for cell 0
    ┗━━━┻━━━┻━━━┛
```

Now let's select the shape at random, and then rotate it at random:
```python
    from mazes import rng
    from mazes.tetris.tetris import shapes, create_tile
    shape = rng.choice(shapes)
    config = rng.choice(shape)
    tile = create_tile(config)
```
What did we get?
```
    >>> tile.shape
    {(1, 'east', 3), (1, 'north', 2), (0, 'north', 1)}
    >>> tile.bbox
    (2, 3)
    >>> tile.zero
    0

    ┏━━━┳━━━┓
    ┃ 2 ┃   ┃           bbox: two columns wide,
    ┣   ╋━━━┫                 three rows high.
    ┃ 1   3 ┃           zero: column offset for cell 0 in the
    ┣   ╋━━━┫                 bottom row.
    ┃ 0 ┃   ┃
    ┗━━━┻━━━┛           T shape, rotated counterclockwise
```

To select a configuration (rotated shape) at random, we use *configs* instead of shapes:
```python
    from mazes import rng
    from mazes.tetris.tetris import configs, create_tile
    config = rng.choice(configs)
    tile = create_tile(config)
```

```
    >>> tile.shape
    {(0, 'east', 1), (2, 'north', 3), (0, 'north', 2)}
    >>> tile.bbox
    (2, 3)
    >>> tile.zero
    0

    ┏━━━┳━━━┓
    ┃ 3 ┃   ┃           bbox: two columns wide,
    ┣   ╋━━━┫                 three rows high.
    ┃ 2 ┃   ┃           zero: column offset for cell 0 in the
    ┣   ╋━━━┫                 bottom row.
    ┃ 0   1 ┃
    ┗━━━┻━━━┛           L shape, not rotated
```

## 4. Simplified Tetris

Now we run some drops to see what happens.  We've made some simplifications:

1. Tetris is a soltaire game, one player against the machine.  Our simplified version is a zero-player game.  It's as if someone started a Tetris game and immediately left for lunch.
2. Instead of all seven tetrominos, we only use the T tetromino.
3. We cheat on the drops -- it's possible for a tile to place itself in any compatible unoccupied place on the grid.
4. The drops try a random column to start -- it it doesn't work, they try the next column.
5. A configuration is deleted if there is no place in the maze where it fits.

The implementation is in module *tests.tetris2*.  Let's run it twice...  To run it:
```
    maze4c> python -m tests.tetris2
```
It just carves T tiles into the maze until it gets stuck.  The placed tiles each receive a unique label.  Here are two sample runs:
```
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃   ┃   ┃   ┃ : ┃   ┃   ┃   ┃ @ ┃ B   B   B ┃   ┃ 9 ┃ E ┃   ┃
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
    ┃   ┃ ; ┃   ┃ :   : ┃ ? ┃ @   @   @ ┃ B ┃ 3 ┃ 9   9 ┃ E   E ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━┫
    ┃ ;   ;   ; ┃ : ┃ ?   ? ┃   ┃ > ┃   ┃ 3   3   3 ┃ 9 ┃ E ┃   ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃   ┃ 8 ┃   ┃ 5 ┃   ┃ ? ┃ >   >   > ┃ D ┃   ┃ 2 ┃ A   A   A ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃ 8   8 ┃ 5   5 ┃ <   <   < ┃   ┃ D   D ┃ 2   2   2 ┃ A ┃ C ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ┫
    ┃   ┃ 8 ┃   ┃ 5 ┃   ┃ < ┃   ┃   ┃ 6 ┃ D ┃   ┃ 0 ┃ = ┃ C   C ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ┫
    ┃   ┃ 7 ┃   ┃ 1   1   1 ┃ 4 ┃ 6   6   6 ┃ 0   0 ┃ =   = ┃ C ┃
    ┣━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━┫
    ┃ 7   7   7 ┃   ┃ 1 ┃ 4   4   4 ┃   ┃   ┃   ┃ 0 ┃ = ┃   ┃   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
22 shapes placed
```
The maze has 120 cells.  88 cells were covered, so 32 cells were missed.  Notice that there is space for 1 tile of type either L or M in the upper left, but the maze is otherwise as full as it can be.  The remaining cells are in connected groups of three or fewer.

```
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃ B   B   B ┃ D ┃   ┃   ┃ 7 ┃ :   :   : ┃ < ┃ ?   ?   ? ┃   ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
    ┃   ┃ B ┃   ┃ D   D ┃ 7   7 ┃ 9 ┃ : ┃ <   <   < ┃ ? ┃ @ ┃   ┃
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━┫
    ┃ A   A   A ┃ D ┃   ┃   ┃ 7 ┃ 9   9 ┃ 5   5   5 ┃   ┃ @   @ ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
    ┃   ┃ A ┃   ┃ C ┃   ┃   ┃ 4 ┃ 9 ┃   ┃ 2 ┃ 5 ┃   ┃   ┃ @ ┃   ┃
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃   ┃ > ┃ C   C   C ┃ 4   4   4 ┃ 2   2   2 ┃ =   =   = ┃   ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
    ┃ >   >   > ┃ ; ┃   ┃   ┃ 1 ┃   ┃   ┃ 6 ┃ 0 ┃   ┃ = ┃ 8 ┃   ┃
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
    ┃   ┃ 3 ┃ ;   ;   ; ┃ 1   1 ┃   ┃ 6   6 ┃ 0   0 ┃   ┃ 8   8 ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
    ┃ 3   3   3 ┃   ┃   ┃   ┃ 1 ┃   ┃   ┃ 6 ┃ 0 ┃   ┃   ┃ 8 ┃   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
21 shapes placed
```
This maze also has 120 cells.  84 cells were covered, so 36 cells were missed.  A square cell would fit in row 4 column 4, and there is place for an L or an M in row 0 column 7.

So what happens if we use all the possibilities?  Module *tests.tetris3* fills that bill.  Here are two sample runs:
```
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃ E   E ┃ H   H   H ┃   ┃   ┃ G ┃   ┃   ┃ = ┃ >   >   > ┃   ┃
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━┫
    ┃ E   E ┃ H ┃ D ┃   ┃ 8 ┃ G   G   G ┃ =   = ┃ > ┃   ┃   ┃ C ┃
    ┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
    ┃ :   :   : ┃ D   D ┃ 8   8 ┃ ; ┃ 6   6 ┃ = ┃ < ┃ C   C   C ┃
    ┣━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━┫
    ┃ 4   4 ┃ : ┃ D ┃ B ┃ 8 ┃ ;   ; ┃ 6   6 ┃ <   < ┃ A   A ┃   ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃ 4 ┃   ┃ 7 ┃ B   B ┃ 5 ┃ ; ┃   ┃ 3   3   3 ┃ < ┃ A   A ┃ F ┃
    ┣   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ┫
    ┃ 4 ┃ 7   7 ┃ B ┃ @ ┃ 5   5 ┃   ┃ 3 ┃   ┃ 9 ┃ ?   ?   ? ┃ F ┃
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ┫
    ┃ 1 ┃   ┃ 7 ┃   ┃ @   @ ┃ 5 ┃   ┃ 2 ┃   ┃ 9 ┃ 0   0 ┃ ? ┃ F ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
    ┃ 1   1   1 ┃   ┃ @ ┃   ┃ 2   2   2 ┃ 9   9 ┃ 0   0 ┃   ┃ F ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
    25 shapes placed
```
(20 unoccupied cells)

```
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃ :   :   : ┃   ┃ A ┃ 7   7 ┃ @   @   @ ┃   ┃   ┃ C ┃ E   E ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
    ┃ : ┃ ?   ? ┃   ┃ A ┃ 7   7 ┃   ┃ @ ┃ F   F ┃ C   C ┃ E   E ┃
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
    ┃ 1   1 ┃ ?   ? ┃ A ┃   ┃ 5   5   5 ┃ F ┃ >   > ┃ C ┃ D ┃   ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━┫
    ┃ 1 ┃   ┃   ┃   ┃ A ┃   ┃ 3 ┃ 5 ┃   ┃ F ┃ > ┃ > ┃ G ┃ D   D ┃
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
    ┃ 1 ┃ =   =   = ┃ 9 ┃   ┃ 3 ┃ B   B   B   B ┃ 8 ┃ G   G ┃ D ┃
    ┣━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━┫
    ┃ 0 ┃ <   < ┃ = ┃ 9   9 ┃ 3 ┃ 4   4 ┃   ┃   ┃ 8 ┃ G ┃ 6   6 ┃
    ┣   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃ 0 ┃ <   < ┃   ┃ 9 ┃   ┃ 3 ┃ 4   4 ┃ ;   ; ┃ 8 ┃   ┃ 6 ┃   ┃
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃ 0   0 ┃   ┃   ┃ 2   2   2   2 ┃   ┃ ;   ; ┃ 8 ┃   ┃ 6 ┃   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
24 shapes placed
```
(24 unoccupied cells)

## 5. Simulated tiles

A *Tile* instance is just a maze, but it happens to be defined in a different way.  So it might be useful to transform one directly into the other.  Going from tile to maze is straightforward -- drop the tile into an empty maze. (At this writing, this is only supported for rectangular mazes.)

For the other direction, there is a utility called *maze2tile* in the *mazes/testris* folder.  It has a built in demo which creates an unrotated T tile:
```
    maze4c$ python -m mazes.tetris.maze2tile
    Simple test of maze2tile.py:
    Creating T maze
    T maze:
    +---+---+---+
    | T   T   T |
    +---+   +---+
    |   | T |   |
    +---+---+---+
    Creating T tile
    If this is working, you should see the description of a T tile:
      shape: {(1, 'east', 3), (1, 'west', 2), (0, 'north', 1)}
       bbox: (2, 3) 	-- (2 rows, 3 columns)
       zero: 1 		-- (column 1 of bottom row)
    SUCCESS!
```

Now let's use *maze2tile* to create a larger tile from a small perfect maze that we will create using Eller's algorithm.  We start in the Python interpreter with some imports...
```
    maze4c$ python
    Python 3.10.12
    >>> from mazes.Grids.oblong import OblongGrid
    >>> from mazes.maze import Maze
    >>> from mazes.Algorithms.eller import Eller
    >>> from mazes.tetris.maze2tile import maze2tile
```
Note that we don't need to import the *Tile* class.  The import of *maze2tile* implicitly handles that.

Next we create the maze.  Then we pick a starting cell for the tile:
```
    >>> maze = Maze(OblongGrid(4, 4))
    >>> print(Eller.on(maze))
          Martin Eller's Spanning Tree (statistics)
                            visits        4
                             cells       16
                          passages       15
               optional merge left        7
               required merge left        0
             required carve upward        6
             optional carve upward        2
                            onward  east
                            upward  north
    >>> start = maze.grid[0,2]
    >>> start.label = 'S'
    >>> print(maze)
    +---+---+---+---+
    |           |   |
    +   +---+---+   +
    |   |           |
    +   +   +---+   +
    |           |   |
    +   +   +---+   +
    |   |     S |   |
    +---+---+---+---+
```

Now we create the tile:
```
    >>> tile = maze2tile(maze, start)
```

Now let us check the result
```
    >>> type(tile)
    <class 'mazes.tetris.tile.Tile'>
    >>> tile.shape
    {(10, 'east', 11), (11, 'north', 14), (5, 'north', 6),
     (12, 'south', 13), (11, 'south', 12), (1, 'north', 2),
     (3, 'south', 4), (3, 'north', 5), (6, 'east', 7),
     (0, 'west', 1), (7, 'east', 8), (9, 'east', 10),
     (2, 'east', 15), (2, 'west', 3), (2, 'north', 9)}
    >>> tile.bbox
    (4, 4)
    >>> tile.zero
    2
```
That's a lot of shape to process.  Is it the right length?
```
    >>> len(tile.shape)
    15
```
The length is correct.  We should see each of the indices from 1 through 14 in the third entry of the vectors...  Let's let Python do the work...
```
    >>> sorted(list(v[3] for v in tile.shape))
    IndexError: tuple index out of range
```
Oops! the third entry in a vector is index 2, not 3.  Try again!
```
    >>> sorted(list(v[2] for v in tile.shape))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
```
Looks good!  Now let's drop it into a maze...  From a user standpoint, this is a bit clunky, but the intent is more as a tool to use in a program or a script.  We need to (1) create an empty maze, (2) set up the drop vector, (3) set up the occupation set, (4) drop the tile, and (5) carve the maze.  Here we go:
```
    >>> new_maze = Maze(OblongGrid(4, 4))
    >>> place = new_maze.grid[0,2]
    >>> places = [place]
    >>> occupied = set()
    >>> tile.drop(places, occupied)
    True
```
The *True* return value indicates that the drop was successful.
```
    >>> tile.carve(new_maze)
    15
    >>> print(new_maze)
    +---+---+---+---+
    |           |   |
    +   +---+---+   +
    |   |           |
    +   +   +---+   +
    |           |   |
    +   +   +---+   +
    |   |       |   |
    +---+---+---+---+
```
Success!  We reproduced the maze that was used to create the tile.  (The *carve* method returned the number of passages carved.)

## 6. Creating a maze with simulated tiles

Let's use simulated tiles to create a maze.  The idea here is to create a roomy structure using 4x4 square rooms built using Eller's algorithm.  The final structure will exhibit some bias (the square Elleresque rooms) and some randomness, as we will complete the maze using Kruskal's algorithm.

### 6.1 Hexadecominos

We start, as usual, with the imports:
```
    maze4c$ python
    Python 3.10.12
    >>>     # INITIALIZATION
    >>> from mazes.Grids.oblong import OblongGrid
    >>> from mazes.maze import Maze
    >>>     # PASSAGE CARVING ALGORITHMS
    >>> from mazes.Algorithms.eller import Eller        # tile carver
    >>> from mazes.Algorithms.tetris import Tetris      # passage carver 1
    >>> from mazes.Algorithms.kruskal import Kruskal    # passage carver 2
    >>>     # TILE ETCHER
    >>> from mazes.tetris.maze2tile import maze2tile
```

We need a subroutine to carve our tile essays and etch our 4x4 square tiles:
```
    >>> def make_shape():
    ...     maze = Maze(OblongGrid(4,4))
    ...     _ = Eller.on(maze)                        # ignore status
    ...     tile = maze2tile(maze, start=maze.grid[0,0])
    ...     box = tuple(list(tile.bbox) + [tile.zero])
    ...     shape = tuple(sorted(tile.shape))
    ...     return shape, box
    ...
```

We use this to create a bag of tiles
``` 
    >>> # create ten distinct tile types
    >>> tiles = list()
    >>> for _ in range(10):
    ...     tiles.append(make_shape())
    ...
```

Now we drop tiles into a large grid to create our 4x4 rooms:
```
>>> maze = Maze(OblongGrid(16,17))
>>> print(Tetris.on(maze, tiles=tiles, N=16, verify=False))
          Tetris tile carver (statistics)
                            visits      256
                             cells      272
                          passages      195
                        tile types       10
                             tiles       23
                             drops      222
                        placements       13
```

In the options, we set *N=16* to indicate that our *hexadecomino* tiles have 16 cells instead of the usual four.  We also set *verify=False* to indicate that we trust the etcher to produce valid tiles.

Here is the result.  I have numbered the 13 rooms (0 through 9 and A, B, C) in the upper left corner:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   | 0 |           | 1             |   |   |   | 2             |
+---+---+   +   +   +   +   +   +---+---+---+---+---+   +   +   +   +
|   |   |       |   |   |   |           |   |   |   |   |   |   |   |
+---+---+   +---+   +   +---+   +---+---+---+---+---+   +---+---+   +
|   |   |       |   |   |   |           |   |   |   |   |       |   |
+---+---+   +   +   +---+   +   +---+---+---+---+---+---+   +   +   +
|   |   |   |   |       |               |   |   |   |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 |           |   | 4             | 5     |       | 6 |           |
+   +   +   +   +---+   +---+---+---+---+   +   +---+   +   +---+   +
|       |   |   |   |   |           |               |   |       |   |
+   +---+   +   +---+   +   +---+---+   +---+   +   +   +   +---+---+
|       |   |   |   |           |   |   |       |   |               |
+   +   +   +---+---+   +---+---+   +---+   +   +   +   +   +---+   +
|   |   |       |   |               |       |   |   |   |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   | 7     |       |   | 8             |   | 9 |           |
+---+---+---+---+   +   +---+---+   +---+---+   +---+   +---+   +   +
|   |   |   |               |   |   |   |   |   |   |       |   |   |
+---+---+---+   +---+   +   +---+   +   +   +---+---+   +---+---+   +
|   |   |   |   |       |   |   |       |       |   |   |           |
+---+---+---+---+   +   +   +---+   +---+   +---+---+   +   +   +---+
|   |   |   |       |   |   |   |               |   |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   | A     |   |   | B |           |   |   | C     |   |   |
+---+---+---+   +---+   +   +   +   +   +   +---+---+   +---+   +   +
|   |   |   |               |       |   |   |   |   |               |
+---+---+---+---+   +---+---+   +---+   +   +---+---+---+   +---+---+
|   |   |   |   |           |       |   |   |   |   |   |           |
+---+---+---+   +---+   +   +   +   +   +---+---+---+   +---+   +   +
|   |   |   |           |   |   |   |       |   |   |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
We placed 13x16=208 cells in 13 rooms.  Each room has 15 passages for a total of 13*15=195 passages.  64 cells remain isolated and are not in any room.

To extend this forest to a perfect maze (i.e. a spanning tree), we need 272-195=76 more passages.  Now we run Kruskal's algorithm to connect the forest into a single tree:
```
>>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      136
                 components (init)       77
               queue length (init)      199
                             cells      272
                          passages       76
                components (final)        1
              queue length (final)       63
```
Here is the final result.  I have again identified the upper left corner of each of the 4x4 rooms:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |     0 |           | 1                 |   |     2             |
+   +---+   +   +   +   +   +   +---+---+---+   +---+   +   +   +   +
|       |       |   |   |   |                           |   |   |   |
+---+   +   +---+   +   +---+   +---+---+---+   +---+   +---+---+   +
|               |   |   |   |               |   |   |   |       |   |
+   +---+   +   +   +---+   +   +---+---+---+---+   +---+   +   +   +
|   |   |   |   |       |               |           |       |       |
+   +   +---+---+---+   +---+---+---+---+---+---+   +   +---+---+---+
| 3 |           |   | 4             | 5     |       | 6 |           |
+   +   +   +   +   +   +---+---+---+---+   +   +---+   +   +---+   +
|       |   |   |       |           |                   |       |   |
+   +---+   +   +---+   +   +---+---+   +---+   +   +   +   +---+---+
|       |   |   |               |   |   |       |   |               |
+   +   +   +---+---+   +---+---+   +---+   +   +   +   +   +---+   +
|   |   |           |               |       |   |   |   |       |   |
+---+---+   +   +---+---+---+   +---+   +---+---+---+---+---+   +---+
|           | 7     |       |   | 8                 | 9 |           |
+---+---+---+---+   +   +---+---+   +---+---+   +---+   +---+   +   +
|       |                   |   |   |   |   |   |   |       |   |   |
+---+   +---+   +---+   +   +   +   +   +   +---+   +   +---+---+   +
|               |       |       |       |           |   |           |
+   +---+   +---+   +   +   +---+   +---+   +---+   +   +   +   +---+
|   |       |       |   |       |               |   |       |       |
+   +   +---+---+---+   +---+---+---+---+---+   +   +---+---+---+---+
|   |       | A     |   |     B |               |     C     |   |   |
+---+   +---+   +---+   +   +   +   +   +   +   +---+   +---+   +   +
|           |               |       |   |   |   |                   |
+   +   +   +---+   +---+---+   +---+   +   +---+---+---+   +---+---+
|   |   |   |   |           |       |   |   |           |           |
+---+   +   +   +---+   +   +   +   +   +---+---+---+   +---+   +   +
|       |   |           |   |   |   |           |               |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Perhaps rooms A and B are the rooms belong to Hansel and Gretel, and room 2 is the evil hag's kitchen...

Or perhaps just note the boxy structure vaguely reminiscent of the the roomy bias in recursive division, as well as the more random corridors produced by Kruskal's algorithm that connect the rooms.

If we had used the simple binary tree algorithm, the roomy bias might be even more evident.  Recall that sidewinder, generalizes simple binary tree, Eller's algorithm generalizes sidewinder, and Kruskal's algorithm generalizes Eller's algorithm.  In this context, the verb "to generalize" means that the set of choices that can be made by the object algorithm is a proper subset of the list of choices that can be made in the subject algorithm.

### 6.2 Pentominos

For another example of tile simulation, see module *mazes.tetris.pentris* and the code generator *mazes.tetris.pentris_generator*.  These are documented in the file *mazes/tetris/pentris.md*.
