from electricity_graph_utils import *
import sys

def with_regular_heap():
    city_graph = city_graph_from_file(vertex_file="electric_cities.txt", edge_file="electric_wires.txt")

    vertex_from_cityname = make_vertex_lookup(city_graph.vertices, "name")

    r = vindex(city_graph, vertex_from_cityname("Minneapolis"))
    mst = mst_graph(prims, city_graph, r, distance)

    print graph_weight(mst, distance)
    print dot_format(mst, fmt_city, distance)

def with_fib_heap():
    city_graph = fib_city_graph_from_file("electric_cities.txt")

    vertex_from_cityname = make_vertex_lookup(city_graph.vertices, "name")

    r = vindex(city_graph, vertex_from_cityname("Seattle"))
    mst = mst_graph(fib_heap_prims, city_graph, r, distance)

    print graph_weight(mst, distance)
    print dot_format(mst, fmt_city, distance)

if len(sys.argv) < 2:
    print "usage: python prob2.py [ reg | fib ]"
    sys.exit()

if sys.argv[1] == "reg":
    with_regular_heap()
elif sys.argv[1] == "fib":
    with_fib_heap()
