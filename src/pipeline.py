"""
Runs the producer-consumer pipeline in separate threads to concurrently generate and process events from the Excel file.
"""
import threading
import os
from src.events.queue_manager import EventQueue
from src.events.producer import Producer
from src.events.consumer import Consumer

excel_path = os.path.abspath('/Users/phillipsmith/Desktop/pythonProjects/real-time-credit-risk-simulation/src/data/raw/dataset_project_1.xlsx')

def run_pipeline():
    queue = EventQueue()
    producer = Producer(excel_path, queue)
    consumer = Consumer(queue)

    producer_thread = threading.Thread(target=producer.generate_events)
    consumer_thread = threading.Thread(target=consumer.consume_events)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

if __name__ == "__main__" or "ipykernel" in __name__:
    final_df = run_pipeline()