from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_async_session

router = APIRouter(
        prefix="/items",
        tags=["items"],
)

@router.get("/")
async def return_default_stats(db: AsyncSession = Depends(get_async_session)):



