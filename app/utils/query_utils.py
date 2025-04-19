import os
import logging
from typing import Dict, List, Optional
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.storage import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_pinecone(question: str) -> Dict[str, Optional[str | List[Dict]]]:
    """
    Query Pinecone with a question and return the answer along with source documents.

    Args:
        question (str): The question to query.

    Returns:
        Dict[str, Optional[str | List[Dict]]]: A dictionary containing the answer and sources.
    """

    try:
        # 1. Check environment variables
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
        
        if not all([pinecone_api_key, pinecone_env, pinecone_index_name]):
            raise ValueError("Missing required Pinecone environment variables")

        # 2. Initialize Pinecone vector store
        vector_store = PineconeVectorStore(
            index_name=pinecone_index_name,
            api_key=pinecone_api_key,
            environment=pinecone_env
        )

        # 3. Load the index
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

        # 4. Query the index
        query_engine = index.as_query_engine()
        response = query_engine.query(question)

        return {
            "answer": str(response),
            "sources": [dict(node.metadata) for node in response.source_nodes]
        }

    except Exception as e:
        logger.error(f"An error occurred while querying Pinecone: {e}")
        return {
            "answer": None,
            "sources": None
        }
