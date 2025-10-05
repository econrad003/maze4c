# Saving a maze for future use

## Description

You've just created a wonderful maze -- but you need to shut things down for some reason... This is about saving it so you can reload it in a separate Python session...

If you've populated one of the available grids, then you're in luck.  For a more exotic grid, you might need to do some additional work.

One example (in three parts) should suffice to explain how it's done and the limitations of the process.

## Example 1A) Saving a maze to a CSV file

The tool is a CSV (or comma-separated variable) file -- well actually it's a PSV (for pipe-separated variable) file or a VBSV (for vertical-bar-separated) file.  Since commas are used in tuples and tuples are used as cell indices, the vertical bar just happens to be more convenient for this purpose.

Let's create a maze... We'll use Wilson's algorithm:
```
$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(8, 15))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       46
                             cells      120
                          passages      119
                 paths constructed       46
                     cells visited      703
                          circuits      190
                    markers placed      467
                   markers removed      348
                     starting cell  (1, 11)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |       |   |                           |       |       |
+   +   +---+   +   +---+---+   +---+---+   +   +   +---+   +
|                   |       |   |   |           |           |
+---+---+   +---+---+   +---+   +   +---+   +   +---+   +---+
|   |   |           |       |   |       |   |   |           |
+   +   +   +---+---+---+   +---+   +   +   +---+---+---+---+
|           |                   |   |   |       |   |       |
+---+   +   +---+---+---+   +   +   +---+---+   +   +   +   +
|       |               |   |   |           |           |   |
+   +---+   +---+   +---+   +   +   +---+   +---+   +   +---+
|       |   |       |   |   |   |   |           |   |       |
+   +---+---+   +---+   +   +   +---+   +---+   +   +---+   +
|   |   |           |   |   |           |   |       |   |   |
+---+   +---+   +   +   +   +   +---+   +   +   +---+   +   +
|               |   |       |       |       |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Now let's create a CSV file to represent this maze.  We need to import the *save\_to* method, and we need to call it with our maze and a filename:
```
>>> from mazes.save_maze import save_to
>>> save_to(maze, "spam.csv")
Saving maze to : spam.csv
Grid type: OblongGrid
positional arguments: (8, 15)
keyword arguments: {}
gathering information:
	cells... 120 cells
	joins... 119 joins (119 edges, 0 arcs)
Saving...
```
What's actually saved is the name of the grid class, constructor arguments, the indices of all cells that are contained in passages, whether undirected (*i.e.* maze edges) or directed (*i.e.* maze arcs).

At this writing, none of our maze algorithms create directed (or one-way) passage, but they are handled by method *save\_to*.

In addition, passage weights are also saved.

Apart from the name of the grid class and a string representation of the constructor arguments, the grid information is not saved.  We'll see how that works in parts B and C...

Before leaving the python session, let's save the drawing above to a file:
```
>>> with open("spam_maze1.txt", "w") as fout:
...    fout.write(str(maze))
...
1053
```
And we exited Python, so the maze is gone.

That last line is the number of characters written to the file.  From the linux command line:
```
$ wc spam_maze1.txt
  16  140 1053 spam_maze1.txt
```

And here are the first seven and last five lines of the CSV file:
```
$ head -n 7 spam.csv
op|A|B|C
cls|OblongGrid||
arg|8||
arg|15||
cell|0|(0, 0)|
cell|1|(0, 1)|
cell|2|(0, 2)|
$ tail -n 5 spam.csv
edge|74|59|1
edge|90|105|1
edge|99|100|1
edge|83|98|1
edge|86|101|1
```
The first line is a header and the next four lines tell us that the grid was created with the call:

* *OblongGrid(8, 15)

If there were a keyword argument like *parity=True*, we would see a line like:
```
    kwarg|parity|True|
```

The *cell* lines identify the cells in the grid and their indices.  Cells that have no passages are numbered but omitted in this file.  So the first *cell* line tells us that cell #1 is the cell in the lower left.

The last *edge* line tells us that there is a passage of weight 1 from cell #86 to cell #101.  (If no weight was specified in the *link* method, the weight of a link is 1.)

If there were directed passages, we would see some *arc* lines.  For example, a directed passage of weight 271828 from cell #42 to cell #314159 would appear as:
```
    arc|42|314159|271828
```

## Example 1B - recreating the grid (hints)

Before we load a maze from a CSV file, we need to create a maze object with an embedded grid.  But if we didn't write down the needed information, can we somehow retrieve it?

As long as we didn't add cells to the grid, we can get an important hint.  Let's bring up the python interpreter and import two methods:
```
$ python
Python 3.10.12
from mazes.load_maze import load_from, hint_from
```

The *load\_from* method displays some of what we need:
```
>>> load_from("spam.csv")
maze = Maze(OblongGrid(8, 15))
```
Of course we would need to import the *Maze* and *OblongGrid* classes.

If we want to write a special handler that automates the imports and calls, we could have the handler call method *hint_from*:
```
>>> hint_from("spam.csv")
'OblongGrid(8, 15)'
```

Method *load\_from* with no maze displays a statement to standard output, but returns nothing, while method *hint\_from* displays nothing, but returns a string which shows call information for the grid.

## Example 1C - recreating the maze

Now let's recreate the maze from CSV file *spam.csv*.  We bring up Python and import *load\_from*:
```
$ python
Python 3.10.12
>>> from mazes.load_maze import load_from
>>> load_from("spam.csv")
maze = Maze(OblongGrid(8, 15))
```

The *Maze* class is in module *mazes.maze* and the *OblongGrid* class is in *mazes.Grids.oblong*.  If the call arguments are not to complicated, we can copy and paste the assignment of *maze* into the console:
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8, 15))
```

Now (finally!) we let *spam.csv* do some actual work:
```
>>> load_from("spam.csv", maze)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |       |   |                           |       |       |
+   +   +---+   +   +---+---+   +---+---+   +   +   +---+   +
|                   |       |   |   |           |           |
+---+---+   +---+---+   +---+   +   +---+   +   +---+   +---+
|   |   |           |       |   |       |   |   |           |
+   +   +   +---+---+---+   +---+   +   +   +---+---+---+---+
|           |                   |   |   |       |   |       |
+---+   +   +---+---+---+   +   +   +---+---+   +   +   +   +
|       |               |   |   |           |           |   |
+   +---+   +---+   +---+   +   +   +---+   +---+   +   +---+
|       |   |       |   |   |   |   |           |   |       |
+   +---+---+   +---+   +   +   +---+   +---+   +   +---+   +
|   |   |           |   |   |           |   |       |   |   |
+---+   +---+   +   +   +   +   +---+   +   +   +---+   +   +
|               |   |       |       |       |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

This looks right, but let's compare the two outputs using the linux shell command *diff*.  Save the display as before:
```
>>> with open("spam_maze2.txt", "w") as fout:
...    fout.write(str(maze))
...
1053
```

That's the correct number of lines.  Now back to the command line:
```
$ diff spam_maze1.txt spam_maze2.txt
```
The *diff* command returned nothing -- that's good news!

## NOTE 1 *diff* -- what if there had been a difference?

If there had been any differences, we would have seen something like the following:
```
$ diff spam_maze1.txt spam_maze3.txt
3c3
< +   +   +---+   +   +---+---+   +---+---+   +   +   +---+   +
---
> +   +---+   +   +   +---+---+   +---+---+   +   +   +---+   +
```

## NOTE 2 *Linux* commands used in this document

Users of operating systems other than Linux might need to find alternatives to some of these commands in order to run their own tests.

* *head* - display the first few lines of a stream.
* + `head -n 7 FILENAME` - displays the first seven lines
* *tail* - display the last few lines of a stream
* + `tail -n 5 FILENAME - display the last five lines
* *wc* - display character counts for a file; in order the counts are the number of lines, the number of words, and the number of characters
* *diff* - looks for differences in two text files

To produce *spam\_maze3.txt* for *NOTE 1* showing what *diff* does with differences, I used the *vim* editor and a utility *trucate* to remove the trailing newline that was added by *vim*.  I used *vim* to move the passage (7,1)--(6,1) one cell to right.  This changed line 3 of the file.