from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os
from rag.prepare_pdf import prepare
from rag.add_vector import prepare_chain

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_and_prepare")
async def handleData(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="only pdf files allowed")
    file_location = os.path.join(UPLOAD_DIR,f"{file.filename}")

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunks = prepare(file_location)
        prepare_chain(chunks)

        return {"message":"ready to answer question"}
    except Exception as e:
        print(f"error saving the file: {str(e)}")
        return HTTPException(status_code=500, detail="Error uploading the file")        