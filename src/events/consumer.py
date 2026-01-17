"""
Pull events from the queue, batch them, store them, and apply ML scoring.
"""
import os
import pandas as pd
import random
# from models import LogisticModel

class Consumer:
    def __init__(self, queue, batch_size=100, delay=float):
        self.queue = queue
        self.batch_size = batch_size
        self.df = pd.DataFrame()
        self.delay = delay
        # self.model = LogisticModel()

    def consume_events(self):
        """Consume events from the queue in batches, export to parquet"""
        batch = []

        while not self.queue.empty():
            event = self.queue.pop()
            batch.append(event)

            if len(batch) >= self.batch_size:
                self.process_batch(batch)
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
        """Export the dataframe to a parquet file"""
        folder_path = 'src/data/processed'
        file_name = 'processed_df.parquet'
        full_path = os.path.join(folder_path, file_name)

        os.makedirs(folder_path, exist_ok=True)

        self.df.to_parquet(full_path, engine='fastparquet', index=False)
        print(f"Exported processed dataframe to {full_path}\n")