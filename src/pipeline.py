import pandas as pd
import logging
import time
from research import research_company
from scoring import score_lead

logger = logging.getLogger(__name__)

def run_pipeline(input_csv: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv)

    # Clean + dedupe
    df["company"] = df["company"].astype(str).str.strip()
    before = len(df)
    df = df.drop_duplicates(subset=["company"]).reset_index(drop=True)
    logger.info(f"Deduped {before} -> {len(df)} rows")

    scores, rationales = [], []
    for i, row in df.iterrows():
        try:
            # 1. Research (API call 1)
            research = research_company(row["company"])
            
            # Sleep 10 seconds after research to pace our requests
            time.sleep(10) 
            
            # 2. Score (API call 2)
            result = score_lead(row["company"], research)
            scores.append(result["score"])
            rationales.append(result["rationale"])
            logger.info(f"[{i+1}/{len(df)}] {row['company']}: {result['score']}")
            
            # Sleep 15 seconds after scoring to ensure we stay under 5 req/min
            time.sleep(15) 
            
        except Exception as e:
            logger.error(f"Failed {row['company']}: {e}")
            scores.append(None)
            rationales.append(None)
            # Sleep even on failure so we don't hammer the API
            time.sleep(15) 

    df["score"] = scores
    df["rationale"] = rationales
    df.to_csv(output_csv, index=False)
    logger.info(f"Wrote {len(df)} rows to {output_csv}")
    return df