from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import SessionLocal, engine, Base
from app.elastic_client import get_elastic_client

# ساخت جدول‌ها در دیتابیس
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency برای Session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/products/", response_model=list[schemas.ProductOut])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

es = get_elastic_client()
index_name = "products"

@app.get("/search")
def search_products(
    brand: str = Query(None),
    price_min: float = Query(None),
    price_max: float = Query(None),
    in_stock: bool = Query(None)
):
    must_clauses = []

    if brand:
        must_clauses.append({"match": {"brand": brand}})
    
    if price_min is not None or price_max is not None:
        range_query = {"range": {"price": {}}}
        if price_min is not None:
            range_query["range"]["price"]["gte"] = price_min
        if price_max is not None:
            range_query["range"]["price"]["lte"] = price_max
        must_clauses.append(range_query)
    
    if in_stock is not None:
        must_clauses.append({"term": {"in_stock": in_stock}})

    query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }

    result = es.search(index=index_name, body=query)
    hits = [hit["_source"] for hit in result["hits"]["hits"]]

    return {"results": hits}