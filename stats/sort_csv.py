"""
stats.sort_csv - sort a csv by column keeping rows grouped
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
import csv

def group_csv(filename, header_rows, group_rows) -> dict:
    """returns a dictionary that shows the grouping

    ARGUMENTS

        filename - the filename for the CSV.
        header_rows - the number of rows in the header.  If there are no
            headers, enter 0.
        group_rows - the number of rows in each group other than the
            header.  For example, if each group conists of a row of mean
            values followed by a row of standard deviations, then the
            value of group_rows is 2.

    RETURNS

        a dictionary g that shows the grouping:
            g[-2] = [header1, header2, ...]
                a list consisting of the headers, one header for each row in
                the header group
            g[-1] = n
                the number of detail groups
            g[0] = [detail0_0, detail0_1, ...]
            g[1] = [detail0_1, detail1_1, ...]
            ...
            g[n-1] = [detailn-1_0, detail0_1, ...]
                lists of detail groups; each list consisting of one entry for
                each row in the group 
    """
    g = dict()
    rows = list()
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)
    g[-2] = rows[:header_rows]
    m = header_rows
    n = 0
    while m < len(rows):
        g[n] = rows[m:m+group_rows]
        n += 1
        m += group_rows
    g[-1] = n
    return g

    # test for "group_csv" method
#filename = "csv/2025-10-07.csv"
#g = group_csv(filename, 1, 2)
#print(g[-2][0])
#print(g[0][0])
#print(g[0][1])
#print(g[-1], "...")
#n = g[-1]
#print(g[n-1][0])
#print(g[n-1][1])

def extract_columns(g, *rowcols) -> list:
    """extract columns for sorting

    ARGUMENTS

        g - the dictionary returned by group_csv

        rowcols - one or more row/column pairs where the row indicates the
            0-based row in a group and the 0-based column in that row

    RETURNS:

        A list of little lists
            the little lists contain the requested data and (last) the
            group number

    EXAMPLE

        Suppose our data has no headers and appears in a spreadsheet
        as follows:

                (A)     (B)     (C)
            1A   55      77     foo
            1B   66      88     bar
            2A   99     111     foobar
            2B  222     333     baz

        The row labels here indicate that the groups consist of 2 rows.
        So our "g" dictionary looks like this:

            g[-2]   []
            g[-1]   2
            g[0]    [[55, 77, foo], [66, 88, bar]]
            g[1]    [[99, 111, foobar], [222, 333, baz]]

        To select column 0 from row 1 and column 2 from row 0, our
        call is:

            result = extract_columns(g, 1, 0, 0, 2)

        The value of result is:

            [[66, foo, 0], [222, foobar, 0]]

        If, instead, we had mixed up the row/column order and entered:

            result = extract_columns(g, 0, 1, 2, 0)

        then an IndexError exception would be raised as g[0][2][0]
        does not exist.
    """
    n = g[-1]
    result = list()
    assert len(rowcols) >= 2
    assert len(rowcols)%2 == 0
    rowcols = tuple(zip(rowcols[::2], rowcols[1::2], strict=True))
    m = len(rowcols)
    for i in range(n):
        selection = list()
        for j in range(m):
            y = rowcols[j][0]
            x = rowcols[j][1]
            selection.append(g[i][y][x])
        selection.append(i)
        result.append(selection)
    return result

    # test for "extract_columns" method
#filename = "csv/2025-10-07.csv"
#g = group_csv(filename, 1, 2)
#result = extract_columns(g, 0, 0, 0, 2, 1, 2)
#print(len(result), "expect", 23)
#print(result[0])
#print("expect:", "Aldous/Broder", 207.8, 6.854, 0)
#print(result[22])
#print("expect:", "Wilson", 208.44, 7.250, 22)

def sort_selection(selections, *types, ascending=True):
    """sort the selection list in the indicated order

    The selection list returned from extract_columns.  It is a list of
    lists.

    Returns a list of group numbers.  These are just the last entries of
    each of the lists after the list of lists has been sorted.
    """
    assert len(types)+1 == len(selections[0])
    unsorted = list()
    for row in selections:
        new_row = list()
        for i in range(len(types)):
            new_row.append(types[i](row[i]))
        new_row.append(row[-1])
        unsorted.append(new_row)
    sorted_list = sorted(unsorted, reverse=not ascending)
    return list(s[-1] for s in sorted_list)

    # test for "sort_selection" method
# filename = "csv/2025-10-07.csv"
# g = group_csv(filename, 1, 2)
# result = extract_columns(g, 0, 2)       # dead ends
# result = extract_columns(g, 0, 5)       # degree-4 cells
# result = extract_columns(g, 0, 10)      # diameter
# result = sort_selection(result, float, ascending=False)
# for i in result:
#    print(g[i][0][0], g[i][0][2], g[i][1][2])  # dead end
#    print(g[i][0][0], g[i][0][5], g[i][1][5])  # degree 4
#    print(g[i][0][0], g[i][0][10], g[i][1][10]) # diameter

# end module stats.sort_csv
