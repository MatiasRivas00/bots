from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from typing import Optional

from datetime import datetime, timezone

class PythonObjectId(ObjectId):
  @classmethod
  def __get_validators__(cls):
    yield cls.validate

  @classmethod
  def validate(cls, value, info):
    if not ObjectId.is_valid(value):
      raise ValueError("invalid ID")
    return ObjectId(value)
  
  @classmethod
  def __get_pydantic_json_schema__(cls, _core_schema, _handler) -> JsonSchemaValue:
      return {"type": "string", "pattern": "^[a-fA-F0-9]{24}$"}
  
class BaseSchema(BaseModel):
  id: Optional[PythonObjectId] = Field(default_factory=PythonObjectId, alias="_id")
  created_at: Optional[datetime] = Field(default_factory=datetime.now(timezone.utc))

  class Config:
    validate_by_name = True
    arbitrary_types_allowed = True
    json_encoders = {
      ObjectId: str,
      datetime: lambda dt: dt.isoformat()
    }