"""
Pull events in batches from the queue, process them, store them, and apply ML.
"""
import os
import pandas as pd
import random
from pathlib import Path
from src.preprocessing import data_cleaning
# from models import LogisticModel

class Consumer:
    def __init__(self, queue, batch_size=10000, delay=float):
        self.queue = queue
        self.batch_size = batch_size
        self.df = pd.DataFrame()
        self.delay = delay
        # self.model = LogisticModel()

    def consume_events(self):
        """Consume events from the queue in batches, export to parquet"""
        batch = []

        print(f"      Event consuming has initiated.")
        while True:
            event = self.queue.pop()

            if event is None:
                break

            batch.append(event)

            if len(batch) >= self.batch_size:
                self.process_batch(batch)
                self.export_parquet()
                batch = []

        if batch:
            self.process_batch(batch)
            self.export_parquet()
            print("      Processing is complete.\n")

    def process_batch(self, batch):
        """Clean the incoming batch and append to the existing df"""
        temp_df = pd.DataFrame(batch)

        cleaned_data = data_cleaning.clean_raw_data(temp_df)
        self.df = pd.concat([self.df, cleaned_data], ignore_index=True)
        # print(f"\nConsumed batch of {len(batch)} events. \nTotal events processed: {len(self.df)}")
        self.delay = random.uniform(0.0, 0.0001)

    def export_parquet(self):
        """Export the updated dataframe to a parquet file"""
        project_root = Path('/Users/phillipsmith/Desktop/pythonProjects/real-time-credit-risk-simulation')
        folder_path = project_root / 'src' / 'data' / 'processed'
        folder_path.mkdir(parents=True, exist_ok=True)  # ensure folder exists
        file_path = folder_path / 'processed_df.parquet'

        self.df.to_parquet(file_path, engine='fastparquet', index=False)