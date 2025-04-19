
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.schema.document import Document
import pinecone

index_name = "chatbot-pdf"

# Initialize Pinecone client
def init_pinecone():
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_env = os.getenv("PINECONE_ENVIRONMENT")

    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, dimension=1536)  # adjust based on model

    return pinecone.Index(index_name)

# Embed and store chunks in Pinecone
def embed_chunks_to_pinecone(chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))

    documents = [
        Document(
            page_content=chunk["chunk"],
            metadata={"pages": chunk["pages"]}
        )
        for chunk in chunks
    ]

    init_pinecone()

    Pinecone.from_documents(documents, embedding=embeddings, index_name=index_name)

    return {"status": "stored", "count": len(documents)}
