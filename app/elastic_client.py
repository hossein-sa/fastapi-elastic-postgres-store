from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")

es = Elasticsearch(ELASTICSEARCH_URL, verify_certs=False)

def get_elastic_client():
    if not es.ping():
        raise ConnectionError("Elasticsearch not available")
    return es
