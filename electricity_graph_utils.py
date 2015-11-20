import math
import csv
import hashlib
from heap import *
from graph import *
from fibheap import *

def read_csv(f):
    res = []
    with open(f, 'r') as csvfile:
        rd = csv.reader(csvfile)
        for row in rd:
            res.append(row)

    return res

# rename some functions
sin   = math.sin
cos   = math.cos
atan2 = math.atan2
sqrt  = math.sqrt

class City:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat  = lat
        self.lon  = lon

    def __eq__(self, other):
        if other == None:
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        latstring, lonstring = "".join(map(str, self.lat)), "".join(map(str, self.lon))
        return int("0x" + hashlib.sha1(self.name + latstring + lonstring).hexdigest(), 0)

def fmt_city(city):
    return city.name

def make_hash_to_city(cities):
    lookup = cities

    def hash_to_city(h):
        for city in lookup:
            if city.__hash__() == h:
                return city

    return hash_to_city

def degrees(gc):   return gc[0]
def minutes(gc):   return gc[1]
def seconds(gc):   return gc[2]
def direction(gc): return gc[3]

def geo_coordinate(degrees, minutes, seconds, direction):
    return [degrees, minutes, seconds, direction]

def degrees_decimal(gc):
    return degrees(gc) + (minutes(gc) / 60.0) + (seconds(gc) / 3600.0)

def radians_decimal(gc):
    return math.radians(degrees_decimal(gc))

def has_direction(gc, d): return direction(gc) == d

def westp(gc):  return has_direction(gc, 'W')
def southp(gc): return has_direction(gc, 'S')

def distance(city_a, city_b):
    R = 3961.0
    lat1, lat2 = map(radians_decimal, [city_a.lat, city_b.lat])
    lon1, lon2 = map(radians_decimal, [city_a.lon, city_b.lon])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2( sqrt(a), sqrt(1-a) )

    return round(R * c, 3)

def make_city(r):
    name = r[0]
    lat  = map(float, r[1:4]) + [r[4]]
    lon  = map(float, r[5:8]) + [r[8]]

    return City(name, lat, lon)

def get_city(name, cities):
    for c in cities:
        if c.name == name:
            return c

    return None

def rmspaces(s):
    return filter(lambda l: l != ' ', s)

def rmspchars(s):
    return ''.join(l for l in s if l.isalnum())

def lprint(l):
    for x in l:
        print x

def entry_from_cities(c1, c2):
    return [c1.name, c2.name, round(distance(c1, c2), 3)]

def nodefn(u, v):
    city1, city2 = u, v
    def make_entry():
        return entry_from_cities(city1, city2)

    return make_entry

# this needs to return of the form [V, E]
def compile_graph(pairs):
    graph = []
    for p in pairs:
        graph.append(nodefn(*p))

    return graph

def format_for_dot(adj_list):
    res = []
    res.append("digraph electricity_graph {")
    res.append("\tgraph [ dpi = 500 ];")
    res.append("\tconcentrate=true")
    res.append("\tsize=\"8,5\"")
    res.append("\tnode [shape = circle];")

    def format_path(n1, n2):
        return "\t{} -> {} [ label = \"{}\", dir=both ];".format(*entry_from_cities(n1.data, n2.data))
        # return "\t{} -> {} [ dir=both ];".format(*entry_from_cities(n1, n2)[:-1])
    
    for k,v in adj_list.items():
        map(lambda c: res.append(format_path(k, c)), v)

    res.append("}")

    return "\n".join(res)

def sortrows(rows):
    return sorted(map(sorted, rows))

def rmdups(sortedrows):
    uniqs = []
    uniqs.append(sortedrows[0])
    for i in range(1, len(sortedrows)):
        if sortedrows[i] != uniqs[-1]:
            uniqs.append(sortedrows[i])


    return uniqs

def city_fmtr(unfmtd_city_row):
    newrow = map(rmspaces, unfmtd_city_row)
    newrow[0] = rmspchars(newrow[0])

    return newrow

def format_list(formatter, rows):
    return map(formatter, rows)

def make_cities(city_rows):
    return map(make_city, city_rows)

def cities_from_file(fname):
    return make_cities(format_list(city_fmtr, read_csv(fname)))

def wire_fmtr(unfmtd_wire_row):
    return map(rmspchars, map(rmspaces, unfmtd_wire_row))

def wires_from_file(fname):
    return rmdups(sortrows(format_list(wire_fmtr, read_csv(fname))))

def empty(l):
    return len(l) == 0

def fib_city_graph_from_file(vfile="electric_cites.txt", efile="electric_wires.txt"):
    city_vertices = vertices_from_file(vfile, FibNode, cities_from_file)
    vertex_from_cityname = make_vertex_lookup(city_vertices, "name")

    city_edges = edges_from_file(efile, wires_from_file, vertex_from_cityname)

    return Graph(city_vertices, city_edges)

def city_graph_from_file(vertex_file="electric_cites.txt", edge_file="electric_wires.txt"):
    city_vertices = vertices_from_file(vertex_file, Vertex, cities_from_file)
    vertex_from_cityname = make_vertex_lookup(city_vertices, "name")

    city_edges = edges_from_file(edge_file, wires_from_file, vertex_from_cityname)

    return Graph(city_vertices, city_edges)

