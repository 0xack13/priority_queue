from priority_queue.pqueue import Node


def test_create_node():
    node = Node('A', 2, 3)
    assert node.value == 'A'
    assert node.priority == 2
    assert node.order == 3
    assert bool(node)


def test_delete_node():
    node = Node('A', 2, 3)
    node.delete()
    assert node.value is None
    assert not bool(node)


def test_sort_nodes_by_priority():
    node1 = Node('A', 0, 1)
    node2 = Node('B', 1, 2)
    assert node1 > node2


def test_stable_sort_of_nodes():
    node1 = Node('A', 1, 1)
    node2 = Node('B', 1, 2)
    assert node1 < node2
