"""
stats.compare - sort the data from 9 October 2025
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

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
from stats.sort_csv import group_csv, extract_columns, sort_selection
#from stats.side_by_side import group_csvs, smerge

basename = "2025-10-09"
header_rows = 1
group_rows = 2

def sort_by(g, *rowcols, types=(float,), ascending=True):
    """returns a list of indices into the g"""
    result = extract_columns(g, *rowcols)
    return sort_selection(result, *types, ascending=ascending)

def extract_data(g, indices, *rowcols, types=(str, float, float)):
    """extract the requested data"""
    rowcols = tuple(zip(rowcols[::2], rowcols[1::2], strict=2))
    assert len(rowcols) == len(types)
    assert len(indices) == g[-1]
    results = list()
    rank = 1
    for j in indices:
        entry = g[j]
        data = list(entry[rc[0]][rc[1]] for rc in rowcols)
        result = list()
        result.append(rank)
        rank += 1
        for k in range(len(types)):
            datum = types[k](data[k])
            result.append(datum)
        results.append(result)
    return results

def output_section(name, g, sortcol):
    """formats the data for a section"""
    print()
    print("## Results for", name)
    print()
    print("```")
    indices = sort_by(g, 0, sortcol, ascending=False)
    results = extract_data(g, indices, 0, 0, 0, sortcol, 1, sortcol)
    print("   %30s     mean      std dev" % "algorithm")
    for result in results:
        fmt = "%2d %30s %10.3f ± %9.3f"
        print(fmt % tuple(result))
    print("```")

print("# Notes statistics dated %s" % basename)
print()
print("The runs consisted of producing 100 perfect mazes for each of 14 different",
      "maze carving algorithm and 3 fractal tesselation algorithms. ",
      "The mazes were all configured on a 16×16 Von Neumann grid",
      "(*OblongGrid(16,16)*)."),
print()
print("For fractal tessellation, four passes were made",
      "starting with a 1×1 trivial maze with each pass doubling the number",
      "of rows and columns.  The three algorithms involved simple placement",
      "(the trivial or identity group), placement after a random rotation",
      "(the rotation group), or placement after a random rotation or reflection",
      "(the dihedral group).  The main purpose here is to compare fractal",
      "tessellation with other algorithms")

filename = "csv/" + basename + ".csv"
g = group_csv(filename, header_rows, group_rows)
output_section("Dead Ends (Degree 1 Cells)", g, 2)
output_section("Degree 2 Cells (I-Junctions and Corners)", g, 3)
output_section("Degree 3 Cells (T-Junctions)", g, 4)
output_section("Degree 4 Cells (Plus-Junctions)", g, 5)
output_section("Diameter (Longest Path Length)", g, 10)

# end module stats.sort
