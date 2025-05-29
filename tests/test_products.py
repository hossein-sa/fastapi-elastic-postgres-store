from fastapi.testclient import TestClient
from app.main import app
import time


client = TestClient(app)


def test_create_product():
    product_data = {
        "name": "Test Product",
        "brand": "TestBrand",
        "price": 123.45,
        "in_stock": True
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == 200
    result = response.json()
    assert result["name"] == product_data["name"]
    assert result["brand"] == product_data["brand"]
    assert result["price"] == product_data["price"]
    assert result["in_stock"] == product_data["in_stock"]


def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert any(p["name"] == "Test Product" for p in result)

def test_get_single_product():
    # ابتدا یک محصول می‌سازیم
    product_data = {
        "name": "Unique Product",
        "brand": "UniqueBrand",
        "price": 321.0,
        "in_stock": True
    }
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 200
    created_product = create_response.json()
    product_id = created_product["id"]

    # حالا محصول ساخته‌شده رو با ID بخونیم
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == product_id
    assert result["name"] == product_data["name"]


def test_update_product():
    # ساخت یک محصول جدید
    original_data = {
        "name": "ProductToUpdate",
        "brand": "OldBrand",
        "price": 50.0,
        "in_stock": True
    }
    create_response = client.post("/products/", json=original_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # اطلاعات جدید برای بروزرسانی
    updated_data = {
        "name": "ProductToUpdate",
        "brand": "NewBrand",
        "price": 99.99,
        "in_stock": False
    }

    update_response = client.put(f"/products/{product_id}", json=updated_data)
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["brand"] == "NewBrand"
    assert result["price"] == 99.99
    assert result["in_stock"] is False


def test_delete_product():
    # ساخت یک محصول جدید
    product_data = {
        "name": "ProductToDelete",
        "brand": "DeleteBrand",
        "price": 10.0,
        "in_stock": True
    }
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # حذف محصول
    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200

    # بررسی اینکه محصول دیگه وجود نداره
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_delete_product():
    # ساخت یک محصول جدید
    product_data = {
        "name": "ProductToDelete",
        "brand": "DeleteBrand",
        "price": 10.0,
        "in_stock": True
    }
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # حذف محصول
    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200

    # بررسی اینکه محصول دیگه وجود نداره
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_autocomplete():
    product_data = {
        "name": "AutoCompletePhone",
        "brand": "AutoBrand",
        "price": 300.0,
        "in_stock": True
    }
    client.post("/products/", json=product_data)

    # صبر کوچیک برای sync با Elastic
    import time
    time.sleep(1)

    # autocomplete با prefix
    response = client.get("/autocomplete", params={"q": "auto"})
    assert response.status_code == 200
    results = response.json()["results"]
    assert any("AutoCompletePhone" in p["name"] for p in results)


def test_fuzzy_search():
    product_data = {
        "name": "SamsungX12",
        "brand": "FuzzyBrand",
        "price": 600.0,
        "in_stock": True
    }
    client.post("/products/", json=product_data)
    time.sleep(1)

    # فازی سرچ با اشتباه تایپی
    response = client.get("/fuzzy-search", params={"q": "SamsongX12"})
    assert response.status_code == 200
    results = response.json()["results"]
    assert any("SamsungX12" in p["name"] for p in results)


def test_suggest_complete():
    product_data = {
        "name": "IPhone 21 Pro Max",
        "brand": "Apple",
        "price": 1299.0,
        "in_stock": True
    }
    client.post("/products/", json=product_data)
    time.sleep(1)

    response = client.get("/suggest-complete", params={"q": "ipho"})
    assert response.status_code == 200
    suggestions = response.json()["suggestions"]
    assert any("IPhone 21 Pro Max" in s for s in suggestions)

def test_term_suggest():
    response = client.get("/suggest", params={"q": "iphine"})
    assert response.status_code == 200
    suggestions = response.json()["suggestions"]
    assert "iphone" in [s.lower() for s in suggestions]
