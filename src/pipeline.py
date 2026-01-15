"""
Wire everything together and run the full simulation.
"""

from events.queue_manager import EventQueue
from events.producer import Producer
from events.consumer import Consumer

excel_path = 'src/data/raw/dataset_project_1.xlsx'

def run_pipeline(excel_path):
    queue = EventQueue()

    print("Producing events...\n")
    producer = Producer(excel_path, queue)
    producer.generate_events()

    print("Consuming events...\n")
    consumer = Consumer(queue)
    consumer.consume_events()

    if queue.full():
        print("Queue is full, cannot add more events.\n Simulation Stopped.")

if __name__ == "__main__":
    final_df = run_pipeline('src/data/raw/dataset_project_1.xlsx')
    print(final_df)