import requests
import time
import logging
from config import HUBSPOT_API_KEY

logger = logging.getLogger(__name__)
HUBSPOT_BASE_URL = "https://api.hubapi.com/crm/v3/objects/contacts"

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
        company_name = row["company"]
        
        # 1. IDEMPOTENCY CHECK: Search if company already exists
        search_payload = {
            "filterGroups": [{
                "filters": [{"propertyName": "company", "operator": "EQ", "value": company_name}]
            }]
        }
        
        try:
            search_resp = requests.post(f"{HUBSPOT_BASE_URL}/search", json=search_payload, headers=headers)
            if search_resp.status_code == 200 and search_resp.json().get("total", 0) > 0:
                logger.info(f"Skipping {company_name} - already exists in HubSpot")
                continue # Skip to the next company
        except Exception as e:
            logger.warning(f"Search failed for {company_name}, proceeding to create: {e}")

        # 2. CREATE RECORD
        payload = {
            "properties": {
                "company": company_name,
                "hs_lead_status": "NEW",
                "lifecyclestage": "lead",
            }
        }
        
        # 3. RETRY LOGIC FOR RATE LIMITS (429)
        for attempt in range(3):
            try:
                resp = requests.post(HUBSPOT_BASE_URL, json=payload, headers=headers, timeout=10)
                if resp.status_code in (200, 201):
                    logger.info(f"Synced {company_name}")
                    synced += 1
                    break
                elif resp.status_code == 429:
                    wait = 2 ** attempt
                    time.sleep(wait)
                else:
                    logger.error(f"Failed {company_name}: {resp.status_code}")
                    break
            except requests.RequestException as e:
                time.sleep(2 ** attempt)
                
    return synced