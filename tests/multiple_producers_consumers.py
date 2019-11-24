import threading
import string
from priority_queue.pqueue import PriorityQueue


def thread_put(errors, queue, value, priority, block=True, timeout=0.3):
    def _put(errors, queue, value, priority, block, timeout):
        try:
            queue.put(value, priority, block, timeout)
        except Exception as e:
            errors.append(e)
    return threading.Thread(target=_put, args=(errors, queue, value, priority, block, timeout))


def thread_get(results, queue, block=True, timeout=0.3):
    def _get(results, queue, block, timeout):
        try:
            r = queue.get(block, timeout)
        except Exception as e:
            r = e
        results.append(r)
    return threading.Thread(target=_get, args=(results, queue, block, timeout))


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
