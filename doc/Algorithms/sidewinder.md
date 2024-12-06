# Sidewinder

Sidewinder is a *generalization* of the Simple Binary Tree algorithm.

## The Algorithm v1

Start with an empty rectangular grid with n cells.

In each row, proceeding from west to east, we keep track of our runs.  In a given cell where we have a choice of carving a passage east or north, we toss a coin.  If the coin lands face up we choose a cell in the run and carve a passage to the north.  If it lands face down, we carve east, adding this cell to the current run.  If this is the end of a row other than the north row, as with the face up coin, we choose a cell in the current run and carve a passage north.  In the north row, all that we can do is carve east until we reach the least cell.

In the northeast cell do nothing.  In the remaining cells in the north row, carve a passage east.  In the remainder of the east column, carve north.  In the remaining cells, toss a coin.  If it lands face up, carve north otherwise carve east.

## The Algorithm v2

```
Prerequisite: An empty rectangular grid with n cells

local data:
    run : list (empty)

In each cell:
    if there is a way east:
        if there is a way north:
            add the cell to the run
            toss a coin:
               (head) choose a random cell in the run and carve north
                      empty the run
               (tail) carve east
        otherwise:
            carve east
    otherwise:
        if there is a way north:
            carve north
        otherwise:
            do nothing
```

See also: Jamis Buck, *Mazes for Programmers*, 2015 (Pragmatic Bookshelf), *pp* 12-15, 27-29, 254-255.

### Example 1

We bring up the python interpreter:
```
    maze4c$ python
    Python 3.10.12
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(5, 8))
    4> from mazes.Algorithms.sidewinder import Sidewinder
    5> print(Sidewinder.on(maze))
```

Lines 1, 2 and 3 set up the prerequisites, in this case an empty rectangular maze with 5 rows and 8 columns.
```
          Sidewinder Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
```

The maze that was carved has n=5x8=40 cells and n-1=39 passages.  If the result is connected, then it will be a tree.  Here is the maze:
```
    6> print(maze)
    +---+---+---+---+---+---+---+---+
    |                               |
    +---+   +---+---+   +   +   +---+
    |               |   |   |       |
    +   +---+---+   +   +---+---+   +
    |   |           |       |       |
    +   +   +   +---+   +---+---+   +
    |   |   |       |   |           |
    +   +   +---+---+   +   +   +   +
    |   |   |           |   |   |   |
    +---+---+---+---+---+---+---+---+
```

As with the simple binary tree algorithm, there is an easy way to get to the northeast corner: go north if we can, otherwise try going east.  So we have a connected maze with n-1 passages -- it's a tree!

This particular example is actually a binary tree as there are no degree 4 cells (cells with four passages).  But sidewinder can create degree 4 cells.

### Some Options

Let's look at how we might play with the sidewinder implementation...  The class *Sidewinder* doesn't actually do much by itself.  We run a class method called *Sidewinder.on*.  This method creates a *Sidewinder.Status* class instance and then repeatedly calls the *visit* method (in the *Status* instance) until told there is no more (method *more* in the *Status* instance).

So where can we look for advice?  The *parse\_args* method in the *Status* class is where the documentation is located.

```
   7> print(Sidewinder.Status.parse_args.__doc__)
   parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                name - handled by __init__ in the base class.

                onward - the onward directions (tail). The default is "east".

                upward - the upward direction (head). The default is "north".

                flip - a function which takes a cell and some keyword arguments
                    as input and returns a boolean value: True for a head and
                    False for a tail.  The default is method 'cointoss' defined
                    above.

                choose_in_run - a function which takes a run and some keyword
                    arguments and returns an ordered pair from the run.  The
                    default is 'run-choice' defined above.

                bias - the probability of a head.  This argument is passed to
                    flip, if present.

                which - the Python built-in any, or an integer, or a tuple of
                    integers which controls the way elements of a run are
                    chosen for carving in the upward direction.
```
This is terse, intended more for programmers than users.  The onward, upward and bias arguments work the same way that they do in the simple binary tree algorithm.  Onward and upward are compass directions and bias is a con toss probability,  The methods *flip* and *choose\_in\_run* are programmed functions.  I will cover *flip* in Example 4.  The description of *which* definitely needs work, but Examples 2 and 3 will use *which*.

The *choose\_in\_run* option could be used to create unusual biases. I'll leave it as a programming exercise.

### Example 2

The which argument allows us to choose from particular elements of the run.  The run itself is just a list.  If it contains 3 entries, the possible indices are 0, 1, 2 (for first, second or third) or -1, -2, -3 (for last, next to last, second from last).  If I enter an invalid index, the default run choice method  will simply fall back to a random choice from the run.

The simple binary tree algorithm is equivalent to setting *which=-1* (for choose last).  If instead I try *which=0$ (for choose first), the result is really just simple binary tree with *onward=west* instead of *onward=east*.

I can combine both approaches as *which=(0,-1)*.  The result is a binary tree which is just a little bit more complicated than the simple binary tree.  That's what I will do...

```
    8> maze = Maze(OblongGrid(5, 8))
    9> print(Sidewinder.on(maze, which=(0,-1)))     # Cocktail Shaker
          Sidewinder Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
    10> print(maze)
    +---+---+---+---+---+---+---+---+
    |                               |
    +   +   +   +   +---+   +   +   +
    |   |   |   |       |   |   |   |
    +   +   +   +---+   +---+---+   +
    |   |   |       |   |           |
    +---+   +---+   +   +---+   +   +
    |       |       |       |   |   |
    +   +   +---+---+   +---+---+   +
    |   |   |           |           |
    +---+---+---+---+---+---+---+---+
```

### Example 4

In this example, in runs of three or more cells, I choose the third cell to carve north.  In runs of 1 or 2 cells, the northward choice is random.  To insure that I get some longer runs, I will make the maze wider a use a smaller bias (increasing the probability of tails).

Remember that Python list indices are numbered starting from 0, so the third entry is entry number 2.

```
    11> maze = Maze(OblongGrid(5, 13))
    12> print(Sidewinder.on(maze, which=2, bias=1/5))
          Sidewinder Tree (statistics)
                            visits       66
                             cells       65
                          passages       64
                            onward  east
                            upward  north
                              bias        0.2000
    13> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                                                   |
    +---+---+   +---+---+---+---+---+---+---+   +---+   +
    |         C                     |         C     | A |
    +   +---+---+---+   +---+---+---+---+---+---+---+---+
    |     B |         C                                 |
    +   +   +---+---+   +---+---+---+---+---+---+---+   +
    | A | A |         C                         |     B |
    +---+---+   +---+---+   +---+---+---+---+---+---+   +
    |         C |         C                 |         C |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
(The cells we labelled manually, with A-rise in first cell, B-rise in second cell, and C-rise in third cell.)

### Example 5

This example illustrates the use of the *flip* keyword argument.  In lines 13 and 14, I created a magical coin that lands face down the first time, and alternates faces each time it is tossed.  Lines 15 creates the uncarved maze and line 16 runs sidewinder using this magical coin.  Line 17 displays the result.

```
    13> from mazes.tools.flipflop import FlipFlop
    14> magicalcoin = FlipFlop(False, True)
    15> maze = Maze(OblongGrid(5, 8))
    16> print(Sidewinder.on(maze, flip=magicalcoin.value))
          Sidewinder Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
    17> print(maze)
    +---+---+---+---+---+---+---+---+
    |                               |
    +   +---+   +   +---+   +---+   +
    |   |       |       |       |   |
    +   +---+---+   +   +---+---+   +
    |       |       |       |       |
    +   +   +---+   +---+---+   +   +
    |   |       |       |       |   |
    +---+   +---+   +---+   +---+   +
    |       |       |       |       |
    +---+---+---+---+---+---+---+---+
```

Note that this maze is a binary tree.  The reason is connected to the lengths of the runs.

### Example 6

Here is another example using *flip*.  In this case I used a specially made magical coin to force all the runs (except the top row) to be four cells in length.  Note that the coin runs through seven values, not eight.  There is no coin flip in the last column.

```
    18> from mazes.tools.counter import Counter
    19> magicalcoin = Counter(False, False, False, True, False, False, False)
    20> maze = Maze(OblongGrid(5, 8))
    21> print(Sidewinder.on(maze, flip=magicalcoin.value))
          Sidewinder Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
    22> print(maze)
    +---+---+---+---+---+---+---+---+
    |                               |
    +---+   +---+---+---+---+---+   +
    |               |               |
    +---+   +---+---+---+---+   +---+
    |               |               |
    +---+---+   +---+---+   +---+---+
    |               |               |
    +---+---+   +---+---+---+   +---+
    |               |               |
    +---+---+---+---+---+---+---+---+
```

Note the degree 4 cells in the second and fourth rows.  This spanning tree is not a binary tree.