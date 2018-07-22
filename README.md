# Blocking Queue

when there are multiple threads it may be useful to consume all produced tasks
that is what BlockingQueue for

```python
queue = BlockingQueue()

next(queue) # will block until some other thread will close or append something

# at the same time in another thread
queue.append('some stuff') # next(q) will return whatever was appended to the queue
queue.close() # next(q) will raise StopIteration
```

there is one more example of how BlockingQueue works in doctests
