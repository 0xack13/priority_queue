import pytest
import threading
import time

from priority_queue.pqueue import PriorityQueue
from queue import Empty, Full


def thread_get_n(results, queue, n,  blocking=True, timeout=0.1):
    def _get(results, queue, n, blocking, timeout):
        try:
            r = queue.get_n(n, blocking, timeout)
        except Exception as e:
            r = [e]
        results.extend(r)
    return threading.Thread(target=_get, args=(results, queue, n,  blocking, timeout))


def test_get_n_from_nonempty():
    q = PriorityQueue()
    q.put('A', 2)
    q.put('B', 1)
    r = []
    t = thread_get_n(r, q, 2)
    t.start()
    t.join()
    assert r == ['A', 'B']


def test_get_n_waits_for_items():
    q = PriorityQueue()
    r = []
    t = thread_get_n(r, q, 2)
    t.start()
    q.put('A', 1)
    q.put('B', 1)
    t.join()
    assert r == ['A', 'B']


def test_get_n_timeout():
    q = PriorityQueue()
    q.put('A', 1)
    r = []
    t = thread_get_n(r, q, 2)
    t.start()
    t.join()
    assert len(r) == 1
    assert isinstance(r[0], Empty)


def test_get_n_with_delay_doesnt_timout(timer):
    q = PriorityQueue()
    r = []
    t = thread_get_n(r, q, 2, timeout=1)
    with timer as m:
        t.start()
        time.sleep(0.1)
        q.put('A', 2)
        time.sleep(0.1)
        q.put('B', 1)
        t.join()
    assert r == ['A', 'B']
    assert m.interval < 0.5 # estimate, should definitely finish in time


def get_n_keeps_correct_order_after_pulling():
    q = PriorityQueue()
    r = []
    t = thread_get_n(r, q, 2)
    t.start()
    q.put('A', 1)
    time.sleep(0.1)
    q.put('B', 2)
    t.join()
    assert r == ['B', 'A']


def test_multiple_consumers():
    q = PriorityQueue()
    r = []
    t1 = thread_get_n(r, q, 2)
    t2 = thread_get_n(r, q, 3)
    t1.start()
    t2.start()
    q.put('A', 5)
    q.put('B', 4)
    q.put('C', 3)
    q.put('D', 2)
    q.put('E', 1)
    t1.join()
    t2.join()
    assert r == ['A', 'B', 'C', 'D', 'E']


def test_multiple_consumers_with_preloaded_queue():
    q = PriorityQueue()
    r = []
    t1 = thread_get_n(r, q, 2)
    t2 = thread_get_n(r, q, 3)
    q.put('A', 5)
    q.put('B', 4)
    q.put('C', 3)
    q.put('D', 2)
    q.put('E', 1)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert r == ['A', 'B', 'C', 'D', 'E']
