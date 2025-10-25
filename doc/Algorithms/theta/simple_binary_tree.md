# Simple binary trees on a theta (or polar) grid

The east/north binary tree algorithm is fairly east to adapt to work on the theta grid.  Our implementation is slightly more general as we have generalized a cocktail shaker version.

## Correspondences

In each ring we designate a lateral direction of flow (either clockwise or counterclockwise) and a privileged cell.  The lateral flow direction corresponds to the easterly direction and the privileged cell in a ring corresponds to the eastmost cell in a row.

The outward direction in the theta grid corresponds to the northerly direction in an oblong grid.

The only real issue is that we might have a choice of outward neighbors.  To insure that the result is a spanning *binary* tree, we need to insure that the resulting maze has no cells with four or more exits.  If we have a choice of outward neighbors, we always choose the one which is laterally farthest.  If the visited *cell* is in a clockwise ring, the designated outward neighbor will be *cell["outward", 0]*.  If the current cell has *n* outward neighbors and is in a counterclockwise ring, then the designated outward neighbor is *cell["outward", n-1]*.

With that background, we can now describe the algorithm.

## The algorithm

```
    In each cell:
        if the cell is privileged:
            if the cell has a designated outward neighbor:
                carve a passage between the cell and the designated neighbor;
            otherwise:
                do nothing;
        otherwise:
            if the cell has a designated outward neighbor:
               flip a coin;
                 heads:
                   carve the designated outward passage;
                 tails:
                   carve the lateral passage;
            otherwise:
                carve the lateral passage.
```

## Proof of correctness

1.  The privileged cells have no laterally forward neighbor.  Except for the one in the last row, they all have outward neighbors.  We are thus required to carve exactly one exit passage from each privileged cell except the one in the outermost row.  We don't carve an exit passage from the privileged cell in the outermost row.
2.  The remaining cells all have a laterally forward neighbor.  So from each of the non-privileged cells, we carve exactly one passage.
3.  Combining the observations in (1) and (2), the number of cells exceeds the number of passages by one.
4.  In each ring except the outermost, each lateral run ends with an outward exit.  So we can always find a path to the outermost ring.  The outermost ring is itself a single path, so in fact, from every cell there is a path to the privileged cell in the outermost row.
5.  From observation (4), we infer that the maze is connected.
6.  From observations (3) and (5), it follows that the maze is a tree.
7.  Can a cell have more than four linked neighbors?  No.  We have at most one inward neighbor, at most one *linked* outward neighbor, and at most two lateral neighbors.
8.  Can a cell have four linked neighbors?  No.  A privileged cell can have at most one linked lateral neighbor and an unprivileged cell with two laterally linked neighbors cannot have an outwardly linked neighbor.
9.  From (7) and (8) each cell in the tree has at most three neighbors.  That is a sufficient condition for the tree to be binary.

The privileged cell in the outermost ring has at most two neighbors, one inward and one lateral. That cell (or any cell with at most two linked neighbors) can be designated as the root of the binary tree.

## Example 1

The images for this example are:

*  *gallery/theta/simple\_binary\_tree\_1A.png*
*  *gallery/theta/simple\_binary\_tree\_2A.png*

For this example, we create a grid with five rings and six cells at the pole.
```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.polar import ThetaGrid
    2> from mazes.maze import Maze
    3> maze = Maze(ThetaGrid(5))
```

Next we carve the maze:
```
    4> from mazes.Algorithms.polar.simple_binary_tree import BinaryTree
    5> print(BinaryTree.on(maze))
          Simple Binary Tree (Theta Maze) (statistics)
                            visits      115
                             cells      114
                          passages      113
                              bias        0.5000
```

There are three random processes that we can specify.  Here we chose the defaults.  The first process is the coin toss that determines which exit we carve from an unprivileged cell in all but the last row.  The default is a simple fair coin toss.  We can bias the coin by simply changing the probability of a head, for example
```
            BinaryTree.on(maze, bias1=0.3)
```
We could also rewrite the coin toss routine, for example:
```
            def magic(cell, bias, option1=None):
                ...
            BinaryTree.on(maze, flip1=magic, bias1=0.7,
                kwargs1={"option1":666})
```

A separate coin toss determines the lateral direction for each row.  Finally in each row, a random range function determines which cell is privileged.  For more information, see the documentation for method *parse\_args* in the program.

Continuing with the example, we next produce a black and white sketch of the maze:
```
    6> from mazes.Graphics.polar1 import Pholcidae
    7> spider = Pholcidae(maze)
    8> spider.setup()
    9> spider.title("Simple Binary Tree")
    10> spider.draw_maze()
    11> spider.show()
```
The small circle in the center of the maze is intended to emphasize the six cells at the pole are only joined laterally in pairs.  They are not joined in the center.

(The first of the two image files was output using the *spider.save\_image* method between lines 10 and 11.  The graphics display in line 11 also contains a button for saving the displayed image to a file.)

The second image above is a linewise sketch of the maze.  It was produced as follows:
```
    12> from mazes.Graphics.polar2 import SpiderWeb
    13> spider = SpiderWeb(maze)
    14> spider.setup()
    15> spider.title("Simple Binary Tree")
    16> spider.draw_maze()
    17> spider.show()
```

## Example 2

The images for this example are:

*  *gallery/theta/simple\_binary\_tree\_1B.png*
*  *gallery/theta/simple\_binary\_tree\_2B.png*

For this example, we creates a grid with five rings and just one cell at the pole.  The only difference in input, apart from the title strings, was in line 3:
```
    3B> maze = Maze(ThetaGrid(5, pole=1))
```

The grid has fewer cells than the grid in Example 1 .  The response to line 5 is as follows:
```
    5B> print(BinaryTree.on(maze))
          Simple Binary Tree (Theta Maze) (statistics)
                            visits       79
                             cells       78
                          passages       77
                              bias        0.5000
```

The big cell in the center of the first image is the pole cell.

## Example 3

Our implementation is like a cocktail shaker variant of the basic algorithm.  In the basic algorithm flow is always northeastward in the sense that, when there is a choice, one always proceeds east or north.  In a simple cocktail shaker variant, the onward direction can vary: in some rows the onward direction is east, and in others west. This gives an average northerly flow, with the westward rows and the eastward rows tending to cancel each other out.

With our implementation, the changes of lateral flow tend on average to cancel each other out, so, on average, paths tend to move very roughly straight from center outward.  The counterpart of the northeastward bias of the basic algorithm is an outward spiraling bias that can be achieved by forcing the lateral flow to be the same in all rows.

We can achieve this spiraling effect with a keyword option.  For this, we add a couple of names in the import in line 4:
```
    4C> from mazes.Algorithms.polar.simple_binary_tree import BinaryTree
    4C> from mazes.Algorithms.polar.simple_binary_tree import true, false
```
(We could also use *import as* syntax:
```
    4C> import mazes.Algorithms.polar.simple_binary_tree as pbt
```
and refer to the algorithm class and methods as *pbt.BinaryTree*, *pbt.true*, and *pbt.false*.  The name *pbt* is short for "polar binary tree".)

Of course we still need to import the algorithm class.  The second import brings in two coin toss functions.  The function *true* always returns *True*, simulating a coin that always lands face up.  The function *false* always returns *False*, simulating a coin that always lands face down.

For our example, we use the same grid as in Example 1.  The coin that controls lateral flow is represented by the option *flip2*.  Setting *flip2=true* creates a counterclockwise outward spiral bias, while setting *flip2=false* causes the outward spiraling to proceed clockwise.  For our example, we will go with the former.

```
   3C> maze = Maze(ThetaGrid(5))
   4C> from mazes.Algorithms.polar.simple_binary_tree import BinaryTree, true
   5C> print(BinaryTree.on(maze, flip2=true))
          Simple Binary Tree (Theta Maze) (statistics)
                            visits      115
                             cells      114
                          passages      113
                              bias        0.5000
```

The images for this example are:

*  *gallery/theta/simple\_binary\_tree\_1C.png*
*  *gallery/theta/simple\_binary\_tree\_2C.png*
*  *gallery/theta/simple\_binary\_tree\_3C.png*

The third image is a distance-based color map of the maze.

### Variations on Example 3

Here we forced the lateral flow to be counterclockwise.  If we only want a tendency to counterclockwise lateral flow, we could instead just increase the bias in the associated coin toss, for example:

```
   5C1> print(BinaryTree.on(maze, bias2=0.75))
```
Here, the coin that decides the flow for a given ring has a 3 out of 4 chance of returning a head.

For clockwise flow, we want a tail (or *False*).  The clockwise analogues are:
```
   5C2> print(BinaryTree.on(maze, flip2=false))
```
and:
```
   5C2> print(BinaryTree.on(maze, bias2=0.25))
```

And we could write our own coin toss function.  For example, if we want flow to be clockwise in odd rings and counterclockwise in even rings:
```
    def even_parity(ring:int, bias:float, **kwargs):
        """ccw flow when even"""
        return ring % 2 == 0

    BinaryTree.on(maze, flip2=even_parity)
```

Additional optional arguments can be supplied as a dictionary using the *kwargs2* keyword argument to *BinaryTree.on*.

## The privileged cells

The keyword argument *randint* determines which cell in a ring is the privileged cell where lateral flow stops.  The default is a uniformly random choice:
```
    random.randrange(n)
```
where *n* is the number of cells in the ring.  A user-defined *randint* function takes two required parameters, a ring number *ring* and the number of cells *n* in the ring.  It returns an integer from 0 to *n-1*, inclusive.  The *kwargs3* option to *BinaryTree.on* can be used to specify optional arguments.


## Biases of the algorithm

The most obvious bias is in the outermost ring: it forms a single path.  The outermost ring is interrupted by just one wall.

Another bias follows immediately from the proof that the maze is a spanning binary tree is that each cell has at most three incident passages.

Perhaps less obvious, but mentioned in the proof, is that there is an easy path from each cell to the outermost ring.  It consists entirely of lateral and outbound moves.  Here is the default:

```
    def randint(ring:int, n:int, **kwargs) -> int:
       """choose an integer in range(n)"""
       return rng.randrange(n)
```

## An afterthought

The biases mentioned here are probably easier to see in the linewise sketches (which emphasize the edges) than in the more conventional areawise sketches which emphasize the cells and the walls.