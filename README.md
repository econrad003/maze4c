# maze4c
Mazes in Python 3

Latest revision: 29 November 2024

After some false starts, I think I have things set up as I need them.  This is still preliminary, but it should be workable.

**FAQ**:

*  Why *maze4c*? It's the third start (*c*) on my attempts (*maze4*) to put together a Python 3 rewrite of my Python 2 maze implementation (*yaMazeImp*).

**Folders**:

*  *demos* - demonstration modules
*  *gallery* - sample image files from demonstration runs
*  *mazes* - the package; the modules in this folder are base classes
    +  *mazes/Algorithms* - algorithm implementations
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

Currently the only grid that is ready is the standard N/S/E/W rectangular (or *oblong*) grid in module *oblong* as class *OblongGrid*.  A support class for ring-like tiers is supported in module *oblong\_rings*.

## Graphics

The only graphics driver is a crude matplotlib driver (*oblong1*) for oblong grids.

## Algorithms

The following algorithms have been implemented:

* module *simple\_binary\_tree* (class *BinaryTree*) - the elementary binary tree algorithm (heads-go north; tails-go east) described in the Jamis Buck book.  (Note that this is just one algorithm for carving a binary spanning tree and it is very speciaized -- there are more general algorithms that produce more interesting binary tree mazes.)  It is implemented here as a passage carver.
* module *sidewinder* (class *Sidewinder*) - the sidewinder algorithm (heads-go north from somewhere in the current run; tails-continue the run eastward), also described in the Jamis Buck book.  It is a true generalization of the simple binary tree algorithm.  The spanning trees that it produces are not in general binary trees, but it isn't hard to restrict the run choice for a head in ways that produce a binary tree.  In particular, always choosing the last cell in the run to carve north yields the simple binary tree algorithm.  Choosing the first or the last at random in a sort of cocktail shaker fashion yields a more general spanning binary tree.
* module *inwinder* (class *Inwinder*) - This is a variant of the sidewinder algorithm that uses rings instead of rows for the runs and carves inward from a run instead of northward when the coin toss is a head.  (It is a variant, not a generalization.)  Because the corner cells in a rectangular ring do not have inward neighbors, and because the rings are circuits (as opposed to rows which are paths), it is slightly more complicated than sidewinder.
  > This particular maze carving algorithm was inspired by the story of Theseus and the Minotaur -- place the Minotaur in the innermost ring and have Theseus enter somewhere in the outermost ring.  (The princess Ariadne gave him a sword to slay the Minotaur and a ball of yarn to find his way back to the entrance.  For thanks, Theseus abandoned Ariadne on an island somewhere between her home in Crete and his home in Athens.)  The algorithm is not mentioned in the Jamis Buck book, but is briefly implied in an exercise in the polar (!) mazes section.

 > Note that *inwinder* has a sort of opposite (*outwinder*) which I haven't (yet?) implemented.

### growing tree algorithms

* module *dfs* (class *DFS*) - the depth-first search (aka DFS aka recursive backtracker) maze carving algorithm.  This is described (as recursive backtracker) in the Jamis Buck book.  It produces mazes that tend to have long winding corridors.  (Depending on how dictionaries are implemented in your Python 3 distribution, you should see much longer but less meandering corridors if you suppress shuffling.)  There are essentially two variants implemented here -- an edge-based variant and a frontier-based variant -- with slighly different biases.  This is really a first cut...  See the next entry...
* module *dfs\_better* (class *DFS*) - a more efficient depth-first search.  It is implicitly edge-based, but it could be tweaked to produce a frontier-based version.
* module *bfs* (class *BFS*) - the breadth-first search maze carving algorithm.  It produces mazes with minimum diameter.
* module *simplified\_Prim* (class *NotPrim*) - an algorithm is superficially similar to Prim's algorithm.  It does produce nice mazes with a radial structure, sort of like spider webs.

## REFERENCES

1. Jamis Buck. Mazes for programmers.  Pragmatic Bookshelf, 2015.