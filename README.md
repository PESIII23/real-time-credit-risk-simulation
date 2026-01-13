# Real-Time Credit Risk Simulation

---

## Project Overview
This project demonstrates a **lightweight, production-style streaming pipeline** for credit risk analysis. Using historical credit data, synthetic events are generated and pushed into an **in-memory queue**, consumed by a pipeline, preprocessed into a DataFrame, scored with a **logistic regression model**, and transformed into **actionable business recommendations**.  

The workflow simulates **real-time data ingestion and processing**, enabling testing of incremental ML scoring, feature engineering, and data validation in a modular architecture. This design mirrors production-ready ETL and analytics pipelines used in real-time decision systems.  

---

## Key Features
- **Event Generation:** Converts static CSV data into a simulated real-time event stream.  
- **Queue-Based Ingestion:** Uses Python’s `queue.Queue` to decouple event arrival from processing.  
- **DataFrame Storage:** Pulls events into a pandas DataFrame for preprocessing, cleaning, and feature engineering.  
- **Machine Learning Scoring:** Applies a trained logistic regression model to classify credit risk.  
- **Business Recommendations:** Converts model output into actionable decisions (e.g., high-risk customer flagging).  
- **Lightweight & Modular:** Fully implemented in Python with minimal dependencies (`pandas`, `numpy`, `scikit-learn`).  
- **Simulation of Real-World Scenarios:** Supports missing values, duplicates, and event-order variations.  

---

## Tools & Libraries
- **Python 3.9+**  
- **pandas** – Data storage, cleaning, and feature engineering  
- **numpy** – Numerical operations and synthetic data generation  
- **scikit-learn** – Logistic regression model scoring  
- **queue / asyncio.Queue** – In-memory queue for event streaming  
- **matplotlib / seaborn (optional)** – Visualization of results and metrics  

---

## Project Workflow

CSV Dataset
│
▼
Event Generator (shuffle / synthetic)
│
▼
In-Memory Queue (queue.Queue)
│
▼
Pull Event → Append to pandas DataFrame
│
▼
Data Cleaning & Feature Engineering
│
▼
ML Scoring / Prediction (logistic regression)
│
▼
Business Recommendations / Results DataFrame
│
▼
Optional: Dashboard / Metrics / Logs

---

## Getting Started

1. **Clone the repository:**  
```bash
git clone https://github.com/yourusername/credit-risk-pipeline.git
````

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the simulation:**

* Load your CSV dataset.
* Generate events into the queue.
* Pull events into a DataFrame and process through the pipeline.
* View ML predictions and recommendations.

---

## Why This Project is Valuable

* Demonstrates **real-time event handling and ML scoring**, not just batch processing.
* Provides **hands-on experience with data pipelines, feature engineering, and predictive modeling**.
* Simulates production-relevant challenges: **data validation, duplicate events, delayed arrivals, and incremental processing**.
* Ideal for showcasing **data engineering, analytics, and ML deployment skills** to recruiters and interviewers.

---

## Future Enhancements

* Integrate **lightweight dashboard** for real-time visualization of predictions and metrics.
* Expand to **async event processing** with `asyncio` or lightweight Kafka for more realistic streaming.
* Implement **rolling feature computation** or **concept drift detection**.
* Introduce **multiple ML models** for ensemble scoring or risk comparison.

---

