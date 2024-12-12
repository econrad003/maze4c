# Change Log

## Release 0.5 - 12 December 2024

### New algorithms

1.  Kruskal's algorithm
2.  Outwinder

See folder doc/algorithms for documentation.

## New modules

1.  mazes.components - connected component management
2.  mazes.tools.automaton1 - a simple cellular automaton
3.  tests.components - for checking mazes.components

## Minor and cosmetic changes

typos, docstring corrections, etc.

## Other changes

Removed all through 0.2 from this changelog.

## Release 0.4 - 9 December 2024

I've started using *git* for updates.  Since 0.3, I've been organizing and reorganizing documentation.

Apart from getting the documentation organized and written, there is one update.  Module *VGT.vprim* now supports the *cache* option.  If you don't want the priority queue to create vertex weights on the fly, you can specify *cache=False*.  This is covered in the *doc/Algorithms/growing\_trees1.md* documentation.  In the next update, I will start removing some of the older entries in the changelog.

## Release 0.3 - 3 December 2024

There is quite a bit here, so this summary may be imcomplete.  Documentation is not up to date.

### New module folders

* *mazes.Queues* - for queuing classes (includes modules defining classes *Stack*, *Queue*, *RandomQueue* and *PriorityQueue*)
* *mazes.AGT* - for arc-based growing tree algorithms (4 new modules)
* *mazes.VGT* - for vertex-based growing tree algorithms (4 new modules)

### New modules

* *mazes.gqueue* - generalized queue virtual class (*GeneralizedQueue*)
* *mazes.Graphics.oblong2* (class *SpiderWeb*) - a linewise graphics driver for oblong grids that inherits from class *Spider* in the *matplotlib* driver
* *mazes.Algorithms.growing\_tree1* (class *VertexGrowingTree*) - a growing tree family of algorithms using queuing classes.  This algorithm generalizes DFS (aka: recursive backtracker" -- using a stack), BFS (using a queue), "simplified Prim" (using a random queue) and "vertex Prim" (using a priority queue). This version of growing tree places cells (vertices) on the queuing structure.
* *mazes.Algorithms.growing\_tree2* (class *ArcGrowingTree*) - a growing tree family of algorithms using queuing classes.  This algorithm generalizes Prim's algorithm.  It places grid arcs (ordered pairs of neighboring cells on the queuing structure.

### Enhancements

* *mazes.Graphics.matplot\_driver* - added method *draw_arrow* to the *Spider* class

### Corrections

* *cell*/*edge*/*arc*/*maze* in *mazes* folder - corrected the unlink sequence

### Cosmetic corrections

* corrected docstrings and formatting in a number of places

