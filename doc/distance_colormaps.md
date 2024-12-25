# Distance-based color maps

There are some sample distance-based colormaps in the *gallery* folder.  They are *png* image files with names that start with *dcm\_* for *d*istance *c*olor *m*ap.  These are created using a python module with the same name in the *demos* folder.  The makefile *distance\_maps.make* updates these as needed.

## making additional distance-based color maps

The demo module *demos/colormaps2.py* can create a large variety of distance-based color maps.  To use it, first take a look at the available (and perhaps intimidating) help.  It is available by specifying the "*-h*" or "*--help*" option:

```
    maze4c$ python -m demos.colormap2 -h
    usage: colormap2.py [-h] [-z ZERO] [-d ROWS COLS] [-s SOURCE]
         [-a ALGORITHM] [--title TITLE] [-p BIAS]
                    [--which WHICH [WHICH ...]]
                    [--no-shuffle] [--merge P Q] [--cutoff CUTOFF]
                    [--failures FAILURES]
                    [hot] [cold]

    fill maze with path-length gradient

    positional arguments:
      hot                   the name of the zero distance color (crimson)
      cold                  the name of the maximum distance color (skyblue)

    options:
      -h, --help            show this help message and exit
      -z ZERO, --zero ZERO  the name of the source cell color (goldenrod).
                       'none' will set this to the hot color
      -d ROWS COLS, --dim ROWS COLS
                        the dimensions of the maze (13, 21)
      -s SOURCE, --source SOURCE
                        one of the corners ('sw', 'se', 'ne', 'nw')) or 'c'
                        for center. Default will use longest path computation.
      -a ALGORITHM, --algorithm ALGORITHM
                        The available algorithms are: '1' or 'sbt' - simple
                        binary tree; '2' or 'sw' - sidewinder; '3' or 'iw' -
                        inwinder; '4' or 'ow' - outwinder; '5' or 'dfs' -
                        depth-first search; '6' or 'bfs' - breadth-first
                        search; '7' or 'ell' - Eller's algorithm; '8' or
                        'oell' - outward Eller; '9' or 'iell' - inward Eller
                        (not yet implemented); '10' or 'ab' - Aldous/Broder;
                        '11' or 'rab' - reverse Aldous/Broder; '12' or 'wil'
                        or 'wilson' - Wilson; '13' or 'hou' or 'houston' -
                        Houston's algorithm; '14' or 'hk' - Hunt & kill
                        algorithm; '15' or 'kr' or 'kruskal' - Kruskal's
                        algorithm; '16' or 'krq' - Kruskal's (RandomQueue);
                        '17' or 'sprim' - Simplified 'Prim'; '18' or 'vprim' -
                        Vertex 'Prim'; '19' or 'prim' - Prim's algorithm; '20'
                        or 'aprim' - Arc 'Prim'. The default is Wilson's
                        algorithm.
      --title TITLE         a title for the plot

    specialized arguments:
      The following arguments are options for some of the maze carving
      algorithms.

      -p BIAS, --bias BIAS  the probability of a head in a coin toss.
                        The default is a fair coin. (default None)
      --which WHICH [WHICH ...]
                        controls selection from a run, for example (0, -1)
                        always selects the first or the last element of the
                        run. The default is to randomly choose an element from
                        each run. (default None)
      --no-shuffle          if this is set, some algorithms will process
                        neighbors on a first-come first-served basis instead
                        of shuffling the neighborhoods. For most Python
                        distributions, setting thisoption will result in a
                        directional bias.
      --merge P Q           the probability P/Q of a run merge in Eller's
                        algorithm. The default probability is 1/3. (default
                        None)
      --cutoff CUTOFF       when the this cutoff proportion is reached,
                        the.algorithm switches. (default None)
      --failures FAILURES   when the failure rate is reached, the.algorithm
                        switches. (default None)

    usage of specialized arguments:
      Options by algorithm: 1) sbt: uses --bias; 2) sw: uses --bias and
      --which; 3) iw: uses --bias and --which; 4) ow: uses --bias and
      --which; 5) dfs: uses --no-shuffle; 6) bfs: uses --no-shuffle;
      7) ell: uses --bias and --merge; 8) oell: uses --bias and --merge;
      9) iell: uses --bias and --merge; 13) hou: uses --cutoff and --failures.
```

We will take this is small bite-sized pieces...

## the color scheme

The default color scheme is based on three colors, a reddish color (crimson) that represents hot as in very close to the starting point, a bluish color (sky blue) which represents cold as in far away from the starting point, and a yellowish color (goldenrod) which represents the starting point.  Colors that are "between" the hot and cold colors indicate distance from start.  So the default scheme produces colors that start with crimson, gradually cool to dull purple hues, and cool further into the blue-grey range.

People react differently to changing colors, so this scheme can be changed.  For example to use red, blue and yellow instead of crimson, sky blue and goldenrod, we type:
```
    maze4c$ python -m demos.colormap2 red blue -z yellow
```
The program will then interpolate between red and blue as cells get farther away from the starting cell.  The hot and cold colors are optional positional arguments.  The "zero" color (following *-z* or *--zero*) identifies the "hottest" spot, namely the start cell.

The color names are the *matplotlib*-assigned names currently available at:

> [https://matplotlib.org/stable/gallery/color/named_colors.html](https://matplotlib.org/stable/gallery/color/named_colors.html)

## the algorithm

There are twenty different algorithms built into this demonstration program.  Each is identified by a number and an abbreviation.  To specify the algorithm, use the "*-a*" or "*--algorithm*" switch followed by the number or the abbreviation.  The abbreviation is case-insensitive.  (The switch is not!)

For example, to prepare a red/blue/yellow colormap of a randomly generated Eller's algorithm maze, type:
```
    maze4c$ python -m demos.colormap2 red blue -z yellow -a ell
```
or
```
    maze4c$ python -m demos.colormap2 red blue -z yellow -a 7
```

If you like the default color scheme, it's simpler:
```
    maze4c$ python -m demos.colormap2 -a ell
```

The failsafe for typing something other than a recognized number or abbreviation is Wilson's algorithm.

Here are the twenty recognized options for algorithm:

| **number** | **name1** | **name2** | **algorithm**                     |
| ---------: | :-------- | :-------- | :-------------------------------- |
|          1 | sbt       |           | simple binary tree                |
|          2 | sw        |           | sidewinder                        |
|          3 | iw        |           | inwinder                          |
|          4 | ow        |           | outwinder                         |
|          5 | dfs       |           | depth-first search                |
|          6 | bfs       |           | breadth-first search              |
|          7 | ell       |           | Eller's algorithm                 |
|          8 | oell      |           | outward Eller                     |
|          9 | iell      |           | inward Eller (TBA)                |
|         10 | ab        |           | Aldous/Broder                     |
|         11 | rab       |           | reverse Aldous/Broder             |
|         12 | wil       | wilson    | Wilson's algorithm                |
|         13 | hou       | houston   | Houston's algorithm               |
|         14 | hk        |           | the Hunt & Kill algorithm         |
|         15 | kr        | kruskal   | Kruskal's algorithm               |
|         16 | krq       |           | "Kruskal" (RandomQueue)           |
|         17 | sprim     |           | simplified "Prim"                 |
|         18 | vprim     |           | vertex "Prim"                     |
|         19 | prim      |           | Prim's algorithm                  |
|         20 | aprim     |           | arc 'Prim                         |

Notes: (TBA) Inward Eller hasn't been implemented yet, so slot 9 is reserved.

Typographical errors give you Wilson's algorithm.

## algorithm-specific options

Some of the easier options have been implemented.  They are listed in the help under the heading "specialized arguments". Below these options is another heading "usage of specialized arguments" which identifies which options apply to a given algorithm.

For example, sidewinder uses "bias" and "which".  To run sidewinder with its defaults:
```
    maze4c$ python -m demos.colormap2 -a sw
```

If we want to create a "cocktail shaker" spanning binary tree which attempts to go upward with 25% probability:
```
   maze4c$ python -m demos.colormap2 -a sw --bias 0.25 --which 0 -1
```

## maze dimensions

The default color maps use a default of 13 rows and 21 columns.  (These are consecutive Fibonacci numbers.)  Some people believe that most desirable rectangles whose sides are in approximate ratio 1:1.618. (1.618 is an approximation of the mean-extreme ratio, now commonly known as the golden ratio.  The golden ratio is actually irrational.)  Consecutive Fibonacci numbers give the best rational approximations to this ratio.  As to the desirability of golden rectangles, I have no opinion.  That consecutive Fibonacci numbers provide best rational approximations of the golden ratio is, however, a mathematically provable fact.  But I digress..

If you have triskaidekaphobia, we're off to a bad start because 13 is a fearsome number.  But, no problem.  If you prefer multiples of three, we can create color maps which have 12 or 15 rows and 21 columns, for example,
```
    maze4c$ python -m demos.colormap2 -a dfs --dim 15 21
```
will produce a maze with 15 rows and 21 columns using depth-first search.

## the source

The default is to find a longest path and use one end of this path as the source cell -- the cell that gets the goldenrod paint.  The four corners or an approximate center can instead be specified as the source.

To specify the center, use the option "*-s c*" or "*--source c".  The center is calculated by dividing the dimensions by two and truncating any fractions.  If both dimensions are odd, this gives the center cell.  If either dimension is even, then the cell will have an edge in the center of the grid. If both dimensions are even, then the cell will have its northwest corner in the center.

For example, to create a distance-based color map for a 15x21 maze created using Prim's algorithm and using distances from the center cell, type:
```
    maze4c$ python -m demos.colormap2 -a prim --dim 15 21 -s c
```
Since both dimensions are odd, the cell in goldenrod is the center cell.

## the title

By default, the title is built using the algorithm name and any options.  For example, the title generated for
```
   maze4c$ python -m demos.colormap2 -a oell
```
is just "Outward Eller", but the title for
```
   maze4c$ python -m demos.colormap2 -a oell --bias 0.3 --merge 1 4
```
is "Outward Eller (rise bias 30.00%, run bias 1/4)" which tells us that the optional rises occur with 30% probability and the merges occur with probability 1/4 (*i.e.*, in one of four cells, or equivalently with 25% probability).

A title can be supplied using the "*--title" option.  For example, the colormap module can be turned into a glorious "hello world" program as follows:
```
    maze4c$ python -m demos.colormap2 -a hou --cutoff 0.9 --title "hello world!"
```
The maze is created using Houston's algorithm with a cutoff rate of 90% and is titled with a friendly and inviting "hello world!" (including one error each in punctuation and capitalization).