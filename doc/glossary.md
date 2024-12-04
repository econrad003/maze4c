# GLOSSARY

This a reference -- refer to it when needed as you would refer to a dictionary or an encyclopedia; please don't read it like a novel.  It's primary purpose is to keep me reasonably consistent as I write.  Be aware that the language is fluid -- different people define the same words in different ways.  This is especially true of technical language.

## A

*adjacency matrix - a matrix whose rows and columns are indexed by the nodes of a network.  If u is not equal to v, the entry for row u column v is the number of arcs from u to v plus the number of edges joining u and v.  If u=v, the entry is double (since loops are counted twice!).

* If we add the numbers in row u, we get the out-degree of node u.
* If we add the numbers in column v, we get the in-degree of node v.
* Leonhard Euler's lemma: If the network is a graph (i.e. no arcs), then the sum of all the entries is twice the number of edges.
* Powers of the adjacency matrix (using matrix multiplication) are related to the number of walks.


*adjacent to* - a relation between vertices -- two vertices are adjacent if there is an edge that joins them, or, equivalently, two vertices are adjacent if they are neighbors.

* See also: incident to, adjacency matrix

## B

*base* of a graph - a maximal spanning forest.  For a connected graph, this will be a spanning tree.

* See also: independent set, perfect maze, rank, spanning tree, tree

## C

*circuit* - a path that starts and ends at the same vertex.

* Note that apart from the terminals, the vertices are all distinct.

*component* - see: "*connected*"


*connected* - two vertices (or cells) in a graph (or undirected maze) are connected if there is a path that joins them.

* A cell is connected to itself.  (Hint: if v is a vertex, then (v) is a path that joins v to v.)
* Connectedness is not always well-defined in a digraph or a network.
* The *component* that contains a cell is the set of all cells that are connected to the given cell.

*cycle* - a walk that starts and ends at the same vertex.

* A circuit is a cycle, but not every cycle is a circuit.  "A simple cycle" is another way of saying "circuit".

## D

*dead end* - in a graph, a vertex of degree 1...

* in a digraph, a vertex with in-degree greater than 0 (implying that it is reachable from another node) and out-degree 0 (implying that you can enter but you cannot leave).
* in a network, a node which is incident to a single edge (as in a graph -- the only way to leave is by retracing your steps), or at least one arc leading in and none leading out (you can enter, but you can't leave), but not both (with an arc leading in and an edge, you can go in via the arc and leave via the edge).

*degree* of a vertex (or node)

* In a graph, the degree of a vertex is the number of edges that are incident to the given vertex, with loops counted twice. (Yes! Loops complicate matters!)
* For a digraph, we distinguish between in-degree and out-degree.  The in-degree of a node in a digraph is the number of edges leading into the node.  The out-degree is the number of edges leading out of the node.)
* For a network, arcs are handled as in digraphs. Edges are counted twice, once in the in-degree and a second time in the out-degree.
* Leonhard Euler's lemma: If our network is a graph, then the sum of all the in-degree and the out-degrees is equal to twice the number of edges.
* Leonhard Euler's lemma: The sum of the degrees of the vertices in a graph is twice the number of edges.  (This is why loops are counted twice in the degree of a vertex.)
* See also: isolated vertex, dead end


*dependent* set of edges (or joins) -- a dependent set of edges is a set that contains a circuit.

* An independent set of edges contains no circuits, that is, there is no way of arranging some of its edges to form a circuit.
* If we can form a circuit with some of the edges of a set of edges, then the set is dependent.  If we need all of the edges in the set, the set is itself a circuit.


*digraph* - a finite mathematical structure consisting of two types of objects, nodes and arcs: the arcs join the nodes in ordered pairs. The formal definition is as follows:

* A digraph D is an ordered pair (N, A) where (i) N and A are disjoint finite sets; and (ii) the members of A are ordered pairs of members of N.  (The members of N are variously called nodes, vertices, or cells.  The members of A are called arcs or joins.)
* See also: graph, grid, maze, network
* A digraph is a network whose joins are all arcs.


## E

*Euler, Leonhard* (1707-1783) A prolific eighteenth century Swiss mathematician who did much of his work in St Petersburg, Russia. Many people cite his corollary as "Euler's formula":
```
        exp iπ = -1
```
Using the derivatives of the sine, the cosine and the natural exponential functions (with angles in radians), it can be verified using power series expansions that:
```
        exp iz = cos z + i sin z
```
for all complex numbers z.  Putting z=π yields the corollary.

Mentioned in several places in this glossary is a lemma: the sum of the degrees of the vertices is twice the number of edges which is a simple observation made in Euler's paper on the Königsberg bridges problem.

Much deeper and also very important in graph theory is his polyhedral formula -- given a convex polyhedron with v vertices, e edges and f faces:
```
        v - e + f = 2
```
For example, a cube has 6 faces (the six faces of a die), 8 vertices (four on the floor and four above), and 12 edges (four bounding the face on the floor, four bounding the face o top, and four standing vertically to connect a vertex on bottom to another on top).
```
        8 - 12 + 6 = 14 - 12 = 2
```
Work on his collected works (*Opera Omnia*) began in 1908.  According to [Wikipedia](https://en.wikipedia.org/wiki/Opera_Omnia_Leonhard_Euler), 80 of 81 volumes had been published as of 2022, with the last in preparation.  Some additional material including manuscripts and correspondence is slated to be published online.  Much of the material has been made available online in the [Euler Archive](http://eulerarchive.maa.org/)

Note: the links above are:

* (Wikipedia)  `https://en.wikipedia.org/wiki/Opera_Omnia_Leonhard_Euler`
* (Euler Archive) `http://eulerarchive.maa.org/`

## F

*forest* - a graph whose components are trees.

* A connected forest is a tree.
* Forests are the independent sets in a graph.

## G

*graph* - a finite mathematical structure consisting of two types of objects, vertices and edges: the edges join the vertices in unordered pairs. The formal definition is as follows:

* A graph G is an ordered pair (V, E) where (i) V and E are disjoint finite sets; and (ii) the members of E are unordered pairs of members of V.  (The members of V are variously called vertices, nodes, or cells.  The members of E are called edges or joins.)
* See also: digraph, grid, maze, network, simple graph, loop, parallel edge
* A graph is a network whose joins are all edges.


*grid* - a connected network which can be viewed as a graph or a digraph.  As a graph, each of its cells (nodes or vertices) is joined by edges to other cells in neighborhoods.  When viewed as a digraph, each of its edges can be viewed as two separate (anti-parallel) arcs that join a pair of cells in two directions.

* Example: An oblong or rectangular grid is a set of cells arranged in a rectangle in a fixed number of rows (from south to north, numbered consecutively from 0 in the south) and in a fixed number of columns (from west to east, likewise numbered consecutively from 0 from the west).  The neighborhood of a cell consists of the cell itself, and the cells 1 unit away to the south, east, north, and west.  If the cell is in any column except the last column, it has a neighbor to the east.  In the graph view, the two cells are joined by an edge.  In the digraph view, they are joined by two arcs, one going east and the other west.
* See also: maze, Moore neighborhood, Von Neumann neighborhood
* Synonym: lattice

## I

*incident to* - a relation between vertices and edges

* vertex v is incident to edge e if it is one of the vertices on the edge.  (For arcs, we need to distinguish between in and out.)  Incidence in this sense is sometimes expressed as "v lies on e".
* edge e is incident to vertex v if v is incident to e.  In this sense, we might say "e contains v".
* If a vertex v is incident to two edges e and f, we typically say something like "e and f meet at v" or just "e and f meet".


*independent* set - a set of edges that does not contain a circuit.

* See also: dependent, forest, spanning tree, tree


*isolated* vertex (or cell or node) - a vertex or node with no incident edges or arcs.

* An isolate has degree 0, in-degree 0 and out-degree 0.
* An isolate is a component consisting of a single vertex (or cell or node)
* See also: degree

## J

*join* - an edge or an arc.

* Synonym: passage


## L

*lattice* - as used here, a synonym for a grid.  In a lattice, points are ordered in some fashion.  For example, in a rectangular grid points are ordered in rows and columns.


*loop* - an edge consisting of a single cell.  Loops are prohibited in a simple graph or a simple network.  A graph that may contains loops but may not contain parallel edges is sometimes called a pseudograph.

* The presence of loops in a graph tends to complicate its analysis.  But sometime we need to deal with them, even if it's only to say we aren't permitting them.
* Loops are, by their very nature, undirected.  Arcs are ordered pairs, so (x,y) and (y,x) are not the same unless y is x.
* Graphs that have no loops and no parallel edges are called "simple graphs".
* See also: parallel, degree


## M

*maze* - in short, a maze is a network.  Usually the joins in a maze are edges, so, for our purposes, a maze is usually just a graph. Its vertices or nodes are generally called cells and its edges (or arcs, or more generally its joins) are usually referred to a passages.

* We'll call a pictorial representation of a maze a sketch, or a drawing, an image, or a picture.  Sometimes we'll carelessly call it a graphic -- with the vain and misguided hope that everyone will be able to distinguish between "graphic" as the adjective form of "graph" as defined above and "graphic" as synonymous with "sketch".

*minimum weight spanning tree* - if each of the edges in a **connected** graph has a non-negative weight then the net weight of any subgraph is the total of the weights of the edges in the subgraph.  If we consider all possible spanning trees and their net weights, a spanning tree with a net weight which is less than or equal to the every possible net weight for a spanning tree, then the spanning tree is a minimum weight spanning tree.  For a given weight function, there may be more than one such tree, but there will always be at least one.

* Prim's algorithm can find a minimum weight spanning tree.
* Kruskal's algorithm can find a minimum weight spanning tree.




*Moore neighborhood* - a neighborhood consisting of a cell and the nearest cells to the south, southeast, east, northeast, north, northwest, west and southwest.  (The Moore neighborhood consists of a cell along with both its orthogonal and its diagonal neighbors.)

* See also: Von Neumann neighborhood

## N

*neighbor* of a cell - any cell joined with the given cell by an edge, or joined by an arc which is directed away from the given cell


*neighborhood* of a cell - the cell and its neighbors

*See also: topology


*network* - a finite mathematical structure consisting of two types of objects, nodes and joins: the joins join the vertices in pairs. The joins may be ordered, in which case they are referred to as arcs, or unordered, in which case they are referred to as edges.  The formal definition is as follows:

* A network D is an ordered pair (N, J) where (i) N and J are disjoint finite sets; and (ii) the members of J are pairs -- either ordered or unordered -- of members of J.  (The members of N are variously called nodes, vertices, or cells.  The members of J are called joins.  The ordered joins are arcs and the unordered joins are edges.)
* See also: digraph, graph, grid, maze


*node* - the fundamental objects in a network.

* Synonyms: points, cells, vertices. When we speak of nodes, we usually are thinking of our structure as a network.


## P

*parallel* - two join in a network are parallel if they have the same endpoints.  If they are arcs running in opposite directions, the are ant-parallel.

* Like loops, parallel edges tend to complicate analysis of graphs.
* A graph that has no loops but can have parallel edges is called a multigraph.
* Note that the definition of a graph also allows parallel loops.
* Graphs that have no loops and no parallel edges are called "simple graphs".
* See also: loops.

*passage* - an edge or an arc.

* Synonym: join


*path* - a walk which may begin and end in the same vertex, but otherwise no vertex is repeated.  The source and the sink may be the same, but the remaining vertices are all distinct from each other and from source and sink.

* See also: connected, walk

*perfect maze* - a spanning tree for a grid. (It's not a judgment of aesthetics.)  Note that a disconnected grid cannot have a perfect maze.

*points* - a general name for fundamental objects.  In geometry, objects such as lines and planes are sets of points.  In a graph, edges are unordered pairs of vertices and the graph itself is essentially a collection of edges, so the fundamental objects or points in a graph are its vertices.

* Synonyms: cells, nodes, vertices.  We usually use vertices for graphs, nodes for digraphs and networks, cells for grids and mazes, and points or cells for lattices.  But note: "*A foolish consistency is the hobgoblin of petty minds.*"

## R

*rank* of a graph - the number of edges in a maximal spanning forest.

* Let G be a graph with v vertices and k connected components.  If the graph is connected (i.e. k=1), then:
```
        r(G) = v-1
```

* In general:
```
        r(G) = v-k
```

## S

*spanning* subgraph - given a graph G=(V,E), a spanning subgraph is a subgraph F=(U,V) of G for which U=V.  (In other words, F is a subgraph of G and the vertices of F *span* the vertex set of G.


*spanning tree* - a spanning subgraph is a subgraph which is also a tree.

* The spanning trees of a connected graph are the maximal independent sets in the graph.  The number of edges in a tree is one less than the number of vertices.  So if a connected graph has v vertices, then every spanning tree contains v-1 edges.  (The rank of a connected grid with v cells is v-1.)
* Synonymns: perfect maze, base (assuming the graph is connected)


*subgraph* - given a graph G=(V,E), a subgraph is a graph H=(U,F) for which U and F are respectively subsets of V and E.


## T

*topology* - the set of neighborhoods in a network.

* Example: Consider a graph G consisting of just three cells A, B and C in a row joined by edges as follows:
```
        A -- B -- C
```
> The neighborhood of A is N(A)={A, B}, of B is N(B)={A, B, C} and of C is N(C)={B, C}.  The topology T(G) of this graph is {N(A), N(B), N(C)}. Expanding:
```
            T(G) = {{A, B}, {A, B, C}, {B, C}}
```

*tree* - a graph that is connected but contains no circuits.

* A tree may be rooted or unrooted.
* A rooted tree is a tree with a designated cell called the root.  The root is labelled 0 to indicate its depth.  The neighbors of the root a labelled 1 (again for their relative depth).  Proceeding recursively unlabelled neighbors of children of relative depth d are labelled with relative depth d+1. Given a cell of relative depth d, its neighbors in a rooted tree have depth d-1 or d+1.  Except for the root, each cell has exactly one lower depth neighbor (the parent of the cell).  Higher depth neighbors are called "children".  Childless cells are called "leaves".
* Trees are independent sets.




## V

*vertex* - the singular of *vertices*: one vertex, two or more vertices


*vertices* (singular: *vertex*) - the fundamental objects in a graph.

* Synonyms: points, cells, nodes. When we speak of a vertex or a collection of vertices, we usually are thinking of our structure as a graph.


*Von Neumann neighborhood* - a neighborhood consisting of a cell and the nearest cells to the south, east, north and west. (These four cells are the cell's orthogonal neighbors.)

* See also: Moore neighborhood


## W

*walk* - in a graph, a path is an alternating sequence of vertices and edges that both begins and ends with a vertex, and each edge between two consecutive vertices is incident to both vertices.

* From the definition, two consecutive vertices in a walk are neighbors.
* In a network, we can replace edges by arcs in the forward direction.  For example, if the nodes in our network are A, B and C and the available arcs are a=(A,B), b=(B,C) and c=(C,B), then (AaBbC) is a walk, but (AaBcC) is not a walk.
* The first node in a walk is the start or the beginning or the *source*.
* The last node in a walk is the end or the finish or the *sink* or (sometimes) the *target*.
* The source and the walk are collectively called the endpoints or the *terminals*.
* The length of a walk is the number of edges in the walk.
* See also: connected, path
