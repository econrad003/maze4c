# A combinatorial tiling problem

As stated, it doesn't have much to do with mazes, but it does deal with plane tilings, so it we could consider it as related to grids.  I'll assume you are familiar with a game called Tetris.  If not, look it up, but I will warn you that it can be addictive.

Most of the present article deals with my attempts to partially solve the problem.  Section 1 talks about the Tetris tiles.  Section 2 states two problems as posed in a *Scientific American* puzzle page, and adds a couple of related problems.  Section 3, the bulk of the present article covers my partial solutions to the three solvable problems.  Section 4 involves how a tiilng might produce a nice maze-building algorithm.

## 1.0 Tiles

Now Tetris involves seven kinds of pieces (or tiles), each built from 4 unit squares.  The tiles are as follows:

```
     (I)         (O)           (L1)          (L2)

    +---+     +---+---+     +---+---+     +---+---+
    |   |     |       |     |       |     |       |
    +   +     +   +   +     +   +---+     +---+   +
    |   |     |       |     |   |             |   |
    +   +     +---+---+     +   +             +   +
    |   |                   |   |             |   |
    +   +                   +---+             +---+
    |   |
    +---+

         (T)                 (Z1)             (Z2)

    +---+---+---+       +---+---+             +---+---+
    |           |       |       |             |       |
    +---+   +---+       +---+   +---+     +---+   +---+
        |   |               |       |     |       |
        +---+               +---+---+     +---+---+
```

The rules for Tetris allow tiles to be rotated through a multiple of a right angle, but reflections are not permitted.  So L1 and L2 count as distinct pieces, as do Z1 and Z2.  But, for example, we can rotate I:

```
         +---+          +---+---+---+---+
         |   |          |               |
         +   +          +---+---+---+---+
         |   |
         +   +
         |   |
         +   +
         |   |
         +---+
```
Rotating I through a right angle in either direction gives a second configuration -- same tile in a different configuration.  The rotation group for A has two distinct configurations since a 180 degree rotation does not change the configuration.

If we look at the rotation groups for each piece, we find the following orbits:

<table align="center" border=1>
<thead>
<tr>
<td></td>
<td>tile</td>
<td>rotations</td>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td align="center">I</td>
<td align="right">2</td>
</tr>
<tr>
<td></td>
<td align="center">O</td>
<td align="right">1</td>
</tr>
<tr>
<td></td>
<td align="center">L1</td>
<td align="right">4</td>
</tr>
<tr>
<td></td>
<td align="center">L2</td>
<td align="right">4</td>
</tr>
<tr>
<td></td>
<td align="center">T</td>
<td align="right">4</td>
</tr>
<tr>
<td></td>
<td align="center">Z1</td>
<td align="right">2</td>
</tr>
<tr>
<td></td>
<td align="center">Z2</td>
<td align="right">4</td>
</tr>
</tbody>
<tfoot>
<tr>
<td>counts</td>
<td>7 tiles</td>
<td>19 placements</td>
</tfoot>
</table>

## 2. The puzzles

There are many problems we can state which involve using at most one tile of each kind.  We will focus on the following four problems.  The first two appear on page 14 of the September 2026 issue of *Scientific American* in the math puzzle column under the title "Tetris paradox":

1. Using each tile exactly once, form a rectangle.
2. Using all but one tile exactly once, form a rectangle.

According to the article, the first problem has no solution, but the second does.

Some related problems are:

1. What rectangles can be formed using at most one of each kind of tile?
2. How many distinct rectangular tilings (up to rotation *and* reflection) can be formed using at most one of each kind of tile?

## 3. Partial solutions

### 3.0 An important observation

Each tile consists of 4 cells, so a tiling consisting of *n* tiles has *4n* cells.  So, if a tiled rectangle has width $a$ and length *b*, both in cells, then *ab=4n*.    We can assume that the width does not exceed the length.

### 3.1 The trivial case (a single tile)

With one tile, we have four cells and two possible rectangles:
```
        1x4   tile I
        2x2   tile O
```

In general, any 1x4n solution requires n I tiles, so 1x4n has a solution if and only if n=1.  We can ignore the factorization 1x4n when n>1.

With 1 tile, there are **2 solutions**.

### 3.2 Two distinct tiles

With two tiles, the only possibility is 2x4.  The only candidate solutions involves two copies of either L1 or L2:
```
                   INADMISSIBLE                INADMISSIBLE
        2x4     +---+---+---+---+           +---+---+---+---+
                | L2        |   |           |   |        L1 |
                +   +---+---+   +           +   +---+---+   +
                |   |        L2 |           | L1        |   |
                +---+-----------+           +---+---+---+---+
```
The conclusion is that it is not possible to construct a 2x4 rwctangle with 2 *distinct* tiles.

Notice that these two tilings are distinct up to rotation, but they are indistinct once we allow reflections.

Since neither of the tilings is admissible, with 2 distinct tiles, **there are no solutions**.

### 3.3 Three distinct tiles

There are 12 cells.  The possible factorizations are 2x6 and 3x4.  2x6 requires 2 copies of the same kind of L tile:
```
                       INADMISSIBLE
        2x6     +---+---+---+---+---+---+
                |               |       |
                +   2 L cells   +   O   +
                |   (same type) |       |
                +---------------+---+---+
```

But 3x4 is possible:
```
       3x4      +---+---+---+---+           +---+---+---+---+
                |    Z2 |    L2 |           | L2        |   |
                +---+   +---+   +           +   +---+---+   +
                |   |       |   |           |   |       |   |
                +   +---+---+   +           +---+   +---+   +
                | L1        |   |           | Z1    |    L1 |
                +---+---+---+---+           +---+---+---+---+
```
These are reflections of one another through the horizontal center, but the two configurations involve different Z-tiles.

With 3 distinct tiles, **there is 1 solution** up to rotation and reflection.

### 3.4 Four distinct tiles

The solutions seem to involve placing the I tile along one of the longer sides of a 3x4 rectangle.  The placement of the I tile breaks some of the symmetry, so this gives two solutions up to rotation and reflection.

I don't think there are other ways of tiling a 3x4 rectangle with distinct Tetris tiles.  But I don't have a proof.

With 3 distinct tiles, **there are at least 2 solutions** distinct up to rotation and reflection.  (I think there are exactly two, but I may be wrong.)

### 3.5 Five distinct tiles

I haven't found a solution, but that's not a proof.  I'm inclined to believe there is none, but I'm happy to be proven wrong.

### 3.6 Six distinct tiles

There is at least one way of assembling a 4x6 square from six tiles:
```
        4x6     +---+---+---+---+---+---+
                |   |       I       |   |
                +   +---+---+---+---+   +
                |  Z2   |       |   Z1  |
                +---+   +   O   +   +---+
                |   |   |       |   |   |
                +   +---+---+---+---+   +
                |  L1       |       L2  |
                +---+---+---+---+---+---+
```
Note that the T tile is not used.  The *Scientific American* article seems to say that there is an obvious reason why this tile is problematic.  Well, either that, or they have a solution which instead omits either the I or the O tile...  (The hint involves symmetry.)

### 3.7 Rectangles

There may be some errors in this table as much of this was developed by trial and error.  *Caveat emptor!*

| cells | rectangle | distinct tiles       | repeated tiles             |
| ----: | :-------: | :------------------- | :------------------------- |
|     4 |    1x4    | I                    |                            |
|       |    2x2    | O                    |                            |
|     8 |    1x8    | no solutions         | 2 I tiles                  |
|       |    2x4    | no solutions         | 2 O tiles or 2 I tiles     |
|       |           |                      | or 2 L tiles (same type)   |
|    12 |    1x12   | no solutions         | 3 I tiles                  |
|       |    2x6    | no solutions         | 3 O tiles or O + 2 L tiles |
|       |    3x4    | Z1 or Z2 with L1, L2 |                            |
|    16 |    1x16   | no solutions         | 4 I tiles                  |
|       |    2x8    | no solutions         | mix of I, O and L          |
|       |    4x4    | I + 3x4              |                            |
|    20 |    1x20   | no solutions         | 5 I tiles                  |
|       |    2x10   | no solutions         | many                       |
|       |    4x5    | no solutions? †      |                            |
|    24 |    1x24   | no solutions         |                            |
|       |    2x12   | no solutions         |                            |
|       |    3x8    | no solutions         |                            |
|       |    4x6    | all but T            |                            |
|    28 |    1x28   | no solutions         |                            |
|       |    2x28   | no solutions         |                            |
|       |    4x28   | no solutions! ††      |                            |

Notes:

† - I didn't find any, but I don't claim any sort of proof.
†† - *Scientific American*, September 2026, page 14.

## 4. Maze building using Tetris tiles

This is just one thought...

Start with a complete rectangular grid, no walls.  Drop Testris tiles into the grid at random -- the boundaries of the tiles create walls.  Treating the dropped tiles as cells, use a passage carving algorithm to carve a maze.