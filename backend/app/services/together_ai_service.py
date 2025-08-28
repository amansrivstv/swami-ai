import os
from typing import List, Dict, Union
from together import Together


class TogetherAIService:
    def __init__(self):
        self.api_key = os.getenv('TOGETHER_API_KEY')
        self.client = None
        self.llm_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
        self.embedding_model = "togethercomputer/m2-bert-80M-32k-retrieval"
        
        if not self.api_key:
            print("Warning: TOGETHER_API_KEY environment variable is not set. TogetherAI features will be disabled.")
            return
        
        try:
            # Set the API key as an environment variable for the Together client
            os.environ['TOGETHER_API_KEY'] = self.api_key
            
            # Initialize the client
            self.client = Together(api_key=self.api_key)
            print("TogetherAI client initialized successfully")
        except Exception as e:
            print(f"Failed to initialize TogetherAI client: {e}")
            self.client = None
    
    def call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """
        Call the TogetherAI LLM with the given prompt and optional system prompt.
        
        Args:
            prompt (str): The user prompt
            system_prompt (str, optional): The system prompt
            
        Returns:
            str: The generated response
        """
        if not self.client:
            return "TogetherAI service is not available. Please set the TOGETHER_API_KEY environment variable."
        
        try:
            # Prepare the full prompt with system prompt if provided
            if system_prompt:
                full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>\n"
            else:
                full_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
            
            # Use the modern API for Together AI v1.5.25
            response = self.client.completions.create(
                model=self.llm_model,
                prompt=full_prompt,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1.1
            )
            
            return response.choices[0].text
            
        except Exception as e:
            print(f"Error calling TogetherAI LLM: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_embeddings(self, input_text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for the given input text.
        
        Args:
            input_text (Union[str, List[str]]): Single text or list of texts to embed
            
        Returns:
            Union[List[float], List[List[float]]]: Single embedding or list of embeddings
        """
        if not self.client:
            print("TogetherAI client not available, returning zero embeddings")
            # Return empty embedding of appropriate size for the model
            if isinstance(input_text, str):
                return [0.0] * 768  # Default embedding size for m2-bert-80M
            else:
                return [[0.0] * 768 for _ in input_text]
        
        try:
            # Ensure input is a list
            if isinstance(input_text, str):
                input_list = [input_text]
                single_input = True
            else:
                input_list = input_text
                single_input = False
            
            # Use the modern API for embeddings
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=input_list
            )
            
            embeddings = response.data[0].embedding
            
            # Return single embedding if single input was provided
            if single_input:
                return embeddings
            else:
                return [embeddings] if isinstance(embeddings, list) else [embeddings]
                
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            # Return empty embedding of appropriate size for the model
            if isinstance(input_text, str):
                return [0.0] * 768  # Default embedding size for m2-bert-80M
            else:
                return [[0.0] * 768 for _ in input_text]

# Create a global instance
together_ai_service = TogetherAIService()