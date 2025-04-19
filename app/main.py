
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from app.utils.pdf_utils import extract_text_by_page
from app.utils.chunk_utils import chunk_text
from app.utils.embedding_utils import embed_chunks_to_pinecone

app = FastAPI()

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # استخراج نصوص الصفحات
        pages = extract_text_by_page(temp_path)
        
        # تقسيم النصوص إلى chunks
        chunks = chunk_text(pages, chunk_size=200, overlap=30)

        # تخزين الـ embeddings داخل Pinecone
        result = embed_chunks_to_pinecone(chunks, index_name="chatbot-pdf")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    os.remove(temp_path)

    return JSONResponse(content={

        "message": "PDF indexed and stored in Pinecone successfully",
        "chunks_stored": result["count"]
    })