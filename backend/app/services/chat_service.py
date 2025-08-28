from typing import List, Dict
from datetime import datetime
import uuid
import asyncio
from app.models.chat import ChatMessage, ChatResponse, ChatSession
from .ai_service import ai_service

class ChatService:
    def __init__(self, weaviate_service=None):
        self.sessions: Dict[str, ChatSession] = {}
        self.weaviate_service = weaviate_service
        
        # If no weaviate service provided, try to initialize one
        if not self.weaviate_service:
            try:
                from .weaviate_service import WeaviateService
                self.weaviate_service = WeaviateService()
                print("ChatService: Initialized Weaviate service")
            except Exception as e:
                print(f"ChatService: Failed to initialize Weaviate service: {e}")
                self.weaviate_service = None
    
    def get_session(self, session_id: str) -> ChatSession:
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession(session_id=session_id, messages=[])
        return self.sessions[session_id]
    
    def add_user_message(self, session_id: str, message: str) -> ChatMessage:
        session = self.get_session(session_id)
        user_msg = ChatMessage(
            id=f"user_{uuid.uuid4().hex[:8]}",
            message=message,
            timestamp=datetime.now().isoformat(),
            is_user=True
        )
        session.messages.append(user_msg)
        return user_msg
    
    def get_relevant_context(self, query: str, limit: int = 3) -> List[Dict]:
        """Get relevant context from Weaviate knowledge base"""
        if not self.weaviate_service:
            print("Weaviate service not available")
            return []
        
        # Ensure weaviate service is connected
        if not self.weaviate_service.client:
            print("Connecting to Weaviate...")
            if not self.weaviate_service.connect():
                print("Failed to connect to Weaviate")
                return []
        
        try:
            # Search for similar chunks
            results = self.weaviate_service.search_similar_chunks(query, limit=limit)
            print(f"Search returned {len(results)} results")
            
            # Format results for response
            context = []
            for obj in results:
                context.append({
                    "chunk": obj.get("chunk", ""),
                    "chunk_index": obj.get("chunk_index", 0)
                })
            
            print(f"Formatted {len(context)} context items")
            return context
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
    
    def add_ai_response(self, session_id: str, message: str) -> ChatResponse:
        session = self.get_session(session_id)
        ai_response = ChatResponse(
            id=f"ai_{uuid.uuid4().hex[:8]}",
            message=message,
            timestamp=datetime.now().isoformat(),
            is_user=False,
        )
        session.messages.append(ai_response)
        return ai_response
    
    async def generate_response_with_context(self, session_id: str, user_message: str) -> ChatResponse:
        """Generate AI response with relevant context from Weaviate using TogetherAI"""
        # Get relevant context
        context_items = self.get_relevant_context(user_message, limit=3)
        print(f"Chat service: Retrieved {len(context_items)} context items")
        
        # Format context as string
        context_text = ""
        for item in context_items:
            context_text += f"{item.get('chunk', '')}\n\n"
        
        # Get conversation history (up to 5 messages)
        session = self.get_session(session_id)
        conversation_history = self._get_conversation_history(session, max_messages=5)
        
        # Add user message to session
        self.add_user_message(session_id, user_message)
        
        # Generate AI response using the AI service with conversation history
        response_message = await ai_service.generate_response_with_history(
            user_message, context_text, conversation_history
        )
        
        # Create and add AI response
        ai_response = self.add_ai_response(session_id, response_message)
        print(f"Chat service: Created AI response")
        
        return ai_response
    
    def _get_conversation_history(self, session: ChatSession, max_messages: int = 5) -> str:
        """Get formatted conversation history for context"""
        if not session.messages:
            return ""
        
        # Get the last max_messages from the conversation
        recent_messages = session.messages[-max_messages:]
        
        history_text = "Previous conversation:\n"
        for msg in recent_messages:
            role = "User" if msg.is_user else "Assistant"
            history_text += f"{role}: {msg.message}\n"
        
        return history_text
    
    def clear_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            self.sessions[session_id].messages.clear()
            return True
        return False
    
    def get_session_history(self, session_id: str) -> ChatSession:
        return self.get_session(session_id)

# Create a singleton instance
chat_service = ChatService()
