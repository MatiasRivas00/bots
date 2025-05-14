from app.schemas.mongo import BaseSchema, PythonObjectId
from pydantic import BaseModel
from typing import Optional

class Category(BaseSchema):
    user_id: PythonObjectId
    name: str
    parent_id: Optional[PythonObjectId] = None  # Si es None, es una categoría principal

class LLMCategory(BaseModel):
    name: str