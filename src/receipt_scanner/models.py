from pydantic import BaseModel
from typing import List, Literal

class Quantity(BaseModel):
    value: float
    unit: Literal['g', 'ml', 'pcs']

class ProductItem(BaseModel):
    name: str
    quantity: Quantity
    price: float

class Receipt(BaseModel):
    storeName: str
    total: float
    products: List[ProductItem]


