import itertools
import heapq
from queue import Empty, Full
import threading

class Node:
    # TODO: Use dataclass in python 3.7
    def __init__(self, value, priority, order):
        self.value = value
        self.priority = priority
        self.order = order
        self.is_deleted = False

    def delete(self):
        self.is_deleted = True
        self.value = None

    def __bool__(self):
        return not self.is_deleted

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.order < other.order
        return self.priority > other.priority


class PriorityQueue:
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self.count = 0
        self.heap = [] # Items organized in heap
        self.entry_finder = {} # Map of items to find if item already is in queue
        self.index = itertools.count() # Items indexer to keep sorting stable
        self.access = threading.Condition()

    def full(self):
        return self.maxsize > 0 and self.count >= self.maxsize

    def qsize(self):
        return self.count

    def empty(self):
        return self.count == 0

    def put(self, value, priority):
        with self.access:
            if value in self.entry_finder:
                orig_node = self._pop_node_by_value(value)
                priority += orig_node.priority
                self.count -= 1
            if self.full():
                raise Full
            node = Node(value, priority, next(self.index))
            self.entry_finder[value] = node
            heapq.heappush(self.heap, node)
            self.count += 1
            self.access.notify()

    def _pop_node_by_value(self, value):
        node = self.entry_finder.pop(value)
        node.delete()
        return node

    def get_nowait(self):
        while self.heap:
            node = heapq.heappop(self.heap)
            if node:
                del self.entry_finder[node.value]
                self.count -= 1
                return node.value
        raise Empty()

    def get_n_nowait(self, n):
        return [self.get_nowait() for i in range(n)]

    def get(self, block=True, timeout=None):
        return self.get_n(1, block, timeout)[0]

    def get_n(self, n, block=True, timeout=None):
        if block:
            with self.access:
                self.access.wait_for(lambda: self.qsize() >= n, timeout)
                return self.get_n_nowait(n)
        else:
            return self.get_n_nowait(n)
