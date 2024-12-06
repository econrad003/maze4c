"""
mazes.tools.const - methods that return constant values
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Class Const creates objects that normally behave like constants.

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

class Const(object):
    """constant objects"""

    __slots__ = ("__value")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, value):
        """constructor"""
        self.__value = value

    def value(self, *args, **kwargs):
        """returns the value regardless of the input"""
        return self.__value

# end module mazes.tools.const