
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from app.utils.pdf_utils import extract_text_by_page
from app.utils.chunk_utils import chunk_text

app = FastAPI()

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        pages = extract_text_by_page(temp_path)
        chunks = chunk_text(pages)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    os.remove(temp_path)

    return JSONResponse(content={
        "pages": pages,
        "chunks": chunks
         })
