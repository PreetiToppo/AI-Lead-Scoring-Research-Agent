import logging
from pipeline import run_pipeline
from crm_sync import sync_to_hubspot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../logs/run.log"),
        logging.StreamHandler(),
    ],
)

if __name__ == "__main__":
    df = run_pipeline("../data/input_companies.csv", "../data/output_scored.csv")
    sync_to_hubspot(df, threshold=70)