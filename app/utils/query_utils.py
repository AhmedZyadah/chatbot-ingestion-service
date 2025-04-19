import os
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

def query_pinecone(question: str):
    # 1. تهيئة Embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))

    # 2. استدعاء الـ index الموجود
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
    vectorstore = Pinecone.from_existing_index(index_name=pinecone_index_name, embedding=embeddings)

    # 3. إعداد LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    # 4. ربط الاسترجاع بالـ LLM (RAG)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    # 5. إرسال السؤال
    result = qa_chain({"query": question})

    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result["source_documents"]]
    }
