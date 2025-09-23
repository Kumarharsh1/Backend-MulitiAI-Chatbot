import os
import requests
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class NewsService:
    def __init__(self):
        # Get API key from environment
        self.databricks_api_key = os.getenv("DATABRICKS_API_KEY")
        self.databricks_endpoint = os.getenv("DATABRICKS_SERVING_ENDPOINT")
        
        if not self.databricks_api_key or not self.databricks_endpoint:
            raise Exception("Databricks API key or endpoint missing in .env")
        
        self.headers = {
            "Authorization": f"Bearer {self.databricks_api_key}",
            "Content-Type": "application/json"
        }

    def get_news(self, query: str, limit: int = 5):
        """Fetch news from Databricks endpoint"""
        payload = {
            "query": query,
            "limit": limit
        }
        try:
            response = requests.post(
                self.databricks_endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Initialize service
news_service = NewsService()
