import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
MODEL = "gemini-3.5-flash"

ICP = {
    "industry": "B2B SaaS or software",
    "size": "10-500 employees",
    "region": "US or Europe",
    "pain_points": ["security compliance", "manual sales ops", "data fragmentation"],
}

if __name__ == "__main__":
    assert GEMINI_API_KEY, "Missing GEMINI_API_KEY in .env"
    print("Config OK")