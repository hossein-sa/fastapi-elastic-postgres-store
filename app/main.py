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
    new_product = crud.create_product(db, product)

    # sync to elastic
    es.index(index=index_name, id=new_product.id, document={
        "name": new_product.name,
        "brand": new_product.brand,
        "price": new_product.price,
        "in_stock": new_product.in_stock,
        "name_suggest": {
            "input": [new_product.name]
        }
    })

    return new_product


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


@app.put("/products/{product_id}", response_model=schemas.ProductOut)
def update(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    # sync updated product to elastic
    es.index(index=index_name, id=updated.id, document={
        "name": updated.name,
        "brand": updated.brand,
        "price": updated.price,
        "in_stock": updated.in_stock,
        "name_suggest": {
            "input": [updated.name]
        }
    })

    return updated



@app.delete("/products/{product_id}", response_model=schemas.ProductOut)
def delete(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    # delete from elastic
    es.delete(index=index_name, id=deleted.id, ignore=[404])

    return deleted



@app.get("/autocomplete")
def autocomplete(q: str = Query(...)):
    query = {
        "query": {
            "prefix": {
                "name.lower": q.lower()
            }
        }
    }

    results = es.search(index=index_name, body=query)
    return {"results": [hit["_source"] for hit in results["hits"]["hits"]]}


@app.get("/fuzzy-search")
def fuzzy_search(q: str = Query(..., min_length=1)):
    query = {
        "query": {
            "match": {
                "name": {
                    "query": q,
                    "fuzziness": "AUTO"
                }
            }
        }
    }

    results = es.search(index=index_name, body=query)
    return {"results": [hit["_source"] for hit in results["hits"]["hits"]]}

@app.get("/suggest")
def suggest_products(q: str = Query(..., min_length=1)):
    query = {
        "suggest": {
            "product-suggest": {
                "text": q,
                "term": {
                    "field": "name"
                }
            }
        }
    }

    results = es.search(index=index_name, body=query)
    
    suggestions = results.get("suggest", {}).get("product-suggest", [])
    options = []

    for entry in suggestions:
        for option in entry.get("options", []):
            options.append(option["text"])

    return {"suggestions": options}


@app.get("/suggest-complete")
def suggest_complete(q: str = Query(..., min_length=1)):
    query = {
        "suggest": {
            "product-suggest": {
                "prefix": q,
                "completion": {
                "field": "name_suggest",
                "fuzzy": {
                    "fuzziness": 1
                }
            }
            }
        }
    }

    results = es.search(index=index_name, body=query)

    suggestions = results.get("suggest", {}).get("product-suggest", [])
    options = []

    for entry in suggestions:
        for option in entry.get("options", []):
            options.append(option["text"])

    return {"suggestions": options}
