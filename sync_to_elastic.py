from app.db import SessionLocal
from app.models import Product
from app.elastic_client import get_elastic_client

es = get_elastic_client()
index_name = "products"

def sync_all_products():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        for p in products:
            es.index(index=index_name, id=p.id, document={
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "in_stock": p.in_stock
            })

            print(f"Synced product ID {p.id}")
    finally:
        db.close()

if __name__ == "__main__":
    sync_all_products()
