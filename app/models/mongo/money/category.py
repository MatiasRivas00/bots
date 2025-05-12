from app.models.mongo.model import MongoModel
from app.schemas.money.category import Category
from app.core.config import MONGO_MONEY_DB

Category = MongoModel(MONGO_MONEY_DB, 'Category', Category)