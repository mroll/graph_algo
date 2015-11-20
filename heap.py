def min_heapify(heap):
    for i in reversed(range(len(heap)//2)):
        _siftup(heap, i)
        
def _siftup(heap, i):
    item = heap[i]
    childpos = 2*i + 1
    startpos = i
    endpos = len(heap)

    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and heap[rightpos] < heap[childpos]:
            childpos = rightpos
        heap[i] = heap[childpos]
        i = childpos
        childpos = 2*i + 1

    heap[i] = item
    _siftdown(heap, startpos, i)

def _siftdown(heap, startpos, pos):
    item = heap[pos]
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if item < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = item

def extract_min(heap):
    enditem = heap.pop()
    if heap:
        res = heap[0]
        heap[0] = enditem
        _siftup(heap, 0)
    else:
        res = enditem

    return res
