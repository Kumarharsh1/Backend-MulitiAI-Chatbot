import os
from dotenv import load_dotenv

load_dotenv()

# backend/utils/security.py
def get_available_services():
    required_keys = ["GROQ_API_KEY", "DATABRICKS_API_KEY"]
    missing_keys = []

    for key in required_keys:
        api_key = os.getenv(key) # Get the key from the .env file
        # Check if the key is missing or still has a placeholder value
        if not api_key or api_key.startswith("your_") or "example" in api_key:
            missing_keys.append(key)

    services = {
        "groq": "GROQ_API_KEY" not in missing_keys,
        "databricks": "DATABRICKS_API_KEY" not in missing_keys,
        "news": True
    }
    return services