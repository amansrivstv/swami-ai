import asyncio
from typing import List, Dict
from .together_ai_service import together_ai_service

class AIService:
    async def generate_response(self, message: str, context: str = None) -> str:
        """
        Generate AI response using TogetherAI LLM with optional context.
        """
        try:
            # Prepare system prompt with context if available
            system_prompt = "You are a wise prophet. Provide philosophical debate responses based on the context provided and the user's question. Ask follow up questins sometimes if it makes sense. Do not at any time let the user know you are using a context, just use it to answer the user's question."

            # Create the user prompt
            user_prompt = message
            if context:
                user_prompt += f"\n\nUse the following context to enrich the response to the user's message:\n{context} do not at any time let the user know you are using a context, just use it to answer the user's question."
            
            # Call TogetherAI LLM
            response = together_ai_service.call_llm(user_prompt, system_prompt)
            
            return response
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return f"Developer fucked up."
    
    async def generate_response_with_history(self, message: str, context: str = None, conversation_history: str = None) -> str:
        """
        Generate AI response using TogetherAI LLM with optional context and conversation history.
        """
        try:
            # Prepare system prompt
            system_prompt = "You are a wise prophet. Provide philosophical debate responses based on the context provided and the user's question. Consider the conversation history to maintain context and continuity. Ask follow up questions sometimes if it makes sense. Do not at any time let the user know you are using a context, just use it to answer the user's question."

            # Create the user prompt with conversation history and context
            user_prompt = message
            
            # Add conversation history if available
            if conversation_history:
                user_prompt = f"{conversation_history}\n\nCurrent question: {message}"
            
            # Add context if available
            if context:
                user_prompt += f"\n\nUse the following context to enrich the response to the user's message:\n{context} do not at any time let the user know you are using a context, just use it to answer the user's question."
            
            # Call TogetherAI LLM
            response = together_ai_service.call_llm(user_prompt, system_prompt)
            
            return response
            
        except Exception as e:
            print(f"Error generating AI response with history: {e}")
            return f"Developer fucked up."
    
    async def query_context(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Query context using Weaviate vector search with TogetherAI embeddings.
        """
        try:
            from .weaviate_service import weaviate_service
            
            # Search for similar chunks using vector similarity
            similar_chunks = weaviate_service.search_similar_chunks(query, limit)
            # Convert to the expected format
            context_results = ""
            for chunk in similar_chunks:
                context_results += chunk.get('chunk', '') + "\n\n"
            
            return context_results
            
        except Exception as e:
            print(f"Error querying context: {e}")
            return []

ai_service = AIService()