from app.models.mongo.model import MongoModel
from app.schemas.money.transaction import Transaction
from app.core.config import MONGO_MONEY_DB

Transaction = MongoModel(MONGO_MONEY_DB, 'Transaction', Transaction)