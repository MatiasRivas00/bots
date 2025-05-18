from app.models.mongo.model import MongoModel
from app.schemas.money import Transaction, Tag, Category
from app.core.config import MONGO_MONEY_DB

Transaction = MongoModel(MONGO_MONEY_DB, 'Transaction', Transaction)

Tag = MongoModel(MONGO_MONEY_DB, 'Tag', Tag)

Category = MongoModel(MONGO_MONEY_DB, 'Category', Category)