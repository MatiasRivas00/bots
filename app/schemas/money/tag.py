from app.schemas.mongo import BaseSchema, PythonObjectId

class Tag(BaseSchema):
    user_id: PythonObjectId
    name: str
    is_active: bool = True  # Permite desactivar tags sin borrarlas