import time
import pytest
import threading


class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


@pytest.fixture
def timer():
    return Timer()


def thread_get(results, queue, block=True, timeout=0.1):
    def _get(results, queue, block, timeout):
        try:
            r = queue.get(block, timeout)
        except Exception as e:
            r = e
        results.append(r)
    return threading.Thread(target=_get, args=(results, queue, block, timeout))


def thread_get_n(results, queue, n,  block=True, timeout=0.1):
    def _get_n(results, queue, n, block, timeout):
        try:
            r = queue.get_n(n, block, timeout)
        except Exception as e:
            r = [e]
        results.extend(r)
    return threading.Thread(target=_get_n, args=(results, queue, n,  block, timeout))


def thread_put(errors, queue, value, priority, block=True, timeout=0.1):
    def _put(errors, queue, value, priority, block, timeout):
        try:
            queue.put(value, priority, block, timeout)
        except Exception as e:
            errors.append(e)
    return threading.Thread(target=_put, args=(errors, queue, value, priority, block, timeout))
