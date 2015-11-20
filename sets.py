"""
Basic set operations using lists.

    - union
    - difference
    - intersection
"""

def rmdups(lst):
    lst.sort()
    res = [lst[0]]

    for x in lst[1:]:
        if x != res[-1]:
            res.append(x)

    return res

def makeset(lst):
    return rmdups(lst)

def union(a, b):
    return makeset(a + b)

def difference(a, b):
    return [x for x in a if x not in b]

def intersection(a, b):
    return [x for x in a if x in b]
