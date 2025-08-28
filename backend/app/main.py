from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.core.config import settings
from app.services.weaviate_service import WeaviateService
from app.services.chat_service import ChatService, chat_service
import os
from contextlib import asynccontextmanager

# Global service instances
weaviate_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    global weaviate_service
    
    # Startup
    print("Starting up AI Chat API...")
    
    # Initialize Weaviate service
    weaviate_service = WeaviateService()
    
    # Define file paths
    chunks_file_path = os.path.join("app", "static", "chunks.txt")
    vectors_file_path = os.path.join("app", "static", "vectors.txt")
    
    # Check if files exist
    if not os.path.exists(chunks_file_path) or not os.path.exists(vectors_file_path):
        print(f"Warning: Data files not found at {chunks_file_path} or {vectors_file_path}")
    else:
        # Initialize collection and load data if needed
        success = weaviate_service.initialize_collection(
            chunks_file_path=chunks_file_path,
            vectors_file_path=vectors_file_path,
        #     max_chunks=3  # Limit to 3 chunks for testing, remove this for full dataset
        )
        
        if success:
            print("Weaviate collection initialized successfully")
            
            # Initialize chat service with Weaviate service
            chat_service.weaviate_service = weaviate_service
            print("Chat service initialized with Weaviate integration")
        else:
            print("Failed to initialize Weaviate collection")
    
    yield
    
    # Shutdown
    print("Shutting down AI Chat API...")
    if weaviate_service:
        weaviate_service.close()
        print("Weaviate connection closed")

app = FastAPI(
    title="AI Chat API",
    version="1.0.0",
    description="A minimalistic AI chatbot API",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Chat API is running"}

@app.get("/health")
async def health_check():
    global weaviate_service
    weaviate_status = "connected" if weaviate_service and weaviate_service.client else "disconnected"
    chat_status = "ready" if chat_service and chat_service.weaviate_service else "not_initialized"
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "weaviate": weaviate_status,
        "chat_service": chat_status
    }

@app.get("/weaviate/status")
async def weaviate_status():
    """Get Weaviate collection status"""
    global weaviate_service
    
    if not weaviate_service or not weaviate_service.client:
        return {"status": "not_initialized"}
    
    try:
        collection = weaviate_service.client.collections.get(weaviate_service.collection_name)
        collection_size = len(collection)
        return {
            "status": "ready",
            "collection_name": weaviate_service.collection_name,
            "collection_size": collection_size
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
