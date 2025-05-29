from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")

es = Elasticsearch(ELASTICSEARCH_HOST, verify_certs=False)


def get_elastic_client():
    return Elasticsearch(hosts=[ELASTICSEARCH_HOST])