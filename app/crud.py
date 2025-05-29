from sqlalchemy.orm import Session
from . import models, schemas
from .elastic_client import get_elastic_client

es = get_elastic_client()
index_name = "products"

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # sync to Elasticsearch
    es.index(index=index_name, id=db_product.id, document={
        "name": db_product.name,
        "brand": db_product.brand,
        "price": db_product.price,
        "in_stock": db_product.in_stock
    })

    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product_data: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None

    for field, value in product_data.dict().items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)

    # sync to Elasticsearch
    es.index(index=index_name, id=db_product.id, document={
        "name": db_product.name,
        "brand": db_product.brand,
        "price": db_product.price,
        "in_stock": db_product.in_stock
    })

    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None

    db.delete(db_product)
    db.commit()

    # remove from Elasticsearch
    es.delete(index=index_name, id=product_id, ignore=[404])

    return db_product
