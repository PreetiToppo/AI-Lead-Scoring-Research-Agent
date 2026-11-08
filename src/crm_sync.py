import requests
import time
import logging
from config import HUBSPOT_API_KEY

logger = logging.getLogger(__name__)
HUBSPOT_URL = "https://api.hubapi.com/crm/v3/objects/contacts"

def sync_to_hubspot(leads_df, threshold: int = 70) -> int:
    if not HUBSPOT_API_KEY:
        logger.error("Missing HUBSPOT_API_KEY")
        return 0

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json",
    }
    qualified = leads_df[leads_df["score"].fillna(0) >= threshold]
    synced = 0

    for _, row in qualified.iterrows():
        payload = {
            "properties": {
                "company": row["company"],
                "hs_lead_status": "NEW",
                "lifecyclestage": "lead",
            }
        }
        for attempt in range(3):
            try:
                resp = requests.post(HUBSPOT_URL, json=payload, headers=headers, timeout=10)
                if resp.status_code in (200, 201):
                    logger.info(f"Synced {row['company']}")
                    synced += 1
                    break
                elif resp.status_code == 429:
                    wait = 2 ** attempt
                    logger.warning(f"Rate limited on {row['company']}, retrying in {wait}s")
                    time.sleep(wait)
                else:
                    logger.error(f"Failed {row['company']}: {resp.status_code} {resp.text[:200]}")
                    break
            except requests.RequestException as e:
                logger.error(f"Request error {row['company']}: {e}")
                time.sleep(2 ** attempt)

    logger.info(f"Synced {synced} leads to HubSpot")
    return synced