from app.models.mongo.model import MongoModel
from app.schemas.users import User as UserSchema
from app.core.config import MONGO_MONEY_DB

User = MongoModel(MONGO_MONEY_DB, 'User', UserSchema)