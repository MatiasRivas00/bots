from app.schemas.mongo import BaseSchema

class User(BaseSchema):
    telegram_id: int
    hashed_password: str
