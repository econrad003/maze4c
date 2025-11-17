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

date = "2025-11-16"
basename = date
filename = "csv/" + basename + ".csv"
header_rows = 1
group_rows = 2
rows = cols = 25
n = 50

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
    writeln(fp, f"# Interpretation of automata results from {date}")
    writeln(fp)

def contents(fp):
    """table of contents"""
    writeln(fp, "## Table of contents")
    writeln(fp)
    writeln(fp, "* 1. Generations (n)")
    writeln(fp, "* 2. The number (k) of components")
    writeln(fp, "* 3. The number (e) of passages")
    writeln(fp, "* 4. The size (|K|) of the largest component")
    writeln(fp, "* 5. The number of isolated cells")
    writeln(fp, "* 6. The number of dead ends")
    writeln(fp, "* 7. 90-degree turns")
    writeln(fp, "* 8. Straightaways")
    writeln(fp, "* 9. Degree-3 cells")
    writeln(fp, "* 10. Degree-4 cells")
    writeln(fp, "* 11. Cells by degree")
    writeln(fp)

def generations(fp):
    """generations"""
    writeln(fp, "## 1. Generations (n)")
    writeln(fp)
    result = sort_selection(extract_columns(g, 0, 1), float, ascending=False)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s" % ("algorithm", "n", "s"))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][1]), float(g[i][1][1])
        if algorithm == "Wilson":
            diagnosis = "passage carver (BASELINE)"
        elif z < n:
            stable = float(g[i][0][2]), float(g[i][1][2])
            crash = float(g[i][0][3]), float(g[i][1][3])
            stability = f"{round(stable[0]*100)}±{ceil(stable[1]*100)}"
            crashes = f"{round(crash[0]*100)}±{ceil(crash[1]*100)}"
            diagnosis = f"stable pct {stability}; crashes pct {crashes}"
        else:
            diagnosis = f"100% unstable after {n} generations"
        writeln(fp, "%-18s  %7.2f  %7.2f  " % (algorithm, z, error) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def components(fp):
    """generations"""
    writeln(fp, "## 2. The number (*k*) of components")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"The number of cells in a {rows}×{cols} maze is given by *{v=}*.")
    writeln(fp)
    c = 4
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s" % ("algorithm", "k", "s"))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        if algorithm == "Wilson":
            diagnosis = "baseline (perfect maze/spanning tree)"
        elif z == 0:
            diagnosis = "z = 0     no fragmenting"
        elif z < 0.025*v:
            diagnosis = "z < v/40  minimal fragmenting"
        elif z < 0.05*v:
            diagnosis = "z < v/20  modest fragmenting"
        elif z < 0.1*v:
            diagnosis = "z < v/10  moderate fragmenting"
        elif z < 0.25*v:
            diagnosis = "z < v/4   major fragmenting"
        elif z < 0.5*v:
            diagnosis = "z < v/2   severe fragmenting"
        else:
            diagnosis = "z ≥ v/2   massive fragmenting"
        writeln(fp, "%-18s  %7.2f  %7.2f  " % (algorithm, z, error) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def passages(fp):
    """passages"""
    writeln(fp, "## 3. The number ($e$) of passages")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"The number of cells in a {rows}×{cols}" \
            + f" maze is given by *{v=}*.  " \
            + "The number of components is denoted *k*." \
            + "  The Euler characteristic χ=*e-v+k is 0 for a tree or forest." \
            + "  The Euler characteristic is always non-negative.  When" \
            + " positive, it indicates the presence of circuits.")
    writeln(fp)
    c = 5
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s  %7s  %7s  %9s" \
        % ("algorithm", "e", "s", "k", "χ", "*(v-e)/k*"))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        k = float(g[i][0][c-1])
        chi = z - v + k         # Euler characteristic
        ratio = f"{(v-k)/z:.2f}" if z > 0 else float("inf")
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s  %7.2f  %7.2f  %7.2f  %7.2f  %7s" \
            % (algorithm, z, error, k, chi, ratio) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def largest(fp):
    """the largest component"""
    writeln(fp, "## 4. The size (|K|) of the largest component")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"If the largest component encompasses almost all the maze," \
            "then the fragments are not a major concern.  Ideally, the " \
            "largest component should encompass all of the maze, but our" \
            " cellular automata are prone to create fragments.  Our working" \
            " definition of \"nearly ideal\" includes the stipulation that " \
            "the largest fragment encompasses 3/4 of the maze.")
    writeln(fp)
    v = rows * cols
    c = 7
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s" % ("algorithm", "|K|", "s"))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round((v-z) * 100/v)
        if z >= v:
            diagnosis = "ideal"
        elif z >= 0.9 * v:
            diagnosis = "very nearly ideal"
        elif z >= 0.75 * v:
            diagnosis = "nearly ideal"
        elif z >= 0.6 * v:
            diagnosis = "fractured"
        elif z >= 0.45 * v:
            diagnosis = "badly fractured"
        else:
            diagnosis = "hopelessly fractured"
        diagnosis += f" {pct}%"
        if algorithm == "Wilson":
            diagnosis += "  (baseline)"
        writeln(fp, "%-18s  %7.2f  %7.2f  " % (algorithm, z, error) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def isolates(fp):
    """isolated cells or islands"""
    writeln(fp, "## 5. The number of isolated cells")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"An isolated cell (or isolate or island) is a cell" \
            " with no incident passages, or equivalently, a degree-0 cell." \
            "  Isolates aren't particularly desirable, but they aren't" \
            " harmful.  They can be thought of as places where no ink should" \
            " be used when sketching the maze.  A perfect maze carving algorithm" \
            " (like Wilson's algorithm) doesn't produce isolated cells.  They are" \
            " hard to avoid with cellular automata.")
    writeln(fp)
    c = 8
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s  %7s" % ("algorithm", "islands", "s", "pct"))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s  %7.2f  %7.2f  %6s%%  " % (algorithm, z, error, pct) \
                + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def dead_ends(fp):
    """dead end or degree-1 cells"""
    writeln(fp, "## 6. The number of dead ends")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A dead end is a cell with exactly one incident" \
            " passages, or equivalently, a degree-1 cell." \
            "  Dead ends tend to be a matter of individual taste.  Some" \
            " algorithms (like DFS or hunt-and-kill) produce very few." \
            "   Some (like Vertex Prim) tend to produce relatively many." \
            "   Here we see how our cellular automata fared.")
    writeln(fp)
    c = 9
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s%9s  %7s  %7s" % ("algorithm", "dead ends", "s", "pct"))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s  %7.2f  %7.2f  %6s%%  " % (algorithm, z, error, pct) \
                + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def turns(fp):
    """90 degree turns"""
    writeln(fp, "## 7. 90-degree turns")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"In a 4-connected rectangular maze, a degree-2 cell can take" \
            " one of six configurations.  Two of those involve going straight," \
            " *i.e*, horizontally from east to west (or *vice versa*) or " \
            "vertically.  The remaining four are 90-degree turns.  Along the" \
            " boundary walls, there is one way to go straight and two ways" \
            " to turn.  In the four corner cells, there is one turn and no" \
            " ways to go straight.")
    writeln(fp)
    c = 10
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s %8s %8s  %7s" \
        % ("algorithm", "turns", "s", "straight", "degree-2", "t/s"))
    for i in result:
        algorithm, z, error = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        v = float(g[i][0][c+1])
        h = float(g[i][0][c+2])
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s  %7.2f  %7.2f  %7.2f  %7.2f  %7.2f" \
             % (algorithm, z, error, h+v, z+h+v, z/(h+v)) \
                + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def straightaways(fp):
    """straightaway degree-2 cells"""
    writeln(fp, "## 8. Straightaways")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A degree-2 cell that doesn't turn must go straight.")
    writeln(fp)
    c = 11
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s %6s %4s %6s %4s %6s" \
        % ("algorithm", "N/S", "s", "E/W", "s", "V/H"))
    for i in result:
        algorithm, z1, s1 = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        z2, s2 = float(g[i][0][c+1]), float(g[i][1][c+1])
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s %6.2f±%4.2f %6.2f±%4.2f %6.2f" \
             % (algorithm, z1, s1, z2, s2, z1/z2) \
                + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def degree3(fp):
    """degree-3 cells"""
    writeln(fp, "## 9. Degree-3 cells")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A degree-3 cell is incident to three passages -- it is" \
            "linked by passages to three of its neighbors.")
    writeln(fp)
    c = 13
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s  %7s" % ("algorithm", "deg=3", "s", "pct"))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s  %7.2f  %7.2f  %6d%%" % (algorithm, z, s, pct) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def degree4(fp):
    """degree-4 cells"""
    writeln(fp, "## 10. Degree-4 cells")
    writeln(fp)
    v = rows * cols
    writeln(fp, f"A degree-4 cell is incident to four passages -- it is" \
            "linked by a passage to each of its four neighbors.")
    writeln(fp)
    c = 14
    result = sort_selection(extract_columns(g, 0, c), float, ascending=True)
    writeln(fp, "```")
    writeln(fp, "%-18s  %7s  %7s %7s" % ("algorithm", "deg=4", "s", "pct"))
    for i in result:
        algorithm, z, s = g[i][0][0], float(g[i][0][c]), float(g[i][1][c])
        pct = round(z * 100 / v)
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s  %7.2f  %7.2f  %6d%%" % (algorithm, z, s, pct) + diagnosis)
    writeln(fp, "```")
    writeln(fp)

def cells_by_degree(fp):
    """cells by degree cells"""
    writeln(fp, "## 11. Cells by degree")
    writeln(fp)
    v = rows * cols
    c = 7       # sort by largest component
    result = sort_selection(extract_columns(g, 0, c), float, ascending=False)
    writeln(fp, "```")
    writeln(fp, "%-18s %5s  %5s  %5s  %5s  %5s  %5s=100%%" \
        % ("algorithm", "0", "1", "2", "3", "4", "total"))
    for i in result:
        algorithm = g[i][0][0]
        z0 = round(float(g[i][0][8]) * 100 / v)
        z1 = round(float(g[i][0][9]) * 100 / v)
        t = float(g[i][0][10])
        vert = float(g[i][0][11])
        h = float(g[i][0][12])
        z2 = round((t + vert + h) * 100 / v)
        z3 = round(float(g[i][0][13]) * 100 / v)
        z4 = round(float(g[i][0][14]) * 100 / v)
        total = z0 + z1 + z2 + z3 + z4
        diagnosis = "  baseline" if algorithm == "Wilson" else ""
        writeln(fp, "%-18s %5d%% %5d%% %5d%% %5d%% %5d%% %5d%%" \
            % (algorithm, z0, z1, z2, z3, z4, total) + diagnosis)
    writeln(fp)
    writeln(fp, " "*30 + "Rounding affects some of the totals.")
    writeln(fp, "```")
    writeln(fp)

def main():
    with open("interpretation.md", "w") as fp:
        header(fp)
        contents(fp)
        generations(fp)
        components(fp)
        passages(fp)
        largest(fp)
        isolates(fp)
        dead_ends(fp)
        turns(fp)
        straightaways(fp)
        degree3(fp)
        degree4(fp)
        cells_by_degree(fp)

main()
# END stats.compare
