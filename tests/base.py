import pytest

from priority_queue.pqueue import PriorityQueue
from queue import Empty, Full


def test_get_empty():
    q = PriorityQueue()
    with pytest.raises(Empty):
        q.get(False)


def test_get_empty_nowait():
    q = PriorityQueue()
    with pytest.raises(Empty):
        q.get_nowait()


def test_put_get_one_item():
    q = PriorityQueue()
    q.put('A', 0)
    assert q.get_nowait() == 'A'


def test_get_removes_item():
    q = PriorityQueue()
    q.put('A', 0)
    q.get_nowait()
    with pytest.raises(Empty):
        q.get_nowait()


def test_get_reflects_priority():
    q = PriorityQueue()
    q.put('A', 0)
    q.put('B', 1)
    assert q.get_nowait() == 'B'
    assert q.get_nowait() == 'A'


def test_get_stable_ordering():
    q = PriorityQueue()
    q.put('A', 0)
    q.put('B', 0)
    assert q.get_nowait() == 'A'
    assert q.get_nowait() == 'B'


def test_sums_priorities_and_doesnt_add():
    q = PriorityQueue()
    q.put('A', 5)
    q.put('A', 0)
    assert q.get_nowait() == 'A'
    with pytest.raises(Empty):
        q.get_nowait()


def test_sums_priorities():
    q = PriorityQueue()
    q.put('A', 1)
    q.put('B', 2)
    q.put('A', 2)
    assert q.get_nowait() == 'A'


def test_sums_negative_priorities():
    q = PriorityQueue()
    q.put('A', 3)
    q.put('B', 2)
    q.put('A', -2)
    assert q.get_nowait() == 'B'


def test_qsize():
    q = PriorityQueue()
    assert q.qsize() == 0
    q.put('A', 1)
    assert q.qsize() == 1
    q.put('B', 1)
    assert q.qsize() == 2
    q.get_nowait()
    assert q.qsize() == 1


def test_qsize_reflects_merging():
    q = PriorityQueue()
    q.put('A', 1)
    q.put('A', 1)
    assert q.qsize() == 1


def test_empty():
    q = PriorityQueue()
    assert q.empty()
    q.put('A', 1)
    assert not q.empty()


def test_get_empty_raises_exception():
    q = PriorityQueue()
    with pytest.raises(Empty):
        q.get_nowait()


def test_zero_capacity_is_unlimited():
    q = PriorityQueue(0)
    q.put('A', 1)
    q.put('B', 1)
    assert q.qsize() == 2


def test_put_full_raises_exception():
    q = PriorityQueue(1)
    q.put('A', 1)
    with pytest.raises(Full):
        q.put_nowait('B', 1)

def test_put_duplicate_to_full():
    q = PriorityQueue(1)
    q.put('A', 1)
    assert q.full()
    q.put('A', 1)
    assert q.full()
