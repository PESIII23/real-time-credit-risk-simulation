"""
Read rows from a CSV and emit them one-by-one as events into a queue.
"""
import pandas as pd
import time
import random
from events.queue_manager import EventQueue

class Producer:
    def __init__(self, excel_path, queue = EventQueue, delay=float):
        self.excel = pd.read_excel(excel_path, skiprows=1)
        self.queue = queue
        self.delay = delay

    def generate_events(self):
        """Simulate event generation from CSV"""
        for _, row in self.excel.iterrows():
            event = row.to_dict()
            self.queue.push(event)
            print(f"Produced event: {event}\n")
            self.delay = random.uniform(0.0, 0.01)
            time.sleep(self.delay)