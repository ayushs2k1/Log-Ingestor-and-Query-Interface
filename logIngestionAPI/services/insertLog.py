from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch, Elasticsearch
from models.logRequestModel import LogRequestDTO
from utils.loggingConfig import logger
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Elasticsearch connection settings
ES_HOST = os.getenv("ES_HOST")
ES_PORT = 9200
ES_INDEX = os.getenv("ES_INDEX")
ES_SCHEME = os.getenv("ES_SCHEME")

# Elasticsearch credentials
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")

class ElasticSearchService:
    def __init__(self):
        self.client = AsyncElasticsearch([{'host': ES_HOST, 'port': ES_PORT, 'scheme': ES_SCHEME}], http_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False)

    async def create_index_if_not_exists(self):
        if await self.client.indices.exists(index=ES_INDEX):
            logger.info("Index already exists")
        else:
            logger.info("Index does not exist. Creating ...")
            await self.client.indices.create(index=ES_INDEX, ignore=400)
            logger.info("Index created!")

    async def insert_log_record(self, log_request_object: LogRequestDTO):
        try:
            await self.create_index_if_not_exists()
            doc_body = log_request_object.dict()
            await self.client.index(index=ES_INDEX, body=doc_body)
            logger.info("Log record inserted successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to insert log record: {e}")
            return False

async def retryInsertLogRecord(log_request_object, max_retries=3):
    es_service = ElasticSearchService()
    for attempt in range(1, max_retries + 1):
        if await es_service.insert_log_record(log_request_object):
            return True
        logger.info(f"Retrying... Attempt {attempt} failed")
        await asyncio.sleep(2 ** attempt)  # Exponential backoff for retry delay
    return False
