from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class ChatMessage(BaseModel):
    id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=1000)
    timestamp: Optional[str] = None
    is_user: bool = True

class ChatResponse(BaseModel):
    id: str
    message: str
    timestamp: str
    is_user: bool = False

class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage] = []

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)