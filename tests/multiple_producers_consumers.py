import string

from priority_queue.pqueue import PriorityQueue
from .conftest import thread_get, thread_put, thread_get_n


def test_many_producers_and_consumers():
    q = PriorityQueue()
    r = []
    threads = []
    for priority, letter in enumerate(string.ascii_letters):
        threads.append(thread_put(r, q, letter, priority))
        threads.append(thread_get(r, q))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(r) == sorted(string.ascii_letters) # Has to be sorted, put() is called in random order


def test_many_producers_and_one_getn_consumer():
    q = PriorityQueue()
    r = []
    threads = []
    for priority, letter in enumerate(string.ascii_letters):
        threads.append(thread_put(r, q, letter, priority))
    threads.append(thread_get_n(r, q, len(string.ascii_letters)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(r) == sorted(string.ascii_letters)
