import threading
from threading import Semaphore

mutex = threading.Lock()
class Queue:
    def __init__(self, capacity = 10):
        self.queue = []
        self.capacity = capacity
        self.semaphoreCapacity = threading.Semaphore(capacity)
        self.semaphoreUsed = threading.Semaphore(0)

    def enqueue(self, item):
        self.semaphoreCapacity.acquire()
        mutex.acquire()
        self.queue.append(item)
        mutex.release()
        self.semaphoreUsed.release()

    def dequeue(self):
        self.semaphoreUsed.acquire()
        mutex.acquire()
        item = self.queue.pop(0)
        mutex.release()
        self.semaphoreCapacity.release()
        return item
