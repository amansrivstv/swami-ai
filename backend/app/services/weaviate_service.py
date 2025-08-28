import weaviate
import ast
import tqdm
import os
from typing import List, Dict, Any
from .together_ai_service import together_ai_service


class WeaviateService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.collection_name = "swamiji"
        
    def connect(self):
        """Connect to Weaviate instance"""
        try:
            # Get Weaviate URL from environment variable, default to localhost
            weaviate_url = os.getenv('WEAVIATE_URL', 'http://localhost:8080')
            print(f"Connecting to Weaviate at: {weaviate_url}")
            
            # Use ConnectionParams for Weaviate v4
            connection_params = weaviate.connect.ConnectionParams.from_url(weaviate_url, grpc_port=50051)
            self.client = weaviate.WeaviateClient(connection_params)
            
            # Connect the client
            self.client.connect()
            
            # Check if connection is ready
            if self.client.is_ready():
                print(f"Weaviate connection ready: {self.client.is_ready()}")
                return True
            else:
                print("Weaviate client is not ready after connection attempt")
                return False
        except Exception as e:
            print(f"Failed to connect to Weaviate: {e}")
            return False
    
    def create_collection(self):
        """Create the swamiji collection if it doesn't exist"""
        if not self.client:
            print("Weaviate client not connected")
            return False
            
        # Ensure client is connected
        if not self.client.is_ready():
            print("Weaviate client not ready, attempting to reconnect...")
            try:
                self.client.connect()
                if not self.client.is_ready():
                    print("Failed to reconnect to Weaviate")
                    return False
            except Exception as e:
                print(f"Failed to reconnect to Weaviate: {e}")
                return False
            
        try:
            # Delete existing collection if it exists
            if self.client.collections.exists(self.collection_name):
                self.client.collections.delete(self.collection_name)
                print(f"Deleted existing collection: {self.collection_name}")
            
            # Create new collection using modern API
            collection = self.client.collections.create(
                name=self.collection_name,
                properties=[
                    weaviate.classes.config.Property(name="chunk", data_type=weaviate.classes.config.DataType.TEXT),
                    weaviate.classes.config.Property(name="chunk_index", data_type=weaviate.classes.config.DataType.INT),
                ]
            )
            print(f"Created collection: {self.collection_name}")
            return True
            
        except Exception as e:
            print(f"Failed to create collection: {e}")
            return False
    

    
    def read_two_files_line_by_line(self, file1_path: str, file2_path: str) -> List[Dict[str, Any]]:
        """Read chunks and vectors from two files and return structured data"""
        chunk_objs = []
        
        try:
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r') as file2:
                chunk_index = 0
                while True:
                    line1 = file1.readline()
                    line2 = file2.readline()

                    # Check if both files have reached the end
                    if not line1 and not line2:
                        break
                    
                    # Process lines
                    if line1 and line2:
                        try:
                            # For chunks.txt, treat the line as raw text content
                            chunk_text = line1.strip()
                            vector_str = line2.strip()
                            
                            # Parse vector string to list of floats
                            vector = [float(x) for x in vector_str.strip('[]').split(',')]
                            
                            # Create chunk object
                            chunk_obj = {
                                "chunk": chunk_text,
                                "chunk_index": chunk_index
                            }
                            
                            chunk_objs.append(chunk_obj)
                            chunk_index += 1
                            
                        except Exception as e:
                            print(f"Error processing line {chunk_index}: {e}")
                            continue

        except FileNotFoundError:
            print("One or both files not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        return chunk_objs
    
    def load_data_to_collection(self, chunks_file_path: str, vectors_file_path: str, max_chunks: int = None):
        """Load data from files into the Weaviate collection"""
        if not self.client:
            print("Weaviate client not connected")
            return False
            
        # Ensure client is connected
        if not self.client.is_ready():
            print("Weaviate client not ready, attempting to reconnect...")
            try:
                self.client.connect()
                if not self.client.is_ready():
                    print("Failed to reconnect to Weaviate")
                    return False
            except Exception as e:
                print(f"Failed to reconnect to Weaviate: {e}")
                return False
            
        try:
            # Read data from files
            chunk_objs = self.read_two_files_line_by_line(chunks_file_path, vectors_file_path)
            
            if not chunk_objs:
                print("No data found in files")
                return False
            
            # Limit chunks if specified
            if max_chunks:
                chunk_objs = chunk_objs[:max_chunks]
            
            print(f"Loading {len(chunk_objs)} chunks into collection...")
            
            # Add objects to collection using modern API
            collection = self.client.collections.get(self.collection_name)
            for chunk_object in tqdm.tqdm(chunk_objs, desc="Loading chunks"):
                try:
                    collection.data.insert(chunk_object)
                    print(f"Added chunk {chunk_object['chunk_index']}")
                except Exception as e:
                    print(f"Failed to add chunk {chunk_object['chunk_index']}: {e}")
            
            print(f"Successfully loaded {len(chunk_objs)} chunks into collection")
            return True
            
        except Exception as e:
            print(f"Failed to load data: {e}")
            return False
    
    def initialize_collection(self, chunks_file_path: str, vectors_file_path: str, max_chunks: int = None):
        """Initialize the collection and load data if empty"""
        print(f"Initializing collection with max_chunks={max_chunks}")
        if not self.connect():
            print("Failed to connect to Weaviate")
            return False
            
        # Check if collection exists, if not create it
        if not self.client.collections.exists(self.collection_name):
            print(f"Collection {self.collection_name} does not exist, creating...")
            if not self.create_collection():
                print("Failed to create collection")
                return False
        else:
            print(f"Collection {self.collection_name} already exists")
            self.client.collections.delete(self.collection_name)
            print(f"Deleted collection {self.collection_name}")
            if not self.create_collection():
                print("Failed to create collection")
                return False
        
        # Check if collection is empty
        try:
            collection = self.client.collections.get(self.collection_name)
            total_count = len(collection)
            print(f"Collection size: {total_count}")
            
            if total_count == 0:
                print("Collection is empty, loading data...")
                return self.load_data_to_collection(chunks_file_path, vectors_file_path, max_chunks)
            else:
                print(f"Collection already contains {total_count} objects")
                return True
        except Exception as e:
            print(f"Error checking collection size: {e}")
            # If we can't check the size, assume it's empty and try to load data
            print("Assuming collection is empty and loading data...")
            return self.load_data_to_collection(chunks_file_path, vectors_file_path, max_chunks)
    
    def search_similar_chunks(self, query: str, limit: int = 5):
        """Search for similar chunks using vector similarity"""
        print(f"Searching for query: '{query}' with limit: {limit}")
        if not self.client:
            print("Weaviate client not connected")
            return []
            
        # Ensure client is connected
        if not self.client.is_ready():
            print("Weaviate client not ready, attempting to reconnect...")
            try:
                self.client.connect()
                if not self.client.is_ready():
                    print("Failed to reconnect to Weaviate")
                    return []
            except Exception as e:
                print(f"Failed to reconnect to Weaviate: {e}")
                return []
            
        try:
            # Generate embedding for the query using TogetherAI
            query_embedding = together_ai_service.generate_embeddings(query)
            print(f"Query embedding generated:{query_embedding[:5]}, {len(query_embedding)} dimensions")
            
            # Check if embedding is all zeros (TogetherAI not available)
            if all(x == 0.0 for x in query_embedding):
                print("Zero embedding detected, falling back to text search")
                raise Exception("Zero embedding - TogetherAI not available")
            
            # Perform vector search using the modern API
            collection = self.client.collections.get(self.collection_name)
            print(f"Collection size before search: {len(collection)}")
            response = collection.query.hybrid(
                query=query,
                alpha=0.5,
                vector=query_embedding,
                limit=limit,
                return_properties=["chunk", "chunk_index"]
            )
            for o in response.objects:
                print(o.properties)
            # Convert response to expected format
            results = []
            print(f"Search response has {len(response.objects)} objects")
            for obj in response.objects:
                result = {
                    "chunk": obj.properties.get("chunk", ""),
                    "chunk_index": obj.properties.get("chunk_index", 0)
                }
                results.append(result)
                print(f"Added result: chunk_index={result['chunk_index']}, chunk_length={len(result['chunk'])}")
            
            print(f"Returning {len(results)} results")
            return results
            
        except Exception as e:
            print(f"Search failed: {e}")
            # Fallback to simple text search if vector search fails
            try:
                collection = self.client.collections.get(self.collection_name)
                response = collection.query.fetch_objects(
                    limit=limit,
                    return_properties=["chunk", "chunk_index"]
                )
                
                results = []
                print(f"Fallback search response has {len(response.objects)} objects")
                for obj in response.objects:
                    result = {
                        "chunk": obj.properties.get("chunk", ""),
                        "chunk_index": obj.properties.get("chunk_index", 0)
                    }
                    results.append(result)
                    print(f"Added fallback result: chunk_index={result['chunk_index']}, chunk_length={len(result['chunk'])}")
                
                print(f"Returning {len(results)} fallback results")
                return results
            except Exception as fallback_error:
                print(f"Fallback search also failed: {fallback_error}")
                return []
    
    def close(self):
        """Close the Weaviate connection"""
        if self.client:
            # Modern Weaviate client has a close method
            self.client.close()
            self.client = None
            print("Weaviate connection closed")

# Create a global instance
weaviate_service = WeaviateService()
