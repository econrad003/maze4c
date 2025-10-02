"""
mazes.tests.tournament - test the simple task handler module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    We use pair of dice combinations to test the tournament module.

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

from mazes.tournament import Tournament

handler = Tournament()
generator = iter(handler)
    # a couple of simple tests
assert next(generator) == None
handler[2] = 1
assert next(generator) == 2

handler[2] = handler[12] = 1
handler[3] = handler[11] = 2
handler[4] = handler[10] = 3
handler[5] = handler[9] = 4
handler[6] = handler[8] = 5
handler[7] = 6

    # first big test - 1000 dice rolls
results = {}
expected = {}
for i in range(2, 13):
    results[i] = 0
    expected[i] = round(1000 * handler[i]/36, 1)
for _ in range(1000):
    i = next(generator)
    results[i] += 1
print("Results of first 1000 rolls")
print("%15s  %10s  %10s" % ("Sum", "Rolls", "Expected"))
total = 0
for i in range(2, 13):
    total += results[i]
    print("%15s  %10d  %10.1f" % (i, results[i], expected[i]))
print("%15s  %10d" % ("TOTAL", total))

print()
handler[2] = handler[12] = None
handler[4] = handler[10] = 2
handler[6] = handler[8] = 4
handler["double"] = 6
results = {}
expected = {}
rolls = [3, 4, 5, 6, 7, 8, 9, 10, 11, "double"]
for i in rolls:
    results[i] = 0
    expected[i] = round(1000 * handler[i]/36, 1)
for _ in range(1000):
    i = next(generator)
    results[i] += 1
print("Results of next 1000 rolls")
print("%15s  %10s  %10s" % ("Sum", "Rolls", "Expected"))
total = 0
for i in rolls:
    total += results[i]
    print("%15s  %10d  %10.1f" % (i, results[i], expected[i]))
print("%15s  %10d" % ("TOTAL", total))

roll = next(generator)
n = len(rolls)
while n > 0:
    print(f"{n} deleting task: {roll}")
    del handler[roll]
    n -= 1
    roll = next(generator)
print(f"{n} last result: {roll}")
assert roll == None
assert next(generator) == None

