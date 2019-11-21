class EmptyError(Exception):
    pass


class Node:
    # TODO: Use dataclass in python 3.7
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority


class PriorityQueue:
    def __init__(self):
        self.data = [] # TODO: Optimize by using heap

    def put(self, value, priority):
        node = self._find_value_in_data(value)
        if node:
            node.priority += priority
        else:
            node = Node(value, priority)
            self.data.append(node)
        self.data.sort(key=lambda n: n.priority, reverse=True)

    def get(self):
        try:
            return self.data.pop(0).value
        except IndexError:
            raise EmptyError()

    def _find_value_in_data(self, value):
        for n in self.data:
            if n.value == value:
                return n
