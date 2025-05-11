from app.core.constants import MONGO_URI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from core.logger import logger

class Mongo:
  _client = None
  
  def connect(cls):
    if cls._client is None:
      cls._client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
      logger.info("Connected successfuly to MongoDB")

    try:
      cls._client.admin.command('ping')
      return cls._client
    except Exception as e:
      raise ConnectionError(f"Failed to connect to MongoDB: {e}")
    