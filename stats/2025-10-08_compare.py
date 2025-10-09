"""
stats.compare - compare the data from 7, 8 October 2025 side-by-side
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
from stats.sort_csv import extract_columns, sort_selection
from stats.side_by_side import group_csvs, smerge

basenames = ("2025-10-07", "2025-10-08")
header_rows = 1
group_rows = 2

def sort_by(gs, *rowcols, types=(float,), ascending=True):
    """returns a list of lists of indices into the gs"""
    lists = list()
    for g in gs:
        result = extract_columns(g, *rowcols)
        result = tuple(sort_selection(result, *types, ascending=ascending))
        lists.append(result)
    return tuple(lists)

def extract_data(gs, indices, *rowcols, types=(str, float, float)):
    """extract the requested data"""
    n = len(gs)
    rowcols = tuple(zip(rowcols[::2], rowcols[1::2], strict=2))
    assert len(rowcols) == len(types)
    assert len(indices) == n
    all_results = list()
    for i in range(n):
        g = gs[i]
        js = indices[i]
        results = list()
        for j in js:
            entry = g[j]
            data = list(entry[rc[0]][rc[1]] for rc in rowcols)
            result = list()
            for k in range(len(types)):
                datum = types[k](data[k])
                result.append(datum)
            results.append(result)
        all_results.append(results)
    return smerge(*all_results)

def output_section(name, gs, sortcol):
    """formats the data for a section"""
    print()
    print("## Results for", name)
    print()
    print("```")
    indices = sort_by(gs, 0, sortcol, ascending=False)
    results = extract_data(gs, indices, 0, 0, 0, sortcol, 1, sortcol)
    print("   %20s            %20s" % basenames)
    for result in results:
            # compress results and correct a typo
        if result[1][:13] == "Breadth-first":
            result[1] = "BF"+result[1][13:]
        elif result[1][:11] == "Depth-first":
            result[1] = "DF"+result[1][11:]
        elif result[1][:9] in {"MT Random", "MT Randon"}:
            result[1] = "MT Rand"+result[1][9:]
        if result[4][:13] == "Breadth-first":
            result[4] = "BF"+result[4][13:]
        elif result[4][:11] == "Depth-first":
            result[4] = "DF"+result[4][11:]
        elif result[4][:9] in {"MT Random", "MT Randon"}:
            result[4] = "MT Rand"+result[4][9:]
        fmt = "%2d %20s %5.1f±%4.1f %20s %5.1f±%4.1f"
        print(fmt % tuple(result))
    print("```")

print("# Comparison of statistics dated %s and %s" % basenames)
print()
print("Both runs consisted of producing 100 perfect mazes for each of 22 different" \
      + " maze carving algorithms.  The mazes were all configured with 21 rows and" \
      + " 34 columns in a Von Neumann grid (*OblongGrid(21,34)*).  The same Python" \
      + " was used to produce the CSVs from which this data was extracted.")
print()
print("For each of the statistics, please take special note of the ranks for" \
      + " Kruskal's and Prim's algorithms as both produce minimum weight spanning" \
      + " trees.  Note that 'Prim/Vertex' and 'Prim/Simplified' designate" \
      + " algorithms which are only superficially related to Prim's algorithm.")
print()
print("Also, please note the ranks of Aldous/Broder and Wilson's algorithm as" \
      + "these algorithms (ideally) produce uniform spanning trees, that is," \
      + "every possible spanning tree is (ideally) carved with equal probability." \
      + "  (I say \"ideally\" because the implementation uses a pseudorandom" \
      + " sequence, so the implementations are not truly random.)")
print()
print("When comparing the data for %s and %s" % basenames,
      "take note of the standard deviation that follows the plus-or-minus",
      "symbol.  *Assuming* the data is normally distributed, there is about",
      "a 2/3 chance that it lies within one standard deviation of the mean",
      "and about a 19/20 chance that it lies within two standard deviations. ",
      "Of course not all data is normally distributed, but Chebyshev's",
      "Inequality (*q.v.*) does set some bounds for other distributions.")
print()
print("To save horizontal space, names of some of the algorithms were",
      "abbreviated in the summaries below.  (One algorithm name was misspelled",
      "in the script that produced the CSVs.)  The means and standard deviations",
      "were displayed to the nearest thousandth.  Here they are rounded to the",
      "nearest tenth to save space.  They could reasonably be rounded to the",
      "nearest integer.")

gs = group_csvs(header_rows, group_rows, *basenames)
output_section("Dead Ends (Degree 1 Cells)", gs, 2)
output_section("Degree 2 Cells", gs, 3)
output_section("Degree 3 Cells", gs, 4)
output_section("Degree 4 Cells (Four-Way Intersections)", gs, 5)
output_section("Diameter (Longest Path Length)", gs, 10)

# end module stats.compare
