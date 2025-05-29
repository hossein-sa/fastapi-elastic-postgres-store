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

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/fastapi-elastic-postgres-store.git
cd fastapi-elastic-postgres-store
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

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
└── requirements.txt
```

---

## 🗃️ PostgreSQL Setup

Make sure you have a PostgreSQL instance running. Create a database called `store`:

```sql
CREATE DATABASE store;
```

Update your `DATABASE_URL` in `app/db.py` accordingly.

---

## 🔎 Elasticsearch Setup

Start an Elasticsearch container (if needed):

```bash
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.12.0
```

Or connect to your existing ES instance.

---

## 🧪 Running Tests

We use `pytest` with `TestClient` and real integration with Elasticsearch:

```bash
pytest
```

Ensure that:
- PostgreSQL and Elasticsearch are running.
- `.env` or settings are properly configured.

---

## 🌐 API Endpoints

| Method | Endpoint             | Description                     |
|--------|----------------------|---------------------------------|
| GET    | `/products/`         | List all products               |
| POST   | `/products/`         | Create new product              |
| GET    | `/products/{id}`     | Retrieve product by ID          |
| PUT    | `/products/{id}`     | Update product by ID            |
| DELETE | `/products/{id}`     | Delete product by ID            |
| GET    | `/search`            | Filter search (brand, price...) |
| GET    | `/autocomplete`      | Autocomplete by product name    |
| GET    | `/fuzzy-search`      | Fuzzy match on product name     |
| GET    | `/suggest`           | Term suggestions                |
| GET    | `/suggest-complete`  | Completion suggester (with fuzzy)|

---

## 🔄 Manual Elasticsearch Sync

Run this script to sync all products from DB to Elasticsearch:

```bash
python sync_to_elastic.py
```

---

## 📌 Notes

- **Pydantic v2** is used — keep in mind `ConfigDict` replaces old `Config` style.
- Elasticsearch mappings and suggesters are managed manually in `manage_index.py`.

---

## 🧠 TODO

- [ ] Add CI pipeline with GitHub Actions
- [ ] Dockerize the whole stack (Postgres + FastAPI + ES)
- [ ] Add more advanced analyzers to ES
- [ ] Extend unit tests to include edge cases

---

## 🧑‍💻 Author

**Hossein Sa** — [GitHub Profile](https://github.com/hossein-sa)

---

## 📝 License

This project is open source under the [MIT License](LICENSE).
