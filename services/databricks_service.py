import os
import requests
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class DatabricksService:
    def __init__(self):
        self.api_key = os.getenv("DATABRICKS_API_KEY")
        self.endpoint = os.getenv("DATABRICKS_SERVING_ENDPOINT")
        
        if not self.api_key or not self.endpoint:
            raise Exception("Databricks API key or endpoint missing in .env")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, message: str):
        """Send message to Databricks LLM"""
        payload = {
            "inputs": message
        }
        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Initialize service
databricks_service = DatabricksService()
