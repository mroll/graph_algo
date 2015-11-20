from electricity_graph_utils import *

city_graph = city_graph_from_file(vertex_file="electric_cities.txt", edge_file="electric_wires.txt")

print dot_format(city_graph, fmt_city, distance)
