# Priority Queue
Python implementation of thread-safe priority queue with items merging.

## Features

- Each inserted item has a priority associated with it.
- If inserted item already exists in the queue, its new priority is the sum of the old and the new priority.
- When extracting, items with the highest priority are returned first.
- Blocking functionality is similar to that of `queue.Queue`.
- Queue allows safe concurrent operations of multiple threads
- Batching results: `get_n(n:int,timeout:float)->List[Item]`. Queue blocks, until at least `n` items are available (or timeout expires) and then returns gathered items.
