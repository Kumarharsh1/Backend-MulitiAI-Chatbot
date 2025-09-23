from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# Define get_available_services function here to avoid import issues
def get_available_services():
    """Check which services are available based on API keys"""
    required_keys = ["GROQ_API_KEY", "DATABRICKS_API_KEY"]
    
    missing_keys = []
    for key in required_keys:
        api_key = os.getenv(key)
        if not api_key or api_key.startswith("your_") or "example" in api_key:
            missing_keys.append(key)
    
    services = {
        "groq": "GROQ_API_KEY" not in missing_keys,
        "databricks": "DATABRICKS_API_KEY" not in missing_keys,
        "news": True
    }
    
    print(f"🔑 Missing keys: {missing_keys}")
    print(f"🛠️ Available services: {services}")
    
    return services

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    chatbot_type: str
    service: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    content: str
    service: str
    model: Optional[str] = None
    usage: Optional[dict] = None
    error: Optional[str] = None

@router.get("/services")
async def get_available_services_route():
    """Get available AI services"""
    try:
        services = get_available_services()
        print(f"✅ Available services: {services}")
        return services
    except Exception as e:
        print(f"❌ Error getting services: {e}")
        return {"groq": False, "databricks": False, "news": True}

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint"""
    try:
        print(f"📨 Received chat request: {request.chatbot_type} via {request.service}")
        
        # Get available services
        available_services = get_available_services()
        print(f"🔧 Available services: {available_services}")
        
        if not available_services.get(request.service):
            return ChatResponse(
                content=f"Service {request.service} is not available. Available services: {available_services}",
                service=request.service,
                error="service_unavailable"
            )
        
        # Convert ChatMessage objects to dictionaries for JSON serialization
        history_dicts = []
        if request.history:
            for msg in request.history:
                # Convert Pydantic model to dictionary
                if hasattr(msg, 'dict'):
                    history_dicts.append(msg.dict())
                else:
                    # Fallback: manually create dict
                    history_dicts.append({
                        "role": getattr(msg, 'role', 'user'),
                        "content": getattr(msg, 'content', '')
                    })
        
        print(f"📝 History converted to dicts: {len(history_dicts)} messages")
        
        if request.service == "groq":
            # Import here to avoid circular imports
            from services.groq_service import groq_service
            
            if groq_service is None:
                return ChatResponse(
                    content="Groq service is not properly initialized. Check your API key.",
                    service="groq",
                    error="service_error"
                )
            
            result = await groq_service.chat(
                request.message, 
                request.chatbot_type, 
                history_dicts  # Use the converted dictionaries
            )
            
            # Convert boolean error to string if needed
            error_value = result.get("error")
            if isinstance(error_value, bool):
                error_value = str(error_value).lower()
            
            return ChatResponse(
                content=result["content"],
                service="groq",
                model=result.get("model"),
                usage=result.get("usage"),
                error=error_value
            )
        
        elif request.service == "databricks":
            # Import here to avoid circular imports
            from services.databricks_service import databricks_service
            
            if databricks_service is None:
                return ChatResponse(
                    content="Databricks service is not properly initialized.",
                    service="databricks",
                    error="service_error"
                )
            
            result = await databricks_service.chat(
                request.message, 
                request.chatbot_type, 
                history_dicts  # Use the converted dictionaries
            )
            
            # Convert boolean error to string if needed
            error_value = result.get("error")
            if isinstance(error_value, bool):
                error_value = str(error_value).lower()
            
            return ChatResponse(
                content=result["content"],
                service="databricks",
                model=result.get("model"),
                error=error_value
            )
        
        else:
            return ChatResponse(
                content=f"Invalid service selected: {request.service}",
                service=request.service,
                error="invalid_service"
            )
            
    except Exception as e:
        print(f"💥 Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return ChatResponse(
            content=f"Server error: {str(e)}",
            service=request.service,
            error="server_error"
        )