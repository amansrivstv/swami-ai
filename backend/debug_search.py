#!/usr/bin/env python3

import os
import sys
sys.path.append('.')

from app.services.weaviate_service import WeaviateService
from app.services.chat_service import ChatService

def test_search():
    print("Testing search functionality...")
    
    # Initialize Weaviate service
    ws = WeaviateService()
    print(f"Weaviate service initialized: {ws}")
    
    # Try to connect
    if ws.connect():
        print("✓ Connected to Weaviate")
        
        # Check if collection exists
        if ws.client.collections.exists(ws.collection_name):
            print(f"✓ Collection '{ws.collection_name}' exists")
            
            # Get collection
            collection = ws.client.collections.get(ws.collection_name)
            print(f"✓ Collection size: {len(collection)}")
            
            # Test search
            query = "What is meditation?"
            print(f"Testing search with query: '{query}'")
            
            try:
                results = ws.search_similar_chunks(query, limit=3)
                print(f"✓ Search returned {len(results)} results")
                for i, result in enumerate(results):
                    print(f"  Result {i+1}: chunk_index={result.get('chunk_index')}, chunk_length={len(result.get('chunk', ''))}")
            except Exception as e:
                print(f"✗ Search failed: {e}")
        else:
            print(f"✗ Collection '{ws.collection_name}' does not exist")
    else:
        print("✗ Failed to connect to Weaviate")

if __name__ == "__main__":
    test_search()
