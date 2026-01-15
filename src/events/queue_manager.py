"""
Decouple producers from consumers using a simple in-memory queue.
"""
from queue import Queue

class EventQueue:
    def __init__(self, maxsize=100000):
        self.queue = Queue(maxsize=maxsize)
    
    def push(self, event):
        self.queue.put(event)
    
    def pop(self):
        return self.queue.get()
    
    def empty(self):
        return self.queue.empty()
    
    def full(self):
        return self.queue.full()