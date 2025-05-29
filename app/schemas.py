from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    brand: str
    price: float
    in_stock: bool = True

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
