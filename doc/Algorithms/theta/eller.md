# The Polar Analogues of Eller's Algorithm

The polar analogues of Eller's algorithm include an inbound version ("inward Eller") and an outbound version ("outward Eller").  They are built on the edifice used to implement Eller's algorithm in a rectangular maze.

## The algorithm

The algorithm in both cases is just Eller's algorithm.  Instead of rows, we use
annular rings.  The direction of flow in a ring (clockwise or counterclockwise) does not make a difference, but we do need to designate a start/stop boundary for each ring.  Rings are either processed from the outermost ring into the pole (inward Eller) or from the pole outward ("outward Eller").

As in the rectangular algorithm, cells in a ring are first optionally merged with predecessors.  This merge phase creates tracks analogous to the runs created in sidewinder or its polar analogues (inwinder and outwinder).  Unlike the runs in sidewinder, these tracks can have gaps, but they are in the same component.

As in sidewinder, after the lateral merges for a ring are completed, passages are carved from each of the tracks into the next ring.  For each track, at least one such passage must be carved.  (The sidewinder algorithm is the special case where exactly one passage is carved from each track.)  The only requirement for additional passages is that no circuit be created.  (This condition is enforced by insuring that the optional passages may only join cells in different components.  This condition is the same condition that insures that Kruskal's algorithm does not yield a circuit.)

## Example 1 - Inward Eller

In our examples, we use a script to create the maze.  We will follow the examples with some of the details.  For our first example, we will create
a maze using the inbound version of Eller's algorithm.

```
    maze4c$ python -m tests.polar_eller --output maze.png
    Namespace(radius=5, pole_cells=6, split=1, outbound=False,
      flip=0.5, toss=0.3333333333333333, debug=False, title='', color=False,
      output='maze.png')
    creating the grid (radius=5, pole cells=6, split=1)...
    carving the maze (outbound=False, flip=0.5, toss=0.3333333333333333)...
    Initializing: self.__inward=True
          Polar Eller (statistics)
                            visits        5
                             cells      114
                          passages      113
               optional merge left       40
               required merge left        3
             required carve upward       45
             optional carve upward       11
                            onward  ccw
                            upward  inward
    Saving image as: maze.png
```

Here, apart from the "--output" option, we simply used the defaults.  (The script displays the actual values.  Note that the default direction is "inward", and the defaults for grid creation are 5 rings, 6 cells at the pole, and a split length of 1.

The output file from this run was moved to the gallery as:

* *gallery/theta/inward\_Eller.png*

## Example 2 - Outward Eller

We will create a larger grid with 8 rings and a single cell at the pole.  The carving algorithm is outward Eller:

```
    maze4c$ python -m tests.polar_eller --output maze.png -o -p 1 -r 8
    Namespace(radius=8, pole_cells=1, split=1, outbound=True, flip=0.5,
        toss=0.3333333333333333, debug=False, title='', color=False,
        output='maze.png')
    creating the grid (radius=8, pole cells=1, split=1)...
    carving the maze (outbound=True, flip=0.5, toss=0.3333333333333333)...
    Initializing: self.__inward=False
          Polar Eller (statistics)
                            visits        8
                             cells      246
                          passages      245
               optional merge left       98
               required merge left       25
             required carve upward       67
             optional carve upward       55
                            onward  ccw
                            upward  outward
Saving image as: maze.png
```

The output file from this run was moved to the gallery as:

* *gallery/theta/outward\_Eller.png*

## Under the Hood

The script's options can be viewed using the "-h" option.  These suffice for straightforward cases, but for fancier situations it may help to have an "under the hood" view.

The first step, as usual, is to create the grid:
```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.polar import ThetaGrid
    2> from mazes.maze import Maze
    3> maze = Maze(ThetaGrid(5))
```

Next we run the maze carving algorithm:
```
    4> import mazes.Algorithms.polar.eller as PE
    5> print(PE.PolarEller.on(maze))   # CARVE THE MAZE
```

The default for *PE.PolarEller* is outward.  We encapsulate the maze carving in a print method in order to display the resulting status.

To change the direction to inward, we specify the upward direction as inward:
```
    5> print(PE.PolarEller.on(maze, upward=PE.INWARD))
```

There are several other options.  These are documented in the source code for class *PE.PolarEller* under the method *parse\_args*.  (Read the documentation!)  As an example, if we want to change the coin flip bias from 50% to 75%, we need to format the parameter as:

```
          (PE.coin\_toss, (), {"bias":3/4})
```

The method *PE.coin\_toss* is just a *p*-distribution simulator taking no optional arguments (hence the second argument is an empty tuple), and having a keyword argument ("bias") which takes a floating point value between 0 and 1, inclusive.  The value 3/4 is equivalent to 75% or 0.75.
```
    5> print(PE.PolarEller.on(maze, flip1=(PE.coin\_toss, (), {"bias":3/4})))
```

(The script that was used in the examples handles this particular situation using the "--flip" option with a value of 0.75.  It won't accept fractions.)

To save and display the sketch:
```
    6> from mazes.Graphics.polar1 import Phocidae
    7> spider = Phocidae(maze)
    8> spider.setup()
    9> spider.title("My Fancy Polar Eller Maze")
    10> spider.draw_maze()
    11> spider.save_image("my_fancy_maze.png")   # SAVE IMAGE
    12> spider.show()                            # DISPLAY MAZE
```

