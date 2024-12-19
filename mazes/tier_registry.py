"""
mazes.tier_registry - tools for managing components in Eller's algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The following class is defined:

        TierRegistry - used to identify components in Eller's algorithm

    In addition, the following exception is defined:

        ComponentError - raised to indicate a component numbering conflict

    This has been adapted especially for Eller's algorithm from class
    ComponentRegistry in module mazes.components

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 189-197, 250.

    [2] "Connectivity (graph theory)" in Wikipedia. 26 September 2024. Web.
        Accessed 10 December 2024.
            URL: https://en.wikipedia.org/wiki/Connectivity_(graph_theory)

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

class ComponentError(KeyError):
    """raised when there is a conflict with component numbering"""
    pass

class TierRegistry(object):
    """for managing components in a graph or maze or grid"""

    __slots__ = ("__components", "__component_for", "__next_component")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, next_component:int=0):
        """constructor"""
        self.__components = dict()          # int : set
        self.__component_for = dict()       # object : int
        if type(next_component) != int:
            raise TypeError("'next_component' must be an integer")
        self.__next_component = next_component

    def register(self, vertex, component:int=None) -> int:
        """assign a vertex to a component

        DESCRIPTION

            If the vertex is not in a component, then a new component (which
            contains the vertex) will be created.  If the vertex is already
            registered, no new component is created.

        ARGUMENTS

            vertex - the vertex being registered

            component - if this value is set, then the component is being
                registered from an earlier tier.  If the vertex has already
                been registered, a ComponentError exception will be raised.
                If this value is None (default), the behavior is as in
                ComponentRegistry.

        RETURNS

            the component number
        """
            # is the object already registered?
        if vertex in self.__component_for:
            if component == None:
                return self.__component_for[vertex]
            raise ComponentError("component numbering conflict")

            # is this being entered in the new tier?  (for Eller carve up)
        if component != None:
            if component in self.__components:
                self.__components[component].add(vertex)
            else:
                self.__components[component] = {vertex}
            self.__component_for[vertex] = component
            return component

            # is the next component # valid?
        if self.__next_component in self.__components:
            raise RuntimeError(f"component {self.__component} already exists")
        component = self.__next_component;
        self.__next_component += 1
            # register the component
        self.__components[component] = {vertex}
        self.__component_for[vertex] = component
        return component

    def component_for(self, vertex):
        """return the component number of an object

        KeyError is raised if the object is not registered.  (Use 'register'
        to avoid this exception.  Use this method to avoid the small amount
        of overhead associated with registering an aleady registered object.)
        """
        return self.__component_for[vertex]

    def merge(self, component1:int, component2:int):
        """merge two components

        returns the number of the merged component
        """
            # validate component 1
        if component1 not in self.__components:
            raise ValueError("'component1' is not a component")
        if component1 == component2:
            return component1               # nothing to do

            # validate component 2
        if component2 not in self.__components:
            raise ValueError("'component2' is not a component")

            # perform the merge
        if component1 < component2:
            return self.__merge(component1, component2)
        return self.__merge(component2, component1)

    def __merge(self, k1, k2):
        """the merger method (called by merge)"""
        # print("merge", k1, k2)
        for item in self.__components[k2]:
            self.__component_for[item] = k1
        # print(k1, self.__components[k1])
        # print(k2, self.__components[k2])
        self.__components[k1].update(self.__components[k2])
        del self.__components[k2]
        return k1

    def are_connected(self, obj1, obj2):
        """returns True if the objects are registered in the same component"""
        return self.register(obj1) == self.register(obj2)

    def __len__(self):
        """return the number of components in the registry"""
        return len(self.__components)

    @property
    def components(self) -> list:
        """return the registered components"""
        return list(self.__components.keys())

    def items_in(self, component) -> list:
        """return the registered items in the component"""
        return list(self.__components[component])

    @property
    def new_tier_state(self):
        """returns a TierRegistry object for the upcoming tier"""
        return TierRegistry(self.__next_component)

# end module mazes.tier_registry