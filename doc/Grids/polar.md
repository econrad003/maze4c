# Theta (or polar) grids

## Six cells at the pole

### Basic usage

As with making an oblong (or rectangular) maze, creating a theta (or polar or circular) maze consists of some basic steps:

1. create a grid;
2. encapsulate the grid in a maze object;
3. carve the maze; and
4. display the result.

There are some differences.  In particular, a theta maze is not easily displayed in a console window -- we use graphics drivers that have been written especially for theta mazes.

```
    Python 3.10.12.
    1> from mazes.Grids.polar import ThetaGrid
    2> from mazes.maze import Maze
    3> maze = Maze(ThetaGrid(5))
    4> print(maze)
    ϴ grid
```

In the portion of the session above, in lines 1, 2 and 3, we have prepared a theta maze for carving.  In step 4, we tried to display the resulting empty maze in the console window.  The result was a single informational line.

Some algorithms for carving a maze will work on a theta grid, but others will not.  Algorithms that use compass directions like north, south, east and west are designed for oblong grids.  Although these can often be adapted to work on a theta grid, they will not work as written (or "out of the box"), *e.g*:

1. simple binary tree;
2. sidewinder, inwinder, and outwinder; and
3. Eller's algorithm.

Other algorithms are independent of grid organization, requiring only a connected grid, *e.g.*:

1. growing tree algorithms like DFS, BFS, Prim's algorithm;
2. unbiased algorithms like Aldous/Broder and Wilson, and hybrids like Houston's algorithm and the hunt and kill algorithm; and
3. Kruskal's algorithm.

### Grid organization

When we created the grid in line 3 with *ThetaGrid(5)*, we specified a circular maze consisting of five concentric annuli (singular *annulus*; a circular ring) consisting of a number of cells.  The innermost ring consists (by default) of six cells around the *pole*, a point at the center of the circle.  Cells typically have clockwise and counterclockwise neighbors in the annulus, as well as neighbors in the inward (towards the pole) and outward (away from the pole) directions.  The innermost cells don't have inward neighbors and the outermost cells don't have outward neighbors.  A cell has at most one inward neighbor and may have more than one outward neighbor.

The number of outward neighbors is determine by another parameter, the outward *split* (default 1).  If the arc length of the outward boundary of a cell exceeds the split, then the cell will have more than one outward neighbor.

The cells are indexed *(r, t)* where *r* is the inner radius of the annulus containing the cell and *t* is the consecutive counterclockwise cell number, starting with 0 just above the positive $x$-axis (or easterly direction).

### Carving the maze

For our first example, we will use simplified "Prim" to carve the maze:

```
    5> from mazes.Algorithms.simplified_Prim import NotPrim
    6> cell1 = maze.grid[0,0]
    7> print(NotPrim.on(maze, start_cell=cell1))
          Simplified "Prim" (statistics)
                            visits      227
                        start cell  (0, 0)
               maximum list length       48
                             cells      114
                          passages      113
```

### Displaying the maze (linewise)

Here we chose a specific starting cell.  Simplified "Prim" tends to reflect distance from start, but is not as extreme in this regard as breadth-first search.  This tendency is reflected in a linewise maze representation where each cell is represented by a single point near the geometric center, and the passages are represented by line segments which join the points in pairs.

```
    8> from mazes.Graphics.polar2 import SpiderWeb
    9> spider = SpiderWeb(maze)
    10> spider.title('Simplified "Prim"')
    11> spider.setup()
    12> spider.draw_maze()
    13> spider.save_image('gallery/theta/linewise_maze1.png')
    14> spider.show()
```

Lines 8 through 11 set up the polar linewise maze driver.  Line 12 draws the maze.  In line 13, we saved the result as a portable network graphics image (or *png*) file in the gallery.  (Take a look.)  In line 14, we displayed the plot in a graphics window.  (The *matplotlib* graphics window includes several buttons, one of which can be used to save an image to a file.)

### Displaying the maze (areawise/monochrome)

The linewise maze gives us a good sense of some of the biases of the algorithm.  But this isn't how we normally display the maze.  A very basic display comes with the "daddy long legs" driver.

```
    15> from mazes.Graphics.polar1 import Pholcidae
    16> spider = Pholcidae(maze)
    17> spider.title('Simplified "Prim"')
    18> spider.setup()
    19> spider.draw_maze()
    20> spider.save_image('gallery/theta/areawise_maze1_bw.png')
    21> spider.show()
```

Lines 15 through 19 prepare the sketch.  Line 20 saves a copy to the gallery.  Line 21 brings up the graphics window.

### Displaying the maze (areawise/many colors)

The monochrome maze may take a little time to get used to.  The white disk in the center marks the pole.  The cells adjacent to the pole are arranged in an annulus around the pole.

We can assign colors to cells.  (Since walls are displayed in black, it is best to use lighter colors.)  We can assign specific colors to individual cells, or we can let *matplotlib* choose the colors by setting the cell color to the value *None*.

We start by creating a color dictionary.  All cells that we want to color (in this call, all the cells in the maze) need to go in the dictionary.  We start by setting the color to the value *None*:
```
    22> fills = {}
    23> for cell in maze.grid:
    ...     fills[cell] = None
    ...
```

If we use this dictionary, then *matplotlib* will choose all the colors.  The cell we called *cell1* (in line 6 above) has two neighbors in the innermost ring and two outward neighbors.  Using a list of color names, we choose goldenrod for *cell1*, two shades of green for its annular neighbors, and a white and gray for its outward neighbors.

```
    24> fills[cell1] = "goldenrod"
    25> fills[cell1.counterclockwise] = "limegreen"
    26> fills[cell1.clockwise] = "seagreen"
    27> fills[cell1.outward(0)] = "antiquewhite"
    28> fills[cell1.outward(1)] = "gray"
```

We create a new driver and assign the fill colors:
```
    29> spider = Pholcidae(maze)
    30> spider.title('Simplified "Prim"')
    31> spider.setup(fillcolors=fills)
    32> spider.draw_maze()
    33> spider.save_image('gallery/theta/areawise_maze1_color.png')
    34> spider.show()
```

Using an image editor, we created a copy of this last image with the starting cell marked with a black dot:
```
        gallery/theta/areawise_maze1_color_marked.png
```
A copy of the script, with the image saves commented out, is included as file '*gallery/theta/script1*'.

## One cell at the pole

The default number of cells in the innermost ring is six.  Any positive integer (within reason) may be used.  The only difference in principle is between one cell and more than one.  With one cell at the pole, the polar region is a disk whereas with more than one, it is an annulus.

A modified script ('*gallery/theta/script2*') was used to demonstrate this.  We will only document the differences here.  The images are included in the gallery with filenames using '*maze2*' instead of 'maze1*'

The first difference is in line 3:

```
    3b> maze = Maze(ThetaGrid(5, pole=1))
```

The parameter '*pole*' is the number of cells at the pole.  (The default is '*pole=6*'.)  We again used simplified "Prm" to carve the maze.  The response to line 7 shows that the maze has fewer cells than the maze in the previous section -- 78 cells here as opposed to 114 cells above.

```
    7b> print(NotPrim.on(maze, start_cell=cell1))
          Simplified "Prim" (statistics)
                            visits      155
                        start cell  (0, 0)
               maximum list length       43
                             cells       78
                          passages       77
```

The remaining differences are best appreciated by comparing the images in the gallery.  The only script changes were in line 3 and in the filenames used in the *save\_image* lines.

## Changing the split rate

We can reduce the number of cells in the maze by increasing the splitting length.  Conversely, we can increase the number of cells by increasing this length.  The change in the script is again in line 3.  Here we increased the splitting length to 2.

```
    3c> maze = Maze(ThetaGrid(5, split=2))
```

The next visible difference is in the response to maze carving:
```
    7c> print(NotPrim.on(maze, start_cell=cell1))
          Simplified "Prim" (statistics)
                            visits      119
                        start cell  (0, 0)
               maximum list length       30
                             cells       60
                          passages       59
```

The number of cells in five rings has gone from 114 with the default split length of 1 down to 60 cells with the split length of 2.  Note that the starting cell has just 3 neighbors instead of 4 with the default split length.  The second ring now has just six cells instead of twelve.

In line 28, we set the color of the second outward neighbor to gray:
```
    28c> fills[cell1.outward(1)] = "gray"
```

If we query this cell in the current setup, we find that this cell doesn't exist in the new grid:
```
    >>> print(cell1.outward(1))
    None
```

So line 28c is equivalent to:
```
    >>> fills[None] = "gray"
```
Since the value *None* does not represent a cell in the grid, it is ignored by the graphics driver.

As with the change from six cells to one at the pole, the easiest way to understand what is going on is to compare the graphs.  Mathematically, the split length is the arc length when measure in radial units.  If the radius is r *units* in length and the arc subtends an angle of t *radians*, then the arc length a (in *units*) is given by:
```
        a = rt
```
A split length of 2 units tells us that if the outer arc length is greater than 2 units and at most 4 units, the cell must have two outward neighbors.  (If the outer arc length is between 4 and 6, the number of outward neighbors goes up to 3. Et cetera.)