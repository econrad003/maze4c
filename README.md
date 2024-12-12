# maze4c
Mazes in Python 3

After some false starts, I think I have things set up as I need them.  This is still preliminary, but it should be workable.

**FAQ**:

*  Why *maze4c*? It's the third start (*c*) on my attempts (*maze4*) to put together a Python 3 rewrite of my Python 2 maze implementation (*yaMazeImp*).

**Folders**:

*  *demos* - demonstration modules
*  *doc* - documentation
*  *gallery* - sample image files from demonstration runs
*  *mazes* - the package; the modules in this folder are base classes
    +  *mazes/Algorithms* - algorithm implementations
    +  *mazes/VGT* - vertex-based growing tree algorithm implementations
    +  *mazes/AGT* - arc-based growing tree algorithm implementations
    +  *mazes/Grids* - grid implementations and grid support classes
    +  *mazesGraphics* - graphics drivers
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

Currently the only grid that is ready is the standard N/S/E/W rectangular (or *oblong*) grid in module *oblong* as class *OblongGrid*.  A support class for ring-like tiers is supported in module *oblong\_rings*.

## Graphics

### Oblong (rectangular) grids

* *oblong1* - a crude matplotlib driver (*oblong1*) for oblong grids.  Arcs are not supported.  It only handles the Von Neumann neighborhood (N/S/E/W), but glued edges (cylinder, Moebius strip, torus, Klein bottle, projective plane) are not a problem.
* *oblong2* - a matplotlib driver (*oblong2*) for oblong grids which creates linewise maps of mazes.  I can handle both (undirected) edges and (directed) arcs.  It works best in Moore neighborhoods (nearest neighbor in up to eight compass directions, no glued edges).

## Algorithms

### Maze generation

The following maze generation algorithms have been implemented:

* module *simple\_binary\_tree* (class *BinaryTree*)
* module *sidewinder* (class *Sidewinder*)
* module *inwinder* (class *Inwinder*) - a sidewinder variant that organizes the rectangular grid in rings instead of rows and columns.
* *outwinder* - an outward version of *inwinder - not as interesting, but it's needed for completeness.
* module *growing\_tree1* (class *VertexGrowingTree*) - vertex-based
* module *growing\_tree2* (class *ArcGrowingTree*) - arc-based
* Kruskal's algorithm - like Prim's algorithm, this is a minimum-weight spanning tree algorithm.  It can perform a number of other tricks as well.

These are documented in *doc/Algorithms*.

## Planned but not yet implemented:

* Eller's algorithm.  The basic algorithm is a generalization of sidewinder.  It should come with inward and outward variations corresponding to inwinder and outwinder, but the outward variety should be pretty cool.
* Aldous/Broder and Wilson's Algorithm
* Hunt and kill
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