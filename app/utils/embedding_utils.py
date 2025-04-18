from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.storage import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode
import os


# Embed and store chunks in Pinecone
def embed_chunks_to_pinecone(chunks):
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

    nodes = [
        TextNode(
            text=chunk["chunk"],
            metadata={"pages": [str(page) for page in chunk["pages"]]}
        )
        for chunk in chunks
    ]

    vector_store = PineconeVectorStore(
        index_name=pinecone_index_name,
        api_key=pinecone_api_key,
        environment=pinecone_env
    )

    print("Vector store created successfully")

    # Create index
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    print("Index created successfully")

    return {"status": "stored", "count": len(chunks)}
