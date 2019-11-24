import time

from priority_queue.pqueue import PriorityQueue
from queue import Full
from .conftest import thread_put


def test_put_no_delay():
    q = PriorityQueue()
    e = []
    t = thread_put(e, q, 'A', 1)
    t.start()
    t.join()
    assert not e
    assert q.get() == 'A'


def test_put_delay_full_delay(timer):
    q = PriorityQueue(1)
    q.put('A', 2)
    e = []
    t = thread_put(e, q, 'B', 1, timeout=0.3)
    with timer as m:
        t.start()
        time.sleep(0.1)
        assert q.qsize() == 1
        assert q.get() == 'A'
        t.join()
    assert not e
    assert q.get() == 'B'
    assert m.interval < 0.3


def test_multiple_put():
    q = PriorityQueue()
    e = []
    t1 = thread_put(e, q, 'A', 2)
    t2 = thread_put(e, q, 'B', 1)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert not e
    assert q.get() == 'A'
    assert q.get() == 'B'


def test_put_to_full_timeout():
    q = PriorityQueue(1)
    q.put('A', 2)
    e = []
    t = thread_put(e, q, 'B', 1)
    t.start()
    t.join()
    assert q.get() == 'A'
    assert isinstance(e[0], Full)
