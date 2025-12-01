# Modules in *mazes.Mazes*

This folder is for modules that create generalized maze structures.  They will, in most cases define classes derived from class *Maze*.

The rest of this *README* is a technical discussion of potential contents.

## Simple and generalized mazes

For our purposes, a (simple) maze consists of a set of cells arranged in a grid.  The grid structure defines neighborhoods for each of its cells.  For each cell in the grid, the maze establishes a set of passages between the cell and its neighbors.  The passages may be directed (*i.e.* *arcs*), undirected (*i.e.* *edges*) or a mix of both.

For a (simple) maze, there are three additional conditions on the passages:

1. (no loops) A passage must link at least two distinct cells;
2. (no hyperedges) A passage must link at most two cells;
3. (no parallel passages) Two distinct passages may not link the same set of cells unless they are directed in a different sense.

A maze which satisfies all three conditions is a simple maze.  *(Unless it is otherwise clear from context, when we say "maze", we imply both simple and undirected.)*

**Remark:**
<blockquote>
If two arcs are directed in the same or opposite sense, we call them parallel or anti-parallel, respectively.  The rules admit pairs of anti-parallel arcs, but not pairs of parallel arcs.  The rules do not admit two edges between the same pair of cells, nor do they admit both an edge and and an arc between the same pair of cells.
</blockquote>

If all the passages are undirected (the usual situation), we the maze is a (simple) (undirected) maze or a (simple) graph.  If all of the passages in a maze are directed, then the maze is a (simple) directed maze or a (simple) digraph.  If the maze is permitted to have a mix of directed and undirected passages, then it is a (simple) mixed maze or a (simple) network.

In graph theory, directed graphs are commonly known as digraphs or networks.  Generally speaking, mixing directed and undirected pairs seems to be a bit taboo, but we'll reserve *digraphs* for directed only and *networks* for graphs which admit both edges and arcs.

## Planarity and embeddings

Although (simple) mazes cannot always be drawn (or embedded) in a plane without passage crossings, a maze is locally a flat or two-dimensional surface.  If we look at a single cell and its neighbors, we can always draw (or embed) the cell and its incident passages in the plane without passage crossings.

A maze which can be drawn (or embedded) in the plane without passage crossings is said to be *planar*.  In general, it is difficult to determine whether a maze is planar, even though sufficient and necessary conditions can be explicitly stated.  A sketch of a maze (on a sheet of paper or a computer monitor) without passage crossings is called an *embedding* of the maze in the plane.

An example of a maze which is typically not planar is a maze on a Moebius strip.

```
       +---+---+           Notes:
    3    A   a    1            A.east=a     B.north=a   C.west=a
       +   +   +               A.south=b    B.west=b    C.north=b
    2  | b   B |  2            A.west=c     B.south=c   C.east=c
       +   +   +
    1    C   c    3
       +---+---+
```

<blockquote>
A classical state is that we have three utilities (*e.g.* electricity, natural gas, and water) and three large customers (*e.g.* ACME Ltd, EastIndia Co Ltd, and EvilEmpire Ltd).  We want to link each utility with each customer without having to place connections (*e.g* pipes) in the same place.  In a Moebius strip world, there is a trivial solution (see above) with each customer adjacent to every utiliity.  If we ignore the labels, the trivial solution above is called *isomorphism class* K(3,3) or a complete *bipartite* graph with three vertices in each of two classes. On the plane, there are no solutions.

Any maze (or graph) which can be *reduced* (using certain operations too technical for this introduction) to K(3,3) is not planar.

The only other condition for planarity is that a graph cannot be *reduced* to a complete graph on five vertices (or K(5)).

The *K* stands for *Kuratowski* after Polish mathematician Kazimierz Kuratowski (1896-1980) who did studied planarity, complete graphs, and complete bipartite graphs.  The relation between planarity and the isomorphism classes K(3,3) and K(5) is known as *Kuratowski's Theorem*.  It was proved in 1930 by Kuratowski, (and independently by Otto and Fink, though their proof was not published).
</blockquote>

Antiparallel arcs, parallel passages (rule 3 violations) and loops (rule 1 violations) do not make a difference in planarity.

## Breaking the rules

### Loops and pseudomazes

A passage that links a single cell is a *loop*,  (It is usually drawn in software as a short arc from one point on the square or circle representing a vertex or cell to another.)  Loops are generally counted as an undirected(!) passage (or edge) from a cell to itself.

A graph which can contain loops (*i.e.* admits violations of rule 1) is commonly called a *pseudograph*.  So mazes which admit violations of rule 1 are *pseudomazes*.  A pseudomaze can be undirected (default assumption), directed, or mixed.

### Parallel passages and multimazes

A graph which is admits violations of rule 3 by allow parallel arcs or edges is commonly referred to as a *multigraph*.  We accordingly speak of *multimazes*.

If we admit loops as well as parallel passages, we can use the clumsy prefix *pseudomulti-* -- *pseudomultigraph*, *pseudomultimaze*, *pseudomultidigraph*, *pseudomultinetwork*, *etc*.

### Simplices, hypergraphs, and higher dimensional manifolds

If we break rule 2, we have a type of passage or join called a *simplex* (plural: *simplices* or *simplexes*).  An *n*-simplex is basically just an object in *n-1*-dimensional space.  An 3-simplex is a triangle; a 4-simplex is a tetrahedron; a 5-simples is a *pentatope* (a four-dimensional figure whose faces are tetrahedra); and so on.

Geometrically speaking, loops (or 1-simplices) are just points and 2-simplices (edges and arcs) are just line segments.

With simplices, the topology of our neighborhoods becomes more compicated.  For example, with a four-cell neighborhood and 3-simplices, the central cell can form a tetrahedron consisting of three faces that include the central cell and one that does not.  The 4-neighborhood is 3-dimensional.  With more cells in the neighborhood, we cannot always fit the tetrahedra into a polyhedron containing the central cell, so generalized graph with 3-simplices is not necessarily *locally* 3-dimensional.

For example, with an unrestricted 6-cell neighborhood, we will have 3 tetrahedra containing the central cell that meet at given triangle.  (Call the central cell O, the central face: OAB, and the three remaining cells C, D, and E.  The three tetrahedra that can meet at OAB are OABC, OABD and OABE.  To be 3D-Euclidean, only two faces can meet.) So an unrestricted 6-cell neighborhood of 3-simplices is not Euclidean.

**Question to ponder:** Is an unrestricted 5-cell neighborhood of 3-simplices three dimensonal Euclidean?

The prefix "*hyper-*" denotes a rule 2 violation: *hypermaze*, "hypergraph*, etc.  To avoid prefix abuse, we will say that rule 1 and 3 violations are also admissible.  If only one type of simplex is allowed, we'll use the adjective "simple", for example:
<blockquote>
A simple (undirected) 3-hypergraph admits 3-simplices, but no loops, edges, or *n*-simplices whenever n>3.
</blockquote>
