from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List
from app.models.chat import ChatRequest, ChatResponse, ChatSession
from app.services.chat_service import chat_service
from app.services.ai_service import ai_service
import json

router = APIRouter(prefix="/chat", tags=["chat"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest, session_id: str = "default"):
    """Send a message and get AI response with Weaviate context"""
    try:
        if not chat_service:
            raise HTTPException(status_code=503, detail="Chat service not initialized")
        
        # Generate response with context from Weaviate
        ai_response = await chat_service.generate_response_with_context(session_id, request.message)
        
        return ai_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-with-ai", response_model=ChatResponse)
async def send_message_with_ai(request: ChatRequest, session_id: str = "default"):
    """Send a message and get AI response using the AI service with conversation history"""
    try:
        if not chat_service:
            raise HTTPException(status_code=503, detail="Chat service not initialized")
        
        # Get conversation history (up to 5 messages)
        session = chat_service.get_session(session_id)
        conversation_history = chat_service._get_conversation_history(session, max_messages=5)
        
        # Add user message to session
        user_msg = chat_service.add_user_message(session_id, request.message)
        
        # Query context
        context = await ai_service.query_context(request.message, limit=3)
        
        # Generate AI response with conversation history
        ai_response_text = await ai_service.generate_response_with_history(
            request.message, context, conversation_history
        )
        
        # Create AI response
        ai_response = chat_service.add_ai_response(session_id, ai_response_text)
        
        return ai_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", response_model=ChatSession)
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not initialized")
    return chat_service.get_session_history(session_id)

@router.delete("/clear/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not initialized")
    success = chat_service.clear_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": f"Chat history cleared for session {session_id}"}

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat with Weaviate context"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message
            request = ChatRequest(**message_data)
            
            if not chat_service:
                await manager.send_personal_message(
                    json.dumps({"error": "Chat service not initialized"}), websocket
                )
                continue
            
            # Generate response with context from Weaviate
            ai_response = await chat_service.generate_response_with_context(session_id, request.message)
            
            # Send AI response
            await manager.send_personal_message(
                json.dumps(ai_response.model_dump()), websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)