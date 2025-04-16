from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from uuid import uuid4
import aiofiles
from contextlib import asynccontextmanager

from receipt_scanner.fastapi.database import get_async_session, async_engine
from receipt_scanner.fastapi.models import Receipt, ReceiptItem, Base
from receipt_scanner.fastapi.eyes import receipt_to_text
from receipt_scanner.agent.main import receipt_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/send_receipt")
async def send_receipt(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_async_session)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    db_item = Receipt(photo_url=file_path)

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    return {"filename": file.filename, "saved_as": unique_filename, "path": file_path}


@app.get("/get_cost/")
async def get_cost(receipt_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Receipt).where(Receipt.id == receipt_id))
    receipt = result.scalars().first()
    if not receipt:
        return {"error": f"Receipt with ID {receipt_id} not found"}

    receipt_text = "\n".join(receipt_to_text(receipt.photo_url))
    final_result = await receipt_agent(receipt_text)

    receipt.store_name = final_result.storeName
    receipt.total_price = final_result.total

    for product in final_result.products:
        item = ReceiptItem(
            receipt_id=receipt.id,
            name=product.name,
            quantity=product.quantity.value,
            unit_price=product.price / product.quantity.value
            if product.quantity.value > 0
            else 0,
        )
        db.add(item)

    await db.commit()
    await db.refresh(receipt)

    result = await db.execute(
        select(ReceiptItem).where(ReceiptItem.receipt_id == receipt.id)
    )
    items = result.scalars().all()

    return {
        "id": receipt.id,
        "store_name": receipt.store_name,
        "total_price": receipt.total_price,
        "items": [
            {
                "name": item.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in items
        ],
        "photo_url": receipt.photo_url,
    }
