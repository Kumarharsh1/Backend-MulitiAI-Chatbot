import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class DatabricksService:
    def __init__(self):
      
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat(self, message: str, chatbot_type: str, history: list = None):
        """Send message to Databricks endpoint"""
        
        system_prompts = {
            "news": "You are a news analysis expert. Provide insightful news commentary and analysis.",
            "personal": "You are a thoughtful personal advisor. Provide wise and considerate personal advice.",
            "creative": "You are an artistic creative assistant. Help with creative writing and artistic projects.",
            "technical": "You are a coding expert. Provide detailed technical explanations and code examples."
        }
        
        system_prompt = system_prompts.get(chatbot_type, "You are a helpful assistant.")
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if history:
            # History is now a list of dictionaries
            messages.extend(history[-4:])
        
        messages.append({"role": "user", "content": message})
        
        payload = {
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 500
        }
        
        try:
            print(f"📤 Sending request to Databricks with {len(messages)} messages")
            response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(payload), timeout=30)
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Received response from Databricks")
            return {
                "content": result["choices"][0]["message"]["content"],
                "model": "databricks-llama-4"
            }
            
        except requests.exceptions.Timeout:
            return {
                "content": "⏰ Timeout Error: The request to Databricks took too long.",
                "error": "timeout_error"
            }
        except requests.exceptions.ConnectionError:
            return {
                "content": "🌐 Connection Error: Cannot reach Databricks endpoint.",
                "error": "connection_error"
            }
        except Exception as e:
            return {
                "content": f"❌ Databricks Error: {str(e)}",
                "error": "databricks_error"
            }

# Initialize the service
try:
    databricks_service = DatabricksService()
    print("✅ Databricks service initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize DatabricksService: {e}")
    databricks_service = None