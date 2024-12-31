# maze4c
Mazes in Python 3

**FAQ**:

*  Why *maze4c*? It's the third start (*c*) on my attempts (*maze4*) to put together a Python 3 rewrite of my Python 2 maze implementation (*yaMazeImp*).

**Folders**:

*  *demos* - demonstration modules
    +  *demos/polar* - demonstration modules for theta (aks: polar) mazes
*  *doc* - documentation
    +  *doc/Algorithms* - algorithm documentation
    +  *doc/Grids* - grid documentation
*  *gallery* - sample image files from demonstration runs
    +  *gallery/theta* - demonstration images for theta (aka: polar) mazes
*  *mazes* - the package; the modules in this folder are base classes
    +  *mazes/Algorithms* - algorithm implementations
    +  *mazes/VGT* - vertex-based growing tree algorithm implementations
    +  *mazes/AGT* - arc-based growing tree algorithm implementations
    +  *mazes/Grids* - grid implementations and grid support classes
    +  *mazes/Graphics* - graphics drivers
*  *tests* - testing to make sure things work as expected

## Running the demonstration modules

These are modules and not scripts, so run them using the *python -m* syntax.
For example, for *demos/simple\_binary\_tree.py* run it from the folder that contains the *mazes* folder.  If the *demos* folder is in the same folder as the *mazes* folder (as in the repository), then the command would be:

```
    python -m demos.simple_binary_tree -h
```
Note that the slashes are replaced by dots and the *.py* extension is discarded.  The demonstration modules use *argparse* for argument parsing -- the *-h* option will display usage information.  The *gallery* folder contains at least one output image from each demonstration program.

> [!NOTE]  
> I don't recommend modifying the Python path as this is a great way to break things.  Unfortunately there does not seem to be *simple* way of using Python 3 to write scripts which are not stored in the current working directory.

For the time being, the graphics drivers use *matplotlib* and *numpy*.  These will need to be installed if you don't already have them.

At some point, I will put up a *turtle* driver at some point using Python's native turtle graphics (which in turn require *tk*), but, unfortunately the *tk* interface does not have a practical way of saving plots to an image file.  (*Tk* does have *ImageGrab* which does a screenshot -- but that's not the same thing as saving the plot as an image.)

## Grids

### Oblong (rectangular) grids

The standard N/S/E/W rectangular (or *oblong*) grid in module *oblong* as class *OblongGrid*.  A support class for ring-like tiers is supported in module *oblong\_rings*.

### Theta (or polar or circular) grids

Theta (or polar or circular) grids are supported as class *ThetaGrid* in module *polar*.

## Graphics

### Oblong (rectangular) grids

* *oblong1* - a crude matplotlib driver (*oblong1*) for oblong grids.  Arcs are not supported.  It only handles the Von Neumann neighborhood (N/S/E/W), but glued edges (cylinder, Moebius strip, torus, Klein bottle, projective plane) are not a problem.
* *oblong2* - a matplotlib driver (*oblong2*) for oblong grids which creates linewise maps of mazes.  I can handle both (undirected) edges and (directed) arcs.  It works best in Moore neighborhoods (nearest neighbor in up to eight compass directions, no glued edges).

### Theta (polar/circular) grids

* *polar1* - a basic graphics driver for theta (or polar) mazes.
* *polar2* - a basic graphics driver for linewise representation of theta mazes.

## Algorithms

### Maze generation

The following maze generation algorithms have been implemented:

* module *simple\_binary\_tree* (class *BinaryTree*)
* module *sidewinder* (class *Sidewinder*)
* module *inwinder* (class *Inwinder*) - a sidewinder variant that organizes the rectangular grid in rings instead of rows and columns.
* *outwinder* - an outward version of *inwinder - not as interesting, but it's needed for completeness.
* module *growing\_tree1* (class *VertexGrowingTree*) - vertex-based
* module *growing\_tree2* (class *ArcGrowingTree*) - arc-based
* module *kruskal* (class *Kruskal*) - Kruskal's algorithm - like Prim's algorithm, this is a minimum-weight spanning tree algorithm.  It can perform a number of other tricks as well.
* module *eller* (class *Eller*) - Eller's algorithm.  The basic algorithm is a generalization of sidewinder with a few tricks which are adapted from Kruskal's algorithm.  In addition, an outward variant (generalizing outwinder) has been implemented.
* module *outward\_eller* (class *OutwardEller*) - outward variant of Eller's algorithm.
*  module *aldous\_broder* (class *AldousBroder) - the first entrance random walk algorithm, known as Aldous/Broder after two independent discoverers. The algorithm is unbiased.
*  module *reverse\_aldous\_broder* (class *ReverseAldousBroder) - the last exit random walk algorithm, known as reverse Aldous/Broder. The algorithm is unbiased.  It's sort of like Aldous/Broder in a universe where time runs backwards.  The algorithm is unbiased.
*  module *wilson* (class *Wilson*) - the circuit-eliminated random walk algorithm, known as Wilson's algorithm after its discoverer.  This is another unbiased algorithm.
*  module *houston* (class Houston) - a hybrid which carves a maze like Aldous/Broder until triggered by a threshold, and completes the maze using Wilson's algorithm.  No proof (to my knowledge) has been given which settles the question of bias.  (One possibility: it converges too quickly on average to be unbiased.)
* module *hunt\_kill* (class *HuntKill*) - the hunt and kill algorithm, a series of random paths, avoiding already visited cells; each path ends when there is no available step... A new path starts with a passage from the visited area into the frontier.  The algorithm has features reminiscent of Aldous/Broder (random walk, but restricted), Wilson (paths leading from the visited area, but working outward from the visited area instead of inward to) and DFS (you might come up with this if you wanted to avoid both a stack and recursive programming).

These are documented in *doc/Algorithms*.

#### Specialized maze generation algorithms

Some of the algorithms listed above (simple binary tree, sidewinder and Eller's algorithms, as well as their variants like inwinder and outward Eller) are specialized to work on an oblong grid in a Von Neumann (N/S/E/W) neighborhood.  They simply won't work on most grids. Others (like the growing tree family, Kruskal, hunt and kill, Wilson, Aldous/Broder, and Houston) will work on any connected grid.

The specialized algorithms can sometimes be adapted to work on other grids.  The variants mentioned above, such as inwinder, can be thought of as clues.  The basic algorithms generally organize an oblong grid into rows and columns.  Inwinder plays by analogy on a row/column arrangement.  The rows in inwinder are rectangular rings.  The columns are essentially vectors of cells starting from the outermost ring and proceeding inward.  It isn't a perfect analogy, as the corner cell vectors are not well-defined, and the rings don't have a definite stop cell. But the analogy is sufficiently close -- the problems can be surmounted.

Adaptations of algorithms for other classes of grids are contained in subfolders.  The variants for other grids, as they become available, are found in:

*   *mazes/Algorithms/polar* - for theta (or polar) grid variants

Documentation, as it becomes available, is found in:

*   *doc/Algorithms/theta* - for theta (or polar) grid variants

In addition to variants, other grids will certainly have their own specialized algorithms that might not have practical oblong counterparts.  These will also go in the above subfolders.

### Other algorithms

In addition to the maze generation algorithms above, the following algorithms are found in the *mazes/Algorithms* folder:

* module *dijkstra* - Dijkstra's shortest path algorithm.  This is a *Swiss army knife* -- it can find path lengths, distances, and shortest paths in a maze.  In trees, it can be used to find the diameter (length of a longest shortest path) as well as a longest shortest path. (For mazes which aren't trees, finding the diameter and finding a longest shortest path are both much harder problems. When finding distances or minimum distance paths, the algorithm will fail there are negative edge weights.)

## Planned but not yet implemented:

* Eller's algorithm should come with an inward variant corresponding to inwinder.
* Recursive division
* An algorithm based on cellular automata (See the last example in the Kruskal's algorithm documentation for a preview.)

## Helper methods for growing trees

### The VGT folder (vertex-based growing trees)

The *mazes/VGT* folder contains several helper methods intended to simplify the setup for *mazes.Algorithms.growing\_tree1* (class *VertexGrowingTree*).  Each of these contains two methods.  Method *init\_maze* sets up a rectangular maze.  The other method has the same name as the module name -- it runs the algorithm.  See *doc/Algorithms/growing\_trees1.md* for examples of usage.

* module *mazes.VGT.dfs* - method *dfs* - depth-first search
* module *mazes.VGT.bfs* - method *bfs* - breadth-first search
* module *mazes.VGT.sprim* - method *sprim* - simplified "Prim"
* module *mazes.VGT.vprim* - method *vprim* - vertex "Prim"

### The AGT folder (arc-based growing trees)

The *mazes/AGT* folder contains several helper methods intended to simplify the setup for *mazes.Algorithms.growing\_tree2* (class *ArcGrowingTree*).  Each of these contains two methods.  Method *init\_maze* sets up a rectangular maze.  The other method has the same name as the module name -- it runs the algorithm.  See *doc/Algorithms/growing\_trees2.md* for examples of usage.

* module *mazes.VGT.dfs* - method *dfs* - depth-first search
* module *mazes.VGT.bfs* - method *bfs* - breadth-first search
* module *mazes.VGT.sprim* - method *sprim* - simplified "Prim"
* module *mazes.VGT.primic* - method *primic* - a Prim's algorithm mimic which can do Prim's algorithm and lots of other stuff.

## REFERENCES

1. Jamis Buck. Mazes for programmers.  Pragmatic Bookshelf, 2015.
2. Lucia Costantini.  *Algorithms for sampling spanning trees uniformly at random* (master's thesis).  Polytechnic University of Catalonia.  Web. Accessed 20 December 2024.
URL: [https://upcommons.upc.edu/bitstream/handle/2117/328169/memoria.pdf](https://upcommons.upc.edu/bitstream/handle/2117/328169/memoria.pdf)
3. Yiping Hu, Russell Lyons and Pengfei Tang.  *A reverse Aldous/Broder
        algorithm.*  Preprint.  Web: arXiv.org.  24 Jul 2019.
URL:[http://arxiv.org/abs/1907.10196v1](http://arxiv.org/abs/1907.10196v1)
4. Jamis Buck. "Maze Generation: Wilson's algorithm" in *the Buckblog*.  Web. Accessed 21 December 2024.
URL: [http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm.html](http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm.html) 
5. Jamis Buck.  "Maze Algorithms".  Web.  Accessed 21 December 2024.
URL: [https://www.jamisbuck.org/mazes/](https://www.jamisbuck.org/mazes/)
