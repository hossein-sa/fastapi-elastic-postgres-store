from app.elastic_client import get_elastic_client

es = get_elastic_client()
index_name = "products"

index_body = {
    "settings": {
        "analysis": {
            "normalizer": {
                "lowercase_normalizer": {
                    "type": "custom",
                    "filter": ["lowercase"]
                }
            }
        }
    },
    "mappings": {
    "properties": {
        "name": {
            "type": "text",
            "fields": {
                "raw": { "type": "keyword" },
                "lower": { "type": "keyword", "normalizer": "lowercase_normalizer" }
            }
        },
        "name_suggest": {   # ✅ الان فیلد مستقل شد
            "type": "completion"
        },
        "brand": { "type": "keyword" },
        "price": { "type": "float" },
        "in_stock": { "type": "boolean" }
    }
}

}


def recreate_index():
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted.")

    es.indices.create(index=index_name, body=index_body)
    print(f"Index '{index_name}' created with custom normalizer.")

if __name__ == "__main__":
    recreate_index()
