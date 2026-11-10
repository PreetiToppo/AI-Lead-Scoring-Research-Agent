import logging
import os
from pipeline import run_pipeline
from crm_sync import sync_to_hubspot

os.makedirs("../logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../logs/run.log"),
        logging.StreamHandler(), # This prints to console (Docker logs)
    ],
)

if __name__ == "__main__":
    df = run_pipeline("../data/input_companies.csv", "../data/output_scored.csv")
    sync_to_hubspot(df, threshold=70)