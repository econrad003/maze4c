# Masked Grids

## Contents

1. A simple example (*demos.masked\_maze*)
2. Creating a text mask (*demos.masked\_maze\_2*)
3. Creating mazes (*demos.masked\_maze\_2*)

## 1. A simple example

### 1A. The demonstration module

Module *demos.masked\_maze* creates a simple maze using a mask.  We will look at the key parts of the code in section 1D.  There are no user-options for this demonstration, but it does use Wilson's algorithm, so the final maze will change from run to run.
```
$ python -m demos.masked_maze
Opening demos/mask1.png... 135×85
threshold mask: 9 rows, 14 columns
The hidden cells are labelled 'X'.  The carving algorithm avoids
the hidden cells.  (CAUTION: Wilson's algorithm will fail if the
revealed cells do not form a connected set.)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       26
                             cells       84
                          passages       83
                 paths constructed       26
                     cells visited      611
                          circuits      214
                    markers placed      371
                   markers removed      288
                     starting cell  (0, 0)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           | X | X | X |       |           | X | X | X |
+   +---+---+---+---+---+   +---+---+---+   +---+---+---+
|   |   |   | X | X | X |   | X | X | X |   | X | X | X |
+   +   +   +---+---+---+   +---+---+---+   +---+---+---+
|                           | X | X | X |   | X | X | X |
+---+   +---+---+---+---+   +---+---+---+   +---+---+---+
|   |   |   | X | X |                               | X |
+   +---+   +---+---+---+   +---+---+---+---+---+   +---+
|   |       | X | X | X |   | X | X | X | X | X |   | X |
+   +---+   +---+---+---+---+---+---+---+---+---+   +---+
|           | X | X | X | X | X | X | X | X | X |       |
+   +---+   +---+---+---+---+---+---+---+---+---+   +   +
|   |   |           |   |               |       |   |   |
+   +   +---+---+   +   +   +---+   +---+   +   +---+   +
|   |   |   |       |   |   |   |   |   |   |   |       |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +
|           |               |               |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

In the display, cells marked with an 'X' have been hidden from the carving algorithm (Wilson).  Selected pixels from a 135×85 pixel image were used to determine which cells were to be hidden.  (The image is saved in a PNG image file, *demos/mask1.png*.)

Of the 11,475 pixels, just 126 were selected to create a 9×14 threshold array.  The threshold array was used to identify 42 cells to be hidden from Wilson's algorithm.  The remaining 84 cells form a *connected* subgrid which was passed through Wilson's algorithm to create a perfect maze.  Note that our implementation of Wilson's algorithm carved 83 passages, the precise number required for a perfect maze on an 84-cell grid.

### 1B. The threshold mask

The threshold mask is a two-dimensional array of zeros and ones.  In this case, it is a 9×14 array -- the zeros correspond to the hidden cells in the grid.
```python
# COLUMNS
# 0  1  2  3  4  5  6  7  8  9 10 11 12 13     ROWS
[[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],   # 8
 [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],   # 7
 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],   # 6
 [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],   # 5
 [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],   # 4
 [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],   # 3
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],   # 2
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],   # 1
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]   # 0
```

### 1C. The text mask

The mask can be saved in a text file using an 'X' character to denote a hidden cell.  The remaining cells are denoted using spaces, and newlines delimit rows.
```
          1
0....5....0...            NOTES
   XXX     XXX|   (The vertical bars represent newlines.)
   XXX XXX XXX|
       XXX XXX|
   XX        X|
   XXX XXXXX X|
   XXXXXXXXX  |
              |
              |
              |
**EOF**
0....5....0...
```

### 1D. Python code

Now let's look at relevant parts of the Python code for the demonstration:

```python
from mazes.tools.image_to_mask import image_open, image_threshold_mask

if __name__ == "__main__":
        # open the image file
    img = image_open("demos/mask1.png", debug=True)

        # create a 0/1 threshold mask
    start = (3, 3)
    step = (10, 10)
    minvalues = (50, 0, 0)
    mask = image_threshold_mask(img, start, step, minvalues, debug=True)

        # create the grid and maze objects
    rows = len(mask)
    cols = len(mask[0])
    grid = OblongGrid(rows, cols)
    maze = Maze(grid)
    for i in range(rows):
        for j in range(cols):
            if mask[rows-i-1][j] == 0:
                grid[i,j].label = "X"           # label the masked cells
                grid[i,j].hide()                # hide the masked cells
```

The code starts with an import of two methods: *image\_open* and *image\_threshold\_mask*.

The next segment creates the threshold mask:
```python
    start = (3, 3)                   # 1
    step = (10, 10)                  # 2
    minvalues = (50, 0, 0)           # 3
    mask = image_threshold_mask(img, start, step, minvalues, debug=True)
```
Line 1 sets the position in the image which is to be used as the start of the mask.  Image coordinates are *(x, y)* where *x* runs horizontally from left to right and *y* runs vertically from top to bottom.  The top left pixel is located at *(x=0, y=0)*.

Line 2 sets the step increment *(h, k)*.  Since the iteration starts at *(3, 3)* near the top left, the neighbors to east, south, and southeast in the mask are at *(13, 3)*, *(3, 13)* and *(13, 13)*.  The iteration stop is determined by the width and height (in pxels) of the image.

Line 3 determines which pixels represent hidden cells.  The three values represent minimum RGB values.  For this selector, a pixel with values *(R, G, B)* is *not* masked if:
```
    R ≥ 50 and G ≥ 0 and B ≥ 0.
```
Since color ranges are from 0 through 255, the green and blue selectors are effectively ignored.

There are some variations on the selectors.  If a value is negative, it is used to indicate a maximum.  For example, if *minvalues* were set to *(50, -50, 0)*, then the selection criteria are now:
```
    R ≥ 50 and G ≤ 50 and B ≥ 0.
```
(The absolute value is used.)

In addition, a disjunctive (*or*) condition can replace the conjunctive (*and*) condition if the mask is created by setting the *AND* option to *False*:
```
    mask = image_threshold_mask(img, start, step, minvalues,
                                AND=False, debug=True)
```

With *minvalues* set as *(50, 0, 0)* and *AND* set to *False*, the threshold condition becomes:
```
    R ≥ 50 or G ≥ 0 or B ≥ 0.
```
Since the second condition always holds, this threshold condition would always hold -- that would leave all cells unmasked.  To ignore the green and blue colors with a disjunctive selector, set the color to 256 (or more):
```
    minvalues = (50, 256, 256)           # 3 disjunctive
    R ≥ 50 or G ≥ 256 or B ≥ 256.
```

The following lines determine the dimensions of the mask:
```
    rows = len(mask)                    # 5
    cols = len(mask[0])                 # 6
```

These are followed by creation of the grid and maze object:
```
    grid = OblongGrid(rows, cols)
    maze = Maze(grid)
```

The remaining lines set up the hidden cells in the grid:
```
    for i in range(rows):
        for j in range(cols):
            if mask[rows-i-1][j] == 0:  # 7
                grid[i,j].label = "X"   # 8     # label the masked cells
                grid[i,j].hide()        # 9     # hide the masked cells
```
Note that the row index in the mask is *rows-i-1* (line #7).  This takes into account that the mask is indexed from north to south, but our maze indices run from south to north.

Line 8 is responsible for labelling the masked cell.  Line 9 is the critical line as it hides the masked cells.

## 2. Creating a text mask

First let's look at the usage information for the second masked maze demonstration module:
```
$ python -m demos.masked_maze_2 -h
usage: masked_maze_2.py [-h] [-s X0 Y0] [-t H K] [-r RED] [-g GREEN] [-b BLUE]
                        [--OR] [-8] [-A ALGORITHM] [-o GRAPHICS]
                        input [output]

a fancier masked maze demo

positional arguments:
  input                 image or text file input (required). If the file is a
                        text file, the first row will determine the number of
                        columns and the file should consist of one or more
                        rows of spaces and 'X' characters. If the file is an
                        image file, the mask will be produced using the start,
                        stop, and minvalues specifications. Text files must
                        have one of the following extensions: '.txt', '.mask'
                        or '.msk'.
  output                an optional text file (optional). If provided, this
                        will be a text mask.

options:
  -h, --help            show this help message and exit
  -s X0 Y0, --start X0 Y0
                        start coordinates (default: 3, 3). Ignored if a text
                        mask is provided as input.
  -t H K, --step H K    step offsets (default: 5, 5). Ignored if a text mask
                        is provided as input.
  -r RED, --red RED     minimum red value for revealed cells (default: 50). To
                        change the direction of the comparison, use a negative
                        integer.
  -g GREEN, --green GREEN
                        minimum green value for revealed cells (default: 0).
                        To change the direction of the comparison, use a
                        negative integer.
  -b BLUE, --blue BLUE  minimum blue value for revealed cells (default: 0). To
                        change the direction of the comparison, use a negative
                        integer.
  --OR                  The default is to accept a pixel if all three
                        conditions are met. Set this option to accept if at
                        least one condition is satisfied. If this option is
                        set and a value for -r, -g, -b is 0, that value will
                        be changed to 256 to force that comparison to fail.

Maze Arguments:
  These arguments are used to create a maze from theimage or the mask that
  was supplied as input. They are ignored if an output mask is specified.

  -M, --Moore           if set, a Moore grid (8 compass neighbors) will be
                        used. If it is not set (default), the usual Von
                        Neumann neighborhood (4 compass neighbors) will be
                        used.
  -A ALGORITHM, --Algorithm ALGORITHM
                        carving algorithm. Permissible entries are 'w'
                        (Wilson's algorithm), 'd' (DFS), 'b' (BFS), and 'k'
                        (Kruskal's algorithm). Wilson's algorithm cannot be
                        used if the revealed part of the grid is not
                        connected.
  -o GRAPHICS, --graphics GRAPHICS
                        optional filename for graphics output, e.g. 'foo.png'
```
Plot-related options aren't displayed above.

To create a text mask from an image, we supply an image file, an output file (extension ".txt" or ".msk" or ".mask"), and, optionally, some selection criteria.

### 2A. Defaults

The selection criteria all have defaults.  Refer to sections 1A and 1D for details:
```python
    start = (3, 3)
    step = (5, 5)
    minvalues = (50, 0, 0)          # R ≥ 50 and G ≥ 0 and B ≥ 0
```
So the default selection is all selected pixels determine a hidden cell if the red value (*R*) is less than 50.  The green and blue values are effectively ignored.

Let's run the demo using the defaults:
```
$ python -m demos.masked_maze_2 demos/mask1.png demos/mask1.txt
['demos/mask1.png', 'demos/mask1.txt']
Namespace(start=(3, 3), step=(5, 5), red=50, green=0, blue=0, OR=False, input='demos/mask1.png', output='demos/mask1.txt', Moore=False, Algorithm='w', graphics=None)
threshold mask: ALL(50, 0, 0)
	R ≥ 50 AND G ≥ 0 AND R ≥ 0
from_text_mask=False, to_text_mask=True
Opening demos/mask1.png... 135×85
threshold mask: 17 rows, 27 columns
mask: 17 rows, 27 columns
wrote mask: demos/mask1.txt (17 rows, 27 columns)
```
The demonstration is fairly verbose, giving quite a few hints as to the results and how they were obtained.  And here is the actual result:
```
*** demos/mask1.txt ***
      XXXXX          XXXXXX
      XXXXX        X XXXXXX
      XXXXX   XXXXXX XXXXXX
              XXXXXX XXXXXX
              XXXXXX XXXXXX
                         XX
      XXXX               XX
      XXXX               XX
      XXXXX   XXXXXXXXX   X
      XXXXXXXXXXXXXXXXX   X
      XXXXXXXXXXXXXXXXX    
                           
                           
                           
                           
                           
                           
*** EOF ***
```

### 2B. Specifying other criteria

Here we specify all the selection options, including the '--OR' option:
```
$ python -m demos.masked_maze_2 demos/mask1.png demos/mask1B.txt \
         -s 0 0 -t 3 5 -r 256 -g -50 -b 256 --OR
['demos/mask1.png', 'demos/mask1B.txt', '-s', '0', '0', '-t', '3', '5', '-r', '256', '-g', '-50', '-b', '256', '--OR']
Namespace(start=[0, 0], step=[3, 5], red=256, green=-50, blue=256, OR=True, input='demos/mask1.png', output='demos/mask1B.txt', Moore=False, Algorithm='w', graphics=None)
threshold mask: ANY(256, -50, 256)
	R ≥ 256 OR G ≤ 50 OR R ≥ 256
from_text_mask=False, to_text_mask=True
Opening demos/mask1.png... 135×85
threshold mask: 17 rows, 45 columns
mask: 17 rows, 45 columns
wrote mask: demos/mask1B.txt (17 rows, 45 columns)
```

Here is the result:
```
*** demos/mask1B.txt ***
XXXXXXXXXXX        XXXXXXXXXXXXXXXXX         
XXXXXXXXXXX       XXXXXXXXXXXXXXXXXX         
XXXXXXXXXXX       XXXXXX         XXX         
XXXXXXXXXXX       XXXXXX         XXX         
XXXXXXXXXXXXXXXXXXXXXXXX         XXX         
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  
XXXXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXX  
XXXXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXX  
XXXXXXXXXXX                            XXXX  
XXXXXXXXXXX                           XXXXX  
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
*** EOF ***
```
Note that this mask would not work with Wilson's algorithm as the spaces form a disconnected set (with four components - there are trailing spaces in the upper right).

### 2C. Using other images

Other RGB images could be used.  As an example, we used a 512×512 TIFF image called *lena\\_color.tif* to produce a mask.  This image, known variously as "Lena" or "Lenna" was used extensively in image processing research in the 1970s and 1980s.  The story behind the image is found in the following Wikipedia article:

[1] "Lenna" in Wikipedia. 5 Oct. 2025. Web. Accessed 24 Oct. 2025.

(The image is proprietary, so it is not in this repository.  The image cannot be reconstructed from the resulting mask.)

Here is the run:
```
$ python -m demos.masked_maze_2 lena_color_512.tif demos/lena.txt \
         -t 10 25 -r 100
['../lena_color_512.tif', 'demos/lena.txt', '-t', '10', '25', '-r', '100']
Namespace(start=(3, 3), step=[10, 25], red=100, green=0, blue=0, OR=False, input='lena_color_512.tif', output='demos/lena.txt', Moore=False, Algorithm='w', graphics=None)
threshold mask: ALL(100, 0, 0)
	R ≥ 100 AND G ≥ 0 AND R ≥ 0
from_text_mask=False, to_text_mask=True
Opening /lena_color_512.tif... 512×512
threshold mask: 21 rows, 51 columns
mask: 21 rows, 51 columns
wrote mask: demos/lena.txt (21 rows, 51 columns)
```
The image has a lot of red, so the red threshold was increased to 100.  There are two bluish low-red regions -- a large feathery hat decoration in the lower left and a diagonal feature on the wall to the right of the model.  These show up in the mask:
```
*** demos/lena.txt ***
                                                   
                                                 XX
                                              XX XX
                                            XX XXXX
                                     X     X XXX   
                                          X XXX    
                                          XX       
                            X            XXX       
                     XX   X           XX XX        
                    XX X           X X  XX         
                X   XX                  X          
         X   XX  XXXX              XX X            
           X  XX  X  X              X              
          X    X   X X            X   X            
          XX                     X                 
XX       X  X   XX XX          XX X                
        X  X      XXXX            X             X  
X      XXX  XX   XX  X              X              
X      XXXXXXX  X   X                              
       X XX XXX  XXX                     X         
X      X  XX XX  X                                 
*** EOF ***
```
The mask isn't suitable for Wilson's algorithm on the usual 4-connected (Von Neumann) rectangular grid because of a diagonal run of spaces in the upper right.  There are also some disconnections in the bottom of the grid which make it unsuitable for use with Wilson on an 8-connected (Moore) grid.

## 3. Creating mazes

The demo module *demos.masked\_maze\_2* can be used to create 4-connected and 8-connected rectangular masked mazes using RGB images or text masks.  If an image is used, the selection criteria build a text mask which is not saved as a file.  Otherwise, the two processes are the same.  We will accordingly just use mask files.  The mazes are displayed as graphics and can optionally be saved as images. The masked cells are displayed in red.

First, we noted that Wilson's algorithm won't work on the output from the Lenna image.

```
$ python -m demos.masked_maze_2 demos/lena.txt
['demos/lena.txt']
Namespace(input='demos/lena.txt', output=None, Moore=False, Algorithm='w', graphics=None)
from_text_mask=True, to_text_mask=False
Maze(OblongGrid(21, 51, '*')
1071 cells: 126 hidden, 945 revealed
The revealed cells do not form a connected set.  (Not good!)
Traceback (edited):
  File "maze4c/demos/masked_maze_2.py", line 248, in <module>
ValueError: Wilson's algorithm not valid for disconnected grid.
```

Switching to a Moore grid doesn't improve the situation:
```
$ python -m demos.masked_maze_2 demos/lena.txt -M
['demos/lena.txt', '-M']
Namespace(input='demos/lena.txt', output=None, Moore=True, Algorithm='w', graphics=None)
from_text_mask=True, to_text_mask=False
Maze(MooreGrid(21, 51, '*')
1071 cells: 126 hidden, 945 revealed
The revealed cells do not form a connected set.  (Not good!)
Traceback (edited):
  File "maze4c/demos/masked_maze_2.py", line 248, in <module>
ValueError: Wilson's algorithm not valid for disconnected grid.
```

### Example 3A. Kruskal's algorithm

Even though the unmasked region is disconnected, we can use Kruskal's algorithm:
```
$ python -m demos.masked_maze_2 demos/lena.txt -A k -o gallery/mask3A.png
Namespace(start=(3, 3), step=(5, 5), red=50, green=0, blue=0, OR=False, input='demos/lena.txt', output=None, Moore=False, Algorithm='k', graphics='gallery/mask3A.png')
from_text_mask=True, to_text_mask=False
Maze(OblongGrid(21, 51, '*')
1071 cells: 126 hidden, 945 revealed
The revealed cells do not form a connected set.  (Not good!)
          Kruskal (statistics)
                            visits     1679
                 components (init)      945
               queue length (init)     1679
                             cells     1071
                          passages      936
                components (final)        9  <---- NOTE!
              queue length (final)        0
Rendering graphics...
Saving to gallery/mask3A.png
```
The result, a maze with 9 components, has been saved to the gallery.

### Example 3B. Kruskal's algorithm with Moore neighborhoods

The *--figure* option resizes the figure.  There are three parameters, namely the width in inches, the height in inches, and the dots per inch.  If both width and height are more than 1 (inch), then these will be used to resize the image.  If the dots per inch is more than 70, the resolution will be increased.  Here we resize the image but don't change the resolution. This brings out the diagonal passages in the graphic. Here is the relevant code in the module:

```python
    if args.figure:
        width, height, dpi = args.figure
        dpi = int(dpi)
        if width > 1 and height > 1:
            spider.fig.set_size_inches(width, height)
        if dpi > 70:
            spider.fig.set_dpi(dpi)
```

```
$ python -m demos.masked_maze_2 demos/lena.txt
         -M -A k -o gallery/mask3B.png --figure 20 10 0
Namespace(input='demos/lena.txt', output=None, Moore=True, Algorithm='k', graphics='gallery/mask3B.png', figure=[20.0, 10.0, 0.0], title=None)
from_text_mask=True, to_text_mask=False
Maze(MooreGrid(21, 51, '*')
1071 cells: 126 hidden, 945 revealed
The revealed cells do not form a connected set.  (Not good!)
          Kruskal (statistics)
                            visits     3298
                 components (init)      945
               queue length (init)     3298
                             cells     1071
                          passages      942
                components (final)        3
              queue length (final)        0
Rendering graphics...
Saving to gallery/mask3B.png
```

## Example 3C. Kruskal again, after some changes

Adding 1 blank line to the end of the Lenna mask yields a connected Moore grid.  But we still need to move or remove some of the 'X' characters to connect the Von Neumann grid.  (And we we did!)  Our 'fixes' are in *demos.lena1.txt* which we will use in the rest of the examples.  We will use the '--figure' option to make the remaining images a bit easier to read.

```
$ python -m demos.masked_maze_2 demos/lena1.txt \
          -A k --figure 11 6 0 -o gallery/mask3C.png
Namespace(input='demos/lena1.txt', output=None, Moore=False, Algorithm='k', graphics='gallery/mask3C.png', figure=[11.0, 6.0, 0.0], title=None)
from_text_mask=True, to_text_mask=False
Maze(OblongGrid(22, 51, '*')
1122 cells: 123 hidden, 999 revealed
The revealed cells form a connected set.  (Good!)
          Kruskal (statistics)
                            visits     1714
                 components (init)      999
               queue length (init)     1781
                             cells     1122
                          passages      998
                components (final)        1     <----- NOTE!
              queue length (final)       67
Rendering graphics...
Saving to gallery/mask3C.png
```

## Example 3D. Wilson's algorithm

Since the mask *lena1* is connected, we can use it with Wilson's algorithm:
```
$ python -m demos.masked_maze_2 demos/lena1.txt \
         --figure 11 6 0 -o gallery/mask3D.png
Namespace(input='demos/lena1.txt', output=None, Moore=False, Algorithm='w', graphics='gallery/mask3D.png', figure=[11.0, 6.0, 0.0], title=None)
from_text_mask=True, to_text_mask=False
Maze(OblongGrid(22, 51, '*')
1122 cells: 123 hidden, 999 revealed
The revealed cells form a connected set.  (Good!)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits      415
                             cells      999
                          passages      998
                 paths constructed      415
                     cells visited     5491
                          circuits     1558
                    markers placed     3518
                   markers removed     2520
                     starting cell  (2, 50)
Rendering graphics...
Saving to gallery/mask3D.png
```

## Example 3E. Breadth-first search

The hidden cells make disrupt breadth-first search, but just a little...
```
$ python -m demos.masked_maze_2 demos/lena1.txt
         --figure 11 6 0 -o gallery/mask3E.png -A b
Namespace(input='demos/lena1.txt', output=None, Moore=False, Algorithm='b', graphics='gallery/mask3E.png', figure=[11.0, 6.0, 0.0], title=None)
from_text_mask=True, to_text_mask=False
Maze(OblongGrid(22, 51, '*')
1122 cells: 123 hidden, 999 revealed
The revealed cells form a connected set.  (Good!)
          Breadth-first Search (BFS) (statistics)
                            visits      999
                        start cell  (14, 22)
              maximum queue length       45
                             cells      999
                          passages      998
Rendering graphics...
Saving to gallery/mask3E.png
```

## Example 3F. Breadth-first search on a Moore grid

The disruption is barely noticeable on the Moore grid:
```
 python -m demos.masked_maze_2 demos/lena1.txt \
        --figure 11 6 0 -o gallery/mask3F.png -A b -M
Namespace(input='demos/lena1.txt', output=None, Moore=True, Algorithm='b', graphics='gallery/mask3F.png', figure=[11.0, 6.0, 0.0], title=None)
from_text_mask=True, to_text_mask=False
Maze(MooreGrid(22, 51, '*')
1122 cells: 123 hidden, 999 revealed
The revealed cells form a connected set.  (Good!)
          Breadth-first Search (BFS) (statistics)
                            visits      999
                        start cell  (5, 10)
              maximum queue length       50
                             cells      999
                          passages      998
Rendering graphics...
Saving to gallery/mask3F.png
```

## Example 3G. Depth-first search

Finally we have depth-first search, perhaps better known as recursive backtracker:
```
$ python -m demos.masked_maze_2 demos/lena1.txt
         --figure 11 6 0 -o gallery/mask3G.png -A d
Namespace(input='demos/lena1.txt', output=None, Moore=False, Algorithm='d', graphics='gallery/mask3G.png', figure=[11.0, 6.0, 0.0], title=None)
from_text_mask=True, to_text_mask=False
Maze(OblongGrid(22, 51, '*')
1122 cells: 123 hidden, 999 revealed
The revealed cells form a connected set.  (Good!)
          Depth-first Search (DFS) (statistics)
                            visits     1997
                        start cell  (15, 26)
               maximum stack depth      423
                             cells      999
                          passages      998
Rendering graphics...
Saving to gallery/mask3G.png
```

The images are found in the gallery (as noted in the displayed results).
