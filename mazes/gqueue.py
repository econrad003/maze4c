"""
mazes.gqueue - base class implementation for generalized queues
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is a virtual base class (GeneralizedQueue).

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

from math import sqrt

class JettisonError(Exception):
    """exception raised when jettison fails"""
    pass

class GeneralizedQueue(object):
    """A virtual base class for queuing structures"""

    NAME = "Generalized Queue (stub)"

    __slots__ = ('__stats', '__sum1', '__sumx', '__sumxx', '__maxlen')

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self):
        """constructor"""
        self.__stats = dict()
        self.__sum1 = 0                 # number of accesses
        self.__sumx = 0                 # sum of lengths
        self.__sumxx = 0                # sum of squares of lengths
        self.__maxlen = 0               # the maximum length

            # MANAGE STATISTICS

    def __len__(self):
        """returns the length (override this!)"""
        raise NotImplementedError

    @property
    def is_empty(self):
        """return True if the queue is empty"""
        return len(self) == 0

    def _increment(self, statistic:str, adjust:'Number'=1):
        """increments the specified statistic"""
        self.__stats[statistic] = self.__stats.get(statistic, 0) + adjust

    def _track(self):
        """track changes in queue length"""
        self.__sum1 += 1
        x = len(self)
        self.__sumx += x
        self.__sumxx += x * x
        self.__maxlen = max(x, self.__maxlen)

            # QUEUE OPERATIONS

    def enter(self, *args, **kwargs):
        """place a packet in the queue (with statistics)"""
        self._increment("enter")
        self._enter(*args, **kwargs)
        self._track()

    def _enter(self, *args, **kwargs):
        """place a packet in the queue (stub)"""
        pass

    def leave(self, *args, **kwargs) -> 'Packet':
        """remove and return a package from the queue"""
        self._increment("leave")
        packet = self._leave(*args, **kwargs)
        self._track()
        return packet

    def _leave(self, **kwargs) -> 'Packet':
        """remove and return a packet from the queue (stub)"""
        pass

    def top(self, **kwargs) -> 'Packet':
        """return but do not remove a packet from the queue (override)

        Not tracked!
        """
        raise NotImplementedError

    def jettison(self):
        """discard the most recent packet returned by top (stub)

        Track with pop()
        """
        raise JettisonError("queue modified since top() was called")

            # REPORT STATISTICS

    @property
    def samples(self):
        """the number of sample points (enters + leaves)"""
        return self.__sum1

    @property
    def mean(self):
        """average queue length"""
        n, sx = self.__sum1, self.__sumx
        if n < 1:
            return 0
        return sx / n

    @property
    def variance(self):
        """variance for queue length (uncorrected)"""
        n, sx, sxx = self.__sum1, self.__sumx, self.__sumxx
        if n < 2:
            return 0
        return (n*sxx - sx*sx) / (n*n)

    def stat(self, statistic):
        """return a statistic"""
        return self.__stats.get(statistic, 0)

    @property
    def sample_variance(self):
        """variance for queue length (Bessel's correction)"""
        n = self.__sum1
        if n < 2:
            return 0
        return self.variance * (n / (n-1))

    @property
    def maxlen(self):
        """maximum length"""
        return self.__maxlen

    def __str__(self):
        """queue statistics"""
        name = f"===== {self.NAME} ====="       # copy
        while len(name) < 37:
            name = " " + name + " "         # center
        s = f"{name}\n"
        s += "%30s  %5d\n" % ("entries", self.stat("enter"))
        s += "%30s  %5d\n" % ("exits", self.stat("leave"))
        s += "%30s  %5d\n" % ("samples", self.samples)
        s += "%30s  %10.4f\n" % ("mean length", self.mean)
        stddev = sqrt(self.sample_variance)
        s += "%30s  %10.4f\n" % ("sample standard deviation", stddev)
        s += "%30s  %5d" % ("maximum length", self.maxlen)
        return s

# end module mazes.gqueue