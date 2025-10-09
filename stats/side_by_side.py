"""
stats.side_by_side - place two lists side-by-side
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
import argparse

from stats.sort_csv import group_csv, extract_columns

def smerge(*lists, ranked=True, debug=False):
    """smerge the two lists

    A warning is issued if the lengths are unequal, or if the individual
    entries in either are inconsistent.

    If the lists are ranked, the rank, starting with 1, is placed in
    the first column of each row of the output.
    """
    def validators(sample:list) -> "tuple(int, tuple)":
        """collect the validation information"""
        types = list()
        for entry in sample:
            types.append(type(entry))
        return len(sample), tuple(types)

    def verify(row, j, which, entry, m, types):
        """check the row"""
        if len(entry) != m:
            print(f"WARNING: the length of list {j}",
                  f"in row {row}",
                  f"is not equal to {m}")
            return
        for i in range(m):
            if type(entry[i]) != types[i]:
                print(f"WARNING: the type of datum {which}",
                      f"in row {row}, list {j}",
                      f"is not {types[i].__name__}")
                return
        # END verify - all tests passed

    p = len(lists)
    lengths = tuple(len(sample) for sample in lists)
    n = min(*lengths)
    nmax = max(*lengths)
    if n != nmax:
        print("WARNING: The list lengths differ...")
        print(f"         Only the first {n} entries will be smerged.")
            # Validation stats
    lengths = list()
    types = list()
    for i in range(p):
        sample = lists[i]
        m, classes = validators(sample[0])
        if debug:
            print(f"list i: {m=}, {classes=}")
        lengths.append(m)
        types.append(classes)
    lengths = tuple(lengths)
    types = tuple(types)

            # build the result
    result = list()
    for i in range(n):              # over the rows...
        entries = list()
        if ranked:
            entries.append(i+1)
        for j in range(p):              # over the entties
            entry = lists[j][i]
            m = lengths[j]
            classes = types[j]
            verify(i, j, p, entry, m, classes)
            entries = entries + entry
        result.append(entries)
    return result

# test1:
#list1 = [["A", 1, 1.1], ["B", 2, 2.2]]
#list2 = [["C", 3, 3.3], ["D", 4, 4.4]]
#print("ranked:")
#result = smerge(list1, list2, debug=True)
#print(result)
#print("unranked:")
#result = smerge(list1, list2, debug=True, ranked=False)
#print(result)

# test2: WARNING list length
#list1 = [["A", 1, 1.1], ["B", 2, 2.2]]
#list2 = [["C", 3, 3.3], ["D", 4, 4.4], ["E", 5, 5.5]]
#result = smerge(list1, list2, debug=True)
#print(result)
#result = smerge(list2, list1, debug=True)
#print(result)

# test2: WARNING entry length/type
#list1 = [["A", 1, 1.1], ["B", 2, 2.2], ["F", 6, 6.6, 666]]
#list2 = [["C", 3, 3.3], ["D", 4, "4.4"], ["E", 5, 5.5]]
#result = smerge(list1, list2, debug=True)
#print(result)

def group_csvs(header_rows, group_rows, *basenames):
    """group the csvs"""
    def pathname(basename):
        """create the pathname"""
        return "csv/" + basename + ".csv"

    gs = list()
    for basename in basenames:
        gs.append(group_csv(pathname(basename), header_rows, group_rows))
    return tuple(gs)

# end module stats.side_by_side
