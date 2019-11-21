import pytest

from priority_queue.queue import PriorityQueue, EmptyError


def test_get_empty():
    q = PriorityQueue()
    with pytest.raises(EmptyError):
        q.get()


def test_put_get_one_item():
    q = PriorityQueue()
    q.put(42, 0)
    assert q.get() == 42


def test_get_removes_item():
    q = PriorityQueue()
    q.put(42, 0)
    q.get()
    with pytest.raises(EmptyError):
        q.get()


def test_get_reflects_priority():
    q = PriorityQueue()
    q.put(42, 0)
    q.put(3.14 , 1)
    assert q.get() == 3.14
    assert q.get() == 42


def test_get_stable_ordering():
    q = PriorityQueue()
    q.put(42, 0)
    q.put(3.14 , 0)
    assert q.get() == 42
    assert q.get() == 3.14


def test_sums_priorities_and_doesnt_add():
    q = PriorityQueue()
    q.put(42, 5)
    q.put(42, 0)
    assert q.get() == 42
    with pytest.raises(EmptyError):
        q.get()


def test_sums_priorities():
    q = PriorityQueue()
    q.put(42, 1)
    q.put(3.14, 2)
    q.put(42, 2)
    assert q.get() == 42


def test_sums_negative_priorities():
    q = PriorityQueue()
    q.put(42, 3)
    q.put(3.14, 2)
    q.put(42, -2)
    assert q.get() == 3.14
