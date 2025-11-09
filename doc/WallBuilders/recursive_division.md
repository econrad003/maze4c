# Recursive division as a wall builder

## Contents

1. Programming implementation notes
2. A simple example
3. A room plan
4. An animation

## 1. Programming implementation notes

Recursive division is usually implemented as a wall builder, but it was implemented here first as a passage carver.  Our wall builder implementation was written by modifying a copy of the passage carver implementation.

There were relatively few changes.  The biggest change was removal of the *carve\_rooms* code -- it simply isn't needed in the wall builder.  Boarding up a room would be the counterpart, but one can just use *carve\_rooms=False* (the default!) with the passage carver implementation to achieve the same effect.

In addition, the methods *carve\_door\_east* and *carve\_door\_north* were replaced respectively by the methods *erect_wall_east* and *erect_wall_north*.  

Other changes, such as replacing classes *Algorithm* and *Algorithm.Status* by *AlgorithmWB* and *AlgorithmWB.Status* and, of course, updating the docstring were trivial in comparison.

## 2. A simple example

Run the wall building implementation of recursive division essentially as you would the passage carving version.  There are just two differences from a user standpoint:

1.  the module is in the *mazes/Wallbuilders* folder; and
2.  the *carve\_rooms* option is not available.

{The behavior is essentially the same as running the passage carver implementation with *carve\_rooms=True*.  If *min\_rows* and *min\_cols* are both 2, the resulting mazes are indistinguishable.)

### Session:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.WallBuilders.recursive_division import RecursiveDivision
>>> maze = Maze(OblongGrid(8, 13))
>>> print(RecursiveDivision.on(maze))
          Recursive Division (Wall Builder) (statistics)
                            visits      207
                             links      187
                             cells      104
                             walls      207
                       wall panels       84
                         max stack        8
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |   |       |   |   |   |   |   |
+---+---+---+   +---+   +---+   +   +   +   +   +   +
|       |   |   |           |   |   |           |   |
+   +   +   +   +   +   +   +   +   +---+   +---+   +
|   |               |   |           |   |       |   |
+   +---+   +---+   +---+   +---+---+   +   +   +   +
|   |       |       |           |   |       |   |   |
+   +---+---+---+---+   +   +---+   +---+   +---+   +
|           |       |   |   |   |   |               |
+---+   +---+   +---+   +   +   +   +   +   +   +   +
|       |   |       |   |               |   |   |   |
+---+   +   +   +   +---+---+---+---+---+---+   +   +
|   |   |   |   |   |   |       |   |   |       |   |
+   +   +   +---+   +   +   +   +   +   +   +   +   +
|                   |       |               |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Analysis:

187 links tells us that the maze object was prepared for crafting by adding 187 passages.  (This is handled by method *initialize()* in the base class *AlgorithmWB.Status*.)

Note that in each visit, one wall was erected.  But when a room consisted of two or more cells in a single row or a single column, no wall panels are erected as we need a door (*i.e.* a passage) to connect the two subdivisions.  Panels are added to separate subdivisions when a room spans cells in more than one row and more than one column.

Starting with 187 passages in the complete maze, after walling off 84 of those passages (with wall panels), we are left with 103 passages.  This is the required number of passages for a perfect maze (or spanning tree) on a grid with 104 cells.

The stack held a maximum of 8 rooms, so there were 8 levels of recursion.

The boxy structure characteristic of mazes produced by recursive division is evident in the maze above.

## 3. A room plan

Setting the options *min\_rows* and *min\cols* to values larger than 2 creates room plans.  (For the passage carving implementation, we would also need to specify *carve\_rooms=True* to call the room carver,)

The *label\_rooms* option can be set to *True* to supply labels for the rooms.

## Session:

Continuing with the imports in section 2, we have:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(RecursiveDivision.on(maze, label_rooms=True, min_rows=5, min_cols=5))
          Recursive Division (Wall Builder) (statistics)
                            visits       33
                             links      187
                             cells      104
                             walls       33
                       wall panels       48
                         max stack        4
                          passages      139
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| b   b   b   b | K   K   K   K   L | D   D   D   D |
+---+   +---+---+---+   +---+---+---+   +   +   +   +
| f   f   f   f   O   P   P   P   P | D   D   D   D |
+   +   +   +   +---+   +---+---+---+   +   +   +   +
| f   f   f   f | S   S   T   T   T | D   D   D   D |
+---+---+   +---+---+---+---+   +---+---+---+---+   +
| e   e   e   e | Z | X   X   X   X | F   F   F   F |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
| e   e   e   e | Y | X   X   X   X   F   F   F   F |
+   +   +   +   +   +   +   +   +   +   +---+---+---+
| e   e   e   e | Y   X   X   X   X | E   E   E   E |
+   +   +   +   +   +---+---+---+   +   +   +   +   +
| e   e   e   e | Y | W   W   W   W | E   E   E   E |
+   +---+---+---+   +   +   +   +   +   +   +   +   +
| c   c   c   c | Y | W   W   W   W | E   E   E   E |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

We can easily remove the labels:
```
>>> for cell in maze.grid:
...   cell.label = " "
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |                   |               |
+---+   +---+---+---+   +---+---+---+   +   +   +   +
|                                   |               |
+   +   +   +   +---+   +---+---+---+   +   +   +   +
|               |                   |               |
+---+---+   +---+---+---+---+   +---+---+---+---+   +
|               |   |               |               |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|               |   |                               |
+   +   +   +   +   +   +   +   +   +   +---+---+---+
|               |                   |               |
+   +   +   +   +   +---+---+---+   +   +   +   +   +
|               |   |               |               |
+   +---+---+---+   +   +   +   +   +   +   +   +   +
|               |   |               |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## An animation

### The video capture:

File #1: *movies/capture-rdiv-wb.mkv*   (wall builder)
File #2: *movies/capture-rdiv.mkv*  (passage carver)

### Capture Session:

Imports:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.WallBuilders.recursive_division import RecursiveDivision
>>> from mazes.Graphics.animation import Animation
```

Prepare the grid.  We don't want linking the complete grid to clutter the animation, so we call the *Maze.link\_all()* method right away:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> maze.link_all()
```

Now we configure the animation.  After resizing the graphics window to make it smaller, we reconfigure using the *Animation.configure()* method:
```
>>> spider = Animation(maze)
Verbose mode: hints will be displayed...
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
>>> spider.configure()             # AFTER RESIZING
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```

Next we recursively divide using the wall builder:
```
>>> print(RecursiveDivision.on(spider.maze))
          Recursive Division (Wall Builder) (statistics)
                            visits      207
                             links        0
                             cells      104
                             walls      207
                       wall panels       84
                         max stack        8
                          passages      103
```

At this point we set up our video capture software.  When ready:
```
>>> spider.animate()
```

Here is the console version of the maze that was crafted:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                           |           |   |       |
+---+   +---+---+---+   +---+   +---+   +   +---+   +
|   |               |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|       |   |   |   |       |   |       |           |
+---+   +---+---+---+   +---+---+   +---+---+   +---+
|   |               |                   |           |
+   +---+---+   +---+---+---+   +---+---+---+---+   +
|               |   |   |           |       |       |
+   +   +---+---+   +   +   +   +   +   +   +   +   +
|   |   |       |   |       |   |       |       |   |
+   +   +   +   +   +   +---+---+   +   +   +---+---+
|   |   |   |   |   |       |       |   |           |
+   +   +   +---+   +---+   +---+---+   +   +   +   +
|   |               |       |           |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Analysis of the video

File #1 is the result of our session.  As wall panel are erected, cells (the small squares turn blue and passages are erased.

File #2 was produced by the passage-carver implementation of recursive division.  For details, see Example 12 in *doc/animation.md*.
