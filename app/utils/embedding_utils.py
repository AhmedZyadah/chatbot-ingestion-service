
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.storage import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode
import os

pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Embed and store chunks in Pinecone
def embed_chunks_to_pinecone(chunks):
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_env = os.getenv("PINECONE_ENVIRONMENT")

    nodes = [
        TextNode(
            text=chunk["chunk"],
            metadata={"pages": chunk["pages"]}
        )
        for chunk in chunks
    ]

    vector_store = PineconeVectorStore(
        index_name=pinecone_index_name,
        api_key=pinecone_api_key,
        environment=pinecone_env
    )

    # Create index
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    return {"status": "stored", "count": len(chunks)}
