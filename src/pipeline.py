"""
Credit Risk Analysis Pipeline

Orchestrates the end-to-end credit risk analysis workflow:
    1. Event ingestion via producer-consumer pattern
    2. Data transformations (cleaning, backfill, missing value tracking)
    3. Feature engineering (log transforms, severity scoring, outliers)
    4. Export modeling-ready DataFrame

Usage:
    CLI:      python -m src.pipeline
    Python:   from src.pipeline import run_pipeline; full_df, modeling_df = run_pipeline()
"""
import threading
import pandas as pd
from pathlib import Path

from src.events.queue_manager import EventQueue
from src.events.producer import Producer
from src.events.consumer import Consumer
from src.preprocessing import data_transformations
from src.preprocessing.feature_engineering import engineer_features


# Config
PROJECT_ROOT = Path('/Users/phillipsmith/Desktop/pythonProjects/real-time-credit-risk-simulation')

class Paths:
    RAW_DATA = PROJECT_ROOT / 'src' / 'data' / 'raw' / 'dataset_project_1.xlsx'
    PROCESSED_DATA = PROJECT_ROOT / 'src' / 'data' / 'processed' / 'processed_df.parquet'
    MODELING_DATA = PROJECT_ROOT / 'src' / 'data' / 'processed' / 'modeling_df.parquet'


def run_pipeline(verbose: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Execute the full pipeline. Returns (full_df, modeling_df)."""
    log = print if verbose else lambda *args, **kwargs: None
    
    log("=" * 60)
    log("CREDIT RISK ANALYSIS PIPELINE")
    log("=" * 60)
    
    # Stage 1: Event Ingestion
    log("\n[1/4] Running event ingestion...")
    queue = EventQueue()
    producer = Producer(str(Paths.RAW_DATA), queue)
    consumer = Consumer(queue)
    producer_thread = threading.Thread(target=producer.generate_events)
    consumer_thread = threading.Thread(target=consumer.consume_events)
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()
    
    # Stage 2: Load & Transform
    log("\n[2/4] Loading and transforming data...")
    df = pd.read_parquet(Paths.PROCESSED_DATA, engine='fastparquet')
    log(f"      Loaded {len(df):,} records")
    df = data_transformations.apply_all_transformations(df)
    
    # Stage 3: Feature Engineering
    log("\n[3/4] Engineering features...")
    full_df, modeling_df = engineer_features(df, n_neighbors=5)
    log(f"      Created {len(modeling_df.columns)} features")
    
    # Stage 4: Export
    log("\n[4/4] Exporting modeling data...")
    Paths.MODELING_DATA.parent.mkdir(parents=True, exist_ok=True)
    modeling_df.to_parquet(Paths.MODELING_DATA, engine='fastparquet', index=False)
    
    # Summary
    log("\n" + "=" * 60)
    log("PIPELINE COMPLETE")
    log("=" * 60)
    log(f"\nFull DataFrame:     {full_df.shape}")
    log(f"Modeling DataFrame: {modeling_df.shape}")
    
    return full_df, modeling_df


if __name__ == "__main__":
    run_pipeline(verbose=True)