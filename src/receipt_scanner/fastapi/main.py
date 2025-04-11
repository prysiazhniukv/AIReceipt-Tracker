from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
import os
from sqlalchemy.orm import Session
from uuid import uuid4
import aiofiles
from receipt_scanner.fastapi.database import get_db, engine
from receipt_scanner.fastapi.models import Receipt, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/send_receipt")
async def send_receipt(file: UploadFile = File(...), db: Session=Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    # Saving it locally since it's not a prod.
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try: 
        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    
    db_item = Receipt(
       photo_url = file_path 
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        "filename": file.filename,
        "saved_as": unique_filename,
        "path": file_path
    }


