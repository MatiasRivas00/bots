from typing import Type, List, Optional

from app.core.config import MONGO_DB
from app.schemas.mongo import BaseSchema

class MongoModel:
  def __init__(self, name: str, schema: Type[BaseSchema]):
    self.collection = MONGO_DB[name]
    self.schema = schema

  def find(self, query: dict = {}) -> List[BaseSchema]:
    documents = self.collection.find(query)
    return [self.schema(**doc) for doc in documents]
  
  def find_one(self, query: dict = {}) -> Optional[BaseSchema]:
    doc = self.collection.find_one(query)
    return self.schema(**doc) if doc else None
  
  def create(self, data: dict):
    instance = self.schema(**data)
    self.collection.insert_one(instance.model_dump(by_alias=True))
    return instance
  
  def update(self, query: dict, update_data: dict):
    return self.collection.update_many(query, {"$set": update_data})
  
  def delete(self, query: dict):
    return self.collection.delete_many(query)
  
  def __call__(self, **kwargs):
    return MongoModelInstance(self, self.schema(**kwargs))
  

class MongoModelInstance:
  def __init__(self, model: MongoModel, instance: BaseSchema):
    self.model = model
    self.instance = instance

  def save(self):
    data = self.instance.model_dump(by_alias=True)
    if "_id" in data and self.model.collection.find_one({ "_id": data["_id"] }):
      self.model.collection.replace_one({ "_id": data["_id"] }, data)
    else:
      self.model.collection.insert_one(data)
    
    return self
  
  def to_dict(self):
    return self.instance.model_dump()
