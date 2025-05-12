from app.schemas.mongo import BaseSchema, PythonObjectId
from typing import Optional

class Category(BaseSchema):
    user_id: PythonObjectId
    name: str
    parent_id: Optional[PythonObjectId] = None  # Si es None, es una categoría principal