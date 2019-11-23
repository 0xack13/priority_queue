import pytest
import threading
import time

from priority_queue.pqueue import PriorityQueue
from queue import Empty, Full


def thread_get(results, q, blocking, timeout):
    try:
        r = q.get(blocking, timeout)
    except Exception as e:
        r = e
    results.append(r)


def test_get_blocking_result_from_nonempty():
    q = PriorityQueue()
    q.put('A', 1)
    r = []
    t = threading.Thread(target=thread_get, args=(r, q, True, 1))
    t.start()
    t.join()
    assert r == ['A']


def test_get_blocking_waits_for_item():
    q = PriorityQueue()
    r = []
    t = threading.Thread(target=thread_get, args=(r, q, True, 1))
    t.start()
    q.put('A', 1)
    t.join()
    assert r == ['A']


def test_get_blocking_timeout():
    q = PriorityQueue()
    r = []
    t = threading.Thread(target=thread_get, args=(r, q, True, 1))
    t.start()
    t.join()
    assert len(r) == 1
    assert isinstance(r[0], Empty)


def test_get_blocking_timeout_with_delay(timer):
    q = PriorityQueue()
    r = []
    t = threading.Thread(target=thread_get, args=(r, q, True, 5))
    with timer as m:
        t.start()
        time.sleep(1)
        q.put('A', 1)
        t.join()
    assert r == ['A']
    assert m.interval < 3
