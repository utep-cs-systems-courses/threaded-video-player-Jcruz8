import threading
from threading import Semaphore

class Queue:
    def __init__(self, capacity):
        self.queue = []
        self.capacity = capacity
        self.semaphoreCapacity = threading.Semaphore(capacity)
        self.semaphoreUsed = threading.Semaphore(0)

    def enqueue(self, item):
        self.semaphoreCapacity.acquire()
        self.queue.append(item)
        self.semaphoreUsed.release()

    def dequeue(self):
        self.semaphoreUsed.acquire()
        item = self.queue.pop(0)
        self.semaphoreCapacity.release()
        return item
