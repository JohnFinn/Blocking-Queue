from threading import Lock, Condition


class BlockingQueue:
    '''
    fetching next will block, until someone append/close
    in the first case return appended value, in the last case 
    raise StopIteration

    >>> from time import sleep
    >>> from threading import Thread
    >>> q = BlockingQueue()
    >>> results = []
    >>> def foo():
    ...     for i in q:
    ...         results.append(i)
    ...     results.append('exited')
    ...
    >>> thread = Thread(target=foo)
    >>> thread.start()
    >>> sleep(.1) # making sure thread blocked
    >>> results
    []
    >>> q.append(99)
    >>> while len(results) != 1: pass
    >>> results
    [99]
    >>> sleep(.1)
    >>> results
    [99]
    >>> q.append(199)
    >>> while len(results) != 2: pass
    >>> results
    [99, 199]
    >>> sleep(.1)
    >>> results
    [99, 199]
    >>> q.close()
    >>> while len(results) != 3: pass
    >>> results
    [99, 199, 'exited']
    '''

    def __init__(self):
        self._storage = []
        self._open = True
        self._lock = Lock()
        self._condition = Condition(self._lock)


    def __iter__(self):
        return self


    def __next__(self):
        with self._condition:
            self._condition.wait_for(lambda: self._storage or not self._open)
            if self._storage:
                return self._storage.pop(0)
            elif not self._open:
                raise StopIteration


    def append(self, obj):
        with self._condition:
            if self._open:
                self._storage.append(obj)
                self._condition.notify()
            else:
                raise RuntimeError("cannot append to closed queue")


    def close(self):
        with self._condition:
            if not self._open:
                raise RuntimeError("already closed")

            self._open = False
            self._condition.notify()
