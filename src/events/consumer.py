"""
Pull events from the queue, batch them, store them, and apply ML scoring.
"""
import os
import pandas as pd
import random
from pathlib import Path
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

        print(f"Event consuming has initiated...")
        while True:
            event = self.queue.pop()

            if event is None:
                break

            batch.append(event)

            if len(batch) >= self.batch_size:
                self.process_batch(batch)
                self.export_parquet()
                print
                batch = []

        if batch:
            self.process_batch(batch)
            self.export_parquet()

    def process_batch(self, batch):
        temp_df = pd.DataFrame(batch)
        self.delay = random.uniform(0.0, 0.001)

        # Perform cleaning
        # Feature engineering

        self.df = pd.concat([self.df, temp_df], ignore_index=True)
        print(f"Consumed batch of {len(batch)} events. Total events processed: {len(self.df)}\n")

        # """Apply ML model"""
        # if not self.df.empty:
        #     self.df['risk_score'] = self.model.predict(self.df)


    def export_parquet(self):
        """Export the dataframe to a parquet file (works in notebooks and scripts)"""

        # Define project root (adjust this path to your project root)
        project_root = Path('/Users/phillipsmith/Desktop/pythonProjects/real-time-credit-risk-simulation')

        # Folder to store processed data
        folder_path = project_root / 'src' / 'data' / 'processed'
        folder_path.mkdir(parents=True, exist_ok=True)  # ensure folder exists

        # Full path to parquet
        file_path = folder_path / 'processed_df.parquet'

        # Write the dataframe
        self.df.to_parquet(file_path, engine='fastparquet', index=False)

