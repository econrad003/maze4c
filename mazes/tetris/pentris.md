# Pentris - playing with pentominos (5-celled tiles)

## The shape maker

The module that creates the pentomino shapes is *mazes.tetris.pentris*.  There are 58 distinct shapes and a number of ways to select all or some of them.

```
    maze4c$ python
    Python 3.10.12.
    >>> import mazes.tetris.pentris
    >>> mazes.tetris.pentris.__all__
    ('shape_lists', 'select_all', 'sample', 'tee', 'ell', 'squares',
     'stubbies', 'shape_range')
```
The data item 'shape_lists' is a list containing several lists, each of which contains all the descriptors for a given shape.  For a given shape, every distinct rotation of every perfect maze on that shape is contained in one entry.  The first entry contains just two descriptors, namely five in a row horizontally and a rotation giving five in a column vertically.

The remaining shapes have either 4 descriptors (each representing a rotation) or 12 descriptors (3 ways to connect the tile with no circuits times 4 rotations per connection).

## Preliminaries

The pentomino tilings carve disconnected forests into rectangular mazes, so we to import the *OblongGrid* and the *Maze* classes:

```
    maze4c$ python
    Python 3.10.12.
    >>> from mazes.Grids.oblong import OblongGrid
    >>> from mazes.maze import Maze
```

If we want to extend the forest to a perfect maze, we need an algorithm like Kruskal's or a growing tree algorithm which can connect a maze only as many passages as is absolutely necessary.  We will use Kruskal's algorithms in our examples:

```
    >>> from mazes.Algorithms.kruskal import Kruskal
```

Finally, we need the tile drop algorithm and the pentomino shapes:

```
    >>> from mazes.Algorithms.tetris import Tetris    # passage carver
    >>> from mazes.tetris.pentris import *            # bag of tiles
```

Let's verify that we imported the tile methods.  We use help:

```
    >>> help(sample)
    Help on function sample in module mazes.tetris.pentris:

    sample(k: int, fill=False, replace=False) -> list
        choose at most k shapes from each list, without replacement

        If a list contains fewer than k shapes, then some shapes will
        be underrepresented.  If you want a full complement of each
        shape set 'fill' to True.  If you want the choices to be made
        with replacement, set 'replace' to True.  Note that if 'replace'
        is True, the the setting of 'fill' is ignored.  If 'fill' is True
        and 'sample' is False, then duplicates will be kept to a minimum.
    (END)
```

So far, so good.  Now let's check what we need for the Tetris tile-drop algorithm.  To do this, we need to look at method *parse_args* in the *Tetris.Status* class.  (This class is derived from the *Algorithm.Status* class and class Tetris is derived from the *Algorithm* class.  These two base classes establish the usual calling conventions for our algorithms that generate mazes.)  Here is the relevant documentation:
```
    >>> help(Tetris.Status.parse_args)
    parse_args(self, tiles: 'TileDescriptorSet' = None, debug=False)
        parse constructor arguments

        POSITIONAL ARGUMENTS

            maze - handled by __init__ in the base class.
                The grid must be an instance of class OblongGrid
                or a subclass thereof.

        KEYWORD ARGUMENTS

            tiles - the tile descriptors; each descriptor is a
                tuple consisting of a tile shape descriptor, a
                tile width, a tile height, and the column location
                of the start cell for the tile. (The starting cell,
                cell 0, is always a cell in the bottom row.)

                If this argument is None, then the descriptor
                set is the set named "configs" imported from
                mazes.tetris.tetris.

                Method "create_tile" defined above is used to
                create the tiles that are dropped.

            N - the number of cells in a tile (default: 4)

            verify - set to False to suppress checks that the
                shape is connected and circuit-free.

        make_tile - use this option to change the tile creation
                routine.
    (END)
```
(This display is likely to change as the algorithm is enhanced to handle fancier tile sets.)

Now we are ready.

## Dropping tiles

Of course we need some tiles.  Let's just use all of them in our first examples:
```
    >>> tiles = select_all()
    58 shapes
```

We need an empty maze to drop the tiles into:
```
    >>> maze = Maze(OblongGrid(10,15))
```

The title drop assumes that tetrominos are being dropped.  We have pentominos, so we need a list of tiles and we need to indicate that they are pentominos.
```
    >>> print(Tetris.on(maze, tiles=tiles, N=5))
          Tetris tile carver (statistics)
                            visits     1114
                             cells      150
                          passages      100
                        tile types       58
                             tiles       83
                             drops      972
                        placements       25
```
With 25 placements, we covered 125 of the 150 cells. At four passages per pentomino, we have a total of 100 passages of the 149 required for a perfect maze. Here is what we have so far:
```
    >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |                   |       |   |       |   |   |   |   |
    +   +---+---+---+---+---+   +---+---+   +---+   +---+---+---+
    |       |   |   |   |   |       |   |       |               |
    +   +---+---+   +---+---+---+   +---+---+   +---+---+---+---+
    |   |           |       |   |   |   |   |   |       |   |   |
    +   +---+---+   +   +---+---+---+---+---+---+---+   +   +---+
    |   |   |   |   |   |               |       |       |       |
    +---+   +---+---+   +---+   +---+---+---+   +   +---+   +---+
    |   |   |       |       |   |   |   |       |   |   |   |   |
    +   +   +   +   +---+---+---+---+   +---+   +---+   +   +---+
    |   |   |   |   |   |           |       |   |   |   |   |   |
    +   +   +   +---+   +   +---+   +   +---+---+---+   +---+---+
    |   |   |   |   |   |   |   |   |       |   |   |           |
    +   +   +---+   +   +---+---+---+---+---+---+---+---+---+---+
    |   |   |       |       |               |   |       |       |
    +   +---+---+   +   +---+---+---+   +---+   +   +---+   +---+
    |   |   |       |   |   |   |   |   |   |   |       |   |   |
    +---+   +---+---+---+   +---+   +---+   +   +   +---+   +---+
    |   |               |           |   |       |   |   |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Let's manually label the 25 pentominos:
```
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    | a | b   b   b   b   b | c   c |   | d   d | e |   |   |   |
    +   +---+---+---+---+---+   +---+---+   +---+   +---+---+---+
    | a   a |   | f |   |   | c   c |   | d   d | e   e   e   e |
    +   +---+---+   +---+---+---+   +---+---+   +---+---+---+---+
    | a | f   f   f | g   g |   | c |   |   | d | h   h | i |   |
    +   +---+---+   +   +---+---+---+---+---+---+---+   +   +---+
    | a | j |   | f | g | k   k   k   k | l   l | h   h | i   i |
    +---+   +---+---+   +---+   +---+---+---+   +   +---+   +---+
    | m | j | n   n | g   g | k |   | o | l   l | h | p | i |   |
    +   +   +   +   +---+---+---+---+   +---+   +---+   +   +---+
    | m | j | n | n | q | r   r   r | o   o | l |   | p | i |   |
    +   +   +   +---+   +   +---+   +   +---+---+---+   +---+---+
    | m | j | n | s | q | r |   | r | o   o |   |   | p   p   p |
    +   +   +---+   +   +---+---+---+---+---+---+---+---+---+---+
    | m | j | s   s | q   q | t   t   t   t | u | v   v | w   w |
    +   +---+---+   +   +---+---+---+   +---+   +   +---+   +---+
    | m | x | s   s | q | y |   | y | t | u | u | v   v | w |   |
    +---+   +---+---+---+   +---+   +---+   +   +   +---+   +---+
    |   | x   x   x   x | y   y   y |   | u   u | v |   | w   w |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
A few observations:  
1. We used the first 25 of the 26 letters of the English alphabet, so we did find all the pentominos.
2. Some configurations were used more than once.  (This is like tossing a coin or a die.  Tosses repeat in a relatively unpredictable way.)  For example, pentominos *c* and *d* are identical, likewise *j* and *m*.
3. Some configurations are congruent by rotation but not identical: compare *c* and *o*; or *b* and *m*.
4. Others are congruent by reflection, *e.g.* pentominos *a* and *k*.
5. Some have the same basic shape but are not congruent: *d* and *l*.

We can think of each pentomino and each isolated cell as a room. We need doors to connect the room.  That's where Kruskal's algorithm will enter the picture. To minimally connect this forest of rooms, we need exactly 49 doors:

```
    >>> print(Kruskal.on(maze))
          Kruskal (statistics)

                       visits      110
                 components (init)       50
               queue length (init)      166
                             cells      150
                          passages       49
                components (final)        1
              queue length (final)       56
```
Perfect!  Now let's see the result:
```
     >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |                               |       |   |       |   |
    +   +---+---+---+---+---+   +---+---+   +---+   +---+   +   +
    |       |           |           |           |               |
    +   +---+---+   +---+---+---+   +---+   +   +   +---+   +---+
    |   |           |       |   |           |           |   |   |
    +   +   +---+   +   +---+   +---+---+---+   +---+   +   +   +
    |   |   |   |       |               |       |       |       |
    +   +   +   +---+   +---+   +   +---+---+   +   +---+   +   +
    |   |   |       |           |   |   |       |   |       |   |
    +   +   +   +   +---+---+   +---+   +---+   +   +   +   +   +
    |       |   |   |   |           |       |   |   |   |   |   |
    +   +   +   +---+   +   +   +   +   +---+   +---+   +---+---+
    |   |       |       |   |   |   |       |       |           |
    +   +   +   +   +   +---+---+   +---+   +   +---+---+---+   +
    |   |   |       |       |               |   |       |       |
    +   +---+---+   +   +---+   +---+   +---+   +   +---+   +---+
    |   |           |   |   |   |   |   |   |   |       |       |
    +   +   +---+---+---+   +---+   +   +   +   +   +   +   +---+
    |   |               |                           |   |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+```
```

We can see a hint of the structure left from the pentomino placement.  I've labelled a few the cells in the display below.  Note in particular pentomino *g*:

```
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    | a |                     c   c     | d   d | e |       |   |
    +   +---+---+---+---+---+   +---+---+   +---+   +---+   +   +
    | a   a |           |     c   c |     d   d | e   e   e   e |
    +   +---+---+   +---+---+---+   +---+   +   +   +---+   +---+
    | a |           | g   g |   | c         | d   h   h |   |   |
    +   +   +---+   +   +---+   +---+---+---+   +---+   +   +   +
    | a |   |   |     g |               |       | h   h |       |
    +   +   +   +---+   +---+   +   +---+---+   +   +---+   +   +
    | m |   |       | g   g     |   |   |       | h |       |   |
    +   +   +   +   +---+---+   +---+   +---+   +   +   +   +   +
    | m     |   |   |   |           |       |   |   |   |   |   |
    +   +   +   +---+   +   +   +   +   +---+   +---+   +---+---+
    | m |       |       |   |   |   |       |       |           |
    +   +   +   +   +   +---+---+   +---+   +   +---+---+---+   +
    | m |   |       |       |               |   |       | w   w |
    +   +---+---+   +   +---+   +---+   +---+   +   +---+   +---+
    | m | x         |   | y |   | y |   |   |   |       | w     |
    +   +   +---+---+---+   +---+   +   +   +   +   +   +   +---+
    |   | x   x   x   x | y   y   y                 |   | w   w |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+```
```

## Extreme bias

We can bias the maze by restricting the tile set.  Let's build a maze using just one tile.  The worst choice is probably either of the A tiles.
```
    >>> from mazes.tetris.pentris import sA
    >>> print(sA[0])
    (((0, 'east', 1), (1, 'east', 2), (2, 'east', 3), (3, 'east', 4)),
     (1, 5, 0))
    >>> print(sA[1])
    (((0, 'north', 1), (1, 'north', 2), (2, 'north', 3), (3, 'north', 4)),
     (5, 1, 0))
```
The first of these is a row of 5 cells, the second a column. We set up the tile set:
```
    tiles = (sA[0],)
```
That comma is necessary since we want a 1-tuple containing a shape descriptor and not just a shape descriptor.  (We could use a list or a set and avoid the comma, but this is a teaching moment.)

Now we create a maze.  I'll go with 8x13 so the dimensions are not divisible by 5.  The drops are by column, but squeezing under can happen when something fits:
```
    >>> maze = Maze(OblongGrid(8,13))
    >>> print(Tetris.on(maze, tiles=tiles, N=5))
          Tetris tile carver (statistics)
                            visits       75
                             cells      104
                          passages       60
                        tile types        1
                             tiles       16
                             drops       57
                        placements       15
```

Before you see the result, make a guess...  Have you made your guess?  Good, take a look.  I added in the labels:
```
    >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   | a   a   a   a   a |   | b   b   b   b   b |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | c   c   c   c   c |   | d   d   d   d   d |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   | e   e   e   e   e |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | f   f   f   f   f | g   g   g   g   g |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   | h   h   h   h   h |   | i   i   i   i   i |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | j   j   j   j   j | k   k   k   k   k |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | l   l   l   l   l | m   m   m   m   m |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | n   n   n   n   n | o   o   o   o   o |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Note the horizontal chains of five cells.  So we expect to see longer than average horizontal chains in the finished maze...
```
    >>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits       71
                 components (init)       44
               queue length (init)      127
                             cells      104
                          passages       43
                components (final)        1
              queue length (final)       56
    >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |                       |                   |
    +   +---+---+---+   +---+   +---+---+---+   +---+---+
    |   |                   |   |                   |   |
    +   +   +---+---+---+---+   +   +---+   +---+   +   +
    |   |   |   |   |                   |   |   |       |
    +   +---+   +   +---+   +---+---+---+---+   +---+---+
    |   |   |                                           |
    +   +   +---+---+---+---+   +   +---+---+   +---+---+
    |       |                   |   |                   |
    +   +---+---+---+---+---+---+---+---+---+   +---+---+
    |       |   |                                       |
    +   +   +   +---+   +---+---+---+---+---+   +---+---+
    |   |                   |                   |       |
    +---+---+---+---+   +---+---+---+   +---+---+---+   +
    |                               |                   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## The squares

Now let's use one of our methods for selecting tiles -- we'll do the ones with 2x2 squares...   Original 10x15 size...

```
    >>> tiles = squares()
    24 shapes
    >>> maze = Maze(OblongGrid(10,15))
    >>> print(Tetris.on(maze, tiles=tiles, N=5))
          Tetris tile carver (statistics)
                            visits      480
                             cells      150
                          passages       92
                        tile types       24
                             tiles       47
                             drops      408
                        placements       23
```
The maze so far:
```
    >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |           |       |           |   |       |   |   |
    +---+---+---+---+   +   +---+---+   +---+---+   +   +   +---+
    |   | c   c |       |       |       |   |   |   |   |       |
    +---+   +---+---+---+---+   +---+---+   +   +   +---+   +   +
    | c   c   c |   |   |   |   |   |   |       |   |   |   |   |
    +---+---+---+---+---+   +---+---+---+---+   +---+---+---+---+
    |           |   |   |   | a   a   a |   |   |   |   |       |
    +---+   +   +---+   +   +   +   +---+---+---+---+---+   +---+
    |   |   |   |   |       | a | a |   |   |       |   |       |
    +---+---+---+---+---+---+---+---+   +   +---+   +   +   +---+
    |   |   |   |   |       |   |   |       |   |       |   |   |
    +---+   +---+---+   +---+   +   +---+   +---+---+---+---+---+
    |   |       |           |       |   |   |       | b   b |   |
    +---+   +---+---+---+---+---+   +---+---+---+   +   +---+---+
    |   |       |       |   |   |   |   |   |       | b   b |   |
    +---+---+---+   +   +---+   +---+---+---+---+   +   +---+   +
    |   |   |   |   |   |   |   |   |       |   |   | b |       |
    +   +   +---+   +---+   +   +---+---+   +   +---+---+---+   +
    |           |   |   |       |   |   |       |   |   |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
I manually labelled just three.

And now Kruskal:
```
    >>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      128
                 components (init)       58
               queue length (init)      160
                             cells      150
                          passages       57
                components (final)        1
              queue length (final)       32
    >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |           |       |           |           |   |   |
    +   +   +   +---+   +   +---+---+   +---+---+   +   +   +   +
    |   |       |       |       |           |   |   |           |
    +---+   +---+   +---+   +   +---+---+   +   +   +   +   +   +
    |           |           |       |           |   |   |   |   |
    +---+   +---+   +---+   +   +---+   +   +   +   +   +   +---+
    |           |   |   |   |           |   |   |   |   |       |
    +---+   +   +---+   +   +   +   +---+---+   +---+---+   +---+
    |   |   |   |   |       |   |       |   |       |           |
    +   +---+---+   +---+---+---+---+   +   +---+   +   +   +---+
    |   |       |               |           |           |       |
    +   +   +---+---+   +---+   +   +---+   +---+---+   +---+---+
    |                       |       |       |               |   |
    +---+   +---+   +---+---+---+   +---+---+---+   +   +---+   +
    |           |           |           |   |       |           |
    +---+---+   +   +   +---+   +   +---+   +   +   +   +---+   +
    |   |   |   |   |   |   |   |   |       |   |   |   |       |
    +   +   +   +   +---+   +   +   +   +   +   +---+---+---+   +
    |           |       |       |   |   |       |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
A maze of twisty passages all (somewhat) alike?  (For the reference, look up a text adventure from the 1970s known variously as Cave, Adventure, and Colossal Cave.) It contains 150 cells, 92+57=149 passages, and is connected (*i.e.* it has one component, so it is perfect (connected and circuit-free).

## Stubbies

The stubbies are the pentominos with maximum dimension 4...
```
    >>> tiles = stubbies()
    16 shapes
    >>> maze = Maze(OblongGrid(10,15))
    >>> print(Tetris.on(maze, tiles=tiles, N=5))
          Tetris tile carver (statistics)
                            visits      344
                             cells      150
                          passages       80
                        tile types       16
                             tiles       36
                             drops      291
                        placements       20
    >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |               |   |   |
    +   +---+---+---+   +---+---+   +   +   +---+---+---+   +---+
    |       |               |   |   |   |   |               |   |
    +   +---+---+---+---+---+---+   +   +---+---+---+---+---+   +
    |   |   | a |   |   |   |   |   |   |               |       |
    +   +---+   +   +---+---+---+   +   +---+---+---+   +---+   +
    |   | a   a |   |   |   |       |       |   |   |   |   |   |
    +---+---+   +   +---+   +---+---+---+---+---+   +---+---+   +
    |   |   | a |   |   |   |   | b |   |   |   |   |   |   |   |
    +---+---+   +   +---+   +---+   +---+---+---+   +---+---+---+
    |   |   | a |       |   |   | b   b   b   b |   |   |   |   |
    +---+---+---+---+---+   +---+---+---+---+---+   +---+---+---+
    |               |       |       |   |   |       |   |   |   |
    +---+---+   +---+---+---+   +---+---+---+---+---+---+   +---+
    |   |   |   |   |   |   |   |               |               |
    +---+---+---+---+---+---+   +---+   +---+---+---+---+---+---+
    |   |   |               |   |   |   |   |   |   |   |   |   |
    +---+---+---+   +---+---+   +---+---+---+   +---+---+   +---+
    |   |   |   |   |   |   |   |               |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Here I labelled two of them.  Now to perfection with Kruskal...
```
    >>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      104
                 components (init)       70
               queue length (init)      195
                             cells      150
                          passages       69
                components (final)        1
              queue length (final)       91
    >>> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |       |       |       |   |   |                       |
    +   +   +   +---+   +---+   +   +   +   +---+---+---+   +   +
    |       |                   |   |       |               |   |
    +   +   +---+---+---+---+   +   +   +---+---+---+---+---+   +
    |   |       |   |       |   |   |   |               |       |
    +   +---+   +   +---+   +---+   +   +---+---+---+   +   +   +
    |   |       |   |       |                   |   |       |   |
    +---+   +   +   +---+   +---+---+---+---+   +   +---+   +   +
    |       |   |   |           |   |       |   |       |   |   |
    +   +---+   +   +---+   +   +   +---+   +---+   +---+   +---+
    |   |       |       |   |                       |       |   |
    +   +---+---+   +---+   +   +---+---+---+---+   +   +---+   +
    |               |       |           |   |               |   |
    +   +---+   +---+---+   +   +   +---+   +---+---+---+   +   +
    |   |               |   |   |               |               |
    +---+   +   +---+---+---+   +---+   +   +---+---+   +---+---+
    |   |   |                   |   |   |   |       |       |   |
    +   +   +---+   +   +   +   +   +---+---+   +   +---+   +   +
    |       |       |   |   |   |               |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

