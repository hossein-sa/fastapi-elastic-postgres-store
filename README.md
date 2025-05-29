# 🛒 FastAPI Elastic Postgres Store

A modern backend for an online product store built with **FastAPI**, **PostgreSQL**, and **Elasticsearch**. It provides a RESTful API for CRUD operations on products, full-text search, autocomplete, fuzzy matching, and suggestion features using Elasticsearch.

---

## 📦 Features

- ✅ Create, Read, Update, Delete (CRUD) for Products
- 🔍 Full-text search with filters (brand, price range, stock)
- 🔠 Autocomplete suggestions
- 🔎 Fuzzy search support
- 🧠 Completion & term suggesters
- 🧪 Test suite with `pytest`, `pytest-asyncio`, and Elasticsearch integration
- 🐳 Fully dockerized environment

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hossein-sa/fastapi-elastic-postgres-store.git
cd fastapi-elastic-postgres-store
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

- FastAPI will be available at: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

To stop:

```bash
docker-compose down
```

---

## 🧪 Run Tests

Make sure PostgreSQL and Elasticsearch containers are running:

```bash
pytest
```

Test coverage includes:

- API endpoints
- Elasticsearch search & suggest features
- CRUD operations

---

## ⚙️ Project Structure

```
.
├── app/
│   ├── main.py           # FastAPI application and endpoints
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # DB operations
│   ├── db.py             # PostgreSQL connection
│   └── elastic_client.py # Elasticsearch client
├── sync_to_elastic.py    # Manual sync script from DB to Elasticsearch
├── manage_index.py       # Index management for Elasticsearch
├── tests/
│   └── test_products.py  # All API and search tests
├── conftest.py           # Pytest fixtures
├── pytest.ini            # Pytest config
├── Dockerfile            # API Dockerfile
├── docker-compose.yml    # Compose file for API + PostgreSQL + Elasticsearch
└── requirements.txt
```

---

## 🌐 API Endpoints

| Method | Endpoint             | Description                      |
|--------|----------------------|----------------------------------|
| GET    | `/products/`         | List all products                |
| POST   | `/products/`         | Create new product               |
| GET    | `/products/{id}`     | Retrieve product by ID           |
| PUT    | `/products/{id}`     | Update product by ID             |
| DELETE | `/products/{id}`     | Delete product by ID             |
| GET    | `/search`            | Filter search (brand, price...)  |
| GET    | `/autocomplete`      | Autocomplete by product name     |
| GET    | `/fuzzy-search`      | Fuzzy match on product name      |
| GET    | `/suggest`           | Term suggestions                 |
| GET    | `/suggest-complete`  | Completion suggester (with fuzzy)|

---

## 🔄 Sync Database with Elasticsearch

Use this script to manually sync all DB products to Elasticsearch:

```bash
python sync_to_elastic.py
```

---

## 🧠 Tech Notes

- Using **Pydantic v2** — `ConfigDict` replaces the old `Config` style
- `model_dump()` replaces `dict()` for model export
- Elasticsearch suggesters and mappings are defined in `manage_index.py`

---

## ✅ TODOs

- [x] Basic CRUD APIs
- [x] Elasticsearch integration
- [x] Pytest coverage for API & ES
- [x] Docker Compose support
- [ ] Add CI/CD with GitHub Actions
- [ ] Add token-based authentication
- [ ] Add user/product relationships

---

## 🧑‍💻 Author

**Hossein Sa**  
[GitHub](https://github.com/hossein-sa)

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
