import networkx as nx
import random

#from DistributedStructure.Consumer import Consumer, SelectRandomConsumerType, SelectRandomResourceType
from DistributedStructure.WindTurbine import WindTurbine
from DistributedStructure.SolarCell import SolarCell

# TODO: Create small graph representation with SimPy which outputs numbers
# TODO: Convert numbers to graphical representation
# TODO: Add more `clusters'

# Constants
WIND_TURBINES = 4
SOLAR_CELLS = 3
CONSUMERS = 7
WING_SIZE = [20, 80]

# Create consumers, solar_cells, and wind_turbines
wind_turbines = [WindTurbine(i, random.randint(*WING_SIZE)) for i in range(WIND_TURBINES)]
solar_cells = [SolarCell(i) for i in range(SOLAR_CELLS)]
consumers = [Consumer(i) for i in range(CONSUMERS)]

G = nx.Graph()

G.add_node(wind_turbines[0])
G.add_nodes_from([wind_turbines[1], wind_turbines[2]])

G.add_edges_from([(wind_turbines[0], wind_turbines[1]),
                 (wind_turbines[1], wind_turbines[2])])

print(list(G.nodes))
print(list(G.edges))
print(list(G.adj[wind_turbines[0]]))