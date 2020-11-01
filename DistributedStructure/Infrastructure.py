import pprint
import random
from collections import defaultdict

from DistributedStructure.WindTurbine import WindTurbine
from DistributedStructure.SolarCell import SolarCell

# Constants
WIND_TURBINES = 3
SOLAR_CELLS = 4
CONSUMERS = 10
WING_SIZE = [20, 80]


class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections):
        self._graph = defaultdict(set)
        self.add_connections(connections)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.items():  # python3: items(); python2: iteritems()
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None


wind_turbines = [WindTurbine(i, random.randint(*WING_SIZE)) for i in range(WIND_TURBINES)]
solar_cells = [SolarCell(i) for i in range(SOLAR_CELLS)]

connections = [(wind_turbines[0], wind_turbines[1]), (wind_turbines[1], wind_turbines[2]),
               (wind_turbines[1], solar_cells[0]), (solar_cells[0], solar_cells[1]),
               (solar_cells[1], solar_cells[2]), (solar_cells[2], solar_cells[3]), ('B', 'C')]
g = Graph(connections)
pretty_print = pprint.PrettyPrinter()
pretty_print.pprint(g._graph)