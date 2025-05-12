from app.models.mongo.model import MongoModel
from app.schemas.money.user import User
from app.core.config import MONGO_MONEY_DB

User = MongoModel(MONGO_MONEY_DB, 'User', User)