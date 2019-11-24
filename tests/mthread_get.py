import time
from priority_queue.pqueue import PriorityQueue
from queue import Empty
from .conftest import thread_get


def test_get_blocking_result_from_nonempty():
    q = PriorityQueue()
    q.put('A', 1)
    r = []
    t = thread_get(r, q)
    t.start()
    t.join()
    assert r == ['A']


def test_get_blocking_waits_for_item():
    q = PriorityQueue()
    r = []
    t = thread_get(r, q)
    t.start()
    q.put('A', 1)
    t.join()
    assert r == ['A']


def test_get_blocking_timeout():
    q = PriorityQueue()
    r = []
    t = thread_get(r, q)
    t.start()
    t.join()
    assert len(r) == 1
    assert isinstance(r[0], Empty)


def test_get_blocking_timeout_with_delay_doesnt_timout(timer):
    q = PriorityQueue()
    r = []
    t = thread_get(r, q, timeout=0.5)
    with timer as m:
        t.start()
        time.sleep(0.1)
        q.put('A', 1)
        t.join()
    assert r == ['A']
    assert m.interval < 0.3 # estimate, should definitely finish in time


def test_multiple_consumers():
    q = PriorityQueue()
    r = []
    t1 = thread_get(r, q)
    t2 = thread_get(r, q)
    t1.start()
    t2.start()
    q.put('A', 2)
    q.put('B', 1)
    t1.join()
    t2.join()
    assert r == ['A', 'B']


def test_multiple_consumers_with_preloaded_queue():
    q = PriorityQueue()
    r = []
    t1 = thread_get(r, q)
    t2 = thread_get(r, q)
    q.put('B', 1)
    q.put('A', 2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert r == ['A', 'B']


def test_multiple_consumers_with_delayed_put():
    q = PriorityQueue()
    r = []
    t1 = thread_get(r, q, timeout=0.5)
    t2 = thread_get(r, q, timeout=0.5)
    t1.start()
    t2.start()
    q.put('A', 2)
    time.sleep(0.1)
    q.put('B', 1)
    t1.join()
    t2.join()
    assert r == ['A', 'B']


def test_multiple_consumers_with_delayed_put_timeout():
    q = PriorityQueue()
    r = []
    t1 = thread_get(r, q, timeout=0.3)
    t2 = thread_get(r, q, timeout=0.3)
    t1.start()
    t2.start()
    q.put('A', 1)
    t1.join()
    t2.join()
    assert len(r) == 2
    assert r[0] == 'A'
    assert isinstance(r[1], Empty)
