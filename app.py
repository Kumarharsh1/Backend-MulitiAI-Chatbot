from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="MultiAI Chatbot API",
    description="Backend for Multi-AI Chatbot with Groq, Databricks, and News Integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - adjust in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Import routes
try:
    from routes.chat import router as chat_router
    from routes.news import router as news_router
    print("✅ Routes imported successfully")
except ImportError as e:
    print(f"❌ Error importing routes: {e}")
    # Create empty routers if imports fail
    from fastapi import APIRouter
    chat_router = APIRouter()
    news_router = APIRouter()

# Include routers
app.include_router(chat_router, prefix="/api/v1")
app.include_router(news_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "MultiAI Chatbot API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "author": "Kumar Harsh, India",
        "contact": "kh949118@gmail.com",
        "phone": "91-9279157296",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "services": "/api/v1/services",
            "chat": "/api/v1/chat",
            "news": "/api/v1/news"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MultiAI Chatbot API",
        "timestamp": "2024-01-01T00:00:00Z"  # You can import datetime to make this dynamic
    }

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "name": "MultiAI Chatbot API",
        "version": "1.0.0",
        "description": "Backend API for Multi-AI Chatbot with Groq and Databricks integration",
        "endpoints": {
            "chat": "/api/v1/chat",
            "news": "/api/v1/news",
            "services": "/api/v1/services"
        }
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "message": "API is working correctly!",
        "status": "success"
    }

# Production settings
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting MultiAI Chatbot API on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)