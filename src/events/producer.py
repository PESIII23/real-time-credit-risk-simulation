"""
Read rows from a CSV and emit them one-by-one as events into a queue.
"""
import pandas as pd
import time
import random
from src.events.queue_manager import EventQueue

excel_path = '/Users/phillipsmith/Desktop/pythonProjects/real-time-credit-risk-simulation/src/data/raw/dataset_project_1.xlsx'

class Producer:
    def __init__(self, excel_path, queue = EventQueue, delay=float):
        self.excel = pd.read_excel(excel_path, skiprows=1)
        self.queue = queue
        self.delay = delay

    def generate_events(self):
        """Simulate event generation from CSV"""
        print(f"Event producing has initiated...\n")
        for _, row in self.excel.iterrows():
            event = row.to_dict()
            if not self.queue.full():
                self.queue.push(event)
                self.delay = random.uniform(0.0, 0.001)
                time.sleep(self.delay)
            else:
                print("Queue is full, producer will be stopped and consumer will be initiated.\n")
                self.delay = random.uniform(2.0, 3.0)
                time.sleep(self.delay)
                break
        self.queue.push(None)
        print(f"All events have been produced...\n")