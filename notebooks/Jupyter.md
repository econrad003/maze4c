# Running mazes in Jupyter

You can, of course, add the folder containing the *mazes* package to the *PYTHONPATH* environment.  (That might be the most portable approach.)

Another option is to change the current directory in the notebook.  That is the approach we have taken here.

The folder containing the *mazes* package is the parent folder of the folder containing this notebook.  In Unix-like operating systems, the parent folder can be accessed as *..*.  (Linux, Mac, and Windows all follow this convention.)  The following Python code sets the current working directory to the parent folder:


```python
import os
os.chdir(os.path.expanduser(".."))
```

You might need to modify the code above to suit your own needs.  In particular, you will probably want to change the folder from *".."* to a relative path from the directory containing your Jupyter notebooks to the folder that contains the *mazes* package.

Good luck!

## Proof of concept

Now we verify that this works (under Linux Mint)...

First we import a few classes:


```python
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson
```

Next we create and display a maze...


```python
maze = Maze(OblongGrid(8, 13))
print(Wilson.on(maze))
print(maze)
```

              Circuit-Eliminated Random Walk (Wilson) (statistics)
                                visits       42
                                 cells      104
                              passages      103
                     paths constructed       42
                         cells visited      383
                              circuits       96
                        markers placed      245
                       markers removed      142
                         starting cell  (3, 9)    
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |                       |   |                   |
    +   +   +---+---+   +   +---+   +---+   +---+   +---+
    |       |           |           |       |   |   |   |
    +   +   +---+---+---+---+   +---+   +   +   +   +   +
    |   |           |       |           |       |   |   |
    +---+   +   +---+   +   +   +---+---+---+---+---+   +
    |       |   |   |   |                       |       |
    +   +   +---+   +---+---+   +---+---+---+   +   +   +
    |   |       |           |           |   |       |   |
    +---+   +---+---+   +---+---+   +   +   +   +   +   +
    |           |   |       |       |       |   |   |   |
    +---+---+---+   +---+   +   +---+   +---+   +---+   +
    |                           |           |   |       |
    +---+   +---+---+---+---+---+---+   +---+---+   +   +
    |               |                   |           |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+


## Timestamp


```python
import datetime
t = datetime.datetime.now()
print(t)
```

    2026-01-11 18:31:06.891472



```python

```
