import itertools
import heapq

class EmptyError(Exception):
    pass


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
    def __init__(self):
        self.heap = [] # Items organized in heap
        self.entry_finder = {} # Map of items to find if item already is in queue
        self.counter = itertools.count() # Items counter to keep sorting stable

    def put(self, value, priority):
        if value in self.entry_finder:
            orig_node = self._pop_node_by_value(value)
            priority += orig_node.priority
        node = Node(value, priority, next(self.counter))
        self.entry_finder[value] = node
        heapq.heappush(self.heap, node)

    def _pop_node_by_value(self, value):
        node = self.entry_finder.pop(value)
        node.delete()
        return node

    def get(self):
        while self.heap:
            node = heapq.heappop(self.heap)
            if node:
                del self.entry_finder[node.value]
                return node.value
        raise EmptyError()
