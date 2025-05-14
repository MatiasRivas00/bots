from app.schemas.mongo import BaseSchema, PythonObjectId
from pydantic import BaseModel

class Tag(BaseSchema):
    user_id: PythonObjectId
    name: str
    is_active: bool = True  # Permite desactivar tags sin borrarlas

class LLMTag(BaseModel):
    name: str
    is_active: bool = True