"""
stats.compare - cellular automaton maze statistics
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This program compares statistics for some maze algorithms that use
    cellular automata.  Wilson's algorithm is used as a baseline.

LICENSE
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from math import ceil, sqrt
from stats.sort_csv import extract_columns, sort_selection, group_csv
# from stats.side_by_side import group_csvs, smerge

date = "2025-12-03"
basename = date
filename = "csv/" + basename + ".csv"
header_rows = 1
group_rows = 2
rows, cols = 40, 40
n = 100

g = group_csv(filename, header_rows, group_rows)
# result = extract_columns(g, 0, 1)       # generations
# result = sort_selection(result, float, ascending=False)
# print(g[-2])
# for i in result:
#   print(g[i][0][0], g[i][0][1], g[i][1][1])  # generations


def writeln(fp, line=""):
    """write a line"""
    fp.write(line + "\n")
    print(line)

def header(fp):
    """write the header"""
    writeln(fp, f"# Interpretation of spanning binary tree results from {date}")
    writeln(fp)

def contents(fp):
    """table of contents"""
    writeln(fp, "## Table of contents")
    writeln(fp)
    writeln(fp, "* Introduction")
    writeln(fp)
    writeln(fp, "* 1. Isolated cells")
    writeln(fp, "* 2. Dead ends")
    writeln(fp, "* 3. Degree-2 cells")
    writeln(fp, "* 3a. Horizontal or E/W passages")
    writeln(fp, "* 3b. Vertical or N/S passages")
    writeln(fp, "* 3c. 90° turns")
    writeln(fp, "* 4. Degree-3 cells")
    writeln(fp, "* 5. Degree-4 cells")
    writeln(fp, "* 6. Diameter")
    writeln(fp)
    writeln(fp, "* Appendix A. Efficiency (time)")
    writeln(fp, "* Appendix B. Euler analysis")
    writeln(fp)

def introduction(fp):
    """introduction to the experiment"""
    writeln(fp, "## Introduction")
    writeln(fp)
    writeln(fp, "The data discussed here were from maze carving runs of a" \
            + " number of algorithms.  With four baseline exceptions, the" \
            + " algorithms are all designed to create spanning binary trees." \
            f"  Each algorithm was run {n} times to carve {rows}×{cols}" \
            + " rectangular mazes on Von Neumann rectangular grids.")
    writeln(fp)
    writeln(fp, "The baseline algorithms were DFS, BFS, Aldous/Broder and" \
            + " Wilson.  Mazes produced by DFS are \"almost\" binary, with" \
            + " a tendency to produce very few degree 4 nodes.")
    writeln(fp)
    writeln(fp, "The spanning binary tree algorithms were the simple binary" \
            + " tree algorithm, the greedy binary growing tree algorithm," \
            + " and the fair binary growing tree algorithm, denoted SBT," \
            + " GBT, and FBT, respectively.  Their implementations are:")
    writeln(fp)
    writeln(fp, "* **SBT** - module *mazes.Algorithms.simple\\_binary\\_tree*," \
            + " class *BinaryTree*")
    writeln(fp, "* **GBT** - module *mazes.Algorithms.binary\\_growing\\_tree1*," \
            + " class *BinaryGrowingTree*")
    writeln(fp, "* **FBT** - module *mazes.Algorithms.binary\\_growing\\_tree2*," \
            + " class *BinaryGrowingTree*")
    writeln(fp)
    writeln(fp, "SBT was run with biases of 25%, 50% (fair coin), and 75%.")
    writeln(fp)
    writeln(fp, "The two binary growing tree algorithms were run in various" \
            + " configurations using stacks (DFS), queues (BFS), split" \
            + " stacks (SS), split queues (SQ), random queues (RQ), and" \
            + " cached priority queues (PQ).")
    writeln(fp)
    writeln(fp, "The binary growing tree algorithms can, in some instances, " \
            + "produce spanning forests which contain isolated vertices." \
            + "  A preliminary test run did not produce any such forests." \
            + "  The run here produced exactly one such configuration.  For" \
            + " more information, see the sections on isolated cells and" \
            + " diameters.")
    writeln(fp)
    writeln(fp, "```")
    writeln(fp, "    1 runs terminated without a spanning tree.")
    writeln(fp, "    For these runs, the diameter was taken to be the number of cells.")
    writeln(fp, "    These runs will have at least one isolated vertex.")
    writeln(fp, "```")
    writeln(fp)

def efficiency(fp):
    """time efficiency"""
    writeln(fp, "## Appendix A. Efficiency (time)")
    writeln(fp)
    writeln(fp, "With the exceptions of Aldous/Broder and Wilson's algorithms," \
            + " the time complexity of the algorithms is asymptotically linear" \
            + " in the number of grid edges.  For rectangular Von Neumann grids," \
            + " with at least five rows and five columns the number of grid edges" \
            + " is between 3 and 4 times the number of cells.  The asymptotic" \
            + " time complexity is roughly proportional to the number of cells.")
    writeln(fp)

def isolates(fp):
    """isolated cells or islands"""
    writeln(fp, "## 1. Isolated cells")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"An isolated cell (or isolate or island) is a cell" \
            " with no incident passages, or equivalently, a degree-0 cell." \
            "  A connected maze with more than 1 cell will never have any" \
            " isolated cells.")
    writeln(fp)
    writeln(fp, f"The binary growing tree algorithms can fail in this way." \
            "  But failures, though very rare, are not unexpected.")
    writeln(fp)
    c = 1
    result = sort_selection(extract_columns(g, 0, c), float, ascending=False)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("algorithm", "isolates", "stdev", "pct"))
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("-"*25, "-"*9, "-"*7, "-"*7))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        if z == 0:
            break
        pct = round(z * 100 / v)
        writeln(fp, "%-25s  %9.2f  %7.2f  %6s%%  " % (algorithm, z, error, pct))
    writeln(fp, "```")
    writeln(fp)

def dead_ends(fp):
    """dead end or degree-1 cells"""
    writeln(fp, "## 2. Dead ends.")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A dead end is a cell with exactly one incident" \
            " passages, or equivalently, a degree-1 cell." \
            "  Dead ends tend to be a matter of individual taste.  Some" \
            " algorithms (like DFS or hunt-and-kill) produce very few." \
            "   Some (like Vertex Prim) tend to produce relatively many." \
            "   Here are the results for the sampled algorithms.")
    writeln(fp)
    c = 2
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("algorithm", "dead ends", "stdev", "pct"))
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("-"*25, "-"*9, "-"*7, "-"*7))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f  %6s%%  " % (algorithm, z, error, pct) \
                + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def degree2(fp):
    """degree-2 cells"""
    writeln(fp, "## 3. Degree-2 cells.")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A degree-2 cell is incident to two passages -- it is" \
            " linked by passages to two of its neighbors.  Degree-2 cells," \
            " in one sense, reflect an absence of choice: if we enter via" \
            " one of the passages, then we must typically exit via the other.")
    writeln(fp)
    c = 3
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("algorithm", "degree 2", "stdev", "pct"))
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("-"*25, "-"*9, "-"*7, "-"*7))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f  %6d%%" % (algorithm, z, s, pct) + diagnosis)
    writeln(fp, "```")
    writeln(fp)
    writeln(fp, "With four directions, there are C(4,2)=6 ways of choosing two" \
            " directions.  One possibility is east and west.  A second possibility" \
            " is north and south.  There are four other combinations.  A degree-2" \
            " cell with passages east and west might be described as horizontal," \
            " while one with north and south passages might be called vertical." \
            "  The four remaining combinations are right-angled turns.")
    writeln(fp)
    writeln(fp, "### 3a. Horizontal or E/W passages")
    writeln(fp)
    c = 12
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("algorithm", "E/W", "stdev", "pct"))
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("-"*25, "-"*9, "-"*7, "-"*7))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f  %6d%%" % (algorithm, z, s, pct) + diagnosis)
    writeln(fp, "```")
    writeln(fp)
    writeln(fp, "### 3b. Vertical or N/S passages")
    writeln(fp)
    writeln(fp, f"With *m*={rows} rows and *n*={cols} columns, there are" \
            + f"*v*={v} cells.  Among these cells, *m*(*n*-2)={rows*(cols-2)}" \
            + f" cells have neighbors both east and west, and " \
            + f"(*m*-2)*n*={(rows-2)*cols} have neighbors both north and south." \
            + f"  An unbiased algorithm should have, on average, a ratio of about " \
            + f"{rows*(cols-2)/((rows-2)*cols):.3f} horizontal to vertical.")
    writeln(fp)
    c = 11
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s  %7s  %7s" \
            % ("algorithm", "NS", "stdev", "pct", "H/V"))
    writeln(fp, "%-25s  %9s  %7s  %7s  %7s" \
            % ("-"*25, "-"*9, "-"*7, "-"*7, "-"*7))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        horiz = float(g[i][0][c+1])
        ratio = float('inf') if z == 0 else horiz/z
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f  %6d%%  %7.2f"
                % (algorithm, z, s, pct, ratio) + diagnosis)
    writeln(fp, "```")
    writeln(fp)
    writeln(fp, "### 3c. 90° turns")
    writeln(fp)
    c = 13
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("algorithm", "turn", "stdev", "pct"))
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("-"*25, "-"*9, "-"*7, "-"*7))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f  %6d%%" % (algorithm, z, s, pct) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def degree3(fp):
    """degree-3 cells"""
    writeln(fp, "## 4. Degree-3 cells.")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A degree-3 cell is incident to three passages -- it is" \
            "linked by passages to three of its neighbors.  Given an " \
            "entrance, a degree-3 cell represents a choice of two " \
            "separate exits.")
    writeln(fp)
    c = 4
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s  %7s" % ("algorithm", "degree 3", "s", "pct"))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f  %6d%%" % (algorithm, z, s, pct) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def degree4(fp):
    """degree-4 cells"""
    writeln(fp, "## 5. Degree-4 cells.")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A degree-4 cell is incident to four passages -- it is" \
            "linked by a passage to each of its four neighbors.  Given an " \
            "entrance, a degree-4 cell represents a choice of three " \
            "separate exits.")
    writeln(fp)
    writeln(fp, f"Cells in binary trees have at most degree 3 (one parent," \
            + " two children).")
    writeln(fp)
    c = 5
    result = sort_selection(extract_columns(g, 0, c), float, ascending=False)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s %7s" % ("algorithm", "degree 4", "s", "pct"))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f  %6d%%" % (algorithm, z, s, pct) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def diameter(fp):
    """diameter-4 cells"""
    writeln(fp, "## 6. Diameter.")
    writeln(fp)
    writeln(fp, f"The diameter of a maze is the length of a longest path." \
            "  (The cells in a (simple) path must be unique.  Repeated" \
            " cells are permitted in a trail (no repeated passages), or a" \
            " walk, or a circuit (but only first and last) or a cycle (a" \
            " walk that starts and ends in the same place).  Terminology" \
            " does vary, so beware.)")
    writeln(fp)
    writeln(fp, "To avoid infinite distances, when isolated vertices are" \
            + " present, the number of cells is used in lieu of the diameter." \
            + "  Results in this instance may be skewed.")
    writeln(fp)
    c = 10
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-25s  %9s  %7s" % ("algorithm", "diameter", "s"))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-25s  %9.2f  %7.2f" % (algorithm, z, s) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def Euler_analysis(fp):
    """grid and maze characteristic"""
    writeln(fp, "## Appendix B. Euler analysis.")
    writeln(fp)
    v = rows * cols
    m, n = rows, cols
    n1b = 2*(m+n-4)
    n1c = (m-2)*(n-2)
    sum1 = 8 + 3*n1b + 4*n1c
    e1 = round(sum1/2)
    e2 = v-1
    sum2 = 2*e2
    writeln(fp)
    writeln(fp, f"The mazes in our samples all have *v*={v}={rows}•{cols} cells." \
            f"  For a perfect maze, we must have *e*=*v-1*={e2} edges." \
            f"  The sum of the degrees of the cells in any undirected maze is" \
            f" twice the number of passages: 2e={sum2}.")
    writeln(fp)
    writeln(fp, "  (This relationship" \
            " between the number of passages (or edges) and the sum of the" \
            " degrees of the cells (or vertices) is a lemma due to Leonhard" \
            " Euler (1807-1883) and published in 1736 in his analysis of the" \
            " Königsberg bridges problem posed by Christian Goldbach,)")
    writeln(fp)

def write_all(fp):
    """the booklet"""
    header(fp)
    contents(fp)
    introduction(fp)
    isolates(fp)
    dead_ends(fp)
    degree2(fp)
    degree3(fp)
    degree4(fp)
    diameter(fp)
    writeln(fp, "# APPENDICES")
    writeln(fp)
    efficiency(fp)
    Euler_analysis(fp)

def main():
    with open("interpretation.md", "w") as fp:
        write_all(fp)

def main1():
    with open("/dev/null", "w") as fp:
        write_all(fp)
    
main()

# END stats.compare
