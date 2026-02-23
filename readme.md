# Real-Time Credit Risk Simulation

A modular Python pipeline for credit risk analysis with simulated real-time event ingestion, feature engineering, and ML-ready data preparation.

---

## Project Structure

```
src/
├── pipeline.py              # Main orchestrator (run_pipeline)
├── events/                  # Event streaming simulation
│   ├── queue_manager.py     # In-memory event queue
│   ├── producer.py          # Event generation from raw data
│   └── consumer.py          # Event consumption and storage
├── preprocessing/
│   ├── data_transformations.py  # Cleaning, backfill, missing value tracking
│   └── feature_engineering.py   # FeatureEngineer class with transforms
├── models/
│   └── credit_risk_model.py     # Model data loading utilities
├── notebooks/
│   └── credit_risk_analysis.ipynb  # EDA and analysis notebook
├── data/
│   ├── raw/                 # Source Excel data
│   └── processed/           # Parquet outputs
└── viz/                     # Visualization utilities
```

---

## Quick Start

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Run the pipeline:**
```bash
python -m src.pipeline
```

**3. Use in Python:**
```python
from src.pipeline import run_pipeline, Paths

full_df, modeling_df = run_pipeline(verbose=True)
```

---

## Pipeline Stages

| Stage | Description |
|-------|-------------|
| **1. Event Ingestion** | Producer-consumer pattern simulates real-time data arrival via queue |
| **2. Load & Transform** | Backfill overdues, track missing values, clean data |
| **3. Feature Engineering** | Log transforms, severity scoring, age normalization, KNN imputation, outlier detection |
| **4. Export** | Save modeling-ready DataFrame to parquet |

---

## Key Features

- **Event Streaming Simulation** – Queue-based ingestion decouples data arrival from processing
- **Feature Engineering** – Log transforms, severity scoring, business scale, IQR outlier detection
- **KNN Imputation** – Handles missing values intelligently
- **Modular Architecture** – Clean separation of concerns across preprocessing, models, and events
- **Dual Output** – Returns both full DataFrame (all columns) and modeling DataFrame (ML-ready features)

---

## Output

The pipeline produces two DataFrames:
- `full_df` – Complete dataset with all engineered features
- `modeling_df` – Subset of features ready for ML training (~13 columns)

Saved to: `src/data/processed/modeling_df.parquet`

---

## Tools & Libraries

- Python 3.9+
- pandas, numpy – Data manipulation
- scikit-learn – KNN imputation
- fastparquet – Efficient data storage
- matplotlib, seaborn – Visualization (notebook)

---

## Support

- Email: pesmithiii7@gmail.com
- Documentation: [Milestone 1](https://docs.google.com/document/d/1PcnBauANcs5RhZ9chxNYY3yiQkt74uMr-pRhGO5KiDA/edit?usp=drive_link) | [Milestone 2](https://docs.google.com/document/d/1exCDFc11iXaxxlIqDk0IfU_Q_Ih7CzlDFMKyCwI5g9g/edit?usp=sharing)
- Repository: [GitHub](https://github.com/PESIII23/real-time-credit-risk-simulation)
