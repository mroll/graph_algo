class FibHeap:
    def __init__(self, min=None):
        self.min = min
        self.n   = 0

class FibNode:
    def __init__(self, data, key=0):
        self.data = data
        self.key = key
        self.pred = None
        self.reset()

    def reset(self):
        self.deg = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

def make_fib_heap():
    return FibHeap()

def make_fib_node(key, data):
    return FibNode(data, key=key)

def dll_remove_node(x):
    x.right.left = x.left
    x.left.right = x.right

# Concat two doubly-linked lists
def dll_concat(x1, y1):
    x2, y2 = x1.left, y1.right

    x1.left = y1
    y1.right = x1

    x2.right = y2
    y2.left = x2

def dll_add(y, x):
    if y == None or x == None:
        return
    z = y
    while z.right != y:
        z.parent = x.parent
        z = z.right

    z.parent = x.parent
    y.left = x.left
    x.left.right = y
    z.right = x
    x.left = z

def fib_heap_insert(H, x):
    x.reset()
    if H.min == None:
        H.min = x
    else:
        w = H.min.left
        y = H.min
        x.left = w
        x.right = y
        w.right = x
        y.left = x
        if x.key < H.min.key:
            H.min = x
    H.n = H.n + 1

def fib_heap_union(H1, H2):
    H = make_fib_heap()
    H.min = H1.min

    dll_concat(H1.min, H2.min)

    if H1.min == None or ( H2.min != None and H2.min.key < H1.min.key):
        H.min = H2.min

    H.n = H1.n + H2.n
    return H


def D(n):
    lg = 0
    while n/2 > 0:
        lg = lg + 1
        n = n / 2

    return lg

def dll_insert(y, x):
    x.left.right = y
    y.left = x.left
    y.right = x
    x.left = y

def add_child(y, x):
    if x.child:
        dll_insert(y, x.child)
    else:
        x.child = y
        y.left = y
        y.right = y

    y.parent = x
    x.deg += 1

def fib_heap_link(y, x):
    dll_remove(y)
    add_child(y, x)
    y.mark = False

def dll_collect(x):
    if not x:
        return

    sibs = [x]
    it = x.right

    while it != x:
        sibs.append(it)
        it = it.right

    return sibs

def consolidate(H):
    A = [None] * H.n
    
    for x in dll_collect(H.min):
        d = x.deg
        while A[d] != None:
            y = A[d]
            if y.key < x.key:
                x,y = y,x
            fib_heap_link(y, x)
            A[d] = None
            d = d + 1
        A[d] = x

    H.min = None

    for x in A:
        if x:
            x.left = x
            x.right = x
            x.parent = None
            if H.min:
                dll_add(x, H.min)
                if x.key < H.min.key:
                    H.min = x
            else:
                H.min = x

def dll_remove(x):
    x.left.right = x.right
    x.right.left = x.left

def fib_heap_extract_min(H):
    x = H.min
    if x != None:
        if x.child != None:
            dll_add(x.child, x)

        dll_remove(x)

        if x == x.right:
            H.min = None
        else:
            H.min = x.right
            consolidate(H)

        H.n = H.n - 1
        x.reset()

    return x

def fib_heap_decrease_key(H, x, k):
    assert(k <= x.key)
    if k == x.key:
        return
    x.key = k
    y = x.parent
    if y != None and x.key < y.key:
        cut(H, x, y)
        cascading_cut(H, y)
    if x.key < H.min.key:
        H.min = x

def cut(H, x, y):
    dll_remove_node(x)

    y.deg -= 1
    y.child = x.right
    if x == x.right:
        y.child = None

    x.parent = None
    x.mark = False

    dll_insert(x, H.min)

def cascading_cut(H, y):
    z = y.parent

    if z:
        if not y.mark:
            y.mark = True
        else:
            cut(H, y, z)
            cascading_cut(H, z)

def print_rootlist(H):
    rl = [H.min]
    x = H.min.right
    
    while x != H.min:
        rl.append(x)
        x = x.right

    print map(lambda x: x.key, rl)

# H = make_fib_heap()
# 
# nodes = map(lambda i: make_fib_node(i, i), range(42))
# 
# for n in nodes:
#     fib_heap_insert(H, n)
# 
# while H.n > 0:
#     print fib_heap_extract_min(H).key
