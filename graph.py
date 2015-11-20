from sys import maxsize
from heap import *
from sets import *
from fibheap import *

class Graph:
    def __init__(self, vertices=[], edges=[]):
        self.vertices = vertices
        self.edges    = edges

class Vertex:
    def __init__(self, data):
        self.data = data
        self.key  = None
        self.pred = None

    def __lt__(self, x):
        return self.key < x.key

    def __eq__(self, x):
        return x == self.data

    def __hash__(self):
        return self.data.__hash__()

def vindex(G, obj):
    return G.vertices.index(obj)

def vertices_from_file(fname, vtype, obj_reader):
    return map(vtype, obj_reader(fname))

def opposite_edge(u, e):
    return difference(e, [u])[0]

def get_adjacents(G, u):
    adjs = []
    for edge in G.edges:
        if u in edge:
            adjs.append(opposite_edge(u, edge))

    return adjs

def setkey(v, k):
    v.key = k

def setpred(v, p):
    v.pred = p

def getkey(v):
    return v.key

def getpred(v):
    return v.pred

def print_vertex(v, fmt_data):
    print "key: {}".format(v.key)
    print "data: {}".format(fmt_data(v.data))

    if v.pred != None:
        print "pred: {}".format(fmt_data(v.pred.data))

def add_vertex(G, v):
    G.vertices.append(v)

def add_vertices(G, V):
    for v in V:
        add_vertex(G, v)

def add_edge(G, e):
    G.edges.append(e)

def add_edges(G, E):
    for e in E:
        add_edge(G, e)

def graph_weight(G, w):
    return reduce(lambda x,y: x + y, map(lambda e: w(e[0].data, e[1].data), G.edges))

def prims(G, r, w):
    V = list(G.vertices)
    newV = []
    
    for v in V:
        setkey(v, maxsize)
        setpred(v, None)

    setkey(V[r], 0)
    Q = list(V)
    min_heapify(Q)

    while len(Q) > 0:
        u = extract_min(Q)

        for v in get_adjacents(G, u):
            if v in Q and w(u.data, v.data) < getkey(v):
                setpred(v, u)
                setkey(v, w(u.data, v.data))

        newV.append(u)
        min_heapify(Q)

    return newV

def fib_heap_prims(G, r, w):
    Q = list(G.vertices)
    newV = []
    
    for v in Q:
        setkey(v, maxsize)
        setpred(v, None)

    setkey(Q[r], 0)

    H = make_fib_heap()
    for node in Q:
        fib_heap_insert(H, node)

    while H.n > 0:
        u = fib_heap_extract_min(H)
        Q.remove(u)

        for v in get_adjacents(G, u):
            if v in Q and w(u.data, v.data) < getkey(v):
                v.pred = u
                fib_heap_decrease_key(H, v, w(u.data, v.data))

        newV.append(u)

    return newV

def mst_graph(mstfunc, orig_graph, startpos, w):
    mst_nodes = mstfunc(orig_graph, startpos, w)
    mst_edges = [[v.pred, v] for v in mst_nodes if v.pred != None]

    return Graph(mst_nodes, mst_edges)

def adjacency_list(G):
    res = {}

    for v in G.vertices:
        res[v] = get_adjacents(G, v)

    return res

def print_adjacency_list(adjlist, fmt_item):
    prn_func = lambda x: fmt_item(x.data)
    
    for k,v in adjlist.items():
        print "{:<15}: {}".format(prn_func(k), map(prn_func, v))
        
def dot_format(G, fmt_data, labelfn):
    res = []
    res.append("digraph electricity_graph {")
    res.append("\tgraph [ dpi = 500 ];")
    res.append("\tconcentrate=true")
    res.append("\tsize=\"8,5\"")
    res.append("\tnode [shape = circle];")

    for e in G.edges:
        u, v = e[0].data, e[1].data
        res.append("\t{} -> {} [ label = \"{}\", dir = both ];".format(fmt_data(u), fmt_data(v), labelfn(u, v)))

    res.append("}")

    return "\n".join(res)

def edges_from_file(fname, objreader, getvertex):
    edges = []
    for edge in objreader(fname):
        edges.append(map(getvertex, edge))

    return edges
    
def make_vertex_lookup(vertices, attr):
    V = list(vertices)

    def lookup(val):
        for v in V:
            if getattr(v.data, attr) == val:
                return v

    return lookup
