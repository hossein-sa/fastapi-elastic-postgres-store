from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    brand: str
    price: float
    in_stock: bool

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
