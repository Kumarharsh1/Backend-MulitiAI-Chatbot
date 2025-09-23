import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
      
        
        if not self.api_key:
            raise Exception("Groq API key not found in .env file")
            
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat(self, message: str, chatbot_type: str, history: list = None):
        """Send message to Groq API based on chatbot type"""
        
        # System prompts for different chatbot types
        system_prompts = {
            "news": "You are a knowledgeable news assistant. Provide accurate, up-to-date news information. Be concise and informative.",
            "personal": "You are a helpful personal assistant. Be friendly, supportive, and provide practical advice.",
            "creative": "You are a creative assistant. Be imaginative, innovative, and help with brainstorming and creative projects.",
            "technical": "You are a technical expert. Provide detailed, accurate technical information and coding help."
        }
        
        system_prompt = system_prompts.get(chatbot_type, "You are a helpful assistant.")
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if history:
            # History is now a list of dictionaries, not Pydantic models
            messages.extend(history[-6:])  # Keep last 6 messages for context
        
        messages.append({"role": "user", "content": message})
        
        payload = {
            "messages": messages,
            "model": "llama-3.1-8b-instant",
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 1,
            "stream": False
        }
        
        try:
            print(f"📤 Sending request to Groq API with {len(messages)} messages")
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 401:
                return {
                    "content": "❌ Authentication Error: Invalid Groq API key. Please check your .env file.",
                    "error": "authentication_error"
                }
            elif response.status_code == 429:
                return {
                    "content": "⏳ Rate Limit Exceeded: Please try again in a few moments.",
                    "error": "rate_limit_error"
                }
            elif response.status_code == 400:
                return {
                    "content": "📝 API Error: Bad request. The message might be too long or malformed.",
                    "error": "bad_request_error"
                }
                
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Received response from Groq API")
            return {
                "content": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {}),
                "model": result["model"]
            }
            
        except requests.exceptions.Timeout:
            return {
                "content": "⏰ Timeout Error: The request took too long. Please try again.",
                "error": "timeout_error"
            }
        except requests.exceptions.ConnectionError:
            return {
                "content": "🌐 Connection Error: Cannot reach Groq API. Check your internet connection.",
                "error": "connection_error"
            }
        except Exception as e:
            return {
                "content": f"❌ Error: {str(e)}",
                "error": "general_error"
            }

# Initialize the service
try:
    groq_service = GroqService()
    print("✅ Groq service initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize GroqService: {e}")
    groq_service = None