# The dihedral groups *D(2)* and *D(4)* and maze orbits

## The underlying theory

*Don't try to take all this in one sitting.  Work on it in a leisurely fashion.  Skip ahead to the computer examples.*

These two groups consist of some rotations and reflection.

*D(4)* is the symmetry group on a square.  It consists of four rotations and four reflections.  If we rotate a square about its center through a counterclockwise angle of 90 degrees, the square remains essentially the same, but the vertex and edge labels move.

Here we label the vertices:
```
               BEFORE                    AFTER
           D            C            C            B
             +--------+                +--------+
             |        |                |        |
             |        |                |        |
             |        |                |        |
             +--------+                +--------+
           A            B            D            A
```

We can express this *action* on the vertices more compactly using matrices:
```
                         A B C D
                         B C D A
```
The top row are the vertices in counterclockwise order.  The bottom row are the new vertices in the same positions.

If we repeat the *action*, we have a 180 degree rotation:
```
                         A B C D
                         C D A B
```
Repeating twice more, we have a 270 degree and a 360 degree rotation:
```
            A B C D                     A B C D
            D A B C                     A B C D
```

But a 360 degree rotation is indistinguishable from no rotation.  We call a rotation of any multiple of 360 degrees an identity rotation.  We can give our four rotations names.  Group theorists use the Greek letters iota and rho:
```
            ι, ρ, ρ², ρ³
```
Iota ι is the identity rotation, rho ρ the 90-degree counterclockwise rotation, rho-squared ρ² the 180-degree rotation, and rho-cubed ρ³ is the 270-degree counterclockwise rotation.  Note that ρ³ is equivant to a 90-degree clockwise rotation.  We can *multiply* these by simply adding exponents or we can reverse direction by using negative exponents.  But any rotation we can obtain by adding or subtracting integer exponents ends up being equivalent to one of these four.

No other rotations are possible.  For example, a 45-degree rotation places the four vertices outside the square,  There are four additional symmetries - these are called reflections (or flips).  We will take our first reflection (called tau: 𝜏) as a horizontal flip:
```
               BEFORE                      AFTER
           D             C            C             D
             +----+----+                +----+----+
             |    |    |                |    |    |
             |    |    |                |    |    |
             |    |    |                |    |    |
             +----+----+                +----+----+
           A             B            B             A

                                𝜏
                             A B C D
                             B A D C
```
Here we draw a vertical line through the center of the square -- this is the axis of the reflection.  The vertices pass horizontally through the axis to the horizontally opposite position.

There are three additional reflections.  We can obtain them by rotating.  In the multiplicative notation, if we first apply transformation S, and then T, we write TS.  (This convention is a technical issue related to function composition.  So rotating the after image is equivalent to multiplying rho times tau (or composing rho and tau in that order) and applying the result.

```
               AFTER ROTATING
               D            A
                 +--------+
                 |        |                   ρ𝜏
                 |        |                A B C D
                 |        |                C B A D
                 +--------+
               C            B
```
Notice that B and D are in their original places, and A and C are now in diagonally opposite positions.

Rotate again to get a vertical reflection:
```
               AFTER ROTATING
               A            B
                 +--------+
                 |        |                  ρ²𝜏
                 |        |                A B C D
                 |        |                D C B A
                 +--------+
               D            C
```

Rotate one more time to get the other diagonal reflection:
```
               AFTER ROTATING
               B            C
                 +--------+
                 |        |                  ρ³𝜏
                 |        |                A B C D
                 |        |                A D C B
                 +--------+
               A            D
```
Here, A and C are fixed, but B and D are fliped.  The reflection is diagonally through AB.

Remember again that multiplication order is opposite the order that transformations are applied.  We can write out a multiplication table:
```
                               S
                  ι   ρ   ρ²  ρ³  |  𝜏   ρ𝜏   ρ²𝜏   ρ³𝜏
              TS  ----------------+-------------------
              ι   ι   ρ   ρ²  ρ³  |  𝜏   ρ𝜏   ρ²𝜏   ρ³𝜏
              ρ   ρ   ρ²  ρ³  ι   |  ρ𝜏  ρ²𝜏  ρ³𝜏   𝜏
              ρ²  ρ²  ρ³  ι   ρ   |  ρ²𝜏 ρ³𝜏  𝜏     ρ𝜏
              ρ³  ρ³  ι   ρ   ρ²  |  ρ³𝜏 𝜏    ρ𝜏    ρ²𝜏
         T    --------------------+-------------------
              𝜏   𝜏   ρ³𝜏  ρ²𝜏 ρ𝜏  |  ι   ρ³   ρ²    ρ
              ρ𝜏  ρ𝜏  𝜏    ρ³𝜏 ρ²𝜏 |  ρ   ι    ρ³    ρ²
              ρ²𝜏 ρ²𝜏 ρ𝜏   𝜏   ρ³𝜏 |  ρ²  ρ    ι     ρ³
              ρ³𝜏 ρ³𝜏 ρ²𝜏  ρ𝜏  𝜏   |  ρ³  ρ²   ρ     ι
```
The multiplication in D(4) has an identity and inverse, and is associative.  This multiplication is, however not commutative.  A reflection is its own inverse.  The rotations form a cycle of length four.

If we delete all rows and columns containing a heading with an odd power of rho, we get the multiplication table for D(2).  This is the group of symmetries for a rectangle which isn't square.  We have two rotations in D(2) (namely 0 and 180 degrees) and two reflections (namely horizontal and vertical).

## The *DihedralGroup* class

This class is used in the fractal tessellation algorithm.  You might want to start reading that documentation.

### Example 1 - actions of the symmetries of a 4×3 rectangle

Let's start with a small rectangular maze with three rows and four columns.  We'll carve it using Wilson's algorithm:
```
$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(3, 4))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits        5
                             cells       12
                          passages       11
                 paths constructed        5
                     cells visited       48
                          circuits       14
                    markers placed       29
                   markers removed       18
                     starting cell  (0, 0)
>>> print(maze)
+---+---+---+---+
|   |           |
+   +   +---+   +
|       |       |
+   +---+---+   +
|       |       |
+---+---+---+---+
```

We can *act* on this maze with any of the four symmetries of the rectangle.  One possibility is to rotate this maze through some multiple of 360 degrees.  The result is the same maze -- both important and trivial.

Let's bring in the *DihedralGroup* class.  We will set the option *debug* to *True* to display the orbit as it is created:
```
>>> from mazes.Algorithms.dihedral import DihedralGroup
>>> group = DihedralGroup(maze, debug=True)
__init__:
+---+---+---+---+
| D |         C |
+   +   +---+   +
|       |       |           "Iota"
+   +---+---+   +
| A     |     B |
+---+---+---+---+
```
I've manually labelled the four corner cells.  I've also named this maze "Iota".  If you read about and understood the theory, you'll know the significance.  If not, no worries as it's just a name.

Now take careful note of the four connected walls in the interior -- they look like this:
```
        +---+
        |
    +---+---+                The f figure
        |
        +
```
I'll refer to it as the f figure because it reminds me of a lower case F.  The two tines at the top point to the right.

At the moment we have just one member of the *orbit* of the *actions* in the group on this maze.  The displayed maze is the result of the *identity* action.  As noted: important, but trivial.  There are three more mazes to obtain.  The method *build\_table* finds them.  I've manually labelled the corresponding corner vertices in each maze.  But also look for what happens to the "f figure" in each of these three mazes.  (I'm naming these three mazes as well.)
```
>>> group.build_table()
create_maze: rotate=2, reflect=False
+---+---+---+---+
| B     |     A |
+   +---+---+   +
|       |       |           "Rho-Square"
+   +---+   +   +
| C         | D |
+---+---+---+---+
create_maze: rotate=0, reflect=True
+---+---+---+---+
| C         | D |
+   +---+   +   +
|       |       |           "Tau"
+   +---+---+   +
| B     |     A |
+---+---+---+---+
create_maze: rotate=2, reflect=True
+---+---+---+---+
| A     |     B |
+   +---+---+   +
|       |       |           "Rho-Square Tau"
+   +   +---+   +
| D |         C |
+---+---+---+---+
4 mazes in orbit
```

Maze Rho-Square was created by rotating the original maze Iota half a revolution or 180 degrees.  The f figure is now upside down with the two tines pointing left.

Maze Tau was created by reflecting the maze horizontally through a central vertical axis.  The f figure is now right-side up, but the two tines point left.

Maze Rho-Square Tau was created by reflecting the maze vertically through a central horizontal axis.  The f figure is now upside down, but the two tines point right.

The *orbit* of the four group *actions* consists of four distinct mazes.  If we had started with a different maze, the orbit might be just one or two mazes.  (It can't be three because four is not a multiple of three.)

### Example 1A - degenerate orbits

Here is a maze with an orbit consisting of just two mazes.
```
+---+---+---+---+
| D           C |
+   +---+   +---+
|   |       |   |           "Iota"
+---+   +---+   +
| A           B |
+---+---+---+---+
```

Rotating halfway:
```
+---+---+---+---+
| B           A |
+   +---+   +---+
|   |       |   |           "Rho"
+---+   +---+   +
| C           D |
+---+---+---+---+
```

Flipping horizontally:
```
+---+---+---+---+
| C           D |
+---+   +---+   +
|   |       |   |           "Tau"
+   +---+   +---+
| B           A |
+---+---+---+---+
```

Flipping vertically:
```
+---+---+---+---+
| A           B |
+---+   +---+   +
|   |       |   |           "Rho-Square Tau"
+   +---+   +---+
| D           C |
+---+---+---+---+
```

Here, rotation does not change the maze, but flipping it does.  (The corner labels do change, but we're really only interested in the location of the passages.)

### Example 1B - degenerate orbits

Here is a maze with an orbit consisting of just one mazes.
```
+---+---+---+---+
| D |   |   | C |
+   +   +   +   +
|               |           "Iota"
+   +   +   +   +
| A |   |   | B |
+---+---+---+---+
```

Rotating or reflecting moves the labels.  Passages remain in the same locations in all four mazes, so the orbit consists of a single maze.

### Example 2 -  actions of the symmetries of a 4×4 square

If our maze is square, we have 90-degree rotations and diagonal reflections.  There are eight symmetries -- four rotations and four reflections.  We need a maze to start the process.  The length of the orbit must be a divisor of 8, so the possible orbits are 1, 2, 4 or 8 mazes.
```
>>> maze = Maze(OblongGrid(4, 4))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits        6
                             cells       16
                          passages       15
                 paths constructed        6
                     cells visited       53
                          circuits       12
                    markers placed       35
                   markers removed       20
                     starting cell  (3, 0)
>>> print(maze)
+---+---+---+---+
|       |       |
+   +---+---+   +
|               |
+---+   +---+---+
|               |
+---+   +---+   +
|       |       |
+---+---+---+---+
```

We set up the dihedral group and the trivial action.  We again set the option *debug* to *True* to display the orbit as it is created:
```
>>> group = DihedralGroup(maze, debug=True)
__init__:
+---+---+---+---+
|       |       |
+   +---+---+   +
|               |
+---+   +---+---+
|               |
+---+   +---+   +
|       |       |
+---+---+---+---+
```

Now we complete the orbit.  It isn't hard to check that the original maze doesn't show up in the rest of the orbit.  It follows that the orbit consists of 8 distinct mazes:
```
>>> group.build_table()
create_maze: rotate=1, reflect=False
+---+---+---+---+
|       |       |
+   +   +   +   +
|   |   |   |   |
+---+   +   +---+
|   |           |
+   +   +   +   +
|       |   |   |
+---+---+---+---+
create_maze: rotate=2, reflect=False
+---+---+---+---+
|       |       |
+   +---+   +---+
|               |
+---+---+   +---+
|               |
+   +---+---+   +
|       |       |
+---+---+---+---+
create_maze: rotate=3, reflect=False
+---+---+---+---+
|   |   |       |
+   +   +   +   +
|           |   |
+---+   +   +---+
|   |   |   |   |
+   +   +   +   +
|       |       |
+---+---+---+---+
create_maze: rotate=0, reflect=True
+---+---+---+---+
|       |       |
+   +---+---+   +
|               |
+---+---+   +---+
|               |
+   +---+   +---+
|       |       |
+---+---+---+---+
create_maze: rotate=1, reflect=True
+---+---+---+---+
|       |       |
+   +   +   +   +
|   |   |   |   |
+---+   +   +---+
|           |   |
+   +   +   +   +
|   |   |       |
+---+---+---+---+
create_maze: rotate=2, reflect=True
+---+---+---+---+
|       |       |
+---+   +---+   +
|               |
+---+   +---+---+
|               |
+   +---+---+   +
|       |       |
+---+---+---+---+
create_maze: rotate=3, reflect=True
+---+---+---+---+
|       |   |   |
+   +   +   +   +
|   |           |
+---+   +   +---+
|   |   |   |   |
+   +   +   +   +
|       |       |
+---+---+---+---+
8 mazes in orbit
```

## *Caveat emptor*

These are technical points:

+ Note that the message does not say "8 distinct mazes" -- the *debug* option only reports how many mazes were produced.
+ Note that when we say the mazes are *distinct*. we are looking at structure relative to the cell in the lower left.  All 8 mazes in the orbit are isomorphic as graphs.  But we looking at structure relative to the cell indices.  So our notion of distinctness is more general than graph isomorphism.