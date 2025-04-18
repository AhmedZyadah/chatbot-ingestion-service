
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    return JSONResponse(content={"message": f"Received {file.filename}"})
